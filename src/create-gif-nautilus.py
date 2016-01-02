#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import tempfile
from os.path import join
from shutil import copyfile
from subprocess import Popen

from gi.repository import Gtk


class EntryWindow(Gtk.Window):
    def __init__(self, on_start_callback, on_open_callback, gif_name=None, fpss=None, resize_percents=None,
                 max_size=None):
        Gtk.Window.__init__(self, title="Provide details")
        self.on_open_callback = on_open_callback
        self.on_start_callback = on_start_callback
        self.set_size_request(200, 200)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        vbox.pack_start(Gtk.Label("Gif name:"), True, True, 0)
        self.gif_name_input = Gtk.Entry()
        self.gif_name_input.set_text(gif_name or "")
        vbox.pack_start(self.gif_name_input, True, True, 0)

        vbox.pack_start(Gtk.Label("Fpss to be generated:"), True, True, 0)
        self.fpss_input = Gtk.Entry()
        self.fpss_input.set_text(fpss or "3 4 5 6")
        vbox.pack_start(self.fpss_input, True, True, 0)

        vbox.pack_start(Gtk.Label("Resize images?"), True, True, 0)
        resizing_radios = Gtk.Box(spacing=6)
        vbox.pack_start(resizing_radios, True, True, 0)

        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Percents")
        button1.connect("toggled", self.on_button_toggled, "--resize")
        resizing_radios.pack_start(button1, False, False, 0)
        self.option = "--resize"

        button2 = Gtk.RadioButton.new_with_label_from_widget(button1, "Hard size")
        button2.connect("toggled", self.on_button_toggled, "--max-size")
        resizing_radios.pack_start(button2, False, False, 0)

        button3 = Gtk.RadioButton.new_with_label_from_widget(button2, "No changes")
        button3.connect("toggled", self.on_button_toggled, "")
        resizing_radios.pack_start(button3, False, False, 0)

        self.resize_value_input = Gtk.Entry()
        self.resize_value_input.set_text(resize_percents or max_size or "40")
        vbox.pack_start(self.resize_value_input, True, True, 0)

        ok_buttons = Gtk.Box(spacing=6)
        vbox.pack_start(ok_buttons, True, True, 0)

        start_btn = Gtk.Button.new_with_label("Create!")
        start_btn.connect("clicked", self.on_start)
        ok_buttons.pack_start(start_btn, True, True, 0)

        open_btn = Gtk.Button.new_with_label("Only open!")
        open_btn.connect("clicked", self.on_open_clicked)
        ok_buttons.pack_start(open_btn, True, True, 0)

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.option = name

    def on_open_clicked(self, button):
        self.on_open_callback()
        self.destroy()

    def on_start(self, button):
        name = self.gif_name_input.get_text()
        fpss = [f for f in [f.strip() for f in self.fpss_input.get_text().split(' ')] if len(f) > 0]
        resize_value = self.resize_value_input.get_text()
        resize_type = self.option
        print('name', name, 'fpss', fpss, 'r_val', resize_value, 'r_type', resize_type)
        self.on_start_callback(name, fpss, resize_type, resize_value)
        self.destroy()


file_names = sys.argv[1:]

print("creating gif of %s" % str(file_names))
cwd = os.getcwd()
print("env cwd", cwd, "files:", str(file_names))

tmp_dir = tempfile.mkdtemp()
gifs_path = join(tmp_dir, 'gifs')
os.mkdir(gifs_path)


def create_gif_function(gif_name, fpss, resize_type, resize_vaue):
    for f in file_names:
        copyfile(join(cwd, f), join(tmp_dir, f))
    resize_part = []
    if len(resize_type) > 0:
        resize_part = [resize_type, resize_vaue]
    command = ['create-gif', '--output', gifs_path, '--gif-name', gif_name] + resize_part + fpss
    print("running command:", str(command), "...")
    Popen(command, cwd=tmp_dir).wait()
    print("gifs createds")
    Popen(['xdg-open', gifs_path]).wait()
    print("file explorer opened")


def open_tmp():
    for f in file_names:
        copyfile(join(cwd, f), join(tmp_dir, f))
    Popen(['gnome-terminal', tmp_dir]).wait()
    Popen(['xdg-open', tmp_dir]).wait()


candidate = sorted(file_names)[0]
gif_name_candidate = os.path.splitext(candidate)[0]
win = EntryWindow(create_gif_function, open_tmp, gif_name=gif_name_candidate)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
print("script end")
