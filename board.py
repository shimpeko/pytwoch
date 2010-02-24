import os
import re

from py2chdlerbase import Py2chdlerBase, Py2chdlerError
from thread import Thread

class Board(Py2chdlerBase):
    def __init__(self, bbsmenu, board_name, board_name_alphabet, board_url):
        self.bbsmenu = bbsmenu
        self.name = board_name
        self.name_alphabet = board_name_alphabet
        self.url = board_url
        self.subject_url = self.url + "subject.txt"
        self.dir_path = self.bbsmenu.settings['base_dir'] + "/" + self.name_alphabet
        self.subject_path = self.dir_path + "/subject.txt"
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        elif not os.path.isdir(self.dir_path):
            raise Py2chdlerError(self.dir_path + " is not a directory.")

    def read(self):
        if os.path.exists(self.subject_path):
            lines = self.read_file(self.subject_path)
        else:
            self.download()
            lines = self.read_file(self.subject_path)
        return lines

    def download(self):
        self.rename_file(self.subject_path)
        dl_data = self.download_file(self.subject_url)
        self.write_file(self.subject_path, dl_data['text'])

    def get_threads(self, *thread_ids):
        threads = list()
        # list to store exist thread_ids ( for error check)
        exist_thread_ids = list()
        subject = self.read()
        thread_regex = '^([0-9]*)\.dat<>(.*)\(([0-9]*)\)$'
        p_thread = re.compile(thread_regex)
        for line in subject:
            r_thread = p_thread.search(line)
            if r_thread:
                thread_id = int(r_thread.group(1))
                if len(thread_ids) == 0 or thread_id in thread_ids:
                    thread = Thread(self, thread_id, r_thread.group(2), r_thread.group(3))
                    threads.append(thread)
                    if thread_id in thread_ids:
                        exist_thread_ids.append(thread_id)
        # raise err if requested thread_id not exists
        if not len(thread_ids) == len(exist_thread_ids):
            err_thread_ids = set(thread_ids) - set(exist_thread_ids)
            err_thread_ids = ', '.join(err_thread_ids)
            raise Py2chdlerError("Thread(s) id: " + err_thread_ids + " are/is not exist(s). Or you may request same thread more than once.")
        return threads
    
    def get_thread(self, thread_id):
        thread = self.get_boards(thread_id)
        return thread[0]

if __name__ == '__main__':
    from bbsmenu import Bbsmenu
    settings = {'base_dir': os.path.abspath('data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    boards = bbsmenu.get_boards('news4vip')
    for board in boards:
        threads = board.get_threads()
        for thread in threads:
            print(thread.title + " " + thread.res_count)
