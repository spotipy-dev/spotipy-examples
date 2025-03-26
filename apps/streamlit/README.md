# FastAPI example

This is a simple example of using Spotipy with FastAPI with multi-user support.

It uses cookies, as it's easier to demonstrate the multi-user experience.
It's probably better (and maybe easier) to switch to a simple request header when using FastAPI as a backend.

## Prerequisites

- Install requirements: `pip3 install -r requirements.txt`
- Fill out the `config.toml` file with the help of the [dashboard](https://developer.spotify.com/dashboard/applications)

## Run the app

```console
python3 -m uvicorn main:app --host 0.0.0.0 --port 15912
```

You can adjust the parameters to your liking, but don't forget to update the redirect URI in the `config.toml` as well as the dashboard.

## Endpoints

### Root (`/`)

Returns the user data (`spotipy.Spotify.me()`) if the user is logged in. If not, a `401 Unauthorised` with the `auth_url` will be returned.
In order to log in, visit the `auth_url`.

### Callback (`/callback`)

After logging in with Spotify, the user should be redirected to this endpoint. If all goes well, the user will be then redirected to root.

### Logout (`/logout`)

Removes the session from the fake database (but not the cookies). Returns code 200 and `{"detail": "success"}` and the user must re-authenticate.
