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


CLIENT_ID_var = config("CLIENT_ID")
CLIENT_SECRET_var = config("CLIENT_SECRET")


class Rec_Helper():
    CLIENT_ID = CLIENT_ID_var
    CLIENT_SECRET = CLIENT_SECRET_var
    credentials = oauth2.SpotifyClientCredentials(
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET)
    token = credentials.get_access_token()

    def __init__(self, k=5):
        self.spotify = spotipy.Spotify(auth=self.token)
        self.spot_scaler = load('SpotScaler.joblib')

    # get the ids of 100 recommendations from spotify
    def get_100(self, target_id):
        res = self.spotify.recommendations(seed_tracks=[target_id], limit=100)
        ids = [i['id'] for i in res['tracks']]
        return(ids)

    def get_features(self, list_id):
        res = self.spotify.audio_features(tracks=list_id)[0]

        feat_dict = {'acousticness': res['acousticness'],
                     'danceability': res['danceability'],
                     'duration_ms': res['duration_ms'],
                     'energy': res['energy'],
                     'instrumentalness': res['instrumentalness'],
                     'key': res['key'],
                     'liveness': res['liveness'],
                     'loudness': res['loudness'],
                     'mode': res['mode'],
                     'speechiness': res['speechiness'],
                     'tempo': res['tempo'],
                     'time_signature': res['time_signature'],
                     'valence': res['valence'],
                     'id': res['id']}
        return feat_dict

    def get_all_features(self, list_id):
        res = self.spotify.audio_features(tracks=list_id)

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

        for i in res:
            feat_dict = {'acousticness': i['acousticness'],
                         'danceability': i['danceability'],
                         'duration_ms': i['duration_ms'],
                         'energy': i['energy'],
                         'instrumentalness': i['instrumentalness'],
                         'key': i['key'],
                         'liveness': i['liveness'],
                         'loudness': i['loudness'],
                         'mode': i['mode'],
                         'speechiness': i['speechiness'],
                         'tempo': i['tempo'],
                         'time_signature': i['time_signature'],
                         'valence': i['valence'],
                         'id': i['id']}
            df = df.append(feat_dict, ignore_index=True)
        return(df)

    def top_recs(self, target_id, k=5):
        df = self.get_all_features(self.get_100(target_id))
        song_df = self.get_all_features(target_id)

        df_scaled = self.spot_scaler.fit_transform(df.drop(['id'], axis=1))
        feats = self.spot_scaler.transform(song_df.drop(['id'], axis=1))

        df['dist'] = list(map(lambda x: norm(x-np.array(feats)[0]),
                              np.array(df_scaled)))
        top = df.sort_values(by='dist').iloc[0:k]

        return top.drop(['dist'], axis=1)

    def feedback(self, target_id):
        vals = self.top_recs(target_id).id.values
        song_info = []
        for i in vals:
            tracks = self.spotify.track(i)
            song_info.append({'large_image': tracks['album']['images'][0]['url'],
                              'med_image': tracks['album']['images'][1]['url'],
                              'small_image': tracks['album']['images'][2]['url'],
                              'artist': tracks['artists'][0]['name'],
                              'song_name': tracks['name'],
                              'id': tracks['id'],
                              'uri': tracks['uri']})
        return(song_info)

    def get_songs(self, song, limit=7):
        songs = self.spotify.search(song, limit=limit, offset=0, type='track', market='US')
        tracks = []
        for i in songs['tracks']['items']:
            tracks.append({'song_name': i['name'],
                           'artist': i['artists'][0]['name'],
                           'id': i['id']})
        return(tracks)
