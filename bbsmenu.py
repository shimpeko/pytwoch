import py2chdler

class Bbsmenu(Py2chdler):
    def __init__(self):
        self.boards = None

    def get_boards(self):
        pass

    def get_board(self, board_name):
        pass

    def read_bbsmenu(self):
        bbsmenu_path = self.base_dir + "/" + bbsmenu
        if os.path.exists:
            self.read_file( bbsmenu_path)
        else:
            data = self.download(self.menu_url)
            self.write_file(bbsmenu_path, data)
  
if __name__ == '__main__':
    py2chdler = Py2chdler('/home/shimpeko/py2chdler/data', 'http://menu.2ch.net/bbsmenu.html')
    exit()
