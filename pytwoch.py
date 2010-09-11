import os, os.path
from libpy2chdler import bbsmenu

class Py2chdler:
    def __init__(self, base_dir, bbsmenu_url):
        self.settings = {'base_dir': base_dir}
        self.bbsmenu = Bbsmenu(self.settings, bbsmenu_url)
        # check rights to base_dir
        if os.path.isdir(base_dir) == False or os.access(base_dir, os.W_OK) == False:
            raise Py2chdlerError(base_dir + " not exists or not writable")

    # methods to construct 2ch objects
    def get_bbsmenu(self):
        return self.bbsmenu;
    def get_boards(self, *board_names):
        return self.bbsmenu.get_boards(board_names)
    def get_board(self, board_name):
        return self.bbsmenu.get_board(board_name)
#    # args are tuple of "board_name" and "thread_id"
#    def get_threads(self, *args):
#        pass
#    def get_thread(self, board_name, thread_id):
#        pass
#    def get_new_thread(self):
#        pass
#    def get_reses(self, *args):
#        pass
#    # args are tuple of "board_name", "thread_id", and "res_id"
#    def get_res(self, board_name, thread_id, res_id):
#        pass
#    def get_new_reses(self):
#        pass


if __name__ == '__main__':
    py2chdler = Py2chdler(os.path.abspath('data'), 'http://menu.2ch.net/bbsmenu.html')
    bbsmenu = py2chdler.get_bbsmenu()
    boards = bbsmenu.get_boards('megami', 'neet4pink')
    for board in boards:
        print(board.board_name + board.board_name_alphabet + board.board_url)
    bbsmenu.download()
