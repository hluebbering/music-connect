## Steps to Create Web App


### Step 1. Environment Setup
1. **Create a GitHub Repository**: This will store your project's code.
2. **Install Necessary Tools**: Python, Flask (a lightweight WSGI web application framework), and requests (HTTP) library.



### Step 2: Register Application with Spotify
1. Log into [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create an app to obtain `Client ID` and `Client Secret`.
3. Set the Redirect URI to point to your local or production environment (e.g., `http://localhost:5000/callback` for development).


------


### Step 3: Flask Backend Setup
#### 1. Initialize Flask App: 
Set up Flask App (`app.py`) to handle authentication and data retrieval.
```python
from flask import Flask, redirect, request, session, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random key for the session

@app.route('/')
def home():
   return 'Welcome to the Spotify Flask App!'

if __name__ == '__main__':
   app.run(debug=True)
```

#### 2. **Implement Spotify Authentication**:
   - **OAuth 2.0 Flow**: Redirect users to the Spotify authorization page and handle the callback to exchange the code for an access token.
   - **Set Up Environment Variables:** Store sensitive info such as Client ID and Secret securely. Use environment variables or .env file (via `python-dotenv` package).
   - **Implement Login and Callback Routes.**
   - **Run Flask App:** Run by executing the `app.py` file. Navigate to *http://localhost:5000/login* to start authentication process.

----

### Step 4: Fetching Data from Spotify
After you've authenticated the user and obtained an access token, you can use this token to make requests to Spotify's API to fetch data such as the user's top tracks and artists.
1. **Use access token to make requests to Spotify’s Web API.**
2. **Define Routes in Your Flask App to Fetch Spotify Data:** Use `/get_data` route to fetch user's top tracks and artists by making GET requests to endpoints like `/v1/me/top/tracks`.



-------

### Step 5: Frontend Development
Create a basic frontend -using HTML, CSS, and JavaScript- that communicates with Flask's backend to retrieve Spotify data and display it to the user.

1. **Create HTML/CSS/JavaScript Files**: Build a simple user interface that displays the data fetched from the backend.
2. **JavaScript Fetch API**: Use JavaScript to connect to your Flask backend, retrieve data, and update the frontend dynamically.

-----

### Step 6: Deployment
1. **Deploy Flask Backend to Heroku**: Deploy a Flask app to a platform like Heroku. This involves setting up `requirements.txt` and `Procfile` files, ensuring environment variables are configured (for storing your client secret and ID securely), and pushing your code to Heroku.

2. **Deploy the Frontend**: Since GitHub Pages supports static sites, you’ll deploy your HTML/CSS/JavaScript files there. Ensure that your frontend code makes calls to the correct backend URL (your Heroku app URL).

------


#### Step 7: Documentation and Publishing
1. **Push to GitHub**:
   - Push all your code to your GitHub repository, excluding sensitive credentials which should be managed through environment variables or config files.



#### Step 7: Documentation and Publishing
1. **Document Your Project**:
   - Write a clear `README.md` that explains what the app does, how to set it up, and how to run it.
2. **Push to GitHub**:
   - Push all your code to your GitHub repository, excluding sensitive credentials which should be managed through environment variables or config files.

This setup creates a full-fledged project utilizing Spotify's data, and it’s great for your GitHub portfolio as it showcases your skills with APIs, Python, Flask, and basic frontend development. If you need any specific code snippets or further clarification on any step, just let me know!









Deploy the Frontend:
Since GitHub Pages supports static sites, you’ll deploy your HTML/CSS/JavaScript files there.
Ensure that your frontend code makes calls to the correct backend URL (your Heroku app URL).



Step 7: Documentation and Publishing
Document Your Project:
Write a clear README.md that explains what the app does, how to set it up, and how to run it.
Push to GitHub:
Push all your code to your GitHub repository, excluding sensitive credentials which should be managed through environment variables or config files.
This setup creates a full-fledged project utilizing Spotify's data, and it’s great for your GitHub portfolio as it showcases your skills with APIs, Python, Flask, and basic frontend development. If you need any specific code snippets or further clarification on any step, just let me know!

heroku config:set SPOTIFY_CLIENT_ID=f7df04eeba2a41fc9b799188376b5d27
heroku config:set SPOTIFY_CLIENT_SECRET=127da41fb0e84b958e08d7bab6807f0b
heroku config:set REDIRECT_URI=http://localhost:5000/callback
heroku config:set REDIRECT_URI="https://fierce-sands-53854-09e86a071da9.herokuapp.com/callback" --app your-app-name

heroku config:set REDIRECT_URI="https://fierce-sands-53854-09e86a071da9.herokuapp.com/callback" --app fierce-sands-53854







