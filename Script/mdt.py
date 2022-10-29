import platform
import sys
import os
from time import sleep
import requests
from os.path import dirname, abspath
import json
from pathlib import Path
from sys import stdout


global amoguss
amoguss = ['''
                      ,▄▄████████▄▄,
                   ╓▄██▀▀`       ▀▀██▄
                  ▄██▀            ,▄███▄▄▄
                 ▐██       ▄███████▀▀▀▀▀██
                ╒██     ╓█████          ╙███
          ▄▄██████▌    ,██ ╜██  ▄▄   \ ▌█▄▀███▄
         ██▀    ██     ██▌▒ ▀██▄ ▄ $▀m`╙    ,████╕
        ▐██    ▐██     ██▌ ╗╥╓██▄ "   ,▄▄████▀▀""
        ██▌    ▐██     ▀██▄    ▀██▄▄████████
        ██▌    ▐██       ▀███████████████▀
        ██▌    ▐██                     ██
        ██▌    ▐██                    ▐██
        ██▌     ██                    ▐██
        ▐██     ██                   ▄██
         ██▄▄█████▌                 ▐██
          ███▀   ███▄                ▀██╖
         ▄██      `▀█████▄▄▄▄          ▀██
         ▀██▄          ▐██"▀██▄         ╙██▄
           ███▄▄,     ▄██`   ▀██▄         ███
             "▀▀███████▀       ▀██▄       ▐██
                                 ▀██▄   ,▄██
                                   ▀█████▀"''',
'''

                           ███████████╓▄▄▄▄
                      ,▄███████Γ""""" ▀▀▀██
                    ╓███▀   ▐█▌          ▀██▄
          ╔▄██████████     ▄▄██  ▄▄ ┌ Y ▌█▄▀███▄
         ▄██      ███   ,███▀▀██ ╙▄ ▌▀∞ ╙    ▄████,
        ]██      ███    ██▀    ██▄ `   ,▄▄████▀▀``
        ▐█▌     ]██    ▐██ ░    ▀██▄▄███▀▀██
        ▐█▌     ██▌     ██▄ ▒╗╥╥╥╥▀▀▀`▒╗U███
        ▐█▌     ██▌      ▀█████▄▄▄▄▄██████▀
        ▐█▌     ██           `▀▀▀▀▀▀▀▀` ██Γ
        ▐██    ▐██                      ██Γ
        ▐██    ▐██                      ██
         ██▌   ▐██                     ███
          ▀███████▄                  ▄██▀
                 ▀██▄             ,▄███
                  ████▄        ██████▌
                  ██▀██▌       ██▌  ██
                  █████▌       ███▄███
                    "██▌       ██▀▀▀`
                     ██▄      ▄██
                     '▀▀██████▀▀''',
'''     
                      ,▄▄████████▄▄,  ,,▄
                   ╓▄██▀▀` ▄██████████████
                  ▄██      ▐█▌          ██▄
                 ▄██       ▐█▌       ▄╒▄▄▀███w
          ▄▄███████     ▄█████▄ ▓ ▀▄▄▐ ▌▀'  ▀███▄
        ,██▀    ██▌    ╒██ ╜ ▀██ 'M     ▄▄▄████▀▀`
        ██▌    j██     ██▌▒    ██▄,,▄████▀▀██▌
        ██     ▐██     ██▌ ╗╥╖╖╓]███▀▀,╥╢░▄██
        ██     ▐██     ▀██▄            ,▄███
        ██     ▐██       ▀███████████████▀
        ██     ▐██                     ██
        ██     ▐██                    ▐██
        ██▌     ██                    ███
        ▐██    ]██                    ██
         ▀████▄███                   ███▄,
         ▄█████████                 ▄██▀▀███▄,
        ██▌     `▀▀             ,▄▄██▀     `███
       ]██              ▄██████████▌         ██
        ██▄,         ,▄██▀       '███▄      ▄██
         "▀████████████▀            ▀██▄  ▄███
                                      ▀████▀`
                                      ''',
'''
                          ,╓▄▄▄▄▄╖╓▄▄▄▄▄████
                      ,▄███▀▀███▀▀▀▀▀▀▀`  ██▄
              ,,,   ,▄██▀    ██▌          ,▀██▄
          ▄███████████▀    ▄▄███  m∞▄j ╙ ██N ▀██▄▄
         ▄██      ███    ▄██▀▀▀██ '▄ ▌'ⁿ     ,▄▄███▌
         ██      ╔██    ▐██ ╜   ██▄     ▄▄▄███▀▀"`
        ▐██      ██▌    ▐█▌ Ç    ▀██▄▄███▀▀██▌
        ▐██     ▐██      ██▄ ╢╗╗╥╗╖▀▀▀`▒@U▄██
        ▐██     ███       ▀█████▄▄▄▄▄███████
        ▐██     ██▌           ▀▀▀▀▀▀▀▀▀` ██▌
        ▐██     ██▌                      ██▌
         ██     ██▌                      ██▌
         ██▌    ██▌                     ▄██
          █████████                    ▐██
             ````███▄▄▄▄              ▄██
                ▄███▀▀▀▀`      ██▄ ,▄███
               ▐██             ▐█████▀
               ██▌             ██▌ ██
               ██▌         ,▄███▀  ██▌
                █████████████▀▀    ██
                  ```````██▌▄▄▄▄▄▄███
                         '▀▀▀▀▀▀▀▀"''']


