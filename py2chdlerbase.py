import os, os.path
import urllib.request
import urllib.parse
import time
import io
import gzip
import fcntl

class Py2chdlerError(Exception):
    pass

class Py2chdlerBase:
    def download_file(self, url, mtime = None, size= None, compress = True):
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

if __name__ == '__main__':
    pass
