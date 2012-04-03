import os, os.path
import re
import urllib.parse

class Browser:

    def __init__(self, cache_dir_path):
        # compile regex patters
        self.p_host = re.compile('^(\w+\.2ch\.net|venus\.bbspink\.net)$')
        self.p_menu = re.compile('^menu\.2ch\.net$')
        self.p_board = re.compile('^/(\w+)(?:/subject\.txt)$')
        self.p_thread_dat = re.compile('^/(\w+)/dat/(\d+).dat(?:#\d{1,4}(?:-\d{1,4}))$')
        self.p_thread_cgi = re.compile('^/test/read\.cgi/(\w+)/(\d+)/'
                                '(?:\#\d{1,4}(?:-\d{1,4}))$')
        # check chache dir exsitance and privileges
        if os.path.isdir(cache_dir_path) == False or \
            os.access(cache_dir_path, os.W_OK) == False:
                raise Exception(cache_dir_path + 'is not exist or not writable.')
        self.cache_dir = cache_dir
        self.twochao = None

    # create instance
    def get_menu(self, url):
        return Menu(self.get_info(url))

    def get_board(self, url): 
        return Board(self.get_info(url))

    def get_thread(self, url):
        return Thread(self.get_info(url))

    def get_type(self, url):
        return self.get_info(url)['type']

    # extract board id, thread id, comment number from url
    def get_info(self, url):
        uo = urllib.parse.urlparse(url)
        # regex pattern matching for URL 
        r_host = self.p_host.match(uo.netloc) 
        r_thread_dat = self.p_thread_dat.match(uo.path)
        r_thread_cgi = self.p_thread_cgi.match(uo.path)
        r_board = self.p_board.match(uo.path)
        r_menu = self.p_menu.match(uo.netloc)
        host_id = None
        thread_id = None
        board_id = None
        comment_num = None
        # extract Ids for each resouce type
        if r_thread_dat or r_thread_cgi:
            resouce_type = 'thread'
            if r_thread_dat:
                board_id = r_thread_dat.group(1)
                thread_id = r_thread_dat.group(2)
                comment_num = r_thread_dat.group(3)
                resource_path = r_thread_dat.group(1) + '/dat/' +\
                               r_thread_dat.group(2) + '.dat'
            elif r_thread_cgi:
                board_id = r_thread_cgi.group(1)
                thread_id = r_thread_cgi.group(2)
                comment_num = r_thread_cgi.group(3)
                resource_path = r_thread_cgi.group(1) + '/dat/' +\
                               r_thread_cgi.group(2) + '.dat'
        elif r_board:
            resource_type = 'board'
            board_id = r_board.group(1)
            resource_path = r_board.group(1) + '/subject.txt'
        elif r_menu:
            resource_type = 'menu'
            resource_path = 'bbsmenu.html'
        else:
            resource_type = None
        # make full URL
        if r_host:
            host_id = r_host.group(1)
            resource_url = "http://" + r_host.group(1) + "/" + resource_path
        else:
            resource_url = None
        return resource_info = { 'type'          : resource_type,
                                 'url'           : resource_url,
                                 'host_id'       : host_id
                                 'board_id'      : board_id,
                                 'thread_id'     : thread_id
                                 'comment_num'   : comment_num }

if __name__ == '__main__':
    b  = Browser()
    t = b.get_type('http://toki.2ch.net/moeplus/')
    print(t)

