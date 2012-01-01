import os
import re

from .base import Base, Py2chdlerError
from .thread import Thread

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
        self.download(self.url, self.filepath)
        subject = set(self.read_file(self.filepath))
        if os.path.exists(self.filepath_old):
            subject_old = set(self.read_file(self.filepath_old))
        else:
            subject_old = set()
        thread_regex = '^([0-9]*)\.dat<>(.*)\(([0-9]*)\)$'
        p_thread = re.compile(thread_regex)
        # list of updated subject from old_subject
        old_subject = subject_old - subject
        # process each line
        for line in subject:
            # seach thread info with regex
            r_thread = p_thread.search(line)
            # if thread info
            if r_thread:
                thread_id = int(r_thread.group(1))
                res_count = int(r_thread.group(3))
                old_res_count = res_count if subject_old else 0
                for old_line in old_subject:
                    old_r_thread = p_thread.search(old_line)
                    if old_r_thread:
                        if thread_id == int(old_r_thread.group(1)):
                            old_res_count = int(old_r_thread.group(3))
                            break
                new_res_count = res_count - old_res_count
                thread_info = {'id':thread_id, 'title':r_thread.group(2), 'res_count':res_count, 'new_res_count':new_res_count}
                thread_infos.append(thread_info)
        return thread_infos

    def read_raw(self):
        self.download(self.url, self.filepath)
        raw_subject = self.read_raw_file(self.filepath)
        return raw_subject

    def get_threads(self, *thread_ids, new=True):
        threads = list()
        # list to store exist thread_ids (for error check)
        exist_thread_ids = list()
        thread_infos = self.read()
        # filter updated thread from thread infos
        if new == True:
            tmp = list()
            for thread_info in thread_infos:
                if not thread_info['new_res_count'] == 0:
                    tmp.append(thread_info)
            thread_infos = tmp
        # if thread_ids is empty get all threads
        if len(thread_ids) == 0:
            for thread_info in thread_infos:
                threads = self.__append_thread(threads, thread_info)
        else:
            for thread_info in thread_infos:
                if thread_info['id'] in thread_ids:
                    threads = self.__append_thread(threads, thread_info)
                    if thread_id in thread_ids:
                        exist_thread_ids.append(thread_id)
            # raise err if requested thread_id not exists
            if not len(thread_ids) == len(exist_thread_ids):
                err_thread_ids = set(thread_ids) - set(exist_thread_ids)
                err_thread_ids = ', '.join(err_thread_ids)
                raise Py2chdlerError("Thread(s) id: " + err_thread_ids + " are/is not exist(s). Or you may request same thread more than once.")
        return threads

    def get_new_threads(self, *thread_ids):
        if thread_ids:
            threads = self.get_threads(thread_ids, new=True)
        else:
            threads = self.get_threads(new=True)
        return threads


    def get_thread(self, thread_id, new=False):
        threads = self.get_threads(thread_id, new)
        return threads[0]

    def get_new_thread(self, thread_id):
        thread = self.get_thread(thread_id, new=True) 
        return thread

    def __append_thread(self, threads, thread_info):
        thread = Thread(self, thread_info['id'], thread_info['title'])
        threads.append(thread)
        return threads

if __name__ == '__main__':
    import time
    from .bbsmenu import Bbsmenu
    homedir = os.path.expanduser('~')
    settings = {'base_dir': os.path.abspath(homedir + '/py2chdler/data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    boards = bbsmenu.get_boards('news4vip')
    for board in boards:
        threads = board.get_threads()
        for thread in threads:
            print(thread.title)
