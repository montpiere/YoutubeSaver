# YoutubeSaver

## Description
Download videos from Youtube with this simple app in high quality (1080p, 720p... if available) with captions. 
It works in command line but no need to write complicated commands.

## Install
Need [Python](https://www.python.org/downloads/) of course.

- Download app into your specific folder
- Run `setup.bat`. It will download and install all dependencies
in a virtual environment automatically.

## Usage:
- Add as many YouTube (full) links and/or playlist links as you want in a new line to the `downloads.txt` file.
- Run `YoutubeSaver.bat`

You can find the downloaded files in the `complete` folder of the program library.

## Notes
If you got first *"400 bad request"*, please give a try to run the `fix_moviepy.bat`. 
Sometimes `pytube` is not installed first properly with its fix.

## How it works
**Slow problem**

You might find the program running slow, it's because YouTube stores the higher quality videos separately from the audio, so we have to download the video and the audio separately and combine them.
___The running time of this depends on your hardware.___
I haven't found a better solution for downloading a higher quality video. I did a lot of research though. If you have it, let me know. 

**Video resolutions**

First, the program tries to download 1080p videos, if it is not found, it tries to download 720p. If you need a higher quality (e.g. 4K), you can modify the script.

**Captions**

If there is a built-in subtitle, the program will try to download it first, if it is not available, it will try the automatic subtitles. The base language is _en_.

_It tested on Windows._

## Updates

*2024.09.24 - an update that manages the playlists too*

## Authors:
_montpiere.gh@gmail.com_
