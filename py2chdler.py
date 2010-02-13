import os, os.path
import urllib.url
import urllib.urlparse

import bbsmenu

class Py2chdlerError(Exception):
    pass

class Py2chdler:
    def __init__(self, base_dir, menu_url):
        self.base_dir = base_dir
        self.menu_url = menu_url
        # check existance and access rights of base_dir
        if os.path.isdir(base_dir) == False or os.access(base_dir, os.W_OK) == False:
            raise Py2chdlerError(base_dir + " not exists or not writable")

    def download(self, url, mtime = None, compress = True, unfreeze = True):
        # create request object
        request = urllib.request.Request(url)
        # add headers
        request.add_header('Accept-Encoding', 'gzip')
        request.add_header('User-Agent', 'Monazilla/1.00')
        # open url
        opener = urllib.request.build_opener()
        remote_file_stream = opener.open(request)
        # read data
        data = remote_file_stream.read()
        remote_file.close()
        # not sure but making "file like object" on memory
        bin = io.BytesIO(data)
        # decompress data
        decompressed = gzip.GzipFile(fileobj=bin, mode="rb")
        # return data
        return decompressed.read()

    def write_file(self, path, data, add=False):
        if add:
           fs = io.open(path, "ba")
        else:
           fs = io.open(path, "bw")
        fcntl.flock(fs.fileno(), fcntl.LOCK_EX)
        fs.write(data)
        fcntl.flock(fs.fileno(), fcntl.LOCK_UN)
        fs.close
        return path

    def read_file(self, path):
        fs = io.open(path, mode='rb')
        fcntl.flock(fs.fileno(), fcntl.LOCK_SH)
        data = fs.read()
        fcntl.flock(fs.fileno(), fcntl.LOCK_UN)
        fs.close()
        data = data.decode('sjis', 'replace')
        lines = data.splitlines()
        return lines


if __name__ == '__main__':
    py2chdler = Py2chdler('/home/shimpeko/py2chdler/data', 'http://menu.2ch.net/bbsmenu.html')
    exit()
