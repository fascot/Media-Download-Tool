import os, sys, platform, requests, json, time
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from sys import stdout

if __name__ == "__main__":
    from functions.name_correct import name_correct
    from functions.download_file import download_file
else:
    from .functions.name_correct import name_correct
    from .functions.download_file import download_file


def newgrounds_check():
    return ("newgrounds.com")

def newgrounds_format_check():
    return True

def newgrounds_resolution_check():
    return True

def newgrounds_change_default_values():
    string = '''
If you want to download adult content you have to be authorized on newgrounds
Enter your username or email: '''
    stdout.write(string)
    stdout.flush()
    username = input()
    string = "Enter your password: "
    stdout.write(string)
    stdout.flush()
    password = input()
    string = "User data will remembered in future"
    stdout.write(string)
    stdout.flush()
    script_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
    with open(f'{script_dir}{os.sep}default_values.json', 'r') as fr:
        default_values = json.load(fr)
        default_values['newgrounds'] = {'username': username, 'password': password}
        with open(f'{script_dir}{os.sep}default_values.json', 'w') as fw:
            json.dump(default_values, fw, ensure_ascii=False, indent=1)
    return username, password


def newgrounds_parser(url):
    if "https://www.newgrounds.com/portal/view/" in url:
        options = Options()
        options.headless = True
        options.set_preference('media.volume_scale', '0.0')

        driver = webdriver.Firefox(options=options)

        driver.get(url)

        try:
            log_in = driver.find_element(by= By.XPATH, value= '//*[@id="errorpage_login"]')
            log_in.click()

            frame = driver.find_element(by= By.XPATH, value= '/html/body/div[3]/iframe')
            driver.switch_to.frame(frame)

            username_input, password_input = None, None
            while username_input is None and password_input is None:
                try:
                    username_input = driver.find_element(by= By.XPATH, value= '/html/body/div[2]/div/div[2]/form/div[1]/div[1]/input')
                    password_input = driver.find_element(by= By.XPATH, value= '/html/body/div[2]/div/div[2]/form/div[1]/div[2]/input')
                    script_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
                    with open(f'{script_dir}{os.sep}default_values.json', 'r') as f:
                        default_values = json.load(f)
                        try:
                            newgrounds = default_values['newgrounds']
                            username_input.send_keys(newgrounds['username'])
                            password_input.send_keys(newgrounds['password'])
                        except KeyError:
                            new_values = newgrounds_change_default_values()
                            username_input.send_keys(new_values[0])
                            password_input.send_keys(new_values[1])

                    log_in = driver.find_element(by= By.XPATH, value= "/html/body/div[2]/div/div[2]/form/div[3]/button")
                    log_in.click()
                    driver.switch_to.default_content()
                    break
                except:
                    continue
        except:
            pass

        try:
            button = driver.find_element(by= By.XPATH, value= '//*[@id="ng-global-video-player"]/div[2]/div/div[2]')                                        
            button.click()
        except:
            print('ERROR: Wrong username or password or account is blocked')

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
            elif res == '8k':
                resolutions.append('4320p')
                res = '4320p'
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

    elif "https://www.newgrounds.com/art/view/" in url:
        page = requests.get(url)
        page = BeautifulSoup(page.text, 'html.parser')

        title = page.find('h2', {'itemprop': 'name'}).contents[0]
        image_link = page.find('div', {'class': 'image'}).findChild('img')['src']
        formats = ['.png', '.gif', '.jpg', '.jpeg']
        for form in formats:
            if form in image_link:
                format = form
        
        return image_link, format, title
    
    elif "https://www.newgrounds.com/audio/listen/" in url:
        page = requests.get(url)
        page = BeautifulSoup(page.text, 'html.parser')

        title = page.find('h2', {'itemprop': 'name'}).contents[0]
        json_script = page.find('div', {'class': 'pod-body'})
        json_script = json_script.next_sibling.next_sibling.next_sibling.next_sibling
        json_script = json_script.next_sibling.next_sibling.next_sibling.next_sibling
        audio_link = json_script.string[53:json_script.string.index(',')-1].replace('\\/\\/', '//').replace('\\/', '///')
        
        return audio_link, title


def newgrounds_info(url):
    if "https://www.newgrounds.com/portal/view/" in url:
        parsed_page = newgrounds_parser(url)
        text = f"Newgrounds video title: {parsed_page[2]}\nAvaliable quality:\n  "
        for res in parsed_page[0]:
            text = text + f"{res}, "
        text = text[:-2]
        return text
    else:
        print("ERROR: It's not a video link")
        sys.exit()


def newgrounds_download(url, opts):
    resolution = opts['resolution']
    video_only = opts['video_only']
    audio_only = opts['audio_only']
    custom_path = opts['path']
    custom_name = opts['name']
    
    # clear func
    if platform.system() == "Windows":
        clear = lambda : os.system('cls')
    else:
        clear = lambda : os.system('clear')
    
    prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()
    if custom_path is None:
        with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as f:
            default_path = json.load(f)['path']
        path = default_path
    else:
        path = custom_path.replace('/', os.sep)

    if "https://www.newgrounds.com/portal/view/" in url:

        parsed_page = newgrounds_parser(url)
        while len(parsed_page[0]) == 0:
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

        try:
            os.mkdir(path)
        except:
            pass

        download_file(link, path, 'output', '.mp4')

        file_size_in_bytes = int(requests.head(link).headers['content-length'])
        while file_size_in_bytes != os.path.getsize(f'{path}{os.sep}output.mp4'):
            continue
        
        if video_only:
            cmd = f"ffmpeg -i {path}/output.mp4 -c:v copy -an {path}/{name}.mp4".replace('/', os.sep)
            os.system(cmd)
            os.remove(f'{path}/output.mp4'.replace('/', os.sep))
            clear()
        elif audio_only:
            cmd = f"ffmpeg -i {path}/output.mp4 -a:v copy -vn {path}/{name}.mp3".replace('/', os.sep)
            os.system(cmd)
            os.remove(f'{path}/output.mp4'.replace('/', os.sep))
            clear()
        else:
            os.rename(f'{path}/output.mp4'.replace('/', os.sep), f"{path}/{name}.mp4".replace('/', os.sep))
            clear()

    else:
        flag = False
        if opts['resolution'] != "best":
            print("WARNING: -r (-resolution) option will be ignored")
            flag = True
        if (opts['audio_only'] is not False) or (opts['video_only'] is not False):
            print("WARNING: -f (-format) option will be ignored")
            flag = True
        if flag:
            print("Use '--help newgrounds' to get more info")

        try:
            os.mkdir(path)
        except:
            pass

        parsed_page = newgrounds_parser(url)
        link = parsed_page[0]

        if "https://www.newgrounds.com/audio/listen/" in url:
            title = parsed_page[1]

            if custom_name is None:
                name = title
            else:
                name = custom_name
            name = name_correct(name)

            download_file(link, path, name, '.mp3')

        elif "https://www.newgrounds.com/art/view/" in url:
            format = parsed_page[1]
            title = parsed_page[2]

            if custom_name is None:
                name = title
            else:
                name = custom_name
            name = name_correct(name)
            clear()
            download_file(link, path, name, format)