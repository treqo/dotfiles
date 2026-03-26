#!/bin/bash
##### Bar Appearance #####
# Configuring the general appearance of the bar.
# These are only some of the options available. For all options see:
# https://felixkratz.github.io/SketchyBar/config/bar
# If you are looking for other colors, see the color picker:
# https://felixkratz.github.io/SketchyBar/config/tricks#color-picker

bar=(
  color=0x40000000
  border_color=0xffff0000
  position=top
  height=40
  notch_display_height=0
  margin=0
  y_offset=0
  corner_radius=0
  border_width=0
  blur_radius=10
  padding_left=0
  padding_right=0
  notch_width=200
  notch_offset=0
  display=all
  hidden=off
  topmost=off
  sticky=on
  font_smoothing=off
  shadow=off
)

sketchybar --bar "${bar[@]}"
