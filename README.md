# YouTube Downloader
A Python class that allows users to download YouTube videos. The class can download both video and audio streams of a video, and provides a progress bar for video downloads.

## Installation
This program requires Python 3.x and the following packages:

- pytube
- tqdm
- rich
To install the packages, run the following command in your terminal:
``` python
pip install pytube tqdm rich
```

## Usage
1. Import the YouTubeDownloader class from the module:
from youtube_downloader import YouTubeDownloader

2. Create an instance of the YouTubeDownloader class by passing in a list of video URLs:
downloader = YouTubeDownloader(["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=Kp7eSUU9oy8"])

3. Call the download_videos() method to download the videos:
downloader.download_videos()

When prompted, you can choose to download only the audio portion of a video. The program will display available audio and video streams and allow you to select the desired stream to download. The video download will be displayed with a progress bar.

## Example

from youtube_downloader import YouTubeDownloader

```python
# Example video URLs
video_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=Kp7eSUU9oy8"
]

# Create a YouTubeDownloader instance
downloader = YouTubeDownloader(video_urls)

# Download the videos
downloader.download_videos()
```

## License
This project is licensed under the MIT License - see the [LICENSE]() file for details.
