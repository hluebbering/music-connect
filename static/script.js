document.addEventListener('DOMContentLoaded', function () {
    // Replace 'your-heroku-app-name' with your actual Heroku app name
    // fetch('/get_data')
    const backendUrl = 'https://your-heroku-app-name.herokuapp.com/get_data';
    fetch(backendUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
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



document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_data')
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
