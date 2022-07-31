import os
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from .functions.name_correct import name_correct
from .functions.download_file import download_file
from sys import stdout
import platform


def newgrounds_check(url):
    if 'newgrounds.com' in url:
        return True
    return False

def newgrounds_opt_func_check():
    return True

def newgrounds_res_func_check():
    return True

def newgrounds_get_docs():
    text = '''
+-------------------------+
| Newgrounds:             |
+------+------------------+---------------------------+---------------------------------------------------------------+
|      |--info            |                           |  returns avaliable resolutions for video downloading          |
|      |-o / -option      |  video_only / audio_only  |  by dafault downloads video and audio                         |
| url  |-p / -path        |  /full/path               |  by default locates downloads into (path to script)/downloads |
|      |-n / name         |  your_name                |  by default name generates with video title                   |
|      |-r / -resolution  |  144p/ 240p/ .../ 2160p   |  by default resolution is highest                             |
+------+------------------+---------------------------+---------------------------------------------------------------+
'''
    return text

def newgrounds_parser(url):

    options = Options()
    options.headless = True
    options.set_preference('media.volume_scale', '0.0')

    driver = webdriver.Firefox(options=options)

    driver.get(url)

    button = driver.find_element(by= By.XPATH, value= '//*[@id="ng-global-video-player"]/div[2]/div/div[2]')
    button.click()
    # stop_button = driver.find_element(by= By.XPATH, value= '//*[@id="ng-global-video-player"]/div/div[4]/div/div[2]/div[1]/button[4]')
    # stop_button.click()

    page = driver.page_source
    driver.close()
    page = BeautifulSoup(page, 'html.parser')

    title = page.find('h2', {'itemprop': 'name'}).contents[0]
    link = page.find('source', type = "video/mp4").attrs['src']
    video_opts = page.find_all("div", {'class': 'ng-video-options'})[1]
    resolutions = []
    for child in video_opts:
        res = child.attrs['data-value']
        if res == '4k':
            resolutions.append('2160p')
            res = '2160p'
        else:
            resolutions.append(child.attrs['data-value'])
        if res in link:
            i = link.index(res)
            link_pt1 = link[:i]
            link_pt2 = link[(i+len(res)):]
    
    get_by_res = {}
    for res in resolutions:
        get_by_res[res] = link_pt1 + res + link_pt2

    return resolutions, get_by_res, title

def newgrounds_info(url):
    if "https://www.newgrounds.com/portal/view/" in url:
        parsed_page = newgrounds_parser(url)
        text = f"Newgrounds video title: {parsed_page[2]}\nAvaliable quality:\n  "
        for res in parsed_page[0]:
            text = text + f"{res}, "
        text = text[:-2]
        return text
    else:
        print("ERROR: It's not a video link, maybe something else...")
    return newgrounds_parser(url)

def newgrounds_downloader(url, opts):
    if "https://www.newgrounds.com/portal/view/" in url:

        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        stdout
        parsed_page = newgrounds_parser(url)

        if resolution == 'best':
            link = parsed_page[1][parsed_page[0][0]]
        else:
            link = parsed_page[1][resolution]

        if custom_name is None:
            name = parsed_page[2]
        else:
            name = custom_name
        name = name_correct(name)

        if custom_path is None:
            path = f'{Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()}/downloads'.replace('/', os.sep)
        else:
            path = custom_path.replace('/', os.sep)

        try:
            os.mkdir(path)
        except:
            pass

        download_file(link, path, name)

        # clear func
        if platform.system() == "Windows":
            clear = lambda : os.system('cls')
        else:
            clear = lambda : os.system('clear')

        if video_only:
            cmd = f"ffmpeg -i {path}/output.mp4 -c:v copy -an {path}/{name}.mp4".replace('/', os.sep)
            os.system(cmd)
            os.remove(f'{path}/output.mp4'.replace('/', os.sep))
            clear()
        elif audio_only:
            cmd = f"ffmpeg -i {path}/output.mp4 -a:v copy -vn {path}/{name}.mp4".replace('/', os.sep)
            os.system(cmd)
            os.remove(f'{path}/output.mp4'.replace('/', os.sep))
            clear()
        else:
            os.rename(f'{path}/output.mp4', f"{path}/{name}.mp4".replace('/', os.sep))
            clear()
        
        stdout.write('Download complete!')
        stdout.flush()
    else:
        print("ERROR: It's not a video link, maybe something else...")