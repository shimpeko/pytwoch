import os, os.path
import re
import urllib.parse
import libpytwoch

class Pytwoch:

    def __init__(self, cache_dir_path=None, cache_size=1000000):
        # Check parameters.
        # Check right to the cache_dir_path
        if os.path.isdir(cache_dir_path) == False or \
           os.access(cache_dir_path, os.W_OK) == False:
            raise PytwoException(cache_dir_path + 'is not exist or not writable.')
        # Check if cache_size is numeric.
        if not isinstance(cache_size,int):
            raise PytwoException('cache_size parameter must be numeric.')
        # save config
        self.config = { 'cache_dir_path'    : cache_dir_path,
                        'cache_size'        : cache_size }
        self.twochao = TwoChAO(self.config)

    # construct 2ch objects
    def get(self, url): 
        return resource_type

    def get_resource_info(self, url):
        url_obj = urllib.parse.urlparse(url)
        r_host = re.match('^(\w+\.2ch\.net|venus\.bbspink\.net)$', url_obj.netloc)
        r_menu = re.match('^menu\.2ch\.net$', url_obj.netloc)
        r_board = re.match('^/(\w+)/{0,1}(?:subject\.txt){0,1}$', url_obj.path)
        r_thread_dat = re.match('^/(\w+)/dat/(\d+).dat$', url_obj.path)
        r_thread_cgi = re.match('^/test/read\.cgi/(\w+)/(\d+)/'
                                '(\d+(?:-\d+){0,1}|l\d{0,4})$', url_obj.path)
        if r_host and (r_thread_dat or r_thread_cgi):
            resource_type = 'thread'
            resource_url = r_host.group(1) + '/'
            if r_thread_dat:
                board_id = r_thread_dat.group(1)
                thread_id = r_thread_dat.group(2)
                resource_url = resource_url + r_thread_dat.group(1) +\
                               '/dat/' + r_thread_dat.group(2) + '.dat'
            elif r_thread_cgi:
                board_id = r_thread_cgi.group(1)
                thread_id = r_thread_cgi.group(2)
                resource_url = resource_url + r_thread_cgi.group(1) +\
                               '/dat/' + r_thread_cgi.group(2) + '.dat' +\
                               '#' + r_thread_cgi.group(3)
        elif r_host and r_board:
            resource_type = 'board'
            board_id = r_board.group(1)
            thread_id = None
            resource_url = r_host.group(1) + '/' +  r_board.group(1) +\
                           '/subject.txt'
        elif r_menu: 
            resource_type = 'menu'
            board_id =  None
            thread_id = None
            resource_url = 'menu.2ch.net/bbsmenu.html'
        else:
            resource_type = None 
        if resource_type:
            resource_info = { 'type'    : resource_type,
                              'url'     : 'http://' + resource_url,
                              'id'      : { 'host_id'   : r_host.group(1),
                                            'board_id'  : board_id,
                                            'thread_id' : thread_id}}
        else:
            resource_info = None
        return resource_info

if __name__ == '__main__':
    pytwoch = Pytwoch('./')
    resource_info = pytwoch.get_resource_info('http://toki.2ch.net/moeplus/')
    print(resource_info)

