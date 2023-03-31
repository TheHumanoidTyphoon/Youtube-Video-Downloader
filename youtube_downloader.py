import pytube
import os
import sys
import datetime 
from tqdm import tqdm
from rich.console import Console

console = Console()
class YouTubeDownloader:
    """
    A class to download YouTube videos.

    Attributes:
    -----------
    video_urls : list of str
        List of YouTube video URLs to be downloaded.

    Methods:
    --------
    download_videos()
        Downloads the videos specified in video_urls.
    _download_audio(yt)
        Downloads only the audio portion of a YouTube video.
    _download_video(yt)
        Downloads the video stream of a YouTube video.
    _print_available_streams(streams)
        Prints the available audio and video streams of a YouTube video.
    """
    def __init__(self, video_urls):
        """
        Constructs all the necessary attributes for the YouTubeDownloader object.

        Parameters:
        -----------
        video_urls : list of str
            List of YouTube video URLs to be downloaded.
        """
        self.video_urls = video_urls
    
    def download_videos(self):
        """
        Downloads the videos specified in video_urls.
        """
        for video_url in self.video_urls:
            try:
                yt = pytube.YouTube(video_url)
                self._download_audio(yt)
                self._download_video(yt)
            except pytube.exceptions.VideoUnavailable:
                console.print(f"[bold red]Download failed: Video is unavailable or has been removed.[/bold red]")
            except Exception as e:
                console.print(f"[bold red]Download failed:[/bold red] {e}")
    
    def _download_audio(self, yt):
        """
        Downloads only the audio portion of a YouTube video.

        Parameters:
        -----------
        yt : pytube.YouTube object
            YouTube video object.

        Returns:
        --------
        None
        """
        while True:
            audio_choice = console.input("\n[bold magenta]Do you want to download only the audio portion of the video[/bold magenta] ([bold green]yes[/bold green]/[bold blue]no[/bold blue])? ").lower()
            if audio_choice == "yes":
                audio_streams = yt.streams.filter(only_audio=True)
                self._print_available_streams(audio_streams)
                audio_choice = console.input("\n[bold magenta]Enter the number of the audio stream you want to download:[/bold magenta] ")
                try:
                    audio_choice = int(audio_choice)
                except ValueError:
                    console.print("[bold red]Invalid choice. Please enter a number.[/bold red]")
                    continue
                if audio_choice < 1 or audio_choice > len(audio_streams):
                    console.print("[bold red]Invalid choice. Please try again.[/bold red]")
                    continue
                audio_stream = audio_streams[audio_choice-1]
                try:
                    audio_file = audio_stream.download()
                except Exception as e:
                    console.print(f"[bold red]Download failed:[/bold red] {e}")
                    return
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_file_name = os.path.splitext(audio_file)[0] + "_" + timestamp + ".mp3"
                try:
                    os.rename(audio_file, audio_file_name)
                except FileNotFoundError:
                    console.print(f"[bold red]Failed to rename file: {audio_file} does not exist.[/bold red]")
                    return
                console.print("[bold green]Audio download successful![/bold green]")
                sys.exit() # Stop the program here
            elif audio_choice == "no":
                break
            else:
                console.print("[bold red]Invalid choice. Please try again.[/bold red]")
    
    def _download_video(self, yt):
        """
        Downloads the YouTube video and displays a progress bar.

        Parameters:
        -----------
        yt : pytube.YouTube
            An instance of the pytube.YouTube class representing the video to be downloaded.
        """
        try:
            streams = yt.streams.filter(progressive=True).order_by('resolution')
            self._print_available_streams(streams)
            while True:
                choice = int(console.input("\n[bold magenta]Enter the number of the stream you want to download:[/bold magenta] "))
                if choice < 1 or choice > len(streams):
                    console.print("[bold red]Invalid choice. Please try again.[/bold red]")
                else:
                    stream = streams[choice-1]
                    break
            video_file = stream.download()
        except Exception as e:
            console.print("[bold red]Error occurred while selecting/downloading stream:[/bold red]")
            console.print(str(e))
            return
        
        try:
            # add progress bar
            file_size = os.path.getsize(video_file)
            with open(video_file, 'rb') as f:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=video_file, ascii=True) as progress_bar:
                    while True:
                        buffer = f.read(1024 * 1024)
                        if not buffer:
                            break
                        progress_bar.update(len(buffer))
            console.print("\n[bold green]Download successful![/bold green]")
        except Exception as e:
            console.print("[bold red]Error occurred while displaying progress bar:[/bold red]")
            console.print(str(e))

    
    def _print_available_streams(self, streams):
        """
        Prints the available video and audio streams of the YouTube video.

        Parameters:
        -----------
        streams : list of pytube.Stream
            List of video and audio streams of the YouTube video.
        """
        try:
            console.print("\n[bold blue]Available streams:[/bold blue]\n")
            for i, stream in enumerate(streams):
                if stream.type == "video":
                    console.print(f"[bold yellow]{i+1}.[/bold yellow] [bold green]{stream.resolution}[/bold green]")
                elif stream.type == "audio":
                    console.print(f"[bold yellow]{i+1}.[/bold yellow ][bold green]{stream.abr}[/bold green] [bold blue]({stream.mime_type.split('/')[1]})[/bold blue]")
        except Exception as e:
            console.print("[bold red]Error occurred while printing available streams:[/bold red]")
            console.print(str(e))


def get_video_urls():
    """
    Prompts the user to enter YouTube video URLs and returns a list of valid URLs.

    Returns:
    --------
    list of str
        List of valid YouTube video URLs entered by the user.
    """
    video_urls = []
    while True:
        try:
            video_url = console.input("[bold yellow]Enter a YouTube video's URL (e.g.[/bold yellow] https://youtu.be/dQw4w9WgXcQ), [bold yellow]or type[/bold yellow] 'done' [bold yellow]when finished:[/bold yellow] ")
            if video_url.lower() == 'done':
                break
            if "youtube.com" in video_url or "youtu.be" in video_url:
                video_urls.append(video_url)
            else:
                console.print("[bold red]Please enter a valid YouTube video URL.[/bold red]")
        except Exception as e:
            console.print("[bold red]Error occurred while getting video URL:[/bold red]")
            console.print(str(e))
    return video_urls


if __name__ == "__main__":
    try:
        video_urls = get_video_urls()
        downloader = YouTubeDownloader(video_urls)
        downloader.download_videos()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]KeyboardInterrupt: Program terminated.[/bold red]")
        sys.exit()








