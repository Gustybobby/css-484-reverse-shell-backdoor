#!/bin/bash

source venv/bin/activate

gnome-terminal -- python eop_server.py
gnome-terminal -- python klg_server.py
gnome-terminal -- python vca_server.py
gnome-terminal -- python itr_server.py