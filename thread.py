from py2chdlerbase import Py2chdlerBase, Py2chdlerError

class Thread(Py2chdlerBase):
    def __init__(self, board, thread_id, title, board_url):
        self.board = board
        self.thread_id = thread_id
        self.title = title
        self.thread_url = board_url + "/dat/" + thread_id + ".dat"
        self.res_count = None
        self.new_res_count = None
        self.reses = None

    def get_reses(self, *res_ids):
        pass
    
    def get_res(self, res_id):
        pass


if __name__ == '__main__':
    pass
