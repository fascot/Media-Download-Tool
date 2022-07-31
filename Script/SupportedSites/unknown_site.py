import random, sys, os, platform, time
from os.path import dirname, abspath
from pathlib import Path
from browsermobproxy import Server
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from .functions.download_file import download_file
from .functions.name_correct import name_correct


def unknown_site_check(url):
    return False

def unknown_site_get_docs():
    text ='''
+-------------------------+
| Unknown Sites:          |
+------+------------------+---------------------------+---------------------------------------------------------------+
|      |--info            |                           |  returns avaliable LINKS and indexes for video downloading    |
| url  |-p / -path        |  /full/path               |  by default locates downloads into (path to script)/downloads |
|      |-n / name         |  your_name                |  by default name generates with video title                   |
+------+------------------+---------------------------+---------------------------------------------------------------+
'''
    return text

def unknown_site_opt_func_check():
    return False

def unknown_site_res_func_check():
    return False

def unknown_site_parser(url):
    # open browsermob-proxy on current OS and start proxy server
    script_dir = dirname(abspath(__file__))
    if platform.system() == "Windows":
        server = Server(f"{script_dir}/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat".replace('/', os.sep))
    if platform.system() == "Linux":
        server = Server(f"{script_dir}/browsermob-proxy-2.1.4/bin/browsermob-proxy".replace('/', os.sep))
    server.start()
    proxy = server.create_proxy()

    # change proxy options for firefox driver and make it headless and muted
    options = Options()
    options.headless = True
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
    formats = ['.3gp','.asf','.flv','.m2ts',
            '.m4v','.mkv','.mov','.mp4','.mts',
            '.ogg','.swf','.vob','.wmv','.rm']
    
    # put all video url adresses into one list and return it
    vid_links = []
    for link in links:
        for form in formats:
            if form in link:
                vid_links.append(link)
                break
            elif not '.webmanifest' in link and '.webm' in link:
                vid_links.append(link)
                break
            elif not '.avif' in link and '.avi' in link:
                vid_links.append(link)

    return vid_links

def unknown_site_info(url):
    text = 'sus'
    return text 

def unknown_site_downloader(url, opts):
    sys.stdout.write('Parsing site...')
    sys.stdout.flush()

    # get video url adresses with parser
    vid_links = unknown_site_parser(url)

    # define options from console
    if len(vid_links) > 0:
        flag = False
        if opts['resolution'] != "best":
            print("WARNING: -r (-resolution) option will be ignored")
            flag = True
        if opts['audio_only'] is not False or opts['video_only'] is not False:
            print("WARNING: -o (-option) option will be ignored")
            flag = True
        if flag:
            print("Use '--help unknown_site' too get more info")
        custom_path = opts['path']
        custom_name = opts['name']

        # get index for video from user
        print("\rAvaliable url adresses:")
        for i in range(len(vid_links)):
            print(f"{i} - {vid_links[i]}")
        print("Please select one adress by index: ", end= '')
        index = int(input())
        link = vid_links[index]

        # define file name
        if custom_name is None:
            name = ""
            for i in range(8):
                name = name + str(random.randint(1, 40))
        else:
            name = custom_name
        name = name_correct(name)
        
        # define file path
        if custom_path is None:
            path = f'{Path(dirname(abspath(__file__))).parent.parent.absolute()}/downloads'.replace('/', os.sep)
        else:
            path = custom_path
        
        # create directory on path
        try:
            os.mkdir(path)
        except:
            pass

        download_file(link, path, name)

    else:
        print("ERROR: No media links on this page")
