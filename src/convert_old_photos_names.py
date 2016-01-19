#!/usr/bin/env python3
import os

from os.path import basename

__author__ = 'mateusz'

wd = os.getcwd()
imgs = [jpg for jpg in os.listdir(wd) if
        jpg.startswith("201") and (jpg.endswith(".jpg") or jpg.endswith(".jpeg"))]

print("working in %s with %s" % (wd, str(imgs)))

for f in imgs:
    print("checking %s" % f)
    name, ext = os.path.splitext(f)
    d = name.split(' ')
    date = d[0]
    time = d[1]
    d = date.split('-')
    if len(d) == 3:
        year = d[0]
        month = d[1]
        day = d[2]
        d = time.split('.')
        if len(d) == 3:
            hour = d[0]
            minutes = d[1]
            sec = d[2]
            # 2014-11-06 12.55.00
            # IMG_20150303_174616386
            new_name = "IMG_%s%s%s_%s%s%s000%s" % (year, month, day, hour, minutes, sec, ext)
            print("renaming %s to %s" % (f, new_name))
            os.rename(f, new_name)
        else:
            print("incorrect old time: %s of file %s" % (time, f))
    else:
        print("incorrect date element %s of file %s" % (date, f))
