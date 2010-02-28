import os, os.path
import shutil
import urllib.request
import urllib.parse
import time
import io
import gzip
import fcntl

class Py2chdlerError(Exception):
    pass

class Base:

    def http_get(self, url, mtime = None, size= None, compress = True):
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
            content = remote_file.read()
            remote_file.close()
            # if compressed, decompress data
            if compress == True:
                bin = io.BytesIO(content)
                decompressed = gzip.GzipFile(fileobj=bin, mode="rb")
                content = decompressed.read()
            else:
                content = content
        # Set default value as None if download fails
        else:
            code = code; etag = None; last_modified = None; content_length = None; content= None
        # make data dic
        response = {"code": code, "etag": etag, "last-modified": last_modified, "content-length": content_length, "content": content}
        return response

    def download(self, url, filepath):
        if os.path.exists(filepath):
            local_mtime = self.convert_time_format(os.path.getmtime(filepath))
        else:
            local_mtime = None
        response = self.http_get(url, local_mtime)
        code = response['code']
        if code == 200 or code == 206:
            self.copy_file(filepath)
            if code == 206:
                add = True
            else:
                add = False
            self.write_file(filepath, response['content'], add)
            remote_mtime = self.convert_time_format(response['last-modified'])
            self.set_mtime(filepath, remote_mtime)
        elif code == 304:
            pass
        else:
            raise Py2chdlerError( "HTTPError: " + code)
        return code


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

    def read_raw_file(self, filepath):
        fs = io.open(filepath, mode='rb')
        fcntl.flock(fs.fileno(), fcntl.LOCK_SH)
        data = fs.read()
        fcntl.flock(fs.fileno(), fcntl.LOCK_UN)
        fs.close()
        return data

    def copy_file(self, from_filepath):
        to_filepath = from_filepath + ".old"
        shutil.copy2(from_filepath, to_filepath)

    def set_mtime(self, filepath, mtime):
        atime = time.time()
        times = (atime, mtime)
        stat = os.utime(filepath, times)
    
    def convert_time_format(self, inp_time , change_tz=True):
        if isinstance(inp_time, str):
            time_struct = time.strptime(inp_time, "%a, %d %b %Y %H:%M:%S %Z")
            ret_time = int(time.mktime(time_struct) + 32400)
        else:
            time_struct = time.gmtime(inp_time - 32400)
            ret_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time_struct)
        return ret_time

if __name__ == '__main__':
    base = Base()
    ret_time = base.convert_time_format("Jan, Thu 01 1970 09:00:00 GMT")
    print(ret_time)
