# Flask API example

This examples shows how to use spotipy as an API and allowing multiple users to sign in from a basic UI.

## Prerequisites

    pip3 install spotipy Flask Flask-Session

From your [app settings](https://developer.spotify.com/dashboard/applications)

    export SPOTIPY_CLIENT_ID=client_id_here
    export SPOTIPY_CLIENT_SECRET=client_secret_here
    export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080' // must contain a port

`SPOTIPY_REDIRECT_URI` must be added to your [app settings](https://developer.spotify.com/dashboard/applications)

### OPTIONAL

In development environment for debug output:

    export FLASK_ENV=development

so that you can invoke the app outside the file's directory include:

    export FLASK_APP=/path/to/spotipy/examples/app.py

On Windows, use `SET` instead of `export`.

## Run app.py

    python3 app.py OR python3 -m flask run

NOTE: If receiving "port already in use" error, try other ports: 5000, 8090, 8888, etc...
    (will need to be updated in your Spotify app and SPOTIPY_REDIRECT_URI variable)
