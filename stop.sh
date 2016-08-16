#!/bin/bash

# Get the directory that this script resides in.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Stop the video.
pkill omxplayer

# Stop the bash script and remove the PID file.
if [ -e $DIR/pid ]
then
    kill $(<"$DIR/pid")
    rm $DIR/pid
fi
