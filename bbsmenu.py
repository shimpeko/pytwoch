import os
import re

from py2chdlerbase import Py2chdlerBase, Py2chdlerError
from board import Board #FIXME

class Bbsmenu(Py2chdlerBase):
    def __init__(self, settings, bbsmenu_url):
        self.settings = settings
        self.bbsmenu_path = self.settings['base_dir'] + "/bbsmenu"
        self.bbsmenu_url = bbsmenu_url

    def read(self):
        if os.path.exists(self.bbsmenu_path):
            lines = self.read_file(self.bbsmenu_path)
        else:
            self.download()
            lines = self.read_file(self.bbsmenu_path)
        return lines

    def download(self):
        self.rename_file(self.bbsmenu_path)
        dl_data = self.download_file(self.bbsmenu_url)
        self.write_file(self.bbsmenu_path, dl_data['text'])

    def get_boards(self, *board_names_alphabet):
        boards = list()
        bbsmenu = self.read()
        # convert tumple to list to use remove method
        board_names_alphabet = list(board_names_alphabet)
        # get requested board number
        req = len(board_names_alphabet)
        url_regex = '<A HREF=(http://[-_a-zA-Z0-9./]+)(2ch.net|bbspink.com|machi.to)/([-_a-zA-Z0-9.]+)/>(.*)</A>'
        p_url = re.compile(url_regex)
        for line in bbsmenu:
            r_url = p_url.search(line)
            if r_url:
                if req == 0 or r_url.group(3) in board_names_alphabet:
                    board = Board(self, r_url.group(4), r_url.group(3), r_url.group(1) + r_url.group(2) + "/" + r_url.group(3) + "/")
                    boards.append(board)
                    if r_url.group(3) in board_names_alphabet:
                        board_names_alphabet.remove(r_url.group(3))
        # raise err if requested board not exists
        if not len(board_names_alphabet) == 0:
            err_boards = ', '.join(board_names_alphabet)
            raise Py2chdlerError("Board(s) name: " + err_boards + " are/is not exist(s). Or you may request same board more than once.")
        return boards

    def get_board(self, board_name_alphabet):
        boards = self.get_boards(board_name_alphabet)
        return boards[0]

if __name__ == '__main__':
    settings = {'base_dir': os.path.abspath('data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    bbsmenu.download()
    boards = bbsmenu.get_boards('news4vip')
    for board in boards:
        print(board.board_name + board.board_name_alphabet + board.board_url)
