"""
Module that deals with call of spotify api
"""

import random
from operator import itemgetter

import numpy as np


def search_playlists_by_keyword(client, keywords: str):
    """
    Make a request to find a playlist given a string of keywords. Also, a list of excluded keywords
    is used to remove playlists with these exluded keywords in its name.

    Parameters:
        client: Spotify client to make the request to
        keywords: string of keywords to lookup for in the playlist name

    Returns a random playlist from the sublist of playlist
    """
    exclude_keywords = ["serie", "films", "disney", "jeux-videos", "culte", "cinema"]

    # Search for playlists by keyword
    playlists = client.search(q=keywords, type="playlist", limit=10)
    filtered_playlists = []

    if playlists["playlists"]["items"]:
        for playlist in playlists["playlists"]["items"]:
            playlist_name = playlist["name"]
            # Check if the playlist contains excluded keywords
            if all(
                exclude_keyword.lower() not in playlist_name.lower()
                for exclude_keyword in exclude_keywords
            ):
                filtered_playlists.append(playlist)
    else:
        return []
    return random.choice(filtered_playlists)


# We can get the popularity of the tracks; popularity is based on a scale from 0 to 100.
# 0 ==> Lowest popularity
# 100 ==> highest popularity

# What we want precisely is a mix of popular and less popular songs,
# but since it's a blind test and is made for fun,
# we would choose an average value above 50, something like 60.
# We want around 20 songs for a nice blind test


def get_n_top_songs(songs, num_elements):
    """
    This method sorts a list of songs by their popularity and returns
    the top n best popular songs from the list.

    Parameters:
        songs: List containing songs
        num_elements: Number of elements to return
    """
    sorted_songs = sorted(songs, key=itemgetter("popularity"), reverse=True)

    # In case the category size is higher than the array length
    if num_elements > len(sorted_songs):
        return sorted_songs

    return sorted_songs[:num_elements]


def get_songs_by_category(songs, min_popularity, category_size):
    """
    Partitions songs into 3 categories of popularity: low, medium, and high.

    Parameters:
        songs: List containing songs
        min_popularity: Minimum popularity (between 0 and 100) to create 3 categories
        category_size: Number of songs we want in the categories
    """
    # Filter songs below the minimum popularity
    filtered_songs = [
        song for song in songs if song["track"]["popularity"] >= min_popularity
    ]
    popularities_array = [song["track"]["popularity"] for song in filtered_songs]

    # Calculate the 1st and 3nd quartiles on the filtered popularities
    q25 = np.percentile(popularities_array, 25)
    q75 = np.percentile(popularities_array, 75)

    # Set thresholds for your categories
    low_threshold = q25
    high_threshold = q75

    # Divide popularities into categories
    low_popularities = [
        song["track"]
        for song in filtered_songs
        if song["track"]["popularity"] <= low_threshold
    ]
    medium_popularities = [
        song["track"]
        for song in filtered_songs
        if low_threshold < song["track"]["popularity"] <= high_threshold
    ]
    high_popularities = [
        song["track"]
        for song in filtered_songs
        if song["track"]["popularity"] > high_threshold
    ]

    # Select the specified number of songs for each category
    selected_low = get_n_top_songs(low_popularities, category_size)
    # For difficulty purposes, we want to have more medium songs than others
    selected_medium = get_n_top_songs(medium_popularities, category_size * 2)
    selected_high = get_n_top_songs(high_popularities, category_size)

    return selected_low + selected_medium + selected_high
