import os, requests, youtube_dl
from bs4 import BeautifulSoup
from pornhub_api import PornhubApi
from pathlib import Path
from os.path import dirname, abspath
from sys import stdout
from .functions.name_correct import name_correct
import platform


def pornhub_check(url):
    if 'pornhub' in url:
        return True
    return False

def pornhub_get_docs():
    text ='''
+-------------------------+
| Pornhub:                |
+------+------------------+---------------------------+---------------------------------------------------------------+
|      |--info            |                           |  returns avaliable resolutions for video downloading          |
|      |-o / -option      |  video_only / audio_only  |  by dafault downloads video and audio                         |
| url  |-p / -path        |  /full/path               |  by default locates downloads into (path to script)/downloads |
|      |-n / name         |  your_name                |  by default name generates with video title                   |
|      |-r / -resolution  |  144p/ 240p/ .../2160p    |  by default resolution is highest                             |
+------+------------------+---------------------------+---------------------------------------------------------------+
'''
    return text

def pornhub_opt_func_check():
    return True

def pornhub_res_func_check():
    return True

def get_resolutions(url):
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    response = requests.get(url).content
    page = BeautifulSoup(response, 'html.parser')
    script = str(page.find(id = 'player').contents[1].__dict__['contents'][0])

    start_index = script.index('"defaultQuality"')+18
    res_list = ['']
    list_index = 0

    for i in range(32):
        symb = script[start_index + i]
        if symb == ']':
            break
        elif symb in numbers:
            res_list[list_index] += symb
        else:
            list_index += 1
            res_list.append('')

    return res_list

def pornhub_info(url):
    resolutions = ['2160','1440','1080','720','480','360','240']

    if '/view_video.php?viewkey=' in url:
        res_list = get_resolutions(url)

    else:
        print("ERROR: Wrong pornhub link: maybe this link is not a video link, but channel or playlist and etc.")

    api = PornhubApi()
    vid_id = url[url.index('=')+1:]
    video = api.video.get_by_id(vid_id).video
    title = video.title
    text = f"{title}\nAvaliable video resolutions: "
    for res in res_list:
        text = f"{text+res}p, "
    text = text[:-2]

    return text

def pornhub_downloader(url, opts):
    resolutions = ['2160','1440','1080','720','480','360','240']

    if '/view_video.php?viewkey=' in url:
        resolution = opts['resolution'][:-1]
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        if custom_path is None:
            path = f"{Path(dirname(abspath(__file__))).parent.parent.absolute()}/downloads".replace('/', os.sep)
        else:
            path = custom_path

        if resolution == 'best' or resolution in resolutions or resolution is None:
            if custom_name is None:
                api = PornhubApi()
                vid_id = url[url.index('=')+1:-1] + url[-1]
                video = api.video.get_by_id(vid_id).video
                name = video.title
            else:
                name = custom_name
            name = name_correct(name)

            if resolution == 'best' or resolution == '':
                format = 'best'
            else:
                format = f'best[height={resolution}]'

            try:
                download_options = {'format': format,
                        'outtmpl': f'{path}/output.mp4'.replace('/', os.sep),
                        'ignoreerrors': True,
                        'nowarnings': True,
                        'nooverwrites': True}

                with youtube_dl.YoutubeDL(download_options) as ydl:
                    ydl.download([url])

            except:
                print("ERROR: Couldn't download video: check your url or resolution of video, maybe it's too big")
        else:
            print("ERROR: Invalid resolution optinon: check documentation")
    else:
        print("ERROR: Wrong pornhub link: maybe this link is not a video link, but channel or playlist and etc.")
    
    # clear func
    if platform.system() == "Windows":
        clear = lambda : os.system('cls')
    else:
        clear = lambda : os.system('clear')
    
    if video_only:
        cmd = f"ffmpeg -i {path}/output.mp4 -c:v copy -an {path}/{name}.mp4".replace('/', os.sep)
        os.system(cmd)
        clear()
        stdout.write("Video download complete!")
        stdout.flush()
    elif audio_only:
        cmd = f"ffmpeg -i {path}/output.mp4 -c:a copy -vn {path}/{name}.mp4".replace('/', os.sep)
        os.system(cmd)
        clear()
        stdout.write("Audio download complete!")
        stdout.flush()
    else:
        os.rename(f"{path}/output.mp4", f"{path}/{name}.mp4".replace('/', os.sep))
        clear()
        stdout.write("Video download complete!")
        stdout.flush()
