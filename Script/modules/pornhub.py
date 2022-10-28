import os, requests, youtube_dl, shutil, platform, json
from bs4 import BeautifulSoup
from pornhub_api import PornhubApi
from pathlib import Path
from os.path import dirname, abspath
from sys import stdout
from functions.name_correct import name_correct
import sys


def pornhub_check():
    return ("pornhub.com")

def pornhub_format_check():
    return True

def pornhub_resolution_check():
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
    if '/view_video.php?viewkey=' in url:
        res_list = get_resolutions(url)

    else:
        print("ERROR: Incorrect pornhub link")

    api = PornhubApi()
    vid_id = url[url.index('=')+1:]
    video = api.video.get_by_id(vid_id).video
    title = video.title
    text = f"{title}\nAvaliable video resolutions: "
    for res in res_list:
        text = f"{text+res}p, "
    text = text[:-2]

    return text

def pornhub_download(url, opts):
    resolutions = ['2160','1440','1080','720','480','360','240']

    if '/view_video.php?viewkey=' in url:
        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()
        if custom_path is None:
            with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as f:
                default_path = json.load(f)['path']
            path = default_path
        else:
            path = custom_path.replace('/', os.sep)
        buffer_path = f"{Path(dirname(abspath(__file__))).parent.parent.absolute()}/downloads/buffer".replace('/', os.sep)

        if custom_name is None:
            api = PornhubApi()
            vid_id = url[url.index('=')+1:-1] + url[-1]
            video = api.video.get_by_id(vid_id).video
            name = video.title
        else:
            name = custom_name
        name = name_correct(name)

        if (resolution == 'best') or (resolution in resolutions):

            if resolution == 'best':
                format = 'best'
            else:
                format = f'best[height={resolution[:-1]}]'

            try:
                download_options = {'format': format,
                        'outtmpl': f'{buffer_path}/output.mp4'.replace('/', os.sep),
                        'ignoreerrors': True,
                        'nowarnings': True,
                        'nooverwrites': True,
                        'cachedir': False}
                with youtube_dl.YoutubeDL(download_options) as ydl:
                    ydl.download([url])
            except:
                print("ERROR: Couldn't download video")
                sys.exit()
        else:
            print("ERROR: Invalid resolution optinon")
            sys.exit()

    elif "/playlist/" in url:
        response = requests.get(url).text
        resp = BeautifulSoup(response, 'html.parser')
        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']
    
        prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()
        if custom_path is None:
            with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as f:
                default_path = json.load(f)['path']
            path = default_path
        else:
            path = custom_path.replace('/', os.sep)
        
        if custom_name is None:
            dir_name = resp.find('h1', {'class': 'playlistTitle watchPlaylistButton js-watchPlaylistHeader js-watchPlaylist'}).contents[0]
        else:
            dir_name = custom_name
        dir_name = name_correct(dir_name)

        try:
            os.mkdir(f'{path}{os.sep}{dir_name}')
        except:
            pass
        
        video_links = resp.find_all('a', {'class': 'fade fadeUp videoPreviewBg linkVideoThumb js-linkVideoThumb img'})
        for i in video_links:
            href = i.attrs['href']
            pornhub_download(f'https://pornhub.com{href}', 
            {
                'resolution': 'best',
                'video_only': video_only,
                'audio_only': audio_only,
                'path': f'{path}{os.sep}{dir_name}',
                'name': None
            })

    else:
        print("ERROR: Incorrect pornhub link")
        sys.exit()
    
    # clear func
    if platform.system() == "Windows":
        clear = lambda : os.system('cls')
    else:
        clear = lambda : os.system('clear')

    if video_only:
        cmd = f"ffmpeg -i {buffer_path}/output.mp4 -c:v copy -an {path}/{name}.mp4".replace('/', os.sep)
        shutil.rmtree(buffer_path)
        os.system(cmd)
        clear()
        stdout.write("Video download complete!")
        stdout.flush()
    elif audio_only:
        cmd = f"ffmpeg -i {buffer_path}/output.mp4 -c:a copy -vn {path}/{name}.mp3".replace('/', os.sep)
        shutil.rmtree(buffer_path)
        os.system(cmd)
        clear()
        stdout.write("Audio download complete!")
        stdout.flush()
    else:
        os.rename(f"{buffer_path}/output.mp4", f"{path}/{name}.mp4".replace('/', os.sep))
        shutil.rmtree(buffer_path)
        clear()
        stdout.write("Video download complete!")
        stdout.flush()


pornhub_download("https://rt.pornhub.com/playlist/241384191", {
    'resolution': 'best',
    'video_only': False,
    'audio_only': False,
    'path': None,
    'name': None
})