from asyncio import IncompleteReadError
import os, sys, shutil, platform, json, time
from pytube import YouTube
from pytube import Playlist
from pathlib import Path
from .functions.name_correct import name_correct
from .functions.download_file import download_file_from_stream
from sys import stdout
from http.client import IncompleteRead


def youtube_check():
    return ["youtube.com", "youtu.be"]

def youtube_format_check():
    return True

def youtube_resolution_check():
    return True

def youtube_parser(url):
    resolutions = {
                '144p': [394, 219, 160],
                '240p': [395, 242, 134],
                '360p': [396, 243, 167, 134],
                '480p': [397, 246, 245, 244, 219, 218, 168, 135],
                '720p': [302, 298, 398, 247, 169, 136],
                '1080p': [303, 299, 399, 248, 170, 137],
                '1440p': [308, 400, 271, 264],
                '2160p': [315, 302, 266, 401, 313, 272, 138],
                }
    res_list = ['144p',
                '240p',
                '360p',
                '480p',
                '720p',
                '1080p',
                '1440p',
                '2160p',]
    audio_quality_tags = {'256kbps': [172, 141],
                        '160kbps': [251],
                        '128kbps': [171, 140],
                        '70kbps': [250],
                        '60kbps': [249],
                        '48kbps': [139]
                        }
    audio_qualities = ['256kbps',
                    '160kbps',
                    '128kbps',
                    '70kbps',
                    '60kbps',
                    '48kbps']
    video_res_list = []
    video_tags = {}
    audio_quality = None
    audio_quality_tag = None
    yt_streams = None
    while yt_streams is None:
        yt_streams = YouTube(url).streams

    for res in res_list:
        for itag in resolutions[res]:
            if yt_streams.get_by_itag(itag) is not None:
                video_res_list.append(res)
                video_tags[res] = itag
                break
    
    flag = 0
    for qua in audio_qualities:
        for itag in audio_quality_tags[qua]:
            if yt_streams.get_by_itag(itag) is not None:
                audio_quality = qua
                audio_quality_tag = itag
                flag = 1
                break
        if flag == 1:
            break

    return tuple(video_res_list), video_tags, audio_quality, audio_quality_tag, yt_streams

def youtube_info(url):
    if "youtube.com/watch?v=" in url or "youtu.be/" in url or 'youtube.com/embed/' in url:
        parsed_url = youtube_parser(url)

        text = f"{YouTube(url).title}\n  Avaliable video resolutions: "
        for res in parsed_url[0]:
            text = f'{text + res}, '
        text = f"{text[:-2]}\n  Audio bitrate: {parsed_url[2]}"

        return text

    else:
        print("ERROR: Not a video link")
        sys.exit()


def youtube_download(url, opts):
    if "list=" in url: 
        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        playlist = Playlist(url)

        # define file name
        if custom_name is None:
            dir_name = playlist.playlist_id
        else:
            dir_name = 'custom_name'
        dir_name = name_correct(dir_name)
        
        # define file path
        prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()
        if custom_path is None:
            with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as f:
                default_path = json.load(f)['path']
            path = f'{default_path}{os.sep}{dir_name}'
        else:
            path = custom_path.replace('/', os.sep)
            path = f'{path}{os.sep}{dir_name}'
        
        try:
            os.mkdir(path)
        except:
            pass
        
        for video_url in playlist.video_urls:
            youtube_download(video_url, {
                'resolution': 'best',
                'video_only': video_only,
                'audio_only': audio_only,
                'path': path,
                'name': None
            })
        

    elif ("/watch?v=" in url) or ("youtu.be/" in url) or ('/embed' in url):
        # define options from console
        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        # parse youtube page
        parsed_ytpage = youtube_parser(url)
        res_list = parsed_ytpage[0]
        res_tags = parsed_ytpage[1]
        audio_tag = parsed_ytpage[3]
        yt_streams = parsed_ytpage[4]

        if resolution == "best":
            resolution = res_list[-1]

        res_tag = res_tags[resolution]

        # define project directory
        prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()

        # create directories for files
        try:
            os.mkdir(f'{prjct_dir}/downloads'.replace('/', os.sep))
        except:
            pass
        try:
            os.mkdir(f'{prjct_dir}/downloads/buffer'.replace('/', os.sep))
        except:
            pass

        # define path for buffer files
        buffer_path = f'{prjct_dir}/downloads/buffer'.replace('/', os.sep)
        video_path = f'{buffer_path}/video.mp4'.replace('/', os.sep)
        audio_path = f'{buffer_path}/audio.weba'.replace('/', os.sep)

        # define file name
        if custom_name is None:
            name = yt_streams.get_by_itag(res_tag).default_filename
        else:
            if video_only:
                name = f'{custom_name}.mp4'
            if audio_only:
                name = f'{custom_name}.weba'
        name = name_correct(name)
        
        # define file path
        if custom_path is None:
            with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as f:
                default_path = json.load(f)['path']
            path = default_path
        else:
            path = custom_path.replace('/', os.sep)

        # clear func
        if platform.system() == "Windows":
            clear = lambda : os.system('cls')
        else:
            clear = lambda : os.system('clear')

        # download video
        if not audio_only:
            video_stream = yt_streams.get_by_itag(res_tag)
            clear()
            download_file_from_stream(video_stream, buffer_path, 'video.mp4')
            while video_stream.filesize != os.path.getsize(video_path):
                continue
        
        if audio_tag is None or video_only:
            if audio_only:
                print("ERROR: This video has no audio")
                sys.exit()
            os.rename(video_path, f'{path}/{name}'.replace('/', os.sep))
            shutil.rmtree(buffer_path)
            clear()
            stdout.write("Video download complete!")
            stdout.flush()

        else:
            audio_stream = yt_streams.get_by_itag(audio_tag)
            clear()
            download_file_from_stream(audio_stream, buffer_path, 'audio.weba')
            while audio_stream.filesize != os.path.getsize(audio_path):
                continue

            if audio_only:
                os.rename(audio_path, f'{path}/{name}'.replace('/', os.sep))
                shutil.rmtree(buffer_path)
                clear()
                stdout.write("Audio download complete!")
                stdout.flush()
            
            else:
                cmd = f"ffmpeg -i {audio_path} -i {video_path} -c:v copy {path}/{name}".replace('/', os.sep)
                os.system(cmd)
                shutil.rmtree(buffer_path)
                clear()
                stdout.write("Video download complete!")
                stdout.flush()

    else:
        print("ERROR: Not a video link")
