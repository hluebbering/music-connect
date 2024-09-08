import requests
from flask import session
import base64
import os

# Your Spotify Client ID and Secret
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


def refresh_access_token():
    refresh_token = session.get("refresh_token")
    if not refresh_token:
        raise ValueError("No refresh token found in session.")

    token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    response = requests.post(
        token_url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={
            "Authorization": f"Basic {client_creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    if response.status_code != 200:
        raise Exception(f"Failed to refresh access token: {response.json()}")
    token_info = response.json()
    session["access_token"] = token_info.get("access_token")
    return token_info.get("access_token")


def fetch_top_tracks_with_genres(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        access_token = refresh_access_token()  # Token expired, refresh it
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch top tracks: {response.json()}")

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

    return {artist["id"]: artist.get("genres", []) for artist in response.json().get("artists", [])}
