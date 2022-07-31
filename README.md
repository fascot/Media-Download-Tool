## This is the Media Download Tool - MDT

# Instalation

Recommended using python versions 3.10+ <br />
You can install python's latest version for Windows on [python.org](https://python.org/downloads/windows/) <br />
If you are on Linux you know how to use python, I guess <br />

The instalation with git: <br />

```bash
1. $ git clone https://github.com/fascot/Media-Download-Tool/
2. $ cd Media-Download-Tool
3. $ python -m pip install -r requirements.txt
```

Download the `ffmpeg` on your machine. <br />

If you are on Windows you have get the latest build version for Windows from this [repository](https://github.com/BtbN/FFmpeg-Builds/releases).
And `ffmpeg` has to be installed into PATH. You can read this [article](https://windowsloop.com/install-ffmpeg-windows-10/#add-ffmpeg-to-Windows-path) with information how to do it. <br />

If you are on Linux, just use Pacman or Apt:
```bash
1. $ sudo pacman -S ffmpeg        'for Manjaro Linux'
2. $ sudo apt-get install ffmpeg  'for Ubuntu'
```

`ffmpeg` is using for output media processing.

Also you have to install firefox and [firefox driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) for selenium

Downloading scripts and libraries Done! <br />

# Usage

By default youtube, pornhub and newgrounds are supported. <br />

You can type commands in no particular order <br />
Except `--help` and `--info`, they have to stand after url adress and no commands after them will be performed <br />
Also, `--help` doesn't get url. <br />

Then, don't type one command twice, only first will be performed. <br />

Base commands, wich heve to work with any type of url: <br />
```bash
| Tool           | Url | Command          | Argument                        | Description                                   |
+----------------+-----+------------------+---------------------------------+-----------------------------------------------+
| python ums.py |     | --help           | all | youtube | unknown_site... | Returns documentation for current url type     |
| python ums.py | url | --info           |                                 | Returns information about page                 |
| python ums.py | url | -n | -name       | custom_name                     | Changes name of the output media file          |
| python ums.py | url | -p | -path       | custom_path                     | Changes path of the output media file          |
```

Commands `-o` and `-r` work only with youtube and pornhub links:
```bash
| python ums.py | url | -o | -option     | video_only | audio_only        | Deletes audio or video from output media file  |
| python ums.py | url | -r | -resolution | 144p | 240p | .... | 2160p     | Changes resolution of the output media file    |
```

BY DEFAULT:

 - video from youtube and pornhub downloads in the highest quality
 - video from youtube and pornhub downloads with video and audio
 - name for output media from unknown sites generates randomly
 - name for output media from youtube and pornhub generates by video title
 - path for output media is in the directory where the script installed
 - index for media from unknown site is None, means that with no given index you'll get the exception

# Plans

- Bug fixes and adding features for already supported sites
- Trying to use Selenium to get media files by doing activity on site
- Also making configs for sites which have no media links on page by default (Selenium automatization)
- Make builds for each os, to not using `python mdt.py` every time
- GUI for average users

# Thanks To The Developers Of

Pytube <br />
BeautifulSoup4 <br />
Youtube-dl <br />
Pornhub-api <br />
Requests <br />
Selenium <br />
Browsermob-proxy <br />
and Python of course <br />
...
