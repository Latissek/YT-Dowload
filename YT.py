#Need FFMPEG and pytube | pip install pytube , does not work on non-own private videos on own put ,use_oauth=True, allow_oauth_cache=True on line 10
from pytube import YouTube
from tqdm import tqdm
import os
import subprocess
pbar = None

def progress_bar_func(stream, chunk, bytes_remaining):
    global pbar
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pbar.update(bytes_downloaded - pbar.n)

##Download function, self asking, if called again it will add/dont_add the audio prefix
def download(uservideo, u_video):
    global pbar
    video = u_video
    yt = YouTube(uservideo, on_progress_callback=progress_bar_func)
    print(yt.streams.filter(file_extension='mp4'))
    streamchoice = int(input('streamid: '))
    stream = yt.streams.get_by_itag(streamchoice)
    if video is None:
        video = input('Video? y/n: ')
    if video == 'n':
        audio_filename = 'audio_' + stream.default_filename
        # Create the progress bar
        pbar = tqdm(total=stream.filesize, unit='B', unit_scale=True)
        stream.download(filename_prefix='audio_')
        pbar.close()
        return audio_filename
    else:
        # Create the progress bar
        pbar = tqdm(total=stream.filesize, unit='B', unit_scale=True)
        stream.download()
        pbar.close()
        return stream.default_filename

## Merge video and audio (optional)
def merge(video, audio):
    input_video = video
    input_audio = audio
    output_video = input('Output put.mp4 at the end: ')
    
    if output_video == '':
        output_video = 'o_'+video
    
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-i', input_audio,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_video
    ]
    subprocess.run(cmd)

def delteFile(filename):
    current_directory = os.getcwd()
    file_name = filename
    file_path = os.path.join(current_directory, file_name)
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print(f"{file_name} has been deleted.")
    else:
        print(f"{file_name} does not exist in the current directory.")

#main
video = None
uservideo = input('YT link: ')
function_output = download(uservideo,video)
u_continue = input('Do you want to continue? y/n: ')
if u_continue == 'y':
    u_video = None
    u_audio = None
    if 'audio_' in function_output:
        video = 'y'
        u_audio = function_output
        u_video = download(uservideo,video)
    else:
        video = 'n'
        u_video = function_output
        u_audio = download(uservideo,video)
    merge(u_video, u_audio)
    u_delete = input('Do you want to delte the subfiles? y/n: ')
    if u_delete == 'y':
        delteFile(u_audio)
        delteFile(u_video)
