"""
Return window arguments for omxplayer, based on the resolution of a video, the
screen width and reserved area at the edges of the screen.

This program calls mediainfo, which must be installed.

The arguments are:

screen width
screen height
reserved_x (number of pixels not to be used at left and right sides of screen)
reserved_y (number of pixels not to be used at top and bottom of screen)
file name
"""

import sys
import os
import subprocess

# Make sure command line arguments are specified.
if len(sys.argv) < 6:
    sys.stderr.write('Error: insufficient arguments\n')
    sys.exit(1)

# Parse command line arguments.
try:
    screen_width = int(sys.argv[1])
    screen_height = int(sys.argv[2])
    reserved_x = int(sys.argv[3])
    reserved_y = int(sys.argv[4])
except ValueError, e:
    sys.stderr.write('Error: integer expected: %s\n' % e)
    sys.exit(1)
fname = sys.argv[5]

# Make sure the input file exists.
if not os.path.isfile(fname):
    sys.stderr.write('Error: %s is not a file or does not exist\n' % fname)
    sys.exit(1)

# Get info about video using mediainfo.
try:
    results = subprocess.check_output(['mediainfo', '-f', fname])
except subprocess.CalledProcessError, e:
    sys.stderr.write('Error: unable to get media infor from %s: %s\n' %
                     (fname, e))
    sys.exit(1)

# Parse output and determine video width, height and pixel aspect ratio.
width = 0
height = 0
pixel_aspect_ratio = 0
for line in results.split('\n'):
    line = line.strip()
    if line.startswith('Width'):
        if line.endswith('pixels'):
            continue
        width = int(line.split(':')[1].strip())
    elif line.startswith('Height'):
        if line.endswith('pixels'):
            continue
        height = int(line.split(':')[1].strip())
    elif line.startswith('Pixel aspect ratio'):
        if line.count(':') > 1:
            continue
        pixel_aspect_ratio = float(line.split(':')[1].strip())
    else:
        continue

# Calculate display width.
width = int(round(width * pixel_aspect_ratio))

# Check if video width is too big.
if width > (screen_width - 2*reserved_x):
    # Adjust width and height.
    w_diff = width - (screen_width - 2*reserved_x)
    w_ratio = (width - float(w_diff))/width
    width = width - w_diff
    height = int(height * w_ratio)

# Check if video height is too big.
if height > (screen_height - 2*reserved_y):
    # Adjust width and height.
    h_diff = height - (screen_height - 2*reserved_y)
    h_ratio = (height - float(h_diff))/height
    height = height - h_diff
    width = int(width * h_ratio)

# Create coordinates for omxplayer.
x1 = (screen_width - width)/2
y1 = (screen_height - height)/2
x2 = x1 + width
y2 = y1 + height

# Return the values as a string.
sys.stdout.write('%s,%s,%s,%s' % (x1, y1, x2, y2))
sys.exit(0)
