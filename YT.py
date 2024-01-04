from pytube import YouTube
from tqdm import tqdm
import os
import subprocess
import sys

# Initialize the progress bar
pbar = None

# Callback function for the progress bar
def progress_bar_func(stream, chunk, bytes_remaining):
    global pbar
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pbar.update(bytes_downloaded - pbar.n)

# Download function
def download(uservideo, u_video):
    global pbar
    video = u_video
    default_c = None

    # Prompt the user to select a stream
    try:
        yt = YouTube(uservideo, on_progress_callback=progress_bar_func)

    # Prompt the user to select a stream
        # If u_video is y then print the video streams
        if video == 'y':
            # Check if 1080p is available
            if yt.streams.get_by_itag(137) is not None:
                print('1080p available ; tag 137')
                default_c = 137
            else:
                print('1080p unavailable')
            print(yt.streams.filter(only_video=True))
        # If u_video is n then print the audio streams
        elif video == 'n':
            # Check for the highest quality audio stream
            if yt.streams.get_by_itag(251) is not None:
                print('Highest quality audio available ; tag 251')
                default_c = 251
            print(yt.streams.filter(only_audio=True))
        # If u_video is None then print both the video and audio streams and check if 1080p is available
        else:
            # Check if 1080p is available
            if yt.streams.get_by_itag(137) is not None:
                print('1080p available ; tag 137')
                default_c = 137
            else:
                print('1080p unavailable')
            print(yt.streams.filter(file_extension='mp4'))
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
    # Prompt the user to select a stream
    try:
        streamchoice = int(input('streamid: '))
    # If the user does not select a stream then use the default_c
    except Exception as e:
        #! Check if default_c is set if yes then use it else exit
        if default_c is None:
            print(f"An error occurred: {e}")
            sys.exit()
        else:
            streamchoice = default_c
            print('Used default_c')
    # Get the stream by the itag
    stream = yt.streams.get_by_itag(streamchoice)

    # Prompt the user to download video or audio
    if video is None:
        if streamchoice == 251:
            video = 'n'
        elif streamchoice == 137:
            video = 'y'
        else:
            video = input('Video? y/n: ')

    # Download the audio file
    if video == 'n':
        audio_filename = 'audio_' + stream.default_filename
        # Create the progress bar
        pbar = tqdm(total=stream.filesize, unit='B', unit_scale=True)
        stream.download(filename_prefix='audio_')
        pbar.close()
        return audio_filename

    # Download the video file
    else:
        # Create the progress bar
        pbar = tqdm(total=stream.filesize, unit='B', unit_scale=True)
        stream.download()
        pbar.close()
        return stream.default_filename

# Merge video and audio (optional)
def merge(video, audio):
    input_video = video
    input_audio = audio
    output_video = input('Output put.mp4 at the end: ')

    # Prompt the user to specify the output file name
    if output_video == '':
        output_video = 'ouput_'+video

    # Run the ffmpeg command to merge the files
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

# Delete a file
def delteFile(filename):
    current_directory = os.getcwd()
    file_name = filename
    file_path = os.path.join(current_directory, file_name)

    # Check if the file exists and delete it
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print(f"{file_name} has been deleted.")
    else:
        print(f"{file_name} does not exist in the current directory.")

# Main function
video = None
uservideo = input('YT link: ')
function_output = download(uservideo, video)
# Prompt the user to continue
u_continue = input('Do you want to continue? y/n: ')
if u_continue == 'y':
    u_video = None
    u_audio = None
    # Check if the downloaded file is audio or video
    if 'audio_' in function_output:
        video = 'y'
        u_audio = function_output
        u_video = download(uservideo, video)
    else:
        video = 'n'
        u_video = function_output
        u_audio = download(uservideo, video)
    # Merge the video and audio files
    merge(u_video, u_audio)
    # Prompt the user to delete the separate video and audio files
    u_delete = input('Do you want to delte the subfiles? y/n: ')
    if u_delete == 'y':
        delteFile(u_audio)
        delteFile(u_video)
