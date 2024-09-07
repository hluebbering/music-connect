document.addEventListener('DOMContentLoaded', function () {
    fetch('https://music-connect-8e0645ff1ca5.herokuapp.com/get_data')
    // fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            const tracks = data.top_tracks.items;
            const artists = data.top_artists.items;

            const tracksList = document.getElementById('top-tracks');
            tracks.forEach(track => {
                const li = document.createElement('li');
                li.textContent = `${track.name} by ${track.artists.map(artist => artist.name).join(', ')}`;
                tracksList.appendChild(li);
            });

            const artistsList = document.getElementById('top-artists');
            artists.forEach(artist => {
                const li = document.createElement('li');
                li.textContent = artist.name;
                artistsList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
