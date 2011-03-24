#!/usr/bin/env python

import urllib2
import datetime
import sys

BASE_DIR = "./tmp/"

CSV_LAST_MODIFIED_TXT = "csv_last_modified.txt"
HTML_LAST_MODIFIED_TXT = "html_last_modified.txt"
GIF_LAST_MODIFIED_TXT = "gif_last_modified.txt"

CSV_URL = "http://www.tepco.co.jp/forecast/html/images/juyo-j.csv"
HTML_URL = "http://www.tepco.co.jp/forecast/index-j.html"
GIF_URL = "http://www.tepco.co.jp/forecast/html/images/juyo-j.gif"

today = datetime.datetime.today()
TODAY_STR = today.strftime("%Y%m%d%H%M%S")


def check_and_save(url, filename, last_modified_file):
    last_modified = open(BASE_DIR + last_modified_file).read()
    opener = urllib2.build_opener()

    request = urllib2.Request(url)
    if last_modified:
        request.add_header('If-Modified-Since', last_modified)

    try:
        s = opener.open(request)
    except urllib2.HTTPError, e:
        if e.code == 304:
            print "%s was not modified" % filename
            return
        else:
            sys.exit(1)
    
    f = open(BASE_DIR + last_modified_file, 'w')
    f.write(s.headers.get('Last-Modified'))
    f.close()

    f = open(BASE_DIR + filename, 'w')
    f.write(s.read())
    
    return

check_and_save(CSV_URL, "%s-juyo_j.csv" % TODAY_STR, CSV_LAST_MODIFIED_TXT)
check_and_save(HTML_URL, "%s-juyo_j.html" % TODAY_STR, HTML_LAST_MODIFIED_TXT)
check_and_save(GIF_URL, "%s-juyo_j.gif" % TODAY_STR, GIF_LAST_MODIFIED_TXT)
