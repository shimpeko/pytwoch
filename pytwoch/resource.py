import abc

class Resouce(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, resource_info, cache_dir_path):

    def retreive(self, url, file_path):
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
            raise Exception("HTTPERROR:" + code + ": Can't access " + url
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

    def get_url(self):
        return self.__url:

if __name__ == '__main__':
    base = Base()
    ret_time = base.convert_time_format("Jan, Thu 01 1970 09:00:00 GMT")
    print(ret_time)
