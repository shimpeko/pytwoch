import os

from py2chdler import Py2chdler

class Board(Py2chdler):
    def __init__(self, settings, board_name, board_name_alphabet, board_url):
        self.setting = settings
        self.board_name = board_name
        self.board_name_alphabet = board_name_alphabet
        self.board_url = board_url
        self.threads = None


if __name__ == '__main__':
    py2chdler = Py2chdler('/home/shimpeko/py2chdler/data', 'http://menu.2ch.net/bbsmenu.html')
    board = Board(py2chdler.settings, None, None, None)
