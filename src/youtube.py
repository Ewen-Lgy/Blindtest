"""
Module that deals with youtube API
"""

from __future__ import unicode_literals

import yt_dlp


def get_clip(title: str, artist: str, output_directory: str):
    """
    Retrieve the youtube video clip of the song of an artist
    and storing it in the specified location.

    Parameters:
        title: Title of the song
        artist: Name of the artist
        output_directory: Path to the location of the video clip
    """
    options = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"download_output/{output_directory}/{title} - {artist}.%(ext)s",
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            ydl.download([f"ytsearch1:{title} {artist} music video official"])
        except yt_dlp.utils.ExtractorError as e:
            print(f"Error extracting information: {e}")
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading video: {e}")
