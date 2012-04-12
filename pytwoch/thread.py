import os
import time
import re
import urllib.parse

from .base import Base, Py2chdlerError


class Thread(Resource):
    def __init__(self, url, cache_dir_path):
        self.url = url
        self.__cache_dir_path = cache_dir_path
        self.__url_pattern = '^/(\w+)(?:/subject\.txt)$'
        self.comment_num = None
        self.isUrlValid = self.__validate_url(url)
        self.isConnected = False

    def connect(self):
        pass

    def next(self):
        res_infos = list()
        self.download(self.url, self.filepath, True)
        dat = set(self.read_file(self.filepath))
        if os.path.exists(self.filepath_old):
            dat_old = set(self.read_file(self.filepath_old))
        else:
            dat_old = set()
        dat_regex = '^(.*)<>(.*)<>(\d{4}/\d{2}/\d{2}\(.\)\s\d{2}:\d{2}:\d{2}(?:\.\d{2}){0,2}) ([a-zA-Z0-9+/?:]{0,12})<>(.*)<>.*$'
        p_dat = re.compile(dat_regex)
        # make new_dat set
        new_dat = dat - dat_old
        # calc res counts
        res_count = len(dat)
        new_res_count = len(new_dat)
        # process each line
        res_num = 1
        for line in dat:
            r_dat = p_dat.match(line)
            if r_dat:
                res_info = dict()
                res_info['id'] = res_num
                res_info['username'] = r_dat.group(1)
                res_info['email'] = r_dat.group(2)
                res_info['posted'] = r_dat.group(3)
                res_info['user_id'] = r_dat.group(4)
                res_info['content'] = r_dat.group(5)
                res_info['new'] = 1 if res_num >= (res_count - new_res_count) else 0
                res_infos.append(res_info)
                res_num += 1
        return res_infos

    def read_raw(self):
        self.download(self.url, self.filepath)
        raw_dat = self.read_raw_file(self.filepath)
        return raw_dat

    def get_reses(self, *res_ids):
        pass
    
    def get_res(self, res_id):
        pass
    

if __name__ == '__main__':
    from bbsmenu import Bbsmenu
    from board import Board
    settings = {'base_dir': os.path.abspath('../data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    boards = bbsmenu.get_boards('megami')
    for board in boards:
        threads = board.get_new_threads()
        for thread in threads:
            thread.read()
