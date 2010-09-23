import os, os.path
from libpytwoch import menu

class Py2chdler:
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
            rase PytwoError(error_msg)

        # save config
        self.config = { 'cache_dir_path'        : cache_dir_path,
                        'cache_maintain_span'   : cache_maintain_span }


    # methods to construct 2ch objects
    def get(self, url):
        pass

if __name__ == '__main__':
