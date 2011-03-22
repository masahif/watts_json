#!/bin/env python

import Image
import urllib
import datetime
import json
import os

class Watts(object):
    def __init__(self):
        urllib.urlretrieve('http://www.tepco.co.jp.cache.yimg.jp/forecast/html/images/juyo-j.gif', '/tmp/juyo-j.gif')

        self.im = Image.open('/tmp/juyo-j.gif')
        self.data = list(self.im.getdata())
        self.x = self.im.size[0]
        self.y = self.im.size[1]

        self.line_color = self.data[0]

        self._upper_line()
        self._lower_line()
        self._time_list()
        self._scan_watts()
        self._calc_watts()

        self._json_write()

    def _upper_line(self):
        start = 50
        end = 60

        xpos = int(self.x / 2)
        base = self.data[start * self.x + xpos]
        for y in xrange(start, end):
            if base != self.data[y * self.x + xpos]:
                # print "upper_lins is %d" % y
                self.upper_line = y
                return

        raise Error

    def _lower_line(self):
        start = 270
        end = 300

        xpos = int(self.x / 2)
        base = self.data[start * self.x + xpos]
        for y in xrange(start, end):
            if base != self.data[y * self.x + xpos]:
                # print "lower_line is %d" % y
                self.lower_line = y
                return

        raise Error

    def _time_list(self):
        start = 50
        end = 590

        self.time_list = list()

        ypos = self.lower_line - 1
        for x in xrange(start, end):
            cur = self.data[self.x * ypos + x]
            if cur == self.line_color:
                self.time_list.append(x)
                if len(self.time_list) >= 24:
                    break

    def _scan_watts(self):
        start = 50
        end = 590
    
        self.raw_watts_list = list()
        for time in self.time_list:
            for y in xrange(self.upper_line + 1, self.lower_line):
                if self.data[y * self.x + (time + 1)] == self.line_color:
                    self.raw_watts_list.append(self.lower_line - y)

        # print self.raw_watts_list

    def _calc_watts(self):
        self.watts = dict()
        factor = 6000.0 / (self.lower_line - self.upper_line)
        # print factor
        time = 0
        for raw_watt in self.raw_watts_list:
            self.watts[time] = raw_watt * factor
            time += 1

    def _json_write(self):
        today = datetime.date.today()
        filename = today.strftime("watts-%Y%m%d.json")
        alias = "watts.json"

        f = open(filename, 'w')
        json.dump(self.watts, f)
        f.close()
        os.remove(alias)
        os.symlink(filename, alias)


if __name__ == '__main__':
    w = Watts()
    print w.watts
