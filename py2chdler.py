import os, os.path
import urllib.request
import urllib.parse
import time
import io
import gzip
import fcntl

import bbsmenu

class Py2chdlerError(Exception):
    pass

class Py2chdler:
    setting = {}
    def __init__(self, base_dir, bbsmenu_url):
        self.settings = {'base_dir': base_dir}
        self.bbsmenu = bbsmenu.Bbsmenu(self.settings, bbsmenu_url)
        # check existance and access rights of base_dir
        if os.path.isdir(base_dir) == False or os.access(base_dir, os.W_OK) == False:
            raise Py2chdlerError(base_dir + " not exists or not writable")

    def download(self, url, mtime = None, size= None, compress = True):
        # create request object
        request = urllib.request.Request(url)
        # add headers
        if mtime:
            request.add_header('If-Modified-Since', mtime)
        if size:
            request.add_header('Range', "bytes=" + str(size) + "-")
        elif compress:
            request.add_header('Accept-Encoding', 'deflate, gzip')
        request.add_header('User-Agent', 'Monazilla/1.00')
        opener = urllib.request.build_opener()
        # Catch HTTPError as set code
        try:
            remote_file = opener.open(request)
            code = remote_file.code
        except urllib.error.HTTPError as e:
            code = e.code
        # if access success, read data
        if code == 200 or code == 206:
            etag = remote_file.headers['etag']
            last_modified = remote_file.headers['last-modified']
            content_length = remote_file.headers['content-length']
            data = remote_file.read()
            remote_file.close()
            # if compressed, decompress data
            if compress == True:
                bin = io.BytesIO(data)
                decompressed = gzip.GzipFile(fileobj=bin, mode="rb")
                text = decompressed.read()
            else:
                text = data
        # Set default value as None if download fails
        else:
            code = code; etag = None; last_modified = None; content_length = None; text= None
        # make dl_data dic
        dl_data = {"code": code, "etag": etag, "last-modified": last_modified, "content-length": content_length, "text": text}
        return dl_data

    def write_file(self, filepath, data, add=False):
        if add:
           fs = io.open(filepath, "ba")
        else:
           fs = io.open(filepath, "bw")
        fcntl.flock(fs.fileno(), fcntl.LOCK_EX)
        fs.write(data)
        fcntl.flock(fs.fileno(), fcntl.LOCK_UN)
        fs.close

    def read_file(self, filepath):
        fs = io.open(filepath, mode='rb')
        fcntl.flock(fs.fileno(), fcntl.LOCK_SH)
        data = fs.read()
        fcntl.flock(fs.fileno(), fcntl.LOCK_UN)
        fs.close()
        data = data.decode('sjis', 'replace')
        lines = data.splitlines()
        return lines

    def rename_file(self, from_filepath):
        # set to_filepath as from_filepath.old
        to_filepath = from_filepath + ".old"
        if os.path.exists(from_filepath):
            os.rename(from_filepath, to_filepath)

    def get_mtime(self, filepath):
        stat = os.stat(filepath)
        return stat.st_mtime

    def set_mtime(self, filepath, mtime):
        atime = time.time()
        times = (atime, mtime)
        stat = os.utime(filepath, times)

    #
    # methods to construct 2ch objects
    #
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
    py2chdler = Py2chdler('/home/shimpeko/py2chdler/data', 'http://menu.2ch.net/bbsmenu.html')
    bbsmenu = py2chdler.get_bbsmenu()
    boards = bbsmenu.get_boards('megami')
    for board in boards:
        print(board.board_name + board.board_name_alphabet + board.board_url)
    bbsmenu.reload()
