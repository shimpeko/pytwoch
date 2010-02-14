import os

class Board(Py2chdler):
    def __init__(self, settings, board_name, board_name_alphabet, board_url):
        self.settings = settings
        self.board_name = board_name
        self.board_name_alphabet = board_name_alphabet
        self.board_url = board_url
        self.subject_url = self.board_url + "subject.txt"
        self.board_dir = self.settings['base_dir'] + "/" + self.board_name_alphabet
        self.subject_path = self.board_dir + "/subject.txt"
        self.threads = None
        if not os.path.exists(self.board_dir):
            os.mkdir(self.board_dir)
        elif not os.path.isdir(self.board_dir):
            raise Py2chdlerError(self.board_dir + " is not a directory.")

    def read():
        pass

    def download():
        self.rename_file(self.subject_path)
        dl_data = self.download_file(self.subject_url)
        self.write_file(self.subject_path, dl_data['text'])

    def get_threads(self, *thread_ids):
        pass
    
    def get_threads(self, thread_id):
        pass


if __name__ == '__main__':
    from py2chdler import Py2chdler, Py2chdlerError #FIXME
    py2chdler = Py2chdler('/home/shimpeko/py2chdler/data', 'http://menu.2ch.net/bbsmenu.html')
    board = Board(py2chdler.settings, None, None, None)
