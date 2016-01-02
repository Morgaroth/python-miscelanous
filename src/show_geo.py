#!/usr/bin/env python3
# coding=utf-8
import re
import sys
import webbrowser

from gi.repository import Gtk


# copy to ~/.local/share/nautilus/scripts
# open nautilus-actions-config-tool and create new action:
#   command parameters: %d %b
#   execution in terminal
#   mimetype filter: image/*


def show_dialog(title, message):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


try:
    from exifread import process_file as read_exif_from_file
except ImportError as e:
    print("exifred is not installed, please")
    e.message = 'ExifRead is not installed.\nPlease install ExifRead, site: ' + \
                'https://pypi.python.org/pypi/ExifRead\nYou may use pip: "pip install exifread".'
    show_dialog("ERROR", e.message)
    raise e

__author__ = 'mateusz'


# spróbować otworzyć google mapy jeśli jest, ewentualnie przeczytac, jak się to inteligentnie robi w ubuntu
# http://stackoverflow.com/questions/4216985/call-to-operating-system-to-open-url


def get_exif(path):
    f = open(path, 'rb')
    from_file = read_exif_from_file(f)
    return from_file


def read_gps_from_exif_value(value):
    regex = "\[(\d+), (\d+), (\d+)/(\d+)\]"
    (degree, minutes, seconds, seconds_factor) = re.search(regex, value).groups()
    degree = int(degree)
    minutes = int(minutes)
    seconds = int(seconds)
    seconds_factor = int(seconds_factor)
    # print degree, minutes, seconds, seconds_factor
    return degree + minutes / 60.0 + seconds / 3600.0 / seconds_factor


def convert_world_direction_letter_to_factor(letter):
    if letter in ['N', 'E', 'n', 'e']:
        return 1
    else:
        return -1


def get_geo_from_tags(tags):
    if 'GPS GPSLatitude' in tags \
            and 'GPS GPSLongitude' in tags \
            and 'GPS GPSLatitudeRef' in tags \
            and 'GPS GPSLongitudeRef' in tags:
        return {
            'latitude':
                read_gps_from_exif_value(tags['GPS GPSLatitude'].printable) *
                convert_world_direction_letter_to_factor(tags['GPS GPSLatitudeRef'].printable),
            'longitude':
                read_gps_from_exif_value(tags['GPS GPSLongitude'].printable) *
                convert_world_direction_letter_to_factor(tags['GPS GPSLongitudeRef'].printable)
        }
    return None


args = sys.argv[1:]

print("show geo for %s" % str(args))

if len(args) is not 2:
    show_dialog("ERROR", "Illegal arguments.")
    sys.exit(1)

directory = args[0]
file_name = args[1]
file_path = "%s/%s" % (directory, file_name)
tags = get_geo_from_tags(get_exif(file_path))
if tags is None:
    show_dialog("ERROR", "The file %s\nhas no GPS localization." % file_path)
    sys.exit(2)

gps = {k: "%.7f" % v for k, v in tags.items()}
url = "https://www.google.pl/maps/@%s,%s,14z" % (gps['latitude'], gps['longitude'])
url2 = "https://maps.google.com/maps?q=loc:%s,%s" % (gps['latitude'], gps['longitude'])
lat = gps['latitude']
long = gps['longitude']
map_type = 't'
zoom = '11'
search_type = 'yp'
url3 = "http://maps.google.com/maps?&z=%s&mrt=%s&t=%s&q=%s+%s" % (zoom, search_type, map_type, lat, long)
url4 = "https://maps.google.com/maps?q=%s,%s&ll=%s,%s&z=%s" % (lat, long, lat, long, zoom)
print(url)
webbrowser.open(url4, new=0, autoraise=True)
