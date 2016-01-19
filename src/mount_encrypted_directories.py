#!/usr/bin/env python3.5
# coding=utf-8
import getpass
from os.path import expanduser, join
from subprocess import Popen, PIPE, DEVNULL
from sys import argv, exit

# from platform import python_version
# print("Running with python=", python_version())

try:
    from libkeepass import open as open_kdbx
except ImportError as e:
    if "libkeepass" in e.msg:
        print('''Keepass library didn\'t installed, install by
        sudo apt-get install python-dev libxml2-dev libxslt-dev #dependencies
        sudo pip install libkeepass''')
        exit(1)
    else:
        raise

argv = [a.lower() for a in argv[1:]]

passwords = {}

if len(argv) == 0 or not (len(argv) == 1 and 'our' in argv):
    filename = join(expanduser('~'), 'Dropbox', 'keepass', 'Morgaroth-prv.kdbx')
    pw = getpass.getpass("Password to keepass database: ")
    try:
        with open_kdbx(filename, password=pw) as kdb:
            entries = kdb.obj_root.findall('.//Entry')
            passwords_entry = next(
                    i for i in entries if
                    len([k for k in i.getchildren() if k.tag == 'String' and k.Value == 'pliki']) > 0)
            passwords_raw = next(
                    i.Value.text for i in passwords_entry.getchildren() if i.tag == 'String' and i.Key == 'Notes')
            passwords = {p[0].strip(): p[1].strip() for p in
                         [password.split("-") for password in passwords_raw.split("\n")]}
            if len(passwords) < 3:
                print("Nie odczytano haseł, odczytano tylko %s" % str(passwords.keys()))
                exit(2)
    except OSError as e:
        if 'Master key invalid' in str(e):
            print("Invalid password to database. Exiting...")
            exit(4)
        else:
            raise

if 'our' in argv:
    pw = getpass.getpass("Password to our directory: ")
    passwords.update({'our': pw})


def mount(ending, pswd):
    p = Popen(['encfs', '-S', '/mnt/ENC/ENCRYPTED%s' % ending, '/mnt/ENC/DECRYPTED%s' % ending], stdin=PIPE)
    p.communicate(pswd.encode('utf-8'))


def mount_std():
    print("Mounting standard directory")
    mount('', passwords['all'])


def mount_prv():
    print("Mounting private directory")
    mount('-PRV', passwords['prv'])


def mount_own():
    print("Mounting own directory")
    mount('-OWN', passwords['own'])


def mount_our():
    print("Mounting our directory")
    mount('-OUR', passwords['our'])


def open_explorer(directory, umount_after_mins=None):
    Popen(['xdg-open', '/mnt/ENC/DECRYPTED%s' % directory], stderr=DEVNULL, stdout=DEVNULL).wait()
    if umount_after_mins is not None:
        wait_in_seconds = umount_after_mins * 60
        Popen(['nohup bash -c \"sleep %d && fusermount -u /mnt/ENC/DECRYPTED%s/\" &' % (wait_in_seconds, directory)],
              shell=True, close_fds=True, stderr=DEVNULL, stdout=DEVNULL)


def open_std():
    open_explorer("")


def open_prv():
    open_explorer("-PRV", umount_after_mins=30)


def open_own():
    open_explorer("-OWN", umount_after_mins=30)


def open_our():
    open_explorer("-OUR", umount_after_mins=3)


if 'all' in argv:
    mount_std()
    mount_prv()
    mount_own()
    open_std()
elif len(argv) == 0:
    mount_std()
    open_std()
else:
    if 'prv' in argv:
        mount_prv()
        open_prv()
    if 'our' in argv:
        mount_our()
        open_our()
    if 'own' in argv:
        mount_own()
        open_own()
    if 'std' in argv:
        mount_std()
        open_std()
