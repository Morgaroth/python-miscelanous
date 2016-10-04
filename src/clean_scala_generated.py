#!/usr/bin/env python3
import shutil
from os import listdir, getcwd
from os.path import isdir, join, abspath
from sys import argv


def rm(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError as e:
        if e.errno == 2:
            pass
        else:
            raise e
    except Exception as e:
        print(e)
        raise e


def clean(f):
    print('Checking {}'.format(f))
    if 'build.sbt' in listdir(f):
        print('\'build.sbt\' present in {}, clearing...'.format(f))
        rm(join(f, 'project', 'project'))
        rm(join(f, 'project', 'target'))
        rm(join(f, 'target'))
    if 'target' in listdir(f):
        target_files = set(listdir(join(f, 'target')))
        scala_indicators = {'resolution-cache', 'streams', 'scala-2.12', 'scala-2.11', 'scala-2.10'}
        if len(scala_indicators.intersection(target_files)) > 0:
            print('\'target\' dir present in {}, clearing...'.format(f))
            rm(join(f, 'target'))


def do_work(path):
    files = listdir(path)
    clean(path)
    dirs = [f for f in files if isdir(join(path, f)) and f not in {'.git', '.idea'}]
    for d in dirs:
        do_work(join(path, d))


if len(argv) > 1:
    path = abspath(argv[1])
else:
    path = getcwd()

if input('Path is {}, proceed? '.format(path)).startswith('y'):
    do_work(path)
