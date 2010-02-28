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
        self.filepath = self.dir_path + "/subject.txt"
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        elif not os.path.isdir(self.dir_path):
            raise Py2chdlerError(self.dir_path + " is not a directory.")

    def read(self):
        if os.path.exists(self.filepath):
            lines = self.read_file(self.filepath)
        else:
            self.download()
            lines = self.read_file(self.filepath)
        return lines

    def download(self):
        mtime = get_mtime(self.filepath)
        self.rename_file(self.filepath)
        dl_data = self.download_file(self.url, mtime)
        self.write_file(self.filepath, dl_data['text'])
        self.set_mtime(self.filepath, dl_data['last-modified'])

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
