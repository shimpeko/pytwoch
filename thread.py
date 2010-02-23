from py2chdlerbase import Py2chdlerBase, Py2chdlerError

class Thread(Py2chdlerBase):
    def __init__(self, board, thread_id, title, res_count):
        self.board = board
        self.thread_id = thread_id
        self.title = title
        self.thread_url = None
        self.dat_url = None
        self.res_count = res_count
        self.new_res_count = None
        self.reses = None

    def get_reses(self, *res_ids):
        pass
    
    def get_res(self, res_id):
        pass


if __name__ == '__main__':
    pass
