import random, os, platform, json
from os.path import dirname, abspath
from pathlib import Path
from sys import stdout
import sys
from browsermobproxy import Server
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from .functions.download_file import download_file
from .functions.name_correct import name_correct


def unknown_site_check():
    return None

def unknown_site_format_check():
    return False

def unknown_site_resolution_check():
    return False

def unknown_site_parser(url):
    string = '''
Required media link may not to load on page by default.
You can press some button on page to load needed file

Do you want to try y/n '''
    stdout.write(string)
    stdout.flush()
    boolean = input()
        

    # open browsermob-proxy on current OS and start proxy server
    script_dir = dirname(abspath(__file__))
    if platform.system() == "Windows":
        server = Server(f"{script_dir}/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat".replace('/', os.sep))
    else:
        server = Server(f"{script_dir}/browsermob-proxy-2.1.4/bin/browsermob-proxy".replace('/', os.sep))
    server.start()
    proxy = server.create_proxy()

    # change proxy options for firefox driver and make it headless and muted
    options = Options()
    if boolean == 'y' or boolean == 'Y':
        options.headless = False
    elif boolean == 'n' or boolean == 'N':
        options.headless = True
    else:
        stdout.write('WTF did you say')
        sys.exit()
    options.set_preference("media.volume_scale", "0.0")
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.http", "localhost")
    options.set_preference("network.proxy.http_port", proxy.port)
    options.set_preference('network.proxy.ssl', "localhost")
    options.set_preference('network.proxy.ssl_port', proxy.port)
    options.set_preference("network.proxy.share_proxy_settings", True)
    options.set_preference("network.proxy.https", "localhost")
    options.set_preference("network.proxy.https_port", proxy.port)

    # start firefox driver with necessary options
    driver = webdriver.Firefox(options=options)
    proxy.new_har("first_and_last")

    # open requested url
    driver.get(url)

    if boolean == 'y' or boolean == 'Y':
        string = "Enter if you are done"
        stdout.write(string)
        stdout.flush()
        sus = input()

    # after loading site get all url adresses from it
    links = []
    entries = proxy.har['log']["entries"]
    for entry in entries:
        if 'request' in entry.keys():
            links.append(entry['request']['url'])
    
    # close proxy server and firefox driver
    driver.quit()
    proxy.close()
    server.stop()

    # video formats
    video_formats = ['.3gp','.asf','.flv','.m2ts',
            '.m4v','.mkv','.mov','.mp4','.mts',
            '.swf','.vob','.wmv','.rm']
    audio_formats = ['.aac', '.wav', '.mid', '.m4a', '.m4p', '.m4b',
            '.3gp', '.ac3', '.aif', '.aiff', '.mpa', '.wma',
            '.aifc', '.flac', '.mp3', '.ogg', '.oga', '.opus', '.amr']
    image_formats = ['.psd', '.tiff', '.bmp', '.jpeg', '.jpg', '.png',
            '.gif', '.ico', '.webp', 'svg', '.heic', '.avif']
    
    # put all video url adresses into one list and return it
    vid_links = []
    aud_links = []
    img_links = []
    vid_frmts = []
    aud_frmts = []
    img_frmts = []
    for link in links:
        for vid_form in video_formats:
            if vid_form in link:
                vid_links.append(link)
                vid_frmts.append(vid_form)
                break
            elif not '.webmanifest' in link and '.webm' in link:
                vid_links.append(link)
                vid_frmts.append('.webm')
                break
            elif not '.avif' in link and '.avi' in link:
                vid_links.append(link)
                vid_frmts.append('.avi')
    
    for link in links:
        for aud_form in audio_formats:
            if aud_form in link:
                aud_links.append(link)
                aud_frmts.append(aud_form)
                break

    for link in links:
        for img_form in image_formats:
            if img_form in link:
                img_links.append(link)
                img_frmts.append(img_form)
                break

    return vid_links, aud_links, img_links, vid_frmts, aud_frmts, img_frmts

def unknown_site_info(url):
    text = 'Nothing interesting'
    return text 

def unknown_site_download(url, opts):
    # get video url adresses with parser
    links = unknown_site_parser(url)
    vid_links = links[0]
    aud_links = links[1]
    img_links = links[2]
    vid_frmts = links[3]
    aud_frmts = links[4]
    img_frmts = links[5]

    # define options from console
    if (len(vid_links) > 0) or (len(aud_links) > 0) or (len(img_links) > 0):
        flag = False
        if opts['resolution'] != "best":
            print("WARNING: -r (-resolution) option will be ignored")
            flag = True
        if opts['audio_only'] is not False or opts['video_only'] is not False:
            print("WARNING: -f (-format) option will be ignored")
            flag = True
        if flag:
            print("Use '--help unknown_site' to get more info")
        custom_path = opts['path']
        custom_name = opts['name']

        # get index for video from user
        if len(vid_links) != 0:
            print('Avaliable video url adresses:')
            for i in range(len(vid_links)):
                print(f'{i+1} - {vid_links[i]}')
        if len(aud_links) != 0:
            print('Avaliable audio url adresses:')
            for i in range(len(aud_links)):
                print(f'{len(vid_links)+i+1} - {aud_links[i]}')
        if len(img_links) != 0:
            print('Avaliable image url adresses:')
            for i in range(len(img_links)):
                print(f'{len(vid_links)+len(aud_links)+i+1} - {img_links[i]}')
        index = int(input())
        if index <= len(vid_links):
            link = vid_links[index-1]
            format = vid_frmts[index-1]
        elif index <= len(vid_links)+len(aud_links)-1:
            link = aud_links[index-len(vid_links)-1]
            format = aud_frmts[index-len(vid_links)-1]
        else:
            link = img_links[index-len(vid_links)-len(aud_links)-1]
            format = img_frmts[index-len(vid_links)-len(aud_links)-1]

        # define file name
        if custom_name is None:
            name = ""
            for i in range(8):
                name = name + str(random.randint(1, 40))
        else:
            name = custom_name
        name = name_correct(name)
        
        # define file path
        prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()
        if custom_path is None:
            with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as f:
                default_path = json.load(f)['path']
            path = default_path
        else:
            path = custom_path.replace('/', os.sep)
        
        # create directory on path
        try:
            os.mkdir(path)
        except:
            pass
        # clear func
        if platform.system() == "Windows":
            clear = lambda : os.system('cls')
        else:
            clear = lambda : os.system('clear')
        clear()
        download_file(link, path, name, format)

    else:
        print("ERROR: No media links on this page")
