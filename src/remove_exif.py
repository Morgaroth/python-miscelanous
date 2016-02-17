#!/usr/bin/env python3
# coding=utf-8
import os, sys

import subprocess

wd = os.getcwd()
argv = sys.argv[1:]
with open('remove-exif.log', 'a+') as log:
    log.write('wd is %s\n' % wd)
    log.write('args are %s\n' % repr(argv))


def execute(command, wd=None, verbose=False):
    def prepare_command():
        cmd = command
        if isinstance(cmd, str):
            cmd = cmd.split(' ')
        if not isinstance(cmd, list):
            raise Exception("Neither string nor list passed to execute command")
        return cmd

    cmd = prepare_command()
    if verbose:
        with open('remove-exif.log', 'a+') as log:
            log.write("executing command:\n\t%s\n" % cmd)
    process = subprocess.Popen(cmd, cwd=wd, env=os.environ.copy(), stdout=subprocess.PIPE)
    out, err = process.communicate()
    ret_code = process.returncode
    return out, err, ret_code


class exiftool_command(object):
    @staticmethod
    def check_installation():
        (out, err, ret) = execute(['exiftool', '--version'])
        if ret != 0:
            raise Exception("exiftool method not installed in system.... install it before continue.")
        print("convert command installed.")

    @staticmethod
    def remove_exif_from(wd, files):
        exiftool_command.check_installation()
        if not isinstance(files, list):
            files = [files]
        out, err, code = execute(['exiftool', '-overwrite_original_in_place', '-all='] + files, wd=wd, verbose=True)
        with open('remove-exif.log', 'a+') as log:
            log.write('executing command end with %s %s %s %s\n' % (wd, out, err, code))


exiftool_command.remove_exif_from(wd, argv)
