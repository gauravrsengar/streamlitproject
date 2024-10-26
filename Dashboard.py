import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import config as cg

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = cg.client_id
SPOTIPY_CLIENT_SECRET = cg.client_secret
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'  # Use localhost redirect URI

# Set the scope to access top artists and tracks
scope = 'user-top-read'

# Set up SpotifyOAuth with token caching to refresh expired tokens automatically
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=scope,
                        cache_path=".spotipyoauthcache")  # Cache file to store tokens


# Get the Spotify client, handling token refresh if needed
def get_spotify_client():
    token_info = sp_oauth.get_cached_token()
    if not token_info:  # If no valid token is cached, prompt for re-authentication
        auth_url = sp_oauth.get_authorize_url()
        print(f"Please navigate to the following URL to authenticate:\n{auth_url}")
        auth_code = 'AQAhBFKuPmycf8wrmec7z_1KtQqbgYlXcjuD2v9PNaU0P_ZACOM7H_Wyr6y9YHCXNyTdi0PXxPjTZm5NOXKEq0vOuElRDsHIwZ76kvCO8fjPKyk0u1HjY7VUJl3E-kmLNIyh3R8edxYMMODako2MTr_5hMIAgid_ldSJP91RgUQlgYDoAdDxQUUq6dSPIbN7iw'
        token_info = sp_oauth.get_access_token(auth_code)

    # Return authenticated Spotify client
    return spotipy.Spotify(auth=token_info['access_token'])


# Get Spotify client with token handling
sp = get_spotify_client()


# Fetch top tracks for the last 6 months (medium_term)
def get_top_tracks(sp, limit=10, time_range='long_term'):
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [(track['name'], track['artists'][0]['name'], track['popularity']) for track in top_tracks['items']]


# Fetch top artists for the last 6 months (medium_term)
def get_top_artists(sp, limit=10, time_range='long_term'):
    top_artists = sp.current_user_top_artists(limit=limit, time_range=time_range)
    return [(artist['name'], artist['popularity']) for artist in top_artists['items']]


# Fetch top tracks and artists
top_tracks_data = get_top_tracks(sp)
top_artists_data = get_top_artists(sp)

# Convert data to DataFrames for easier visualization
top_tracks_df = pd.DataFrame(top_tracks_data, columns=['Track', 'Artist', 'Popularity'])
print(top_tracks_df)
top_artists_df = pd.DataFrame(top_artists_data, columns=['Artist', 'Popularity'])
print(top_artists_df)



# Display Analytics using Streamlit
st.title("Spotify Top Tracks and Artists Analytics (Last 6 Months)")
st.write("Data based on your top listening trends over the last 6 months")

# Display Top 10 Tracks
st.subheader("Top 10 Tracks")
st.bar_chart(top_tracks_df.set_index('Track')['Popularity'])

# Display Top 10 Artists
st.subheader("Top 10 Artists")
st.bar_chart(top_artists_df.set_index('Artist')['Popularity'])


