#!/usr/bin/env python3
import argparse
import os
import subprocess

__author__ = 'mateusz'

convert_checked = False


def execute(command, verbose=False):
    def prepare_command():
        cmd = command
        if isinstance(cmd, str):
            cmd = cmd.split(" ")
        if not isinstance(cmd, list):
            raise Exception("Neither string nor list passed to execute command")
        return cmd

    cmd = prepare_command()
    if verbose:
        print("executing command:\n\t%s" % cmd)
    process = subprocess.Popen(cmd, env=os.environ.copy(), stdout=subprocess.PIPE)
    out, err = process.communicate()
    ret_code = process.returncode
    return out, err, ret_code


class ConvertChecked(object):
    checked = False


class convert_command(object):
    @staticmethod
    def check_installation():
        if ConvertChecked.checked is False:
            (out, err, ret) = execute(['convert', '-version'])
            if ret != 0:
                raise Exception("convert method not installed in system.... install it before continue.")
            print("convert command installed.")
            ConvertChecked.checked = True


class CONVERT(convert_command):
    @staticmethod
    def convert_percent(percent, file_name, verbose=False):
        CONVERT.check_installation()
        output = "%d%%-%s" % (percent, file_name)
        print("Converting %s using %d%% ratio to %s..." % (file_name, percent, output))
        return output, execute(['convert', file_name, '-quality', '100', '-resize', '%d%%' % percent, output], verbose)


class GIF(convert_command):
    @staticmethod
    def create(files_list, output, frames_per_second=3.0, verbose=False):
        GIF.check_installation()
        delay = int(100 * 1.0 / frames_per_second)
        print("Making %s..." % output)
        return execute(['convert', '-delay', str(delay), '-loop', '0'] + files_list + [output], verbose)


parser = argparse.ArgumentParser(description='Converts images to smaller size & creates gifs.')
parser.add_argument('fps', metavar='fpss', type=float, nargs='+',
                    help='list of frames per second for creating gifs')
parser.add_argument('-r', '--resize', type=int, metavar='percents',
                    help='resize ratio in percents to resize images before create gif.')
parser.add_argument('-s', '--max-size', type=float, metavar='max_size',
                    help='if passed, images will be resized to rich passed size.')
parser.add_argument('-p', '--prefix-of-input-files', metavar='prefix', default='IMG',
                    help='prefix of input files to converting.')
parser.add_argument('-v', '--verbose',
                    help='increase verbosity.')
args = parser.parse_args()

print("Arguments %s" % args)

if args.max_size is not None and args.resize is not None:
    print("provided both --max-size (-s) and --resize (-r) options, they are exclusive, provide only one")
    exit(1)

wd = os.getcwd()
jpgs = [jpg for jpg in os.listdir(wd) if jpg.endswith(".jpg") or jpg.endswith(".jpeg")]
pngs = [png for png in os.listdir(wd) if png.endswith(".png")]
imgs = None

if len(jpgs) != 0 and len(pngs) != 0:
    answer = input('In %s exists both jpg files and png, which You want use? [png/jpg]: ' % wd)
    if answer == 'jpg':
        imgs = jpgs
    elif answer == 'png':
        imgs = pngs
    else:
        print("Bad response, exiting.")
        exit(1)
elif len(jpgs) != 0:
    imgs = jpgs
elif len(pngs) != 0:
    imgs = pngs
else:
    print("No images in %s, exiting." % wd)
    exit(0)

imgs = [img for img in imgs if img.startswith(args.prefix_of_input_files)]


def average_of_file_size(files, verbose=False):
    """
    :return: average size of files, in MB
    :rtype int
    """
    sizes = [os.path.getsize(fil) for fil in files]
    size_avg = sum(sizes) * 1.0 / len(sizes) / 1024 / 1024
    if verbose:
        print("File size average: %.4fMB, calculated from sizes: %s" % (size_avg, sizes))
    return size_avg


imgs.sort()

name = input('Provide name of gif: ')

fpss = args.fps
resize = args.resize
if resize is None:
    resize = args.max_size
    if resize is not None:
        resize = int(resize * 100 / average_of_file_size(imgs, args.verbose) + 6)

if resize is not None:
    imgs = [f[0] for f in map(lambda f_n: CONVERT.convert_percent(resize, f_n, args.verbose), imgs)]

if len(fpss) == 1:
    GIF.create(imgs, '%s.gif' % name, int(fpss[0]), verbose=args.verbose)
else:
    for fps in fpss:
        GIF.create(imgs, '%s-%sfps.gif' % (name, fps), float(fps), args.verbose)