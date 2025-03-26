from fastapi import FastAPI, Depends, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from spotipy import Spotify
from spotipy.cache_handler import CacheHandler
from spotipy.oauth2 import SpotifyOAuth
import toml
import secrets

# toml is included in newer Python releases, but not everybody is running the newest version
config = toml.load("./config.toml")

app = FastAPI()

# fake database to store sessions. Prevents users from obtaining the Spotify token via cookies.
sessions = dict()


class FastAPICacheHandler(CacheHandler):
    """
    A cache handler that stores tokens in a fake database and applies a session cookie to the response.
    """

    def __init__(self, request: Request, response: Response = None):
        self.request = request
        self.response = response

    def get_cached_token(self):
        return sessions.get(self.request.cookies.get("session"))

    def save_token_to_cache(self, token_info):
        session = secrets.token_urlsafe(64)
        sessions[session] = token_info
        self.response.set_cookie("session", session)


def get_spotipy_user(cache_handler=Depends(FastAPICacheHandler)) -> Spotify:
    """
    Returns a spotipy.Spotify object if the user is logged in.
    If not, then a HTTPException is raised with the authentication URL included.
    """
    auth_manager = SpotifyOAuth(**config["spotipy"], cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        print(auth_url)
        raise HTTPException(status_code=401, detail=auth_url)

    return Spotify(auth_manager=auth_manager)


@app.get("/")
def get_user(spotify: Spotify = Depends(get_spotipy_user)):
    """
    Get infos about the user (spotipy.Spotify.me())
    """
    return spotify.me()


@app.get("/callback")
def callback(code: str, cache_handler=Depends(FastAPICacheHandler)):
    """
    Callback function for Spotify OAuth2
    """
    cache_handler.response = RedirectResponse("/")
    auth_manager = SpotifyOAuth(**config["spotipy"], cache_handler=cache_handler)
    auth_manager.get_access_token(code)
    return cache_handler.response


@app.get("/logout")
def logout(request: Request):
    session = request.cookies.get("session")
    if session in sessions:
        del sessions[session]
    return {"detail": "success"}
