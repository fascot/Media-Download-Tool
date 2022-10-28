from sys import stdout
from time import sleep
import os
import platform


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
                     ██▄,,,,,,▄██
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