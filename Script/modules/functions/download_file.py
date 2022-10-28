from sys import stdout
import requests
import os
from threading import Thread
import time
from pytube import Stream
import platform

def download_file(link, path, name, format):
    def animating_download(file_size_in_bytes, name, path, format):
        # define file size in B,KB,MB,GB
        if file_size_in_bytes >= 1073741824:
            file_size = f'{round(file_size_in_bytes/1073741824, 2)}GB'
        elif file_size_in_bytes >= 1048576:
            file_size = f'{round(file_size_in_bytes/1048576, 2)}MB'
        elif file_size_in_bytes >= 1024:
            file_size = f'{round(file_size_in_bytes/1024, 2)}KB'
        else:
            file_size = f'{file_size_in_bytes}B'
        
        # define some default values
        list_of_download_speed = [0, 0, 0, 0]
        list_of_end_time = [0, 0, 0, 0]
        half_sec_counter = 0
        previous_downloaded_file_size_in_bytes = 0
        previous_frame = ''

        # clear func
        if platform.system() == "Windows":
            clear = lambda : os.system('cls')
        else:
            clear = lambda : os.system('clear')

        # animate download
        while True:
            if half_sec_counter == 4:
                half_sec_counter = 0
            
            # get downloaded file size
            try:
                downloaded_file_size_in_bytes = os.path.getsize(f'{path}/{name}{format}'.replace('/', os.sep))
            except:
                break

            # define file size in B,KB,MB,GB
            if downloaded_file_size_in_bytes >= 1073741824:
                downloaded_file_size = f'{round(downloaded_file_size_in_bytes/1073741824, 2)}GB'
            elif downloaded_file_size_in_bytes >= 1048576:
                downloaded_file_size = f'{round(downloaded_file_size_in_bytes/1048576, 2)}MB'
            elif downloaded_file_size_in_bytes >= 1024:
                downloaded_file_size = f'{round(downloaded_file_size_in_bytes/1024, 2)}KB'
            else:
                downloaded_file_size = f'{downloaded_file_size_in_bytes}B'
            
            # define visual ratio between downloaded file size and final file size
            for i in range(26):
                if downloaded_file_size_in_bytes >= file_size_in_bytes//25*(25-i):
                    percentage_frame = '░'*(25-i)
                    while len(percentage_frame) < 25:
                        percentage_frame = percentage_frame + ' '
                    percentage_frame = '|' + percentage_frame + '|'
                    break

            # define completed part of download in percents
            percentage = round(downloaded_file_size_in_bytes/file_size_in_bytes*100, 1)

            # define download speed
            list_of_download_speed[half_sec_counter] = downloaded_file_size_in_bytes - previous_downloaded_file_size_in_bytes
            average_download_speed_in_bytes = sum(list_of_download_speed)//2
            if average_download_speed_in_bytes >= 1048576:
                download_speed = f'{round(average_download_speed_in_bytes/1048576, 2)}mbps'
            elif average_download_speed_in_bytes >= 1024:
                download_speed = f'{round(average_download_speed_in_bytes/1024)}kbps'
            else:
                download_speed = f'{average_download_speed_in_bytes}bps'
            previous_downloaded_file_size_in_bytes = downloaded_file_size_in_bytes

            # define time until the end of download
            list_of_end_time[half_sec_counter] = (file_size_in_bytes-downloaded_file_size_in_bytes)//(average_download_speed_in_bytes+0.00000000001)
            average_end_time_in_sec = sum(list_of_end_time)//4
            if average_end_time_in_sec >= 604800:
                end_time = '∞'
            elif average_end_time_in_sec >= 86400:
                end_time = f'{round(average_end_time_in_sec/86400)}dys'
            elif average_end_time_in_sec >= 3600:
                end_time = f'{round(average_end_time_in_sec/86400)}hrs'
            elif average_end_time_in_sec >= 60:
                end_time = f'{round(average_end_time_in_sec/60)}min'
            else:
                end_time = f'{round(average_end_time_in_sec)}sec'
            

            # output data into console every half a second
            next_frame = f'\rDownloading {name}{format} {percentage_frame} {percentage}% | {downloaded_file_size}/{file_size} | {download_speed} | {end_time}'
            if len(next_frame) < len(previous_frame):
                next_frame += ' '*(len(previous_frame)-len(next_frame))
            stdout.write(next_frame)
            stdout.flush()
            previous_frame = next_frame

            # stops animating if file is downloaded
            if downloaded_file_size_in_bytes == file_size_in_bytes:
                break

            # sleep for half a second
            time.sleep(0.5)
            half_sec_counter += 1
        
        # warn about download complete
        clear()
        stdout.write('\rDownload complete!')
        stdout.flush()

    def download_file(link, name, path, format):
        # open file with appending bytes option
        with open(f'{path}/{name}{format}'.replace('/', os.sep), 'ab') as file:
            response = requests.get(link, stream = True)

            # write new data into file every 1024 loaded bytes
            for chunk in response.iter_content(1024):
                file.write(chunk)

    # get file size from url adress headers
    file_size_in_bytes = int(requests.head(link).headers['content-length'])

    # create threads for animating and downloading
    downloading_thread = Thread(target= download_file, args=(link, name, path, format))
    animating_thread = Thread(target= animating_download, args=(file_size_in_bytes, name, path, format))

    # create file and start threads
    open(f'{path}/{name}{format}'.replace('/', os.sep), 'x').close()
    downloading_thread.start()
    animating_thread.start()


