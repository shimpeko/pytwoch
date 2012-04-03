import os, os.path
import shutil
import urllib.request
import urllib.parse
import time
import io
import gzip
import fcntl
import re

class TwoChAO: 

    def __init__(self, config):
        
        self.config = config
    
    def get(self, resource_info):
        """ Access 2ch data
        """
        response = self.__http_get(resource_info['url'])
        return response

    def __http_get(self, url, mtime=None, byte_from=None):
        """ http get
        """
        request = urllib.request.Request(url)

        # add header
        if mtime:
            request.add_header('If-Modified-Since', mtime)
        if byte_from:
            request.add_header('Range', "bytes=" + str(byte_from) + "-")
        else:
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
            status_code = e.code
        # process data if success
        if status_code == 200 or status_code == 206:
            content = response.read()
            response.close()
            # if compressed, decompress data
            if byte_from == None:
                if re.search('.*(gzip|deflate).*',
                             response.headers['content-encoding'])
                    b = io.BytesIO(content)
                    decompressed = gzip.GzipFile(fileobj=b, mode="rb")
                    content = decompressed.read()
            response = { "status"           : status_code,
                         "last-modified"    : response.headers['last-modified'],
                         "content-length"   : response.headers['content-length'],
                         "content"          : content[1-] }
        else:
            response.close()
            response = { "status"           : status_code,
                         "last-modified"    : None,
                         "content-length"   : None,
                         "content"          : None }
        return response

    def __check_abone(self):
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


    def __get_cache_file_path(self, resource_info, config):
        if resource_info['type'] == 'menu':
            cache_file_path = config['cache_dir_path'] + '/' + 'bbsmenu.html'
        elif resource_info['type'] == 'board':
            cache_file_path = config['cache_dir_path'] + '/' +\
                              resource_info['id']['board_id'] + 'subject.txt'
        elif resource_info['type'] == 'thread':
            cache_file_path = config['cache_dir_path'] + '/' +\
                              resource_info['id']['board_id'] +\
                              resource_info['id']['thread_id']
        else:
            cache_file_path = None
        return cache_file_path

    def __save_cache(self, response)
        if response['code'] == 200:
            self.write_file(file_path, response['content'])
        if response['code'] == 206:
            self.write_file(file_path, response['content'], True)
        self.set_mtime(filepath, 
                       self.convert_time_format(response['last-modified']))

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
