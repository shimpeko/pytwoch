import os, os.path
import re
import urllib.parse
import libpytwoch

class Pytwoch:

    def __init__(self, cache_dir_path, cache_maintain_span=90):
        # Check parameters.
        ## set error_msg to None
        error_msg = None

        ## Check right to the cache_dir_path
        if os.path.isdir(cache_dir_path) == False or \
           os.access(cache_dir_path, os.W_OK) == False:
            error_msg = cache_dir_path + ' is not exist or not writable'

        ## Check if cache_maintain_span is numeric and is between 0 to 730.
        if not isinstance(1,int):
            error_msg = 'Cache maintain span must be numeric and must be fall '+\
            'in 0 to 730'

        ## raise error if errormsg
        if error_msg:
            raise PytwoError(error_msg)

        # save config
        self.config = { 'cache_dir_path'        : cache_dir_path,
                        'cache_maintain_span'   : cache_maintain_span }


    # methods to construct 2ch objects
    def get_resource(self, url):
        resource_type = self.__get_resource_type_from_url(url)
        return resource_type

    def __get_resource_type_from_url(self, url):
        # Valid url list
        # www.2ch.net or menu.2ch.net
        # menu.2ch.net/bbsmenu.html
        # *.2ch.net/*/
        # *.2ch.net/*/subject.txt
        # *.2ch.net/test/read.cgi/*/*/
        # *.2ch.net/*/dat/*.dat
        # *.2ch.net/test/read.cgi/*/*/*
        # venus.bbspink.net/*/
        # venus.bbspink.net/*/subject.txt
        # venus.bbspink.net/test/read.cgi/*/*
        # venus.bbspink.net/dat/*.dat
        # venus.bbspink.net/test/read.cgi/*/*/*
        url_obj = urllib.parse.urlparse(url)
        r_host = re.match('^(\w+\.2ch\.net|venus\.bbspink\.net)$', url_obj.netloc)
        r_board = re.match('^/(\w+)/{0,1}(?:subject\.txt){0,1}$', url_obj.path)
        r_thread_dat = re.match('^/(\w+)/dat/(\d+\.dat)$', url_obj.path)
        r_thread_cgi = re.match('^/test/read\.cgi/(\w+)/(\d+)/'
                                '(\d+(?:-\d+){0,1}|l\d{0,4})$', url_obj.path)
        if r_host and (r_thread_dat or r_thread_cgi):
            resource_type = 'thread'
            resource_url = r_host.group(1) + '/'
            if r_thread_dat:
                resource_url = resource_url + r_thread_dat.group(1) +\
                               '/dat/' + r_thread_dat.group(2)
            elif r_thread_cgi:
                resource_url = resource_url + r_thread_cgi.group(1) +\
                               '/dat/' + r_thread_cgi.group(2) + '.dat' +\
                               '#' + r_thread_cgi.group(3)
        elif r_host and r_board:
            resource_type = 'board'
            resource_url = r_host.group(1) + '/' +  r_board.group(1) +\
                           '/subject.txt'
        elif re.match('^(www|menu)\.2ch\.net$', url_obj.netloc):
            resource_type = 'menu'
            resource_url = 'menu.2ch.net/bbsmenu.html'
        else:
            raise PytwoError('Passed URL: ' + url + ' is not 2ch URL')
        resource_url = 'http://' + resource_url
        return {'resource_type': resource_type, 'resource_url': resource_url}


if __name__ == '__main__':
    pytwoch = Pytwoch('./')
    resource_info = pytwoch.get_resource('http://toki.2ch.net/moeplus/')
    print(resource_info)

