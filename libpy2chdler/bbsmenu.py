import os
import re

from base import Base, Py2chdlerError
from board import Board #FIXME

class Bbsmenu(Base):
    def __init__(self, settings, bbsmenu_url):
        self.settings = settings
        self.filepath = self.settings['base_dir'] + "/bbsmenu"
        self.filepath_old = self.filepath + "_old"
        self.url = bbsmenu_url

    def read(self):
        board_infos = list()
        self.download(self.url, self.filepath)
        bbsmenu = self.read_file(self.filepath)
        url_regex = '<A HREF=(http://[-_a-zA-Z0-9./]+)(2ch.net|bbspink.com)/([-_a-zA-Z0-9.]+)/>(.*)</A>'
        no_board_names = ['wiki','rank']
        p_url = re.compile(url_regex)
        for line in bbsmenu:
            r_url = p_url.search(line)
            if r_url:
                if not r_url.group(3) in no_board_names:
                    board_info = dict()
                    board_info['name'] = r_url.group(4)
                    board_info['romaji_name'] = r_url.group(3)
                    board_info['url'] = r_url.group(1) + r_url.group(2) + "/" + r_url.group(3) + "/"
                    board_infos.append(board_info)
        return board_infos

    def read_raw(self):
        self.download(self.url, self.filepath)
        raw_bbsmenu = self.read_raw_file(self.filepath)
        return raw_bbsmenu

    def get_boards(self, *romaji_board_names):
        boards = list()
        board_infos = self.read()
        # list to store obtained board names
        exist_romaji_board_names = list()
        if len(romaji_board_names) == 0:
            for board_info in board_infos:
                boards = self.__append_board(boards, board_info)
        else:
            for board_info in board_infos:
                if board_info['romaji_name'] in romaji_board_names:
                    boards = self.__append_board(boards, board_info)
                    # if requested board name is in bbsmenu, add the board name to obtabined_romaji_boarad_names list
                    if board_info['romaji_name'] in romaji_board_names:
                        exist_romaji_board_names.append(board_info['romaji_name'])
            # raise err if requested board not exists
            if not len(romaji_board_names) == len(exist_romaji_board_names):
                err_romaji_board_names = set(romaji_board_names) - set(exist_romaji_board_names)
                err_romaji_board_names = ', '.join(err_romaji_board_names)
                raise Py2chdlerError("Board(s) name: " + err_romaji_board_names + " are/is not exist(s). Or you may request same board more than once.")
        return boards

    def get_board(self, romaji_board_name):
        boards = self.get_boards(romaji_board_name)
        return boards[0]

    def __append_board(self, boards, board_info):
        board = Board(self, board_info['name'], board_info['romaji_name'], board_info['url'])
        boards.append(board)
        return boards

if __name__ == '__main__':
    import time
    settings = {'base_dir': os.path.abspath('../data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    board_infos = bbsmenu.read()
    for board_info in board_infos:
        print(board_info)
    time.sleep(3)
    boards = bbsmenu.get_boards('news4vip', 'pc')
    for board in boards:
        print(board.name + "|" + board.romaji_name + "|" + board.url + "|" + board.filepath + "|" + board.filepath_old + "|" + board.dir_path)
    time.sleep(3)
    boards = bbsmenu.get_boards()
    for board in boards:
        print(board.name + "|" + board.romaji_name + "|" + board.url + "|" + board.filepath + "|" + board.filepath_old + "|" + board.dir_path)
    time.sleep(3)
    board = bbsmenu.get_board('news4vip')
    print(board.name + "|" + board.romaji_name + "|" + board.url + "|" + board.filepath + "|" + board.filepath_old + "|" + board.dir_path)
