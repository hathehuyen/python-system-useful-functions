#!/usr/bin/python
from urllib2 import urlopen
from datetime import datetime
from rfc822 import parsedate_tz


# Download url to file with buffered read and progress display
def download(url, file_name):
    u = urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,

    f.close()


# Check last modified time of an url using Last-Modified header
def check_last_modified(url):
    u = urlopen(url)
    meta = u.info()
    last_modified = meta.getheaders("Last-Modified")[0]
    # modified = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S GMT')
    modified = datetime(*parsedate_tz(last_modified)[:7])
    return modified