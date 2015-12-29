#!/usr/bin/env python3.5
# coding=utf-8
import getpass
from os.path import expanduser, join
from subprocess import Popen, PIPE
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

filename = join(expanduser('~'), 'Dropbox', 'keepass', 'Morgaroth-prv.kdbx')
pw = getpass.getpass("Password to keepass database: ")
passwords = {}
try:
    with open_kdbx(filename, password=pw) as kdb:
        # print(kdb.pretty_print().decode("unicode_escape"))
        entries = kdb.obj_root.findall('.//Entry')
        passwords_entry = next(
                i for i in entries if len([k for k in i.getchildren() if k.tag == 'String' and k.Value == 'pliki']) > 0)
        passwords_raw = next(
                i.Value.text for i in passwords_entry.getchildren() if i.tag == 'String' and i.Key == 'Notes')
        passwords = {p[0].strip(): p[1].strip() for p in
                     [password.split("-") for password in passwords_raw.split("\n")]}
except OSError as e:
    if 'Master key invalid' in str(e):
        print("Invalid password to database. Exiting...")
        exit(4)
    else:
        raise


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


if len(passwords) < 3:
    print("Nie odczytano haseł, odczytano tylko %s" % str(passwords.keys()))
    exit(2)

if 'all' in argv:
    mount_std()
    mount_prv()
    mount_own()
elif len(argv) == 0:
    mount_std()
else:
    if 'prv' in argv:
        mount_prv()
    if 'own' in argv:
        mount_own()
    if 'std' in argv:
        mount_std()
