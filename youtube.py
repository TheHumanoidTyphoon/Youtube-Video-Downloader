from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import random
import requests
import subprocess
from tqdm import tqdm
import threading
import datetime
import dailymotion
from vimeo import VimeoClient


# Define a list of user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.54',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39'
]


def choose_video_quality(streams):
    video_streams = [s for s in streams if s.mime_type.startswith('video/')]
    audio_streams = [s for s in streams if s.mime_type.startswith('audio/')]

    while True:
        choice = input(
            "Would you like to download only video, only audio, or both video and audio? (video/audio/both): ")
        if choice.lower() == "video":
            print("\nAvailable video quality options:\n")
            for i, stream in enumerate(video_streams):
                print(f"  {i+1}. Resolution: {stream.resolution}")
            while True:
                video_choice = input(
                    "\nChoose the number corresponding to the video quality you want to download:")
                try:
                    video_choice = int(video_choice)
                    if video_choice >= 1 and video_choice <= len(video_streams):
                        return video_streams[video_choice-1]
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid choice. Please try again.")
        elif choice.lower() == "audio":
            print("\nAvailable audio quality options:\n")
            for i, stream in enumerate(audio_streams):
                print(f"  {i+1}. Bitrate: {stream.abr} kbps")
            while True:
                audio_choice = input(
                    "\nChoose the number corresponding to the audio quality you want to download:")
                try:
                    audio_choice = int(audio_choice)
                    if audio_choice >= 1 and audio_choice <= len(audio_streams):
                        return audio_streams[audio_choice-1]
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid choice. Please try again.")
        elif choice.lower() == "both":
            print("\nAvailable video and audio quality options:\n")
            for i, stream in enumerate(streams):
                if stream in video_streams:
                    stream_info = f"Resolution: {stream.resolution}"
                else:
                    stream_info = f"Bitrate: {stream.abr} kbps"
                print(f"  {i+1}. {stream_info}, Format: {stream.mime_type}")
            while True:
                both_choice = input(
                    "\nChoose the number corresponding to the video/audio quality you want to download:")
                try:
                    both_choice = int(both_choice)
                    if both_choice >= 1 and both_choice <= len(streams):
                        return streams[both_choice-1]
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid choice. Please try again.")


def get_download_location():
    download_location = input("Enter the download location: ")
    return download_location


def download_multiple_videos(links):
    try:
        total_size = 0
        streams = []
        threads = []
        download_location = get_download_location()
        for link in links:
            try:
                if "dailymotion.com" in link:
                    video_id = link.split("/")[-1]
                    api = dailymotion.Dailymotion()
                    api_url = f"https://api.dailymotion.com/video/{video_id}?fields=url"
                    response = api.get(api_url)
                    url = response['url']
                elif "vimeo.com" in link:
                    video_id = link.split("/")[-1]
                    v = VimeoClient(token='YOUR_ACCESS_TOKEN')
                    video = v.get(f'/videos/{video_id}')
                    url = video.files[-1]['link']
                else:
                    yt = YouTube(link)
                    url = yt.streams.filter(file_extension='mp4')[0].url
                r = requests.head(
                    url, headers={'User-Agent': random.choice(user_agents)})
                size = int(r.headers.get('Content-Length', 0))
                total_size += size
                stream = {'url': url, 'filesize': size}
                # Store the chosen stream in the list
                streams.append(stream)
            except VideoUnavailable:
                print(f"Error: Video at {link} is not available")
                continue

        total_downloaded = 0
        for i, link in enumerate(links):
            if "dailymotion.com" in link:
                video_id = link.split("/")[-1]
                chosen_stream = {'url': url, 'filesize': 0}
            elif "vimeo.com" in link:
                video_id = link.split("/")[-1]
                chosen_stream = {'url': url, 'filesize': 0}
            else:
                chosen_stream = choose_video_quality(
                    yt.streams.filter(file_extension='mp4'))

            thread = threading.Thread(target=download_video, args=(
                link, i+1, chosen_stream, download_location))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("\nDownload complete!")
    except KeyboardInterrupt:
        print("\nDownloads interrupted by user.")


def download_video(link, num_videos, chosen_stream, download_location):
    try:
        num_videos += 1
        extension = chosen_stream.mime_type.split('/')[-1]
        if 'audio' in chosen_stream.mime_type:
            filename = f'audio{num_videos}.{extension}'
        elif 'video' in chosen_stream.mime_type:
            filename = f'video{num_videos}.{extension}'
        else:
            filename = f'file{num_videos}.{extension}'

        yt = YouTube(link)
        file_size = chosen_stream.filesize
        if file_size < 1024*1024:  # Check if file size is less than 1 MB
            print(f"Downloading {filename}...")
            chosen_stream.download(
                output_path=download_location, filename=filename)
            print(f"Downloaded {filename} successfully.")
        else:
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
            yt.register_on_progress_callback(
                lambda chunk, fh, bytes_remaining: progress_bar.update(file_size - bytes_remaining))
            chosen_stream.download(
                output_path=download_location, filename=filename)
            progress_bar.close()
            print(f"\nDownloaded {filename} successfully.")

        # Check if the video has subtitles
        caption = yt.captions['en']
        if caption:
            caption_file = f"{download_location}/{filename.split('.')[0]}.srt"
            print(f"Downloading subtitles for {filename}...")
            with open(caption_file, "w", encoding='utf-8') as f:
                f.write(caption.generate_srt_captions())
            print(f"Downloaded subtitles for {filename} successfully.")

        # Convert the downloaded video to other formats using FFmpeg
        if extension == 'mp4':
            output_format = 'mp3'
        elif extension == 'webm':
            output_format = 'avi'
        else:
            return True

        input_file = f"{download_location}/{filename}"
        output_file = f"{download_location}/{filename.split('.')[0]}.{output_format}"
        command = f"ffmpeg -i \"{input_file}\" \"{output_file}\""
        subprocess.call(command, shell=True)
        print(f"Converted {filename} to {output_format} successfully.")

        return True
    except VideoUnavailable:
        error_msg = f"Error: Video at {link} is not available"
        print(error_msg)
        log_error(error_msg)
    except Exception as e:
        error_msg = f"Error downloading video at {link}: {str(e)}"
        print(error_msg)
        log_error(error_msg)
    return False


def log_error(error_msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error.log", "a") as f:
        f.write(f"[{timestamp}] {error_msg}\n")


if __name__ == '__main__':
    links = input("""Please provide a list of video URLs separated by commas, 
or enter a single video URL from YouTube, Vimeo, or Dailymotion: """).split(',')
    download_multiple_videos(links)

