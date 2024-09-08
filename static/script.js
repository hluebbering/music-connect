document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_data')
        // fetch('https://music-connect-8e0645ff1ca5.herokuapp.com/get_data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);  // Debug: log data to console to verify structure
            const tracks = data.top_tracks ? data.top_tracks.items : [];
            const artists = data.top_artists ? data.top_artists.items : [];
            const genres = data.genres ? data.genres : [];  // Adjusted for potential structure issues

            const tracksList = document.getElementById('top-tracks');
            const artistsList = document.getElementById('top-artists');
            const genresList = document.getElementById('top-genres');

            if (tracksList) {
                tracks.forEach(track => {
                    const li = document.createElement('li');
                    li.textContent = `${track.name} by ${track.artists.map(artist => artist.name).join(', ')}`;
                    tracksList.appendChild(li);
                });
            }

            if (artistsList) {
                artists.forEach(artist => {
                    const li = document.createElement('li');
                    li.textContent = artist.name;
                    artistsList.appendChild(li);
                });
            }

            if (genresList) {
                genres.forEach(genre => {
                    const li = document.createElement('li');
                    li.textContent = genre;
                    genresList.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Failed to load data. Please check the console for more details.');
        });



    // Fetch analyzed clustering data
    fetch('/analyze')
        .then(response => response.json())
        .then(data => {
            const clusters = data.labels;
            const topGenres = data.top_genres;

            // Display the optimal number of clusters
            const optimalClustersElement = document.getElementById('optimal-clusters');
            optimalClustersElement.textContent = `Optimal Clusters: ${data.optimal_clusters}`;

            // Display cluster information for each track
            const clusterList = document.getElementById('cluster-list');
            clusters.forEach((cluster, index) => {
                const li = document.createElement('li');
                li.textContent = `Track ${index + 1} belongs to Cluster: ${cluster}`;
                clusterList.appendChild(li);
            });

            // Display the user's top genres based on clustering
            const genresList = document.getElementById('cluster-genres');
            topGenres.forEach(genre => {
                const li = document.createElement('li');
                li.textContent = genre;
                genresList.appendChild(li);
            });

            // Automatically fetch and display recommendations for the first cluster
            fetch(`/recommend?cluster=0`)
                .then(response => response.json())
                .then(recommendationData => {
                    const recommendationsList = document.getElementById('recommendations');
                    recommendationData.recommendations.forEach(rec => {
                        const li = document.createElement('li');
                        li.textContent = `Track ID: ${rec}`;  // Replace with track name if available
                        recommendationsList.appendChild(li);
                    });
                })
                .catch(error => console.error('Error fetching recommendations:', error));
        })
        .catch(error => console.error('Error fetching clustering data:', error));
});