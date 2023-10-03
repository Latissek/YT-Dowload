#Need FFMPEG and pytube | pip install pytube , does not work on non-own private videos on own put ,use_oauth=True, allow_oauth_cache=True on line 10
from pytube import YouTube
import subprocess
##Global variable


##Download function, self asking, if called again it will add/dont_add the audio prefix
def download(uservideo, u_video):
    video = u_video
    yt = YouTube(uservideo)
    print(yt.streams.filter(file_extension='mp4'))
    streamchoise = int(input('steamid: '))
    stream = yt.streams.get_by_itag(streamchoise)
    if video is None:
        video = input('Video? y/n: ')
    if video == 'n':
        stream.download(filename_prefix='audio_')
        return 'audio_'+stream.default_filename
    else:
        
        stream.download()
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