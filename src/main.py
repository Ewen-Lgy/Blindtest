"""
Main script to load environment variables and process command-line arguments.
"""

import os
import sys
from datetime import datetime

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

from spotify import get_songs_by_category, search_playlists_by_keyword
from youtube import get_clip


def main():
    """
    Main function
    """
    # Load environment variables from the .env file
    load_dotenv()

    category_size = int(sys.argv[1])
    min_popularity = int(sys.argv[2])
    keywords = " ".join(
        sys.argv[3:]
    )  # We allow spaces for keywords (ex : for artists its easier => Ed Sheeran)

    # Configure authentication information
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET")
    )

    # Get the spotipy client
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Use the function with exclusion of certain keywords
    playlist = search_playlists_by_keyword(client=sp, keywords=f" best {keywords}")

    # Retrieve the songs of the playlist
    songs = sp.playlist_items(playlist["id"])

    selected_songs = get_songs_by_category(
        songs["items"], min_popularity, category_size
    )

    # Get the clip of each songs selected

    directory = datetime.now().strftime("%d-%m-%Y")
    for song in selected_songs:
        print(song["name"])
        print(song["artists"])
        get_clip(song["name"], song["artists"][0]["name"], directory)


# Check if the script is executed directly (rather than being imported as a module)
if __name__ == "__main__":
    # Call the main function if the script is executed directly
    main()
