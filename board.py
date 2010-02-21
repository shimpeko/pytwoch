import os

from py2chdlerbase import Py2chdlerBase, Py2chdlerError
from thread import Thread

class Board(Py2chdlerBase):
    def __init__(self, bbsmenu, board_name, board_name_alphabet, board_url):
        self.bbsmenu = bbsmenu
        self.board_name = board_name
        self.board_name_alphabet = board_name_alphabet
        self.board_url = board_url
        self.subject_url = self.board_url + "subject.txt"
        self.board_dir = self.bbsmenu.settings['base_dir'] + "/" + self.board_name_alphabet
        self.subject_path = self.board_dir + "/subject.txt"
        self.threads = None
        if not os.path.exists(self.board_dir):
            os.mkdir(self.board_dir)
        elif not os.path.isdir(self.board_dir):
            raise Py2chdlerError(self.board_dir + " is not a directory.")

    def read():
        if os.path.exists(self.subject_path):
            lines = self.read_file(self.subject_path)
        else:
            self.download()
            lines = self.read_file(self.subject_path)
        return lines

    def download():
        self.rename_file(self.subject_path)
        dl_data = self.download_file(self.subject_url)
        self.write_file(self.subject_path, dl_data['text'])

    def get_threads(self, *thread_ids):
        pass
    
    def get_thread(self, thread_id):
        pass


if __name__ == '__main__':
    pass
