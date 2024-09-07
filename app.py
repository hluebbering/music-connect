import time
from flask import Flask, redirect, request, session, jsonify, url_for, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import base64
import logging
from collections import Counter

load_dotenv()  # Load environment variables from .env file
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = "ynx2ftyq"
app.config['DEBUG'] = False
CORS(app)  # This will enable CORS for all domains on all routes

# Your Spotify Client ID and Secret
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')




@app.route('/refresh_token')
def refresh_token():
    refresh_token = session.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token not found'}), 401

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET')
        }
    )

    if response.status_code != 200:
        return jsonify({'error': 'Failed to refresh token'}), response.status_code

    new_tokens = response.json()
    session['access_token'] = new_tokens.get('access_token')
    return jsonify({'message': 'Token refreshed successfully'})



@app.route('/')
def home():
    if 'access_token' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login')
def login():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-top-read"
    app.logger.debug(f"Redirecting to Spotify auth URL: {auth_url}")
    return redirect(auth_url)





@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        logging.error(f"Spotify authorization error: {error}")
        return jsonify({"error": f"Spotify authorization error: {error}"}), 400

    code = request.args.get('code')
    if not code:
        logging.error("Authorization failed: No code received in callback.")
        return jsonify({"error": "Authorization failed: No code received"}), 400

    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    token_headers = {
        'Authorization': f"Basic {client_creds_b64}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    if token_response.status_code != 200:
        error_info = token_response.json()
        error_message = error_info.get('error_description', 'Failed to retrieve access token')
        logging.error(f"Token exchange failed: {error_message}, Status Code: {token_response.status_code}")
        return jsonify({'error': error_message, 'error_details': error_info}), token_response.status_code
    
    token_info = token_response.json()
    session['access_token'] = token_info.get('access_token')
    session['refresh_token'] = token_info.get('refresh_token')
    session['token_expires_in'] = time.time() + token_info.get('expires_in')
    logging.info("Access token and refresh token successfully received and stored.")

    return redirect(url_for('home'))



@app.route('/get_data')
def get_data():
    access_token = session.get('access_token')
    if not access_token:
        logging.warning("Redirecting to login: Access token not found in session.")
        return redirect(url_for('login'))

    headers = {'Authorization': f'Bearer {access_token}'}
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks'
    top_artists_url = 'https://api.spotify.com/v1/me/top/artists'

    top_tracks_response = requests.get(top_tracks_url, headers=headers)
    if top_tracks_response.status_code != 200:
        logging.error(f"Failed to fetch top tracks: {top_tracks_response.json()}")
        return jsonify({'error': 'Failed to fetch top tracks', 'details': top_tracks_response.json()}), top_tracks_response.status_code

    top_artists_response = requests.get(top_artists_url, headers=headers)
    if top_artists_response.status_code != 200:
        logging.error(f"Failed to fetch top artists: {top_artists_response.json()}")
        return jsonify({'error': 'Failed to fetch top artists', 'details': top_artists_response.json()}), top_artists_response.status_code

    top_tracks = top_tracks_response.json()
    top_artists = top_artists_response.json()

    genres = [genre for artist in top_artists['items'] for genre in artist['genres']]
    genre_counts = Counter(genres)
    top_genres = genre_counts.most_common(5)  # Adjust the number to display more or fewer genres

    return jsonify({
        'top_tracks': top_tracks,
        'top_artists': top_artists,
        'genres': top_genres
    })



@app.route('/display_data')
def display_data():
    access_token = session.get('access_token')
    if not access_token:
        logging.warning("Access token is missing. User needs to authenticate again.")
        return redirect(url_for('login'))

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve data: {response.json()}")
        return jsonify({'error': 'Failed to retrieve top tracks', 'details': response.json()}), response.status_code

    top_tracks = response.json()
    # Here you could add logic to format or process the data for presentation
    return jsonify(top_tracks)



if __name__ == '__main__':
    app.run(debug=True)
    