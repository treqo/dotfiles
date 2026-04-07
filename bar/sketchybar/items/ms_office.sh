#!/bin/bash

#### MS_Office – suite of MS tools

PLUGIN_DIR="$CONFIG_DIR/plugins"

sketchybar --add item ms_office right \
  --set ms_office \
  icon.font="Hack Nerd Font:Regular:24.0" \
  icon="󰏆" \
  click_script="$PLUGIN_DIR/ms_office_toggle.sh"