def url_check(url):
    check = requests.head(url)
    if check.status_code in [200, 303]:
            return True
    return False

def docs(docs_dict, url_type):
    try:
        return docs_dict[url_type]
    except KeyError:
        print(f"ERROR: No supported site called {url_type}")
        sys.exit()

def get_url_info(url, url_type):
    string = f'''
from modules import {url_type}

sys.stdout.write({url_type}.{url_type}_info('{url}'))
sys.stdout.flush()
'''
    exec(string)
    sys.exit()

def download(url, url_type, opts):
    string = f'''
from modules import {url_type}

{url_type}.{url_type}_download('{url}',{opts})
'''
    exec(string)
    sys.exit()


def input_processing():
    cmd = sys.argv
    url = cmd[1]
    if len(cmd) < 2:
        print('ERROR: No arguments')
        sys.exit()

    modules = []
    script_dir = dirname(abspath(__file__))
    for site_file in os.scandir(f'{script_dir}{os.sep}modules'):
        if site_file.is_file():
            modules.append(site_file.name[:-3])
    
    prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
    with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as fr:
        values = json.load(fr)
        if values["path"] == '':
            print("First setup, it takes time...")
            values["path"] = f"{prjct_dir}{os.sep}downloads"
        with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'w') as fw:
            json.dump(values, fw, ensure_ascii=False, indent=1)

    with open('modules_info.json', 'r') as fr:
        global modules_info
        modules_info = json.load(fr)
        if set(modules_info['modules']) != set(modules):

            global format_sites
            global resolution_sites
            format_sites = []
            resolution_sites = []
            docs_by_module = modules_info["docs_by_module"]
            doc_template = modules_info["doc_template"]

            for module in modules:
                string = f'''
from modules.{module} import {module}_format_check, {module}_resolution_check, {module}_check

modules_info["{module}_check"] = {module}_check()

if {module}_format_check():
    format_sites.append('{module}')
if {module}_resolution_check():
    resolution_sites.append('{module}')
'''
                exec(string, globals())
                modules_info["format_sites"] = format_sites
                modules_info["resolution_sites"] = resolution_sites

                module_doc = [doc_template["upper_edge"],
                "| "+module+" "*(len(doc_template["upper_edge"])-len(module)-3)+"|",
                doc_template["middle_edge"],
                doc_template["info_opt"],
                doc_template["path_opt"],
                doc_template["name_opt"],
                doc_template["lower_edge"]]
                if module in format_sites:
                    module_doc = module_doc[:4]+[doc_template["form_opt"]]+module_doc[4:]
                if module in resolution_sites:
                    module_doc = module_doc[:-1]+[doc_template["res_opt"]]+[module_doc[-1]]
                
                docs_by_module[module] = module_doc
            
            docs_by_module["all"][11] = str(format_sites)[1:-1].replace("'", '')
            docs_by_module["all"][18] = str(resolution_sites)[1:-1].replace("'", '')

            for module in modules_info["modules"]:
                if module not in modules:
                    del modules_info[f"{module}_check"]
                    del modules_info["docs_by_module"][str(module)]
            
            modules_info["modules"] = modules

            with open('modules_info.json', 'w') as fw:
                json.dump(modules_info, fw, ensure_ascii=False, indent=1)
        else:
            docs_by_module = modules_info["docs_by_module"]


    if url == '--help':
        if len(cmd) > 2:
            for string in docs(docs_by_module, cmd[2]):
                stdout.write(f'{string}\n')
        else:
            for string in docs(docs_by_module, 'all'):
                stdout.write(string)
        stdout.flush()
        sys.exit()

    elif url == '--default_path':
        if len(cmd) > 2:
            prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
            with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'r') as f:
                default_values = json.load(f)
                if cmd[2][-1] in ['/', '\\']:
                    default_values['path'] = cmd[2][:-1]
                else:
                    default_values['path'] = cmd[2]
                with open(f'{prjct_dir}/Script/default_values.json'.replace('/', os.sep), 'w') as f:
                    json.dump(default_values, f, ensure_ascii=False, indent=4)
        else:
            print("ERROR: No argument after '--default_path' option")
        sys.exit()
    
    elif url == '--amogus':
        lengths = []
        for i in amoguss:
            for j in i.splitlines():
                lengths.append(len(j))
        max_length = max(lengths)

        new_amoguss = []
        for i, amogus in enumerate(amoguss):
            new_amoguss.append("")
            for j in amogus.splitlines():
                j += " "*(max_length-len(j))
                new_amoguss[-1] += f"{j}\n"
            new_amoguss[-1] = new_amoguss[-1][:-2]

        # clear func
        if platform.system() == "Windows":
            clear = lambda : os.system('cls')
        else:
            clear = lambda : os.system('clear')

        i = 0
        while True:
            if i == 4:
                i = 0
            clear()
            stdout.write(f"\r{new_amoguss[i]}")
            stdout.flush()
            i+=1
            sleep(0.25)

    elif url_check(cmd[1]):
        opts = {'video_only': False,
                'audio_only': False,
                'resolution': "best",
                'name': None,
                'path': None
                }
        ignore_element = False
        format_flag = False
        resolution_flag = False
        name_flag = False
        path_flag = False

        with open('modules_info.json', 'r') as f:
            modules_info = json.load(f)
            url_type = None
            for module in modules:
                if modules_info[f"{module}_check"] != None:
                    for unique_url_part in modules_info[f"{module}_check"]:
                        if unique_url_part in url:
                            url_type = module
                            break
            if url_type is None:
                    url_type = 'unknown_site'

        if len(cmd) > 2:

            if cmd[2] == '--info':
                if len(cmd) > 3:
                    print("WARNING: options after --info will be ignored")
                get_url_info(url, url_type)
                # return 0

            for i in range(2, len(cmd)):

                if ignore_element:
                    ignore_element = False
                    continue

                elif cmd[i] == '-f' or cmd[i] == '-format':
                    if format_flag:
                        print("WARNING: other -f (-format) options will be ignored")
                        ignore_element = True

                    elif len(cmd) > i+1:
                        if cmd[i+1] == 'video_only':
                            opts['video_only'] = True
                        elif cmd[i+1] == 'audio_only':
                            opts['audio_only'] = True
                        else:
                            print(f"ERROR: -f (-format) option have no {cmd[i]} argument")
                            sys.exit()

                        format_flag = True
                        ignore_element = True
                    
                    else:
                        print("ERROR: No arguments after -f (-format) option")
                        sys.exit()

                elif cmd[i] == '-r' or cmd[i] == '-resolution':
                    if resolution_flag:
                        print("WARNING: other -r (-resolution) options will be ignored")
                        ignore_element = True

                    elif len(cmd) > i+1:
                        opts['resolution'] = cmd[i+1]
                        resolution_flag = True
                        ignore_element = True

                    else:
                        print("ERROR: No arguments after -r (-resolution) option")
                        sys.exit()
                
                elif cmd[i] == '-n' or cmd[i] == '-name':
                    if name_flag:
                        print("WARNING: other -n (-name) option will be ignored")
                        ignore_element = True

                    elif len(cmd) > i+1:
                        opts['name'] = cmd[i+1]
                        name_flag = True
                        ignore_element = True

                    else:
                        print("ERROR: No arguments after -n (-name) option")
                        sys.exit()
                
                elif cmd[i] == '-p' or cmd[i] == '-path':
                    if path_flag:
                        print("WARNING: other -p (-path) options will be ignored")
                        ignore_element = True

                    elif len(cmd) > i+1:
                        opts['path'] = cmd[i+1]
                        path_flag = True
                        ignore_element = True

                    else:
                        print("ERROR: No arguments after -p (-path) option")
                        sys.exit()

                else:
                    print(f"ERROR: No option called {cmd[i]}")
                    sys.exit()

        return download(url, url_type, opts)

    print('ERROR: Invalid url')
    sys.exit()


if __name__ == '__main__':
    input_processing()