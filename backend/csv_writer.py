import csv
import platform
from exceptions import *


class Writer(object):
    def __init__(self, category, article_category, date, time):
        self.date = date
        self.time = time

        self.file = None
        self.initialize_file(category, article_category)

        self.csv_writer = csv.writer(self.file)

    def initialize_file(self, category, article_category):
        output_path = f'../output'
        if os.path.exists(output_path) is not True:
            os.mkdir(output_path)

        file_name = f'{output_path}/{category}_{article_category}_{self.date}_{self.time}.csv'
        if os.path.isfile(file_name):
            raise ExistFile(file_name)

        user_os = str(platform.system())
        if user_os == "Windows":
            self.file = open(file_name, 'w', encoding='euc-kr', newline='')
        # Other OS uses utf-8
        else:
            self.file = open(file_name, 'w', encoding='utf-8', newline='')

    def write_row(self, arg):
        self.csv_writer.writerow(arg)

    def close(self):
        self.file.close()