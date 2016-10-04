#!/usr/bin/env bash


chmod +x ./add_nautilus_menu_entry.py
chmod +x ./link_nautilus_script.py
chmod +x ./link.py

./link.py ./src/create_gif.py
./link.py ./src/create-gif-nautilus.py
./add_nautilus_menu_entry.py "Create GIF" create-gif %F "image/*"
nautilus -q