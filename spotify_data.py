import requests




def fetch_top_tracks_with_genres(access_token):
    top_tracks_url = "https://api.spotify.com/v1/me/top/tracks?limit=50"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(top_tracks_url, headers=headers)
    
    # If the token is expired, refresh it
    if response.status_code == 401:
        access_token = refresh_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(top_tracks_url, headers=headers)
    
    data = response.json()
    
    if "items" not in data:
        raise KeyError(f"Expected 'items' in response but got: {data}")

    top_tracks = []
    for track in data["items"]:
        track_info = {
            "id": track["id"],
            "name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "artist_ids": [artist["id"] for artist in track["artists"]],
        }
        top_tracks.append(track_info)

    return top_tracks


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
