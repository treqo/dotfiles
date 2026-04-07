#!/bin/sh
# Toggle the Microsoft Suite launcher
APP_NAME="MicrosoftSuite"
APP_PATH="/Applications/$APP_NAME/$APP_NAME.app"

if pgrep -x "$APP_NAME" >/dev/null; then
  open -a "$APP_PATH"
else
  open "$APP_PATH"
fi
