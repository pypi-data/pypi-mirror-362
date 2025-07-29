#!/bin/bash

set -e


# put log into stdout to get it collected
# watches for new files to appear in the directory and starts `tail -F` on them
DIRAC_DATA_DIR="/home/dirac/data"
inotifywait -m -e create --format "%f" "$DIRAC_DATA_DIR" | while read NEWFILE; do
  if [[ "$NEWFILE" == *.out || "$NEWFILE" == *.err ]]; then
    tail -F "$DIRAC_DATA_DIR/$NEWFILE" &
  fi
done &

/usr/sbin/automount
exec /usr/sbin/sshd -D -e -o LogLevel=DEBUG1
