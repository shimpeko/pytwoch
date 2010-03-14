import os
import time
from base import Base, Py2chdlerError

class Res():
    def __init__(self, thread, id, username, posted, user_id, content, new):
        self.thread = thread
        self.id = id
        self.username = username
        self.posted_raw = posted
        p_posted = re.compile('^(\d{4}/\d{2}/\d{2})(\(.\))\s(\d{2}:\d{2}:\d{2})(\.\d{2}){0,1}$')
        r_posted = r_posted.match(self.posted_raw)
        time_struct = time.strptime(r_posted.group(1) + r_posted.group(2) + "JST", "%Y/%m/%d%H:%M:%S%Z")
        self.posted_epoc = time.mktime(time_struct)
        self.user_id = user_id
        self.content = content
        self.new = new

if __name__ == '__main__':
    pass
