import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from collections import Counter


def preprocess_data(audio_features, genres):
    # Convert audio features to DataFrame
    features_df = pd.DataFrame(audio_features)

    # Get the numeric columns from audio features
    numeric_columns = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    ]

    # Normalize numeric data
    scaler = StandardScaler()
    scaled_audio_features = scaler.fit_transform(features_df[numeric_columns])

    # Process genres: Take top 5 genres, one-hot encode them
    genre_counts = Counter(genres)
    top_genres = [genre for genre, _ in genre_counts.most_common(5)]  # Top 5 genres
    genres_df = pd.DataFrame(
        [
            [1 if genre in track_genres else 0 for genre in top_genres]
            for track_genres in genres
        ]
    )

    # Merge audio features and genres into a single dataset
    combined_features = pd.concat(
        [pd.DataFrame(scaled_audio_features), genres_df], axis=1
    )

    # Returning data and top genres for later use
    return combined_features, top_genres


def combine_track_audio_and_genres(top_tracks, audio_features, artist_genres):
    """
    Combine track data with audio features and genres.
    """
    combined_data = []

    for track, features in zip(top_tracks, audio_features):
        genres = []
        for artist_id in track["artist_ids"]:
            genres.extend(
                artist_genres.get(artist_id, [])
            )  # Add all genres from artists

        combined_track = {
            "id": track["id"],
            "name": track["name"],
            "artists": track["artists"],
            "genres": list(set(genres)),  # Remove duplicates from genre list
            "danceability": features["danceability"],
            "energy": features["energy"],
            "tempo": features["tempo"],  # Other audio features
            "valence": features["valence"],  # Positivity of the track
        }
        combined_data.append(combined_track)

    return combined_data
