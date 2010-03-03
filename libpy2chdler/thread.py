import urllib.parse
import os
from base import Base, Py2chdlerError


class Thread(Base):
    def __init__(self, board, thread_id, title, res_count):
        self.board = board
        self.id = thread_id
        self.title = title
        self.filepath = self.board.dir_path + "/" + str(self.id) + ".dat"
        self.res_count = res_count
        self.new_res_count = None
        self.reses = None
        self.url = self.board.url + "dat/" + str(self.id) + ".dat"

    def read(self):
        if os.path.exists(self.filepath):
            lines = self.read_file(self.filepath)
        else:
            self.download()
            lines = self.read_file(self.filepath)
        return lines

    def download(self):
        mtime = self.get_mtime(self.filepath)
        self.rename_file(self.filepath)
        dl_data = self.download_file(self.url, mtime)
        self.write_file(self.filepath, dl_data['text'])
        self.set_mtime(self.filepath, dl_data['last-modified'])


    def get_reses(self, *res_ids):
        pass
    
    def get_res(self, res_id):
        pass

if __name__ == '__main__':
    from bbsmenu import Bbsmenu
    settings = {'base_dir': os.path.abspath('../data')}
    bbsmenu = Bbsmenu(settings, 'http://menu.2ch.net/bbsmenu.html')
    boards = bbsmenu.get_boards('megami')
    for board in boards:
        threads = board.get_threads()
        for thread in threads:
            thread.download()
            print(thread.url)

