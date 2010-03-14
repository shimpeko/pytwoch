import os, os.path
import shutil
import urllib.request
import urllib.parse
import time
import io
import gzip
import fcntl
import re

class Py2chdlerError(Exception):
    pass

class Base:

    def http_get(self, url, mtime = None, size=None, compress=True):
        # create request object
        request = urllib.request.Request(url)
        # add headers
        if mtime:
            request.add_header('If-Modified-Since', mtime)
        if size:
            request.add_header('Range', "bytes=" + str(size) + "-")
        elif compress:
            request.add_header('Accept-Encoding', 'deflate, gzip')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)')
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
            if compress == True and size == None:
                content_encoding = remote_file.headers['content-encoding']
                p_zip = re.compile('.*(gzip|deflate).*')
                r_zip = p_zip.search(content_encoding) if content_encoding else False
                if r_zip:
                    bin = io.BytesIO(content)
                    decompressed = gzip.GzipFile(fileobj=bin, mode="rb")
                    content = decompressed.read()
        # Set default value as None if download fails
        else:
            code = code; etag = None; last_modified = None; content_length = None; content= None
        # make data dic
        response = {"code": code, "etag": etag, "last-modified": last_modified, "content-length": content_length, "content": content}
        return response

    def download(self, url, filepath, err_stop=True):
        file_existance = os.path.exists(filepath)
        local_mtime = self.convert_time_format(os.path.getmtime(filepath)) if file_existance else None
        # pass size to http_get method if request file is dat
        p_dat = re.compile('^.*\.dat$')
        r_dat = p_dat.match(url)
        if r_dat:
            filesize = os.path.getsize(filepath) - 1 if file_existance else None
        else:
            filesize = None
        # get remote file
        response = self.http_get(url, local_mtime, filesize)
        # chk abone
        if response['code'] == 206:
            content = response['content'].decode('sjis', 'replace')
            if not content[0] == "\n":
                response = self.http_get(url, local_mtime)
        # get response code
        code = response['code']
        if code == 200 or code == 206 or code == 304:
            if file_existance:
                self.copy_file(filepath)
            if code == 200 or code == 206:
                if file_existance:
                    self.copy_file(filepath)
                # add to file if response code eq 206
                add = True if code == 206 else False
                self.write_file(filepath, response['content'], add)
                remote_mtime = self.convert_time_format(response['last-modified'])
                self.set_mtime(filepath, remote_mtime)
        elif err_stop == True:
            raise Py2chdlerError("HTTPERROR: Can't access " + url +". The response code is: " + str(code))
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
        to_filepath = from_filepath + "_old"
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
            time_struct = time.gmtime(inp_time)
            ret_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time_struct)
        return ret_time

if __name__ == '__main__':
    base = Base()
    ret_time = base.convert_time_format("Jan, Thu 01 1970 09:00:00 GMT")
    print(ret_time)
