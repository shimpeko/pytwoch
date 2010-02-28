import os
import re

from base import Base, Py2chdlerError
from board import Board #FIXME

class Bbsmenu(Base):
    def __init__(self, settings, bbsmenu_url):
        self.settings = settings
        self.filepath = self.settings['base_dir'] + "/bbsmenu"
        self.url = bbsmenu_url
        self.download(self.url, self.filepath)

    def read(self):
        board_infos = list()
        lines = self.read_file(self.filepath)
        url_regex = '<A HREF=(http://[-_a-zA-Z0-9./]+)(2ch.net|bbspink.com|machi.to)/([-_a-zA-Z0-9.]+)/>(.*)</A>'
        p_url = re.compile(url_regex)
        for line in lines:
            r_url = p_url.search(line)
            if r_url:
                board_info = {'name':r_url.group(4), 'romaji_name':r_url.group(3), 'url':r_url.group(1) + r_url.group(2) + "/" + r_url.group(3) + "/"}
                board_infos.append(board_info)
        return board_infos

    def read_raw():
        data = read_raw_file()
        return data

    def get_boards(self, *romaji_board_names):
        boards = list()
        board_infos = self.read()
        # list to store obtained board names
        obtained_romaji_board_names = list()
        url_regex = '<A HREF=(http://[-_a-zA-Z0-9./]+)(2ch.net|bbspink.com|machi.to)/([-_a-zA-Z0-9.]+)/>(.*)</A>'
        p_url = re.compile(url_regex)
        for board_info in board_infos:
            if len(romaji_board_names) == 0 or board_info['romaji_name'] in romaji_board_names:
                board = Board(self, board_info['name'], board_info['romaji_name'], board_info['url'])
                boards.append(board)
                if board_info['romaji_name'] in romaji_board_names:
                    obtained_romaji_board_names.append(board_info['romaji_name'])
        # raise err if requested board not exists
        if not len(romaji_board_names) == len(obtained_romaji_board_names):
            err_romaji_board_names = romaji_board_names - set(obtained_romaji_board_names)
            err_romaji_board_names = ', '.join(err_romaji_board_names)
            raise Py2chdlerError("Board(s) name: " + err_romaji_board_names + " are/is not exist(s). Or you may request same board more than once.")
        return boards

    def get_board(self, romaji_board_name):
        boards = self.get_boards(romaji_board_name)
        return boards[0]

if __name__ == '__main__':
    settings = {'base_dir': os.path.abspath('../data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    boards = bbsmenu.get_boards('news4vip')
    for board in boards:
        print(board.name + board.romaji_name + board.url)
