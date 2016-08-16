#!/bin/bash
# Play videos in the "videos" subdirectory continously.
# stop.sh stops this script and the video being played.

# This script assumes the videos are being displayed on an HD monitor
# (1920 x 1080). It calls omxplayer to play the videos, centering them
# in the screen. It leaves a 90 pixel area at the top and bottom of the screen
# free so the menu bar will continue to be visible.

# Get the directory that this script resides in.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# If the PID file for this script exists, abort.
if [ -e $DIR/pid ]
then
    echo Is the process already running? Try running stop.sh.
    echo Exiting.
    exit 1
fi

# Save the PID of this script in a file.
echo $$ > $DIR/pid

# Loop continuosly.
while [ 1 ]
do
    # Play each video in the videos directory.
    for i in $( ls $DIR/videos ); do
        # Determine the window size based on the aspect ratio
        WINARGS=$(python $DIR/omxwinargs.py 1920 1080 50 90 $DIR/videos/$i)
        omxplayer --win $WINARGS -o hdmi $DIR/videos/$i 2> /dev/null
        sleep 2
    done
done
