!/usr/bin/bash
#start swww
WALLPAPERS_DIR=~/Pictures/wallpapers/current/
WALLPAPER=$(find "$WALLPAPERS_DIR" -type f | shuf -n 1)
swww img "$WALLPAPER"