def download_file_from_stream(stream, path, name):
    def animating_download_from_stream(stream: Stream, path, name):
        # get file size from stream
        file_size_in_bytes = stream.filesize

        # define file size in B,KB,MB,GB
        if file_size_in_bytes >= 1073741824:
            file_size = f'{round(file_size_in_bytes/1073741824, 2)}GB'
        elif file_size_in_bytes >= 1048576:
            file_size = f'{round(file_size_in_bytes/1048576, 2)}MB'
        elif file_size_in_bytes >= 1024:
            file_size = f'{round(file_size_in_bytes/1024, 2)}KB'
        else:
            file_size = f'{file_size_in_bytes}B'
        
        # define some default values
        list_of_download_speed = [0, 0, 0, 0]
        list_of_end_time = [0, 0, 0, 0]
        half_sec_counter = 0
        previous_downloaded_file_size_in_bytes = 0
        previous_frame = ''

        # clear func
        if platform.system() == "Windows":
            clear = lambda : os.system('cls')
        else:
            clear = lambda : os.system('clear')

        # animate download
        while True:
            if half_sec_counter == 4:
                half_sec_counter = 0
            
            # get downloaded file size
            try:
                downloaded_file_size_in_bytes = os.path.getsize(f'{path}/{name}'.replace('/', os.sep))
            except:
                break

            # define file size in B,KB,MB,GB
            if downloaded_file_size_in_bytes >= 1073741824:
                downloaded_file_size = f'{round(downloaded_file_size_in_bytes/1073741824, 2)}GB'
            elif downloaded_file_size_in_bytes >= 1048576:
                downloaded_file_size = f'{round(downloaded_file_size_in_bytes/1048576, 2)}MB'
            elif downloaded_file_size_in_bytes >= 1024:
                downloaded_file_size = f'{round(downloaded_file_size_in_bytes/1024, 2)}KB'
            else:
                downloaded_file_size = f'{downloaded_file_size_in_bytes}B'
            
            # define visual ratio between downloaded file size and final file size
            for i in range(26):
                if downloaded_file_size_in_bytes >= file_size_in_bytes//25*(25-i):
                    percentage_frame = '░'*(25-i)
                    while len(percentage_frame) < 25:
                        percentage_frame = percentage_frame + ' '
                    percentage_frame = '|' + percentage_frame + '|'
                    break

            # define completed part of download in percents
            percentage = round(downloaded_file_size_in_bytes/file_size_in_bytes*100, 1)

            # define download speed
            list_of_download_speed[half_sec_counter] = downloaded_file_size_in_bytes - previous_downloaded_file_size_in_bytes
            average_download_speed_in_bytes = sum(list_of_download_speed)//2
            if average_download_speed_in_bytes >= 1048576:
                download_speed = f'{round(average_download_speed_in_bytes/1048576, 2)}mbps'
            elif average_download_speed_in_bytes >= 1024:
                download_speed = f'{round(average_download_speed_in_bytes/1024)}kbps'
            else:
                download_speed = f'{average_download_speed_in_bytes}bps'
            previous_downloaded_file_size_in_bytes = downloaded_file_size_in_bytes

            # define time until the end of download
            end_time_in_sec = (file_size_in_bytes-downloaded_file_size_in_bytes)//(average_download_speed_in_bytes+0.00000000001)
            if end_time_in_sec >= 604800:
                end_time = '∞'
            elif end_time_in_sec >= 86400:
                end_time = f'{round(end_time_in_sec/86400)}dys'
            elif end_time_in_sec >= 3600:
                end_time = f'{round(end_time_in_sec/86400)}hrs'
            elif end_time_in_sec >= 60:
                end_time = f'{round(end_time_in_sec/60)}min'
            else:
                end_time = f'{round(end_time_in_sec)}sec'

            # output data into console every half a second
            next_frame = f'\rDownloading {name} {percentage_frame} {percentage}% | {downloaded_file_size}/{file_size} | {download_speed} | {end_time}'
            if len(next_frame) < len(previous_frame):
                next_frame += ' '*(len(previous_frame)-len(next_frame))
            stdout.write(next_frame)
            stdout.flush()
            previous_frame = next_frame

            # stops animating if file is downloaded
            if downloaded_file_size_in_bytes == file_size_in_bytes:
                break

            # sleep for half a second
            time.sleep(0.5)
            half_sec_counter += 1

        clear()

    def download_file_from_stream(stream: Stream, path, name):
        stream.download(output_path= path, filename= name)

    # create threads for animating and downloading
    downloading_thread = Thread(target= download_file_from_stream, args=(stream, path, name))
    animating_thread = Thread(target= animating_download_from_stream, args=(stream, path, name))

    # create file and start threads
    open(f'{path}/{name}'.replace('/', os.sep), 'x').close()
    downloading_thread.start()
    animating_thread.start()  