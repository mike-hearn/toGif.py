#!/usr/bin/env python

import argparse
import os
import re
import shutil
import subprocess
import uuid

# Set up arguments
parser = argparse.ArgumentParser(description='Converts any video to GIF format. Requires ffmpeg, ImageMagick and gifsicle.')
parser.add_argument('-i','--input', help='Input file.', required=True)
parser.add_argument('-r','--framerate', help='Framerate of GIF. Default is 24.')
parser.add_argument('-w','--width', help='Specify the width of the GIF. Default is 400.')
parser.add_argument('-c','--colors', help='Number of colors to be used. Default is 256.')
parser.add_argument('-nd','--nodither', help='Turn off dithering.', action='store_true')
parser.add_argument('-p','--pause', help='Pauses after creating PNG files to allow for editing', action='store_true')
args = vars(parser.parse_args())

# Set up all path & filename variables
basename, extension = os.path.splitext(os.path.basename(args['input']))
path = os.path.abspath(args['input']).split(basename)[0]
fullname = path+basename+extension

# Set up temporary folders; use system tmp, otherwise create in /tmp/
uid = uuid.uuid4()
if os.environ['TMPDIR']:
    temp_folder = os.environ['TMPDIR'] + 'mp4ToGIF/' + uid.hex + '/'
else:
    temp_folder = '/tmp/mp4ToGIF-temp/'
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)
else:
    shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)

# Set defaults

# Framerate
if not args['framerate']:
    p = subprocess.Popen(['ffmpeg','-i',fullname],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()
    print err
    args['framerate'] = re.findall('(\d+\.?\d+?) fps', err)[0]
    print args['framerate']

# Width
if not args['width']:
    args['width'] = '400'

# Color
if not args['colors']:
    args['colors'] = '256'

# Convert frames of video into PNG
subprocess.call(['ffmpeg',
    '-i',fullname,
    '-r',args['framerate'],
    '-vf','scale='+args['width']+':trunc(ow/a/1)*1',
    '-y',
    temp_folder+basename+"%05d.png"])

# Convert each PNG file into a GIF
png_files = os.listdir(temp_folder)
for idx, each_file in enumerate(png_files):
    print "Converting %s (%s out of %s)." % (each_file, str(idx+1), str(len(png_files)))
    each_file = temp_folder + each_file
    subprocess.call(["convert",each_file,each_file+".gif"])
    os.remove(each_file)

if args['pause']:
    subprocess.call(['open',temp_folder])
    print "Press any key to continue..."
    raw_input()

# Convert to GIF
gif_files = []
for files in os.listdir(temp_folder):
    if files.endswith('.gif'):
        gif_files.append(temp_folder + files)

gifsicle_command = ['gifsicle',
    '--optimize=3',
    '--colors=%s' % args['colors'],
    '--delay=' + str(int(round(100/float(args['framerate'])))),
    '--loop',
    '--output',path+basename+'.gif']
gifsicle_command.extend(gif_files)
if not args['nodither']:
    # Yes this is confusing, but dithering should be the default
    gifsicle_command.append('--dither')

subprocess.call(gifsicle_command)

shutil.rmtree(temp_folder)
