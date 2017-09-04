#!/usr/bin/env python3
import os
from os import getcwd, listdir, mkdir, rmdir
from os.path import join, isdir
from shutil import move

wd = getcwd()
directories = [m4a for m4a in listdir(wd) if isdir(m4a)]

print("working in %s with %s" % (wd, str(directories)))

target = join(wd, 'mp3')
if not os.path.exists(target):
    mkdir(target)

for f in directories:
    print("checking %s" % f)
    music_files_inside = [m4a for m4a in listdir(join(wd, f)) if m4a.lower().endswith(".m4a")]
    if len(music_files_inside) == 1:
        print("Found file {} in {}".format(music_files_inside[0], f))
        move(join(wd, f, music_files_inside[0]), join(wd, music_files_inside[0]))
        rmdir(join(wd, f))
