import numpy as  np
import matplotlib.pyplot as plt
import pandas as pd
import requests

#gets the access token
def get_header(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url, 
        {
        "grant_type" : "client_credentials",
        "client_id": client_id,
        "client_secret" : client_secret
        }
    )
    auth_response_data = auth_response.json()
    access_token = auth_response_data["access_token"]
    header = {
        "Authorization" : "Bearer {token}".format(token=access_token)
    }
    return header
#request artist top tracks
def request_api_artist(artist_id, header):
    base_url = "https://api.spotify.com/v1/"
    top_track_res = requests.get(base_url + "artists/" + artist_id + "/top-tracks?market=de", headers=header)
    top_track_res = top_track_res.json()
    df_t = pd.DataFrame(top_track_res["tracks"])
    fig = plt.figure(figsize=(18,10))
    ax = fig.add_axes([0,0,1,1])
    ax.bar(df_t["name"], df_t["popularity"])
    plt.savefig('top_tracks.jpg',bbox_inches='tight', dpi=150)
    return fig

#converts string to use %25 instead of spaces for search function
def space_to_percent(string):
    string = string.replace(" ", "%25")
    return string


#search for artists, returns list of artists
def artist_search(search_term, header):
    base_url = "https://api.spotify.com/v1/"
    #contains information about market, search type and result limit
    market = "&type=artist&market=de&limit=10"
    search_term = space_to_percent(search_term)
    artist_res = requests.get(base_url + "search?q=" + search_term + market, headers=header)
    artist_res = artist_res.json()
    df_artist = pd.DataFrame(artist_res["artists"]["items"])
    df_artist = df_artist.drop(["external_urls", "followers", "genres", "href", "images", "popularity", "type", "uri"], axis=1)
    return df_artist




