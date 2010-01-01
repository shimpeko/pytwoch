#/usr/bin/env python3

import urllib.request
import urllib.error
import zlib, gzip
import io
import inspect
import os, os.path
import time
import difflib

class ChDL:
    def __init__(self, base_dir, target_url):
        self.base_dir = base_dir
        self.target_url = target_url
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, 0o755)
        if not os.path.exists(self.base_dir + "dat"):
            os.mkdir(self.base_dir + "dat", 0o755)
            
        if not os.path.exists(self.base_dir + "raw_dat"):
            os.mkdir(self.base_dir + "raw_dat", 0o755)
        return None

    def dl_dat(self):
        return_status = 0
        return return_status

    def rm_dat(self):
        return None
    
    def get_updated_subjects(self):
        self.dl_subject()
    
    def dl_subject(self):
        # set subject url and path
        subject_url = self.target_url + "subject.txt"
        subject_path = self.base_dir + "subject.txt"
        # get subject.txt mtime if exists
        if os.path.exists(subject_path):
            subject_mtime = self.get_file_mtime(subject_path)
        else:
            subject_mtime = None 
        # download
        dl_data = self.download_data(subject_url, subject_mtime)
        if dl_data['code'] == 200:
            raw_subject = dl_data['text']
            # decode to unicode
            subject = raw_subject.decode('sjis', 'replace')
            # sort
            lines = io.StringIO(subject).readlines()
            lines.sort()
            lines.reverse()
            subject = "".join(lines)
            # save subject.txt
            if os.path.exists(subject_path):
                os.rename(subject_path. subject_path + ".old")
            self.save_file(subject_path, subject)
            self.set_file_mtime(subject_path, dl_data['last-modified'])
        return dl_data['code']

    def download_data(self, url, mtime, size=None):
        request = urllib.request.Request(url)
        # add headers
        if mtime:
            request.add_header('If-Modified-Since', mtime)
            print(mtime)
        if size:
            request.add_header('Range', "bytes="+size+"-")
        else:
            request.add_header('Accept-Encoding', 'gzip')
        request.add_header('User-Agent', 'Monazilla/1.00')
        # make handler
        opener = urllib.request.build_opener()
        # open url
        try:
            remote_file = opener.open(request)
            code = remote_file.code
        except urllib.error.HTTPError as e:
            code = e.code
        if code == 200:
            # read data
            last_modified = remote_file.headers['last-modified']
            data = remote_file.read()
            # close utl
            remote_file.close()
            # decompress
            bin = io.BytesIO(data)
            decompressed = gzip.GzipFile(fileobj=bin, mode="rb")
            dl_data = {"text": decompressed.read(), "last-modified": last_modified, "code": code}
        else:
            dl_data = {"text": None, "last-modified": None, "code": code}
        return dl_data

    def save_file(self, path, data):
        f = open(path, "bw")
        f.write(data.encode('sjis', 'replace'))
        f.close
        return path

    def get_file_mtime(self, path):
        stat_info = os.stat(path)
        # get file mtime in GMT
        struct_mtime = time.gmtime(stat_info.st_mtime)
        mtime = time.strftime("%a, %d %b %Y %H:%M:%S GMT", struct_mtime)
        return mtime

    def set_file_mtime(self, path, rfc1123_time):
        struct_mtime = time.strptime(rfc1123_time, "%a, %d %b %Y %H:%M:%S %Z")
        # add 9 hours to make mtime local
        mtime = time.mktime(struct_mtime) + 60*60*9
        atime = time.mktime(time.localtime())
        times = (atime, mtime)
        # set file access time and modified time
        os.utime(path, times)
        return None

# Main
if __name__ == "__main__":
    target_url="http://venus.bbspink.com/megami/"
    base_dir="/var/www/megami.fusq.net/tmp/chdl/"
    ch_downloader = ChDL(base_dir, target_url)
    subject = ch_downloader.get_subject()
