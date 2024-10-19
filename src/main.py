import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
from dotenv import load_dotenv
from youtube import getClip
from datetime import datetime
import os

from spotify import search_playlists_by_keyword, get_songs_by_category


def main():
    # Load environment variables from the .env file
    load_dotenv()

    CATEGORY_SIZE = int(sys.argv[1])
    MIN_POPULARITY = int(sys.argv[2])
    KEYWORDS = " ".join(
        sys.argv[3:]
    )  # We allow spaces for keywords (ex : for artists its easier => Ed Sheeran)

    # Configure authentication information
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET")
    )

    # Get the spotipy client
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Use the function with exclusion of certain keywords
    playlist = search_playlists_by_keyword(client=sp, keywords=f" best {KEYWORDS}")

    # Retrieve the songs of the playlist
    songs = sp.playlist_items(playlist["id"])

    selected_songs = get_songs_by_category(
        songs["items"], MIN_POPULARITY, CATEGORY_SIZE
    )

    # Get the clip of each songs selected

    directory = datetime.now().strftime("%d-%m-%Y")
    for song in selected_songs:
        print(song["name"])
        print(song["artists"])
        getClip(song["name"], song["artists"][0]["name"], directory)


# Check if the script is executed directly (rather than being imported as a module)
if __name__ == "__main__":
    # Call the main function if the script is executed directly
    main()
