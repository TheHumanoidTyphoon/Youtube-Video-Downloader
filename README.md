# YouTube Downloader
This Python class enables users to download videos from YouTube, providing access to both audio and video streams. Additionally, it offers a convenient progress bar for monitoring video downloads. Whether you need to download an entire video or just the audio, this class simplifies the process and makes it more accessible for developers looking to incorporate video downloading capabilities into their projects.

## Installation
This program requires Python 3.x and the following packages:

- `pytube`
- `tqdm`
- `rich` 

To install the packages, run the following command in your terminal:
``` python
pip install pytube tqdm rich
```

## Usage
1. Import the `YouTubeDownloader` class from the module:
```python
from youtube_downloader import YouTubeDownloader
```

2. Create an instance of the `YouTubeDownloader` class by passing in a list of video URLs:
```python
downloader = YouTubeDownloader(["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=Kp7eSUU9oy8"])
```

3. Call the `download_videos()` method to download the videos:
```python
downloader.download_videos()
```

When prompted, you can choose to download only the audio portion of a video. The program will display available audio and video streams and allow you to select the desired stream to download. The video download will be displayed with a progress bar.

## Example

```python
from youtube_downloader import YouTubeDownloader

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
