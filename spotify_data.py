import requests


def fetch_top_tracks_with_genres(access_token):
    """
    Fetch user's top tracks and the corresponding artist IDs.
    """
    top_tracks_url = "https://api.spotify.com/v1/me/top/tracks?limit=50"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(top_tracks_url, headers=headers)
    data = response.json()

    top_tracks = []

    for track in data["items"]:
        track_info = {
            "id": track["id"],
            "name": track["name"],
            "artists": [
                artist["name"] for artist in track["artists"]
            ],  # Get artist names
            "artist_ids": [
                artist["id"] for artist in track["artists"]
            ],  # Collect artist IDs for genres
        }
        top_tracks.append(track_info)

    return top_tracks  # Returns track info with artist names and IDs


def fetch_audio_features(access_token, track_ids):
    """
    Fetch audio features for a list of track IDs.
    """
    features_url = (
        f"https://api.spotify.com/v1/audio-features?ids={','.join(track_ids)}"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(features_url, headers=headers)
    return response.json()["audio_features"]


def fetch_artist_genres(access_token, artist_ids):
    """
    Fetch genres for a list of artist IDs.
    """
    artist_genres_url = f"https://api.spotify.com/v1/artists?ids={','.join(artist_ids)}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(artist_genres_url, headers=headers)

    return {
        artist["id"]: artist.get("genres", [])
        for artist in response.json()["artists"]
    }
