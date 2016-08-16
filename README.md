Raspberry Pi Videoloop Application
==================================

start.sh plays videos in the "videos" subdirectory continously.

stop.sh stops start.sh and the video being played.

For each video, start.sh calls omxwinargs.py, which calls mediainfo to
determine the size of the video. omxwinargs.py returns a string consisting of
four integers which tells omxplayer where to display the video.

The values passed to omxwinargs.py in start.sh assume the videos are being
displayed on an HD monitor (1920 x 1080), and that we want a 90 pixel area at
the top and bottom of the screen free so the menu bar will continue to be
visible.
