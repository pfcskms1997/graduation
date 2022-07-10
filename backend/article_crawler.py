import os
import sys
import platform
import calendar
import requests
import time
import datetime
import threading
from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
from exceptions import *
from article_parser import ArticleParser
from csv_writer import Writer
from keyword_extraction import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.develop')

import django
django.setup()

from blog.models import News


class ArticleCrawler(object):
    def __init__(self):
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110}
        self.selected_categories = []
        #self.date = {'year': 0, 'month': 0, 'day': 0}
        self.date = ''
        self.latest_nid = ''
        self.latest_page = 0
        self.recall_flag = 0
        self.find_flag = 0
        self.user_operating_system = str(platform.system())

    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

    # Crawling할 기사의 URL date를 오늘 날짜로 지정
    def set_date(self):
        self.date = datetime.datetime.now().strftime('%Y%m%d')

    #@staticmethod
    def make_article_url(self, category_url):
        page_urls = []

        # 오늘 날짜의 url 생성
        url = category_url + self.date

        # 존재하지 않는 큰 수를 페이지로 입력하여 마지막 page로 redirect 시킴.
        total_page = ArticleParser.find_news_totalpage(url + "&page=10000")

        valid_page = int(total_page)
        if self.latest_page != 0:
            valid_page = int(total_page) - self.latest_page + 1 # 이전 사이클에서 크롤링한 페이지는 제외
        # 뒷 페이지일수록 먼저 작성된 기사이기 때문에 list를 거꾸로 생성
        for page in range(valid_page, 0, -1):
            page_urls.append(url + "&page=" + str(page))

        self.latest_page = int(total_page)

        return page_urls

    @staticmethod
    def get_url_data(url, max_tries=5):
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                return requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            except requests.exceptions:
                sleep(1)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    def crawling(self, category_name):
        threading.Timer(300, self.crawling, args=(category_name,)).start() # 5분에 한 번씩 crawling 함수 호출

        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))

        self.set_date()

        t = datetime.datetime.now().strftime('%H%M')
        writer = Writer(category='Article', article_category=category_name, date=self.date, time=t)
        key_extraction = KeyExtraction()

        url_form = f'https://news.naver.com/main/list.naver?mode=LSD&mid=shm&sid1={self.categories.get(category_name)}&date='
        target_urls = self.make_article_url(url_form) # URL page list
        print(category_name + " Urls are generated")

        crawling_cnt = 0
        for url in target_urls:
            request = self.get_url_data(url)
            document = BeautifulSoup(request.content, 'html.parser')

            # html - newsflash_body - type06_headline, type06
            # 각 페이지에 있는 기사들 가져오기
            temp_post = document.select('.newsflash_body .type06_headline li dl')
            temp_post.extend(document.select('.newsflash_body .type06 li dl'))

            # 각 페이지에 있는 기사들의 url 저장
            post_urls = []
            for line in temp_post:
                # 해당되는 page에서 모든 기사들의 URL을 post_urls 리스트에 넣음
                post_urls.append(line.a.get('href'))
            post_urls.reverse()
            del temp_post

            for content_url in post_urls:  # 기사 url
                # 크롤링 대기 시간
                sleep(0.01)

                # 기사 HTML 가져옴
                request_content = self.get_url_data(content_url)

                try:
                    post_html = BeautifulSoup(request_content.content, 'html.parser')
                except:
                    continue

                try:
                    # ID 생성 (sid=분야ID(3자), oid=신문사ID(3자), aid=기사ID(10자) 조합)
                    news_id = ArticleParser.make_newsID(content_url)

                    if bool(self.recall_flag): # 함수가 재호출 될 때에만 수행(최초 수행 시에 아래 코드가 수행되지 않도록 함)
                        if news_id == self.latest_nid: # news ID가 같을 경우 데이터를 수집하지 않고 건너 뜀
                            self.find_flag = 1
                            self.recall_flag = 0 # test
                            continue
                        elif (news_id != self.latest_nid) and (not(self.find_flag)):
                            continue

                    self.latest_nid = news_id # 주기적인 크롤링을 위해 마지막 news_id를 기록

                    # 기사 제목 태그 추출
                    tag_title = post_html.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})

                    # 뉴스 기사 제목 초기화
                    text_title = ''
                    text_title = text_title + ArticleParser.clear_headline(str(tag_title[0].find_all(text=True)))
                    # 공백일 경우 기사 제외 처리
                    if not text_title:
                        continue

                    # 기사 본문 태그 추출
                    tag_content = post_html.find_all('div', {'id': 'articleBodyContents'})[0]

                    # 뉴스 기사 본문 초기화
                    text_content = ''
                    text_content = text_content + str(tag_content)
                    withoutTag_content = ''
                    withoutTag_content = withoutTag_content + ArticleParser.clear_content(str(tag_content.find_all(text=True)))

                    # 공백일 경우 기사 제외 처리
                    if not text_content:
                        continue

                    keywords = ",".join(key_extraction.extraction(withoutTag_content))

                    # 기사 언론사 태그 추출
                    tag_press = post_html.find_all('meta', {'property': 'me2:category1'})

                    text_press = ''
                    text_press = text_press + str(tag_press[0].get('content'))

                    # 공백일 경우 기사 제외 처리
                    if not text_press:
                        continue

                    # 기사 작성 시간 추출
                    c_date = ArticleParser.extract_writingtime(request_content.text)

                    # CSV 작성
                    writer.write_row([news_id, c_date, category_name, text_press, text_title, text_content, content_url, keywords])
                    #news, flag = News.objects.create(news_id=news_id, category=category_name, url=content_url, title=text_title,
                    #                 main_contents=text_content, press=text_press, create_date=c_date, keywords=keywords)

                    if not flag:
                        news.delete()

                    del news_id, time, c_date
                    del text_title, text_content, text_press
                    del tag_title, tag_content, tag_press
                    del request_content, post_html

                # UnicodeEncodeError
                except Exception as ex:
                    del request_content, post_html
                    pass

                crawling_cnt = crawling_cnt + 1
                print('{}(PID: {}) {}번째 크롤링 완료'.format(category_name, str(os.getpid()), crawling_cnt))

        writer.close()
        self.recall_flag = 1
        self.find_flag = 0
        print("Function execution is teminated")

    def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()


if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category('정치') # '정치', '경제', '사회', '생활문화', '세계', 'IT과학', '오피니언'
    Crawler.start()