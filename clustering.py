import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
import logging
from sklearn.metrics import silhouette_score



def perform_kmeans(data):
    # Extract numeric features for clustering (make sure all features are numeric)
    features = np.array(
        [[track["danceability"], track["energy"], track["tempo"]] for track in data]
    )

    max_k = 10  # Test a range of clusters from 2 to max_k
    optimal_k = 2  # Start with 2 clusters
    best_score = -1
    
    # Find the optimal number of clusters using silhouette score
    for k in range(2, max_k + 1):
        kmeans = KMeans(n_clusters=k, n_init=10)
        cluster_labels = kmeans.fit_predict(features)
        score = silhouette_score(features, cluster_labels)
        
        if score > best_score:
            best_score = score
            optimal_k = k

    # Run KMeans clustering with the optimal number of clusters
    kmeans_model = KMeans(n_clusters=optimal_k, n_init=20, random_state=42).fit(features)
    cluster_labels = kmeans_model.labels_

    return kmeans_model, optimal_k, cluster_labels


def determine_optimal_clusters(inertia):
    # Calculate the second derivative (change of changes)
    differences = np.diff(inertia)
    return np.argmin(differences) + 1



def recommend_songs_by_cluster(cluster_id, cluster_labels, combined_data):
    """
    Recommend songs based on the cluster the user is interested in.
    """
    recommendations = []

    for i, label in enumerate(cluster_labels):
        if label == cluster_id:
            track_name = combined_data[i].get("name", "Unknown Track")
            artists = ", ".join(combined_data[i].get("artists", []))
            genres = ", ".join(combined_data[i].get("genres", []))

            recommendations.append(f"{track_name} by {artists} (Genres: {genres})")

    return recommendations
