#!/usr/bin/env python3
# coding=utf-8

from subprocess import Popen, PIPE
from urllib import unquote

from gi.repository import Nautilus, GObject


def getexiftool(filename):
    options = '-fast2 -f -m -q -q -s3 -ExifIFD:DateTimeOriginal'
    exiftool = Popen(['/usr/bin/exiftool'] + options.split() + [filename],
                     stdout=PIPE, stderr=PIPE)
    output, errors = exiftool.communicate()
    return output.split('\n')


class MyExtension(Nautilus.ColumnProvider, Nautilus.InfoProvider, GObject.GObject):
    def __init__(self):
        pass

    def get_columns(self):
        return (
            Nautilus.Column(name='MyExif::DateTime',
                            attribute='Exif:Image:DateTime',
                            label='Date Original',
                            description='Data time original'
                            ),
        )

    def update_file_info_full(self, provider, handle, closure, file_info):
        if file_info.get_uri_scheme() != 'file':
            return

        filename = unquote(file_info.get_uri()[7:])
        attr = ''

        if file_info.get_mime_type() in ('image/jpeg', 'image/png'):
            GObject.timeout_add_seconds(1, self.update_exif,
                                        provider, handle, closure, file_info)
            return Nautilus.OperationResult.IN_PROGRESS

        file_info.add_string_attribute('Exif:Image:DateTime', attr)

        return Nautilus.OperationResult.COMPLETE

    def update_exif(self, provider, handle, closure, file_info):
        filename = unquote(file_info.get_uri()[7:])

        try:
            data = getexiftool(filename)
            attr = data[0]
        except:
            attr = ''

        file_info.add_string_attribute('Exif:Image:DateTime', attr)

        Nautilus.info_provider_update_complete_invoke(closure, provider,
                                                      handle, Nautilus.OperationResult.COMPLETE)
        return False
