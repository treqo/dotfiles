!/usr/bin/bash
# swww setup from https://www.reddit.com/r/hyprland/comments/1df3c93/tutorial_swww_how_to_setup/
#start swww
WALLPAPERS_DIR=~/Pictures/wallpapers/current/
WALLPAPER=$(find "$WALLPAPERS_DIR" -type f | shuf -n 1)
swww img "$WALLPAPER"
