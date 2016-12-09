#!/usr/bin/env python3
# coding=utf-8
from argparse import ArgumentParser, ArgumentTypeError
from datetime import timedelta
from os import rename
from os.path import exists
from subprocess import Popen, PIPE


def check_is_reasonable(value):
    ivalue = int(value)
    if ivalue < -12 or ivalue > 11:
        raise ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


parser = ArgumentParser(description='Renames GoPro photos to Morgaroth\'s common name format.')
parser.add_argument('timezone-shift', metavar='shift', type=int, default=0, help='number of hours to shift',
                    action=check_is_reasonable)
parser.add_argument('input-files', metavar='input', nargs='+', help='list of files to rename')
args = parser.parse_args()


def exif_date_reader(time_in_str):
    from datetime import datetime
    return datetime.strptime(time_in_str, '%Y:%m:%d %H:%M:%S')


def get_exif_data(filename):
    exiftool = Popen(['/usr/bin/exiftool'] + [filename], stdout=PIPE, stderr=PIPE)
    output, errors = exiftool.communicate()
    result = {}
    for line in [l for l in output.decode('ascii', 'ignore').split('\n') if len(l) > 0]:
        d = line.split(':', 1)
        result[d[0].strip()] = d[1].strip()
    return result


def common_format(date, millis):
    return "IMG_%04d%02d%02d_%02d%02d%02d%03d.jpg" % (
        date.year, date.month, date.day, date.hour, date.minute, date.second, millis)


# files = [f for f in argv[1:] if f.lower().endswith('.jpg')]
files = [f for f in args.input if f.lower().endswith('.jpg')]

grouped = {}
for f in files:
    exif_dict = get_exif_data(f)
    date = exif_date_reader(exif_dict['Date/Time Original']) + timedelta(hours=args.shift)
    if (not f.startswith("GOPR")) or exif_dict['Make'] != 'GoPro' or exif_dict['Camera Model Name'] != 'HERO':
        print('File {} ignored due to incorrect meta-data, it isn\'t GoPro image'.format(f))
        continue

    d = (int(f[4:].lower().rstrip(".jpg")), f)
    try:
        grouped[date].append(d)
    except KeyError as e:
        grouped[date] = []
        grouped[date].append(d)

moving = []
for date, images in grouped.items():
    step = 1000 / len(images)
    sorted_images = images.sort(key=lambda x: x[0])
    for idx, img in enumerate([f[1] for f in sorted_images]):
        target = common_format(date, idx * step)
        moving.append((img, target))
        if exists(target) is False:
            print(img, "->", target)
            rename(img, target)
        else:
            print('target', target, 'of', img, 'exists')
