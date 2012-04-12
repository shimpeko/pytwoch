import sys
import os, os.path
import re
import urllib.parse

class Browser:

    def __init__(self, cache_dir_path):
        # check chache dir exsitance and privileges
        if os.path.isdir(cache_dir_path) == False or \
            os.access(cache_dir_path, os.W_OK) == False:
                raise Exception(cache_dir_path + 'is not exist or not writable.')
        self.cache_dir_path = cache_dir_path
        self.twochao = None

    # create instance
    def get_menu(self, url):
        return self.get(url)

    def get_board(self, url): 
        return self.get(url)

    def get_thread(self, url):
        return self.get(url)

    def get(self, url):
        return self.guess_resource_type(url)
        if resource_type:
           m = getattr(sys.module[__name__], resource_type)
        else:
            m = lambda u, cdp: None
        return m(url, self.cache_dir_path)

    def guess_resource_type(self, url, patterns=None):
        # define patterns if parameter is not passed
        if patterns == None:
            host = '^http://(\w+\.2ch\.net|venus\.bbspink\.net)'
            patterns  = \
                (
                    ('menu',    '^http://menu\.2ch\.net/bbsmenu.html'),
                    ('board',   host + '/\w+(/|/subject.txt)?$'),
                    ('thread',  host + '/\w+/dat/\d+.dat(#\d{1,4}(-\d{1,4})?)?$'),
                    ('thread',  host + '/test/read\.cgi/\w+/\d+/(\d{1,4}(-\d{1,4})?)?$'),
                    (None,      '.*')
                )
        # return type
        for (type, pattern) in patterns:
            if re.match(pattern, url):
                return type

if __name__ == '__main__':
    b  = Browser(".cache")
    for url in ('http://toki.2ch.net/moeplus/','http://toro.2ch.net/test/read.cgi/musicjg/1332398296/701-800'):
        print(b.get(url))

