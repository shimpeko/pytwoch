import os, os.path
import shutil
import urllib.request
import urllib.parse
import time
import io
import gzip
import fcntl
import re

class PytwochError(Exception):
    pass

class Resouce:

    def __init__(self, url):



    
    def get_resouce(self, url, file_path):

        if re.match('^.*\.dat$', url):
            is_dat_url = True
        else:
            is_dat_url = False
        is_cache_exists = os.path.exists(file_path)

        cache_mtime = self.get_mtime(file_path)
        if is_cache_exists and is_dat_url:
            cache_size = os.path.getsize(file_path) - 1
        else:
            cache_size = None

        response = self.http_get(url)

        # check abone and retry if abone
        if is_dat_url and is_cache_exists:
            if not response['content'][0].decode('sjis', 'replace') == "\n":
                response = self.http_get(url, cache_mtime)

        # save cache
        if response['code'] == 200 or response['code'] == 206:
            if response['code'] == 206:
                shutil.copy2(file_path, file_path + "_old")
            self.__save_cache(response)
        elif response['code'] == 304:
        else:
            raise Py2chdlerError("HTTPERROR:" + code + ": Can't access " + url
                                 + ".")

        # make return value 
        if response['code'] == 200 or response['code'] == 206 or\
           response['code'] == 304:
            ret_val = { "code"   : response['code'],
                        "content": response['content'][1-] }
        else:
            ret_val = { "code"   : response['code'],
                        "content": None }
        return ret_val


    def __get_type(url):

    def __get_cache_file_path():
        pass

    def is_updated():
        pass
    
    def reload():
        pass

    def get_content():
        pass

    def _set_url(self, url):
        if self.__is_url_valid():
            self.url = url
        else:
            self.url = self.__correct_url()
        return url

    def __is_url_valid():
        return ret_val

    def __correct_url():
        return url

    def __download():

        if re.match('^.*\.dat$', url):
            is_dat_url = True
        else:
            is_dat_url = False
        is_cache_exists = os.path.exists(file_path)

        cache_mtime = self.get_mtime(file_path)
        if is_cache_exists and is_dat_url:
            cache_size = os.path.getsize(file_path) - 1
        else:
            cache_size = None

        response = self.http_get(url)

        # check abone and retry if abone
        if is_dat_url and is_cache_exists:
            if not response['content'][0].decode('sjis', 'replace') == "\n":
                response = self.http_get(url, cache_mtime)

        # save cache
        if response['code'] == 200 or response['code'] == 206:
            if response['code'] == 206:
                shutil.copy2(file_path, file_path + "_old")
            self.__save_cache(response)
        elif response['code'] == 304:
        else:
            raise Py2chdlerError("HTTPERROR:" + code + ": Can't access " + url
                                 + ".")

        # make return value 
        if response['code'] == 200 or response['code'] == 206 or\
           response['code'] == 304:
            ret_val = { "code"   : response['code'],
                        "content": response['content'][1-] }
        else:
            ret_val = { "code"   : response['code'],
                        "content": None }
        return ret_val


    def __save_cache(self, response)
        if response['code'] == 200:
            self.write_file(file_path, response['content'])
        if response['code'] == 206:
            self.write_file(file_path, response['content'], True)
        self.set_mtime(filepath, 
                       self.convert_time_format(response['last-modified']))


    def __http_get(self, url, mtime, byte_from):
        request = urllib.request.Request(url)

        # add header
        if mtime:
            request.add_header('If-Modified-Since', mtime)
        if byte_from:
            request.add_header('Range', "bytes=" + str(byte_from) + "-")
        else:
            is_compressed = True
            request.add_header('Accept-Encoding', 'deflate, gzip')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; '
                           'en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 '
                           '(.NET CLR 3.5.30729)')

        # open request
        opener = urllib.request.build_opener()
        try:
            response = opener.open(request)
            response_coode = response.code
        except urllib.error.HTTPError as e:
            response_code = e.code

        # if success process data
        if response_code == 200 or response_code == 206:
            content = response.read()
            response.close()
            # if compressed, decompress data
            if is_compressed == True and byte_from == None:
                if re.search('.*(gzip|deflate).*',
                             response.headers['content-encoding'])
                    bin = io.BytesIO(content)
                    decompressed = gzip.GzipFile(fileobj=bin, mode="rb")
                    content = decompressed.read()
            response = { "code"             : response_code,
                         "etag"             : response.headers['etag'],
                         "last-modified"    : response.headers['last-modified'],
                         "content-length"   : response.headers['content-length'],
                         "content"          : content }
        else:
            response.close()
            response = { "code"             : response_code,
                         "etag"             : None,
                         "last-modified"    : None,
                         "content-length"   : None,
                         "content"          : None }
        return response


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

    def set_mtime(self, file_path, mtime):
        atime = time.time()
        times = (atime, mtime)
        stat = os.utime(file_path, times)

    def get_mtime(file_path):
        mtime = None
        if os.path.exists(file_path):
            mtime = self.convert_time_format(os.path.gettime(file_path))
        return mtime

    def convert_time_format(self, inp_time, change_tz=True):
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
