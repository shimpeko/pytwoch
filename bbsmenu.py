import os
import re

class Bbsmenu(Py2chdler):
    def __init__(self, settings, bbsmenu_url):
        self.settings = settings
        self.bbsmenu_path = self.settings['base_dir'] + "/bbsmenu"
        self.bbsmenu_url = bbsmenu_url
        self.bbsmenu = None
        self.boards = None

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

    def get_boards(self, *board_names):
        boards = list()
        bbsmenu = self.read()
        url_regex = '<A HREF=(http://[-_a-zA-Z0-9./]+)(2ch.net|bbspink.com|machi.to)/([-_a-zA-Z0-9.]+)/>(.*)</A>'
        p_url = re.compile(url_regex)
        if len(board_names) == 0:
            for line in bbsmenu:
                r_url = p_url.search(line)
                if r_url:
                    boards.append(self.get_board(r_url.group(4), r_url.group(3), r_url.group(1) + r_url.group(2) + "/" + r_url.group(3) + "/"))
        else:
            for board_name in board_names:
                for line in bbsmenu:
                    r_url = p_url.search(line)
                    if r_url:
                        if board_name == r_url.group(3):
                            boards.append(self.get_board(r_url.group(4), r_url.group(3), r_url.group(1) + r_url.group(2) + "/" + r_url.group(3) + "/"))
        return boards

    def get_board(self, board_name, board_name_alphabet, board_url):
        board = Board(self.settings, board_name, board_name_alphabet, board_url)
        return board


if __name__ == '__main__':
    from py2chdler import Py2chdler #FIXME
    from board import Board #FIXME
    py2chdler = Py2chdler('/home/shimpeko/py2chdler/data')
    bbsmenu = Bbsmenu(py2chdler.settings, 'http://menu.2ch.net/bbsmenu.html')
    boards = bbsmenu.get_boards('megami')
    for board in boards:
        print(board.board_name + board.board_name_alphabet + board.board_url)
