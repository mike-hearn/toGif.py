# toGif.py

toGif.py is a command-line tool for converting any video that is playable with ffmpeg into an animated GIF.

### Requirements

This tool requires the following programs:

* ffmpeg
* ImageMagick (specifically `convert`)
* gifsicle

On Unix-based machines, all three can be installed via package manager. For OS X, I recommend using [homebrew][1] and for Linux variants use your OS's default package manager.

[1]: http://brew.sh/

### Options

	-h, --help            show this help message and exit
	
	-i INPUT, --input INPUT
	                    Input file.
	
	-r FRAMERATE, --framerate FRAMERATE
	                    Framerate of GIF. Default is 24.
	
	-w WIDTH, --width WIDTH
	                    Specify the width of the GIF. Default is 400.
	
	-c COLORS, --colors COLORS
	                    Number of colors to be used. Default is 256.
	
	-nd, --nodither       Turn off dithering.
	
	-p, --pause           Pauses after creating PNG files to allow for editing