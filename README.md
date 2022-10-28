## This is the Media Download Tool - MDT

# Instalation

Recommended using python versions 3.10+ <br />
You can install python's latest version for Windows on [python.org](https://python.org/downloads/windows/) <br />
If you are on Linux you know how to use python, I guess <br />

Install [Java](https://www.java.com/ru/download/) for browsermob-proxy work<br />

Script instalation with git: <br />

```bash
1. $ git clone https://github.com/fascot/Media-Download-Tool/
2. $ cd Media-Download-Tool
3. $ python -m pip install -r requirements.txt
```

Download `ffmpeg`. <br />

If you are on Windows you can get the latest build version for Windows from this [repository](https://github.com/BtbN/FFmpeg-Builds/releases).
And `ffmpeg` has to be installed into PATH. You can read this [article](https://windowsloop.com/install-ffmpeg-windows-10/#add-ffmpeg-to-Windows-path) with information how to do it. <br />

If you are on Linux, just use Pacman or Apt:
```bash
1. $ sudo pacman -S ffmpeg        'for Manjaro Linux'
2. $ sudo apt-get install ffmpeg  'for Ubuntu'
```

`ffmpeg` is using for output media processing.

Also you have to install Firefox and [Firefox driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) for selenium

Downloading scripts and libraries Done! <br />

# Usage

By default youtube, pornhub and newgrounds are supported. <br />

You can type most of the commands in no particular order <br />

Then, don't type one command twice, only first will be performed. <br />

Basic commands, wich work with any url type:
```bash
+----------------+------------------------+---------------------------------+------------------------------------------------+
| Tool           | Url | Command          | Argument                        | Description                                    |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python mdt.py  |     | --help           | all | youtube | unknown_site... | Return documentation for module                |
| python mdt.py  | url | --info           |                                 | Return information about page                  |
| python mdt.py  | url | -n | -name       | custom_name                     | Change name of the output media file           |
| python mdt.py  | url | -p | -path       | custom_path                     | Change path of the output media file           |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
```
Option `-f` work only with newgrounds and youtube links:
```bash
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python mdt.py  | url | -f | -format     | video_only | audio_only         | Remove audio or video from output VIDEO file   |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
```
Option `-r` work only with newgrounds and youtube links:
```bash
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python mdt.py  | url | -r | -resolution | 144p | 240p | .... | 2160p      | Change resolution of output VIDEO file         |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
```
You can change default download path with `--default_path` option:
```bash
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python mdt.py  |     | --default_path   | full_path                       | Change default path                            |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
```
Also an amogus animation is supported with `--amogus` option:
```bash
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python mdt.py  |     | --amogus         |                                 | ඞඞඞඞඞඞඞඞඞඞඞඞ                            |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
```

# Modulization

If your site is not supported in this app you can write your own module

In this case, you have to follow these rules:

1. Module file has to be in `./Script/modules` folder.
2. All functions in module has to be named with module name in beginning.
Example: `def youtube_download(): ...`
3. There has to be `module_download(url: str, opts: dict)-> None` function
Argument `opts` always has:
- `resolution` key, which by default is `"best"`
- `video_only` key, which by default is `False`
- `audio_only` key, which by default is `False`
- `path` key, which by default is `None`
- `name` key, which by default is `None`
Example: 
```bash
youtube_download("https://youtube.com/whatch=something", {
    'resolution': '144p',
    'video_only': True,
    'audio_obly': False,
    'path': None,
    'name': 'sugoma'
})
```
4. There has to be `module_format_check()-> bool` and `module_resolution_check()-> bool` functions
They return module's ability work with `-f` and `-r` options
It requires for `--help` docs generation
5. There has to be `mofule_info(url)-> str` function which return some useful information about received url, like avaliable video resolutions and etc.
6. There has to be `module_check(url)-> list` function which return the unique parts related to this module
It requires for url type difining 

There is also some optional things:
1. If you need you can save some data in `./Script/default_values.json`
It requires sometimes to save user data like username and password
2. If you download file from media link, you can use function `download_file(url, path, name, extention)` which animate download process
It would be better for user
Example:
```bash
download_file(
    "https:/uwu.com/video.mp4",
    "/path/somewhere",
    "uwu",
    ".mp4"
)
```

# Plans

- Bug fixes and adding features for already supported sites
- GUI for average users

# Thanks To The Developers Of

Pytube <br />
BeautifulSoup4 <br />
Youtube-dl <br />
Requests <br />
Selenium <br />
Browsermob-proxy <br />
and Python of course <br />
...
