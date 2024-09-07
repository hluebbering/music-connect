document.addEventListener('DOMContentLoaded', function () {
    fetch('https://music-connect-8e0645ff1ca5.herokuapp.com/get_data')
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
});
