#!/usr/bin/env python3
import os
import stat
from os import chmod, symlink
from os.path import abspath, join, basename, expanduser, exists
from sys import argv

script = abspath(argv[1])
name = basename(script)
if name.endswith(".py"):
    name = name[:-3]
name = name.replace('_', '-')
target_script = join(expanduser('~'), '.local', 'share', 'nautilus-python', 'extensions', name)
if not exists(target_script):
    st = os.stat(script)
    chmod(script, st.st_mode | stat.S_IEXEC)
    symlink(script, target_script)
else:
    print("Target link already exists, doing nothing")
