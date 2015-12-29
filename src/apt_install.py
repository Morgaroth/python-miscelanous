#!/usr/bin/env python3

import sys
import subprocess

if len(sys.argv) < 2:
    print("Incorrect arguments, provide at least one package to install")
    sys.exit(1)

subprocess.Popen(['sudo', '-E', 'apt-get', 'install', '-y'] + sys.argv[1:], shell=False).wait()
