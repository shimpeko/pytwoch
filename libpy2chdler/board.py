import os
import re

from base import Base, Py2chdlerError
from thread import Thread

class Board(Base):
    def __init__(self, bbsmenu, board_name, romaji_board_name, board_url):
        self.bbsmenu = bbsmenu
        self.name = board_name
        self.romaji_name = romaji_board_name
        self.url = board_url + "subject.txt"
        self.dir_path = self.bbsmenu.settings['base_dir'] + "/" + self.romaji_name
        self.filepath = self.dir_path + "/subject"
        self.filepath_old = self.dir_path + "/subject_old"
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        elif not os.path.isdir(self.dir_path):
            raise Py2chdlerError(self.dir_path + " is not a directory.")

    def read(self):
        thread_infos = list()
        response_code = self.download(self.url, self.filepath)
        print(response_code)
        subject = set(self.read_file(self.filepath))
        if os.path.exists(self.filepath_old):
            subject_old = set(self.read_file(self.filepath_old))
        else:
            subject_old = set()
        thread_regex = '^([0-9]*)\.dat<>(.*)\(([0-9]*)\)$'
        p_thread = re.compile(thread_regex)
        new_lines = subject - subject_old
        old_lines = subject_old - subject
        for line in new_lines:
            r_thread = p_thread.search(line)
            if r_thread:
                thread_id = int(r_thread.group(1))
                res_count = int(r_thread.group(3))
                old_res_count = 0
                for old_line in old_lines:
                    old_r_thread = p_thread.search(old_line)
                    if old_r_thread:
                        if thread_id == int(old_r_thread.group(1)):
                            old_res_count = int(old_r_thread.group(3))
                            break
                new_res_count = res_count - old_res_count
                thread_info = {'id':thread_id, 'title':r_thread.group(2), 'res_count':res_count, 'new_res_count':new_res_count}
                thread_infos.append(thread_info)
        return thread_infos

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
    settings = {'base_dir': os.path.abspath('../data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    boards = bbsmenu.get_boards('news4vip')
    for board in boards:
        for b in board.read():
            print(b)
