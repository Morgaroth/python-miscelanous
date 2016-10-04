#!/usr/bin/env python3
# coding=utf-8
from sys import argv
from os import system

system('nautilus-actions-new --label="{}" --command="{}" --parameters="{}" --mimetype="{}"  --desktop'.format(argv[1], argv[2], argv[3], argv[4]))
