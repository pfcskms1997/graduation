# TextRank를 이용한 keywords 추출 프로그램
# 처리 시간이 오래 걸리는 데에 비해 빈도 추출 버전의 결과와 크게 차이가 없어 사용하지 않음

# -*- coding: utf-8 -*-
from konlpy.tag import Hannanum
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from kss import split_sentences
import numpy as np


class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize = SentenceTokenizer()  # kkma, okt 로드, stopword 지정
        self.sentences = self.sent_tokenize.text2sentences(text)
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)
        self.graph_matrix = GraphMatrix()
        #self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        #self.rank = Rank()
        #self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        #self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)
        #self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        #self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)


    def keywords(self, word_num=7):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        keywords = []
        index = []

        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)

        # index.sort()
        for idx in index:
            keywords.append(self.idx2word[idx])
        return keywords


class SentenceTokenizer(object):
    def __init__(self):
        self.hannanum = Hannanum()
        self.stopwords = ["중인", "만큼", "마찬가지", "꼬집었", "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자"
            , "아", "휴", "아이구", "아이쿠", "아이고", "이상", "이하", "이전", "이후", "어", "나", "우리", "저희", "따라", "의해"
            , "을", "를", "에", "의", "가"]

    def text2sentences(self, text):
        sentences = split_sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx - 1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence != '':
                nouns.append(' '.join([noun for noun in self.hannanum.nouns(str(sentence))
                                       if noun not in self.stopwords and len(noun) > 1]))
        return nouns


class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []

    def build_sent_graph(self, sentence):
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return self.graph_sentence

    def build_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word]: word for word in vocab}


class Rank(object):
    def get_ranks(self, graph, d=0.85):  # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0  # diagonal 부분을 0으로
            link_sum = np.sum(A[:, id])  # A[:, id] = A[:][id]
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1
        B = (1 - d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B)  # 연립방정식 Ax = b
        return {idx: r[0] for idx, r in enumerate(ranks)}


if __name__ == "__main__":
    url = '서울 연합뉴스 최인영 기자  단계적 일상회복 시행 이후 신종 코로나바이러스 감염증 코로나19 확진자 규모가 증가하는 가운데 위중증 환자 수도 눈에 띄게 늘고 있다. 중앙방역대책본부는 6일 0시 기준으로 재원 중인 위중증 환자가 411명이라고 밝혔다. 위중증 환자 수가 400명을 넘긴 것은 지난 8월 31일 409명  이후 67일 만에 처음이다. 최다 위중증 환자 수 기록은 8월 25일 434명이다. 400명대 위중증 환자 수는 지난 1월 6 10일 닷새 동안 이어졌고, 4차 유행이 확산하던 8월 21일 403명 과 24 29일에도 유지된 바 있다. 9월 이후 위중증 환자는 300명대를 유지하다가 약 2달 만에 다시 400명대로 올라섰다. 특히 최근 일주일 사이 332명 343명 347명 378명 365명 382명 411명으로 급증세를 보였다. 위중증 환자는 고유량 high flow  산소요법, 인공호흡기, 체외막산소공급 ECMO , 지속적신대체요법 CRRT  등으로 격리 치료 중인 환자를 말한다. 정부는 일상회복 전환을 지속해서 추진하려면 중증환자를 안정적으로 관리해야 한다고 강조하고 있다. 방역완화에 따른 확진자 규모 증가를 피할 수 없더라도, 의료체계가 충분히 중환자 치료에 대응할 수 있는 수준을 유지해야 한다는 설명이다 위중증 환자 411명 중 241명 58.64% 은 남성, 170명 41.36% 은 여성이다. 위중증 환자 대부분은 고령층이다. 60대가 117명 28.47% 으로 가장 많고, 70대가 111명 27.01% , 80세 이상이 97명 23.60% 으로 뒤를 이었다. 411명 중 79%가 60세 이상 고령층이다. 50대가 35명 8.52% , 40대가 29명 7.06% , 30대는 18명 4.38% 이다. 20대는 3명 0.73% 이고 10대는 1명 0.24% 이다. 정부는 위증증 환자 대부분이 미접종자 사이에서 발생한다고 밝힌 바 있다. 지난 8월 29일부터 8주간 누적 위중증 환자 1천400명 가운데 68%는 미접종자였다는 것이다. 그러나 고령층은 백신 접종완료율이 높다. 전날 기준으로 60대는 93.7%, 70대는 92.4%, 80세 이상은 81.8%의 접종완료율을 기록했다. 다만 고령자들은 초기 접종자로서 접종한 지 6개월이 지났거나 도달하고 있는 경우가 많다. 사망자도 증가세다. 전날 신규 사망자는 20명, 누적 사망자는 2천956명이다. 최근 사망자 수 추이를 보면 일상회복이 시작된 지난 1일 9명, 2일 16명, 3일 18명, 4일 24명, 5일 20명, 이날 20명이다. 신규 사망자 중 13명 65% 은 80세 이상이고, 70대가 4명, 60대 2명, 50대 1명이다. 정부는 확진자 규모와 더불어 위중증 환자와 사망자 발생 추이를 지켜보고 있다. 전날에는 확진자 증가에 대비해 행정명령을 내려 추가 병상 확보에 나섰다. 전날 오후 5시 기준 전국 중증환자 전담 병상은 1천121개 확보돼 있고, 이 가운데 553개가 사용 중이며 568개 병상이 남아 있다. 정부는 위기 상황이 오면, 단계적 일상회복 추진을 잠시 중단하는 서킷 브레이커 비상계획 를 발동할 계획이다. 비상계획은 위증증·사망자 발생 비율과 의료시스템 역량 등을 종합적으로 고려해 정밀한 기준을 마련한다는 방침이다.'
    #textrank = TextRank(url)
    #for row in textrank.summarize(3):
    #    print(row)
    #print('keywords :', textrank.keywords())
    keyword = ", ".join(TextRank(url).keywords())
    print(keyword)

