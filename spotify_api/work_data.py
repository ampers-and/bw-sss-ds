import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from decouple import config
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from numpy.linalg import norm
from joblib import load


CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
credentials = oauth2.SpotifyClientCredentials(
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET)
token = credentials.get_access_token()

spotify = spotipy.Spotify(auth=token)
spot_scaler = load('SpotScaler.joblib')


# get the ids of 100 recommendations from spotify
def get_100(target_id):
    res = spotify.recommendations(seed_tracks=[target_id], limit=100)
    ids = [i['id'] for i in res['tracks']]
    return(ids)


def audio_features_to_dict(feats):
    feat_dict = {'acousticness': feats['acousticness'],
                 'danceability': feats['danceability'],
                 'duration_ms': feats['duration_ms'],
                 'energy': feats['energy'],
                 'instrumentalness': feats['instrumentalness'],
                 'key': feats['key'],
                 'liveness': feats['liveness'],
                 'loudness': feats['loudness'],
                 'mode': feats['mode'],
                 'speechiness': feats['speechiness'],
                 'tempo': feats['tempo'],
                 'time_signature': feats['time_signature'],
                 'valence': feats['valence'],
                 'id': feats['id']}
    return feat_dict


def get_features(target_id):
    res = spotify.audio_features(tracks=target_id)[0]

    return audio_features_to_dict(res)


def get_all_features(list_id):
    feats_list = spotify.audio_features(tracks=list_id)

    df = pd.DataFrame(columns=['acousticness',
                               'danceability',
                               'duration_ms',
                               'energy',
                               'instrumentalness',
                               'key',
                               'liveness',
                               'loudness',
                               'mode',
                               'speechiness',
                               'tempo',
                               'time_signature',
                               'valence',
                               'id'])

    for feat in feats_list:
        feat_dict = audio_features_to_dict(feat)
        df = df.append(feat_dict, ignore_index=True)
    return(df)


def top_recs(target_id, k=5):
    df = get_all_features(get_100(target_id))
    song_df = get_all_features(target_id)

    df_scaled = spot_scaler.fit_transform(df.drop(['id'], axis=1))
    feats = spot_scaler.transform(song_df.drop(['id'], axis=1))

    df['dist'] = list(map(lambda x: norm(x-np.array(feats)[0]),
                          np.array(df_scaled)))
    top = df.sort_values(by='dist').iloc[0:k]

    return top.drop(['dist'], axis=1)


# Get an array of data pertaining to a list of recommendations
def songs_data(res_df):
    vals = res_df.id.values
    song_info = []
    for i in vals:
        tracks = spotify.track(i)
        song_info.append({'large_image': tracks['album']['images'][0]['url'],
                          'med_image': tracks['album']['images'][1]['url'],
                          'small_image': tracks['album']['images'][2]['url'],
                          'artist': tracks['artists'][0]['name'],
                          'song_name': tracks['name'],
                          'id': tracks['id'],
                          'uri': tracks['uri']})
    return song_info


# Get an array of data pertaining to a list of recommendations based on target
def rec_data(target_id):
    return songs_data(top_recs(target_id))


def get_songs(song, limit=7):
    songs = spotify.search(song,
                           limit=limit,
                           offset=0,
                           type='track',
                           market='US')
    tracks = []
    for i in songs['tracks']['items']:
        tracks.append({'song_name': i['name'],
                       'artist': i['artists'][0]['name'],
                       'id': i['id'],
                       'uri': i['uri']})
    return(tracks)
