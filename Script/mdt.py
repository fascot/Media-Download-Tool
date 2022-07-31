import sys
import os
import requests
from os.path import dirname, abspath

module_names = []
docs_by_module = {}
script_dir = dirname(abspath(__file__))

def url_check(url):
    check = requests.head(url)
    try:
        if check.status_code == 200:
            return True
        else:
            raise(ValueError)
    except ValueError:
        return f"Invalid url: respose gets {check.status_code} error"

for site_file in os.scandir(f'{script_dir}/SupportedSites'.replace('/', os.sep)):
    if site_file.is_file():
        module_names.append(site_file.name[:-3])
        string = f"from SupportedSites.{site_file.name[:-3]} import *"
        exec(string)

opt_able_sites = []
res_able_sites = []
try:
    url = sys.argv[1]
except:
    print("ERROR: No url got")
    sys.exit()
url_type = None
for module in module_names:
    if url_type is not None:
        break
    string = f'''
if {module}_opt_func_check():
    opt_able_sites.append('{module}')
if {module}_res_func_check():
    res_able_sites.append('{module}')

check = {module}_check(url)
if check:
    url_type = module
docs_by_module['{module}'] = {module}_get_docs()
'''
    exec(string)
if url_type is None:
    url_type = 'unknown_site'

docs_by_module['all'] = f'''
Base commands, wich work with any type of url:
+----------------+------------------------+---------------------------------+------------------------------------------------+
| Tool           | Url | Command          | Argument                        | Description                                    |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python uwvp.py |     | --help           | all | youtube | unknown_site... | Returns documentation for input item           |
| python uwvp.py | url | --info           |                                 | Returns information about page                 |
| python uwvp.py | url | -n | -name       | custom_name                     | Changes the name of the output media file      |
| python uwvp.py | url | -p | -path       | custom_path                     | Changes the path of the output media file      |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+

Command -o works with {str(opt_able_sites)[1:-1]} links:
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python uwvp.py | url | -o | -option     | video_only | audio_only         | Removes audio or video from output media file  |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+

Command -r works with {str(res_able_sites)[1:-1]} links:
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
| python uwvp.py | url | -r | -resolution | 144p | 240p | .... | 2160p      | Changes resolution of the output media file    |
+----------------+-----+------------------+---------------------------------+------------------------------------------------+
'''

def docs(docs_dict, site):
    try:
        print(docs_dict[site])
    except KeyError:
        print(f"No supported site called {site}")

def get_url_info(url):
    string = f"print({url_type}_info('{url}'))"
    exec(string)
    sys.exit()

def downloader(url, opts):
    if url_check(url):
        string = f"{url_type}_downloader('{url}',{opts})"
        exec(string)

def main(docs_dict, url_type):
    cmd = sys.argv

    if len(cmd) > 1:

        if cmd[1] == '--help':
            if len(cmd) > 2:
                return docs(docs_dict, cmd[2])
            else:
                return docs(docs_dict, 'all')
        
        elif url_check(cmd[1]):
            opts = {'video_only': False,
                    'audio_only': False,
                    'resolution': "best",
                    'name': None,
                    'path': None
                    }
            ignore_element = False
            option_flag = False
            resolution_flag = False
            name_flag = False
            path_flag = False

            if len(cmd) > 2:

                for i in range(2, len(cmd)):

                    if ignore_element:
                        ignore_element = False
                        pass

                    elif cmd[i] == '--info':
                        if len(cmd) > 3:
                            print("WARNING: commands after --info will be ignored")
                        print(get_url_info(cmd[1]))

                    elif cmd[i] == '-o' or cmd[i] == '-option':
                        if option_flag:
                            print("WARNING: other -o (-option) commands will be ignored")
                            ignore_element = True

                        elif len(cmd) > i+1:
                            if cmd[i+1] == 'video_only':
                                opts['video_only'] = True
                            elif cmd[i+1] == 'audio_only':
                                opts['audio_only'] = True
                            else:
                                print(f"ERROR: -o (-option) command don't have {cmd[i]} argument")
                                sys.exit()

                            option_flag = True
                            ignore_element = True
                        
                        else:
                            print("ERROR: No arguments after -o (-option) command")

                    elif cmd[i] == '-r' or cmd[i] == '-resolution':
                        if resolution_flag:
                            print("WARNING: other -r (-resolution) commands will be ignored")
                            ignore_element = True

                        elif len(cmd) > i+1:
                            opts['resolution'] = cmd[i+1]
                            resolution_flag = True
                            ignore_element = True

                        else:
                            print("ERROR: No arguments after -r (-resolution) command")
                            sys.exit()
                    
                    elif cmd[i] == '-n' or cmd[i] == '-name':
                        if name_flag:
                            print("WARNING: other -n (-name) commands will be ignored")
                            ignore_element = True

                        elif len(cmd) > i+1:
                            opts['name'] = cmd[i+1]
                            name_flag = True
                            ignore_element = True

                        else:
                            print("ERROR: No arguments after -n (-name) command")
                            sys.exit()
                    
                    elif cmd[i] == '-p' or cmd[i] == '-path':
                        if path_flag:
                            print("WARNING: other -p (-path) commands will be ignored")
                            ignore_element = True

                        elif len(cmd) > i+1:
                            opts['path'] = cmd[i+1]
                            path_flag = True
                            ignore_element = True

                        else:
                            print("ERROR: No arguments after -p (-path) command")
                            sys.exit()

                    else:
                        print(f"ERROR: No command called {cmd[i]}")
                        sys.exit()
                
            return downloader(cmd[1], opts)

    else:
        print("ERROR: Got no arguments")
        sys.exit()


if __name__ == '__main__':
    main(docs_by_module, url_type)