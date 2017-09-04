#!/usr/bin/env python3
import os
from os import getcwd, listdir, mkdir
from os.path import join
from subprocess import Popen

ret = Popen(['avconv', '-version']).wait()
if ret != 0:
    raise Exception("avonv method not installed in system.... install it before continue, for example by 'sudo apt "
                    "install libav-tools'.")
print("Required commands installed.")

wd = getcwd()
m4as = [m4a for m4a in listdir(wd) if m4a.lower().endswith(".m4a")]

print("working in %s with %s" % (wd, str(m4as)))

target = join(wd, 'mp3')
if not os.path.exists(target):
    mkdir(target)

for f in m4as:
    print("converting %s" % f)
    name, ext = os.path.splitext(f)
    Popen(['avconv', '-y', '-i', join(wd, f), join(target, name + '.mp3')], cwd=wd).wait()
