import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import numpy as np
from operator import itemgetter
import sys
import os
from dotenv import load_dotenv

def search_playlists_by_keyword(client, keywords):

    exclude_keywords = [
        'serie',
        'films',
        'disney',
        'jeux-videos',
        'culte',
        'cinema']

    # Recherche de playlists par mot-clé
    playlists = client.search(q=keywords, type='playlist', limit=10)
    filterd_playlists = []

    if playlists['playlists']['items']:
        print(f"Playlists avec le mot-clé '{keywords}':")
        for playlist in playlists['playlists']['items']:
            playlist_name = playlist['name']
            # Vérifiez si la playlist contient des mots-clés à exclure
            if all(exclude_keyword.lower() not in playlist_name.lower() for exclude_keyword in exclude_keywords):
                filterd_playlists.append(playlist)
    else:
        return []
    return random.choice(filterd_playlists)

# We can get the popularity of the tracks, popularity is based on a scale from 0 to 100.
# 0 ==> Lowest popularity
# 100 ==> highest popularity

# What do we want precisely, is a mix of popular and less popular songs
# But since it's a blindtest and is made for fun,
# we would choose an average value above 50, something like 60.
# We want around 20 songs for a nice blindtest


def get_n_top_songs(songs, num_elements):
    """
    This method sort a list of song by their popularity. returns the top n best popular songs from the list

    Parameters:
        songs: List containing songs
        Parameters: num_elements: Number of elements to return
    """
    sorted_songs = sorted(songs, key=itemgetter('popularity'), reverse=True)

    # In case category size is higher than the array length
    if num_elements > len(sorted_songs):
        return sorted_songs

    return sorted_songs[:num_elements]


def get_songs_by_category(songs, min_popularity, category_size):
    # Filtrer les sons en dessous de la popularité minimale
    filtered_songs = [song for song in songs if song['track']['popularity'] >= min_popularity]
    popularities_array = [song['track']['popularity'] for song in filtered_songs]

    # Calculez le 1er et 2ème quartiles sur les popularités filtrées
    q25 = np.percentile(popularities_array, 25)
    q75 = np.percentile(popularities_array, 75)

    # Définissez les seuils pour vos catégories
    low_threshold = q25
    high_threshold = q75

    # Divisez les popularités en catégories
    low_popularities = [song['track'] for song in filtered_songs if song['track']['popularity'] <= low_threshold]
    medium_popularities = [song['track'] for song in filtered_songs if low_threshold < song['track']['popularity'] <= high_threshold]
    high_popularities = [song['track'] for song in filtered_songs if song['track']['popularity'] > high_threshold]

    # Sélectionnez le nombre spécifié de sons pour chaque catégorie
    selected_low = get_n_top_songs(low_popularities, category_size)
    selected_medium = get_n_top_songs(medium_popularities, category_size * 2)
    selected_high = get_n_top_songs(high_popularities, category_size)

    return selected_low + selected_medium + selected_high




def main():

    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()

    CATEGORY_SIZE = int(sys.argv[1])
    MIN_POPULARITY = int(sys.argv[2])
    CLIENT_ID = 'ae0e8df4f008454ba1db538f5ca59d78'
    CLIENT_SECRET = 'f20fb86fc2ae475f8fa6295d9b8633ec'

    # Configurez les informations d'authentification
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Get the spotipy client
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Utilisation de la fonction avec exclusion de certains mots-clés
    playlist = search_playlists_by_keyword(client=sp, keywords='blind test +2000')
    print(playlist['name'])

    # Retrieve the songs of the playlist
    songs = sp.playlist_items(playlist["id"])
    print(songs['total'])

    selected_sounds = get_songs_by_category(songs['items'], MIN_POPULARITY, CATEGORY_SIZE)
    print(len(selected_sounds))

    print([(sound['name'], sound['popularity']) for sound in selected_sounds])

# Vérifie si le script est exécuté directement (plutôt que d'être importé comme un module)
if __name__ == "__main__":
    # Appelle la fonction main si le script est exécuté directement
    main()
