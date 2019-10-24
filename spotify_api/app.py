from flask import Flask, render_template, request, url_for, redirect, jsonify

from decouple import config
from dotenv import load_dotenv
from work_data import *
from flask_cors import CORS
import pygal
from pygal.style import Style
from chart_style import fixed_style

load_dotenv()

API_KEY = config("API_KEY")


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/songs/<key>/<value>')
def song_search(key, value):
    if key == API_KEY:
        songs = get_songs(value)
        return jsonify(songs)

@app.route('/auto_search/<key>/<value>')
def auto_search(key, value):
    if key == API_KEY:
        songs = get_songs(value, limit=1)
        songs = songs[0]
        id = songs['id']
        recs = rec_data([id])
        track = songs_data_single(id)
        recs.insert(0,track)
        return jsonify(recs)


@app.route('/features/<key>/<value>')
def song_features(key, value):
    if key == API_KEY:
        features = get_features(value)
        return jsonify(features)


@app.route('/recs/<key>/<value>')
def recommendations(key, value):
    if key == API_KEY:
        recs = rec_data([value])

        return jsonify(recs)


@app.route('/embed/<key>/<value>')
def embed(key, value):
    if key == API_KEY:
        recs = rec_data([value])

        return render_template('embed.html', recs=recs)


@app.route('/graph/<key>/<value>')
def graph(key, value):
    if key == API_KEY:
        recs = top_recs([value])

        features = pd.concat([get_all_features([value]), recs])

        custom_style = fixed_style

        radar_chart = pygal.Radar(style=custom_style)
        radar_chart.title = ('Comparison of Recommendations for \"' +
                             spotify.track(value)['name'] + '\"')
        radar_chart.x_labels = list(features.drop('id', axis=1).keys())

        for id, feature_vec in zip(features.id, features.drop('id', axis=1).values):
            radar_chart.add(spotify.track(id)['name'],
                            spot_scaler.transform([feature_vec])[0])

        graph_data = radar_chart.render_data_uri()

        return render_template('radar.html',
                                graph_data=graph_data,
                                title='Song Feature Graph')

@app.route('/graph_data/<key>/<value>')
def graph_data(key, value):
    if key == API_KEY:
        recs = top_recs([value])

        features = pd.concat([get_all_features([value]), recs])

        feat_dict = songs_data(features)

        custom_style = fixed_style
        radar_chart = pygal.Radar(style=custom_style)

        radar_chart.title = ('Comparison of Recommendations for \"' +
                             spotify.track(value)['name'] + '\"')
        radar_chart.x_labels = list(features.drop('id', axis=1).keys())

        for id, feature_vec in zip(features.id, features.drop('id', axis=1).values):
            radar_chart.add(spotify.track(id)['name'],
                            spot_scaler.transform([feature_vec])[0])

        graph_data = radar_chart.render_data_uri()
        graph_dict = [{'graph_uri':graph_data},feat_dict]
        return jsonify(graph_dict)


# http://127.0.0.1:5000/avg_mood/0?playlist=['1h2vCbRUWpWnYEgb2hfQbi', '498ZVInMGDkmmNVpSWqHiZ', '3bidbhpOYeV4knp8AIu8Xn', '7B1QliUMZv7gSTUGAfMRRD', '2qYsSHsYkihWx043HVJQRV']
# Get default mood from playlist
@app.route('/avg_mood/<key>', methods=['GET'])
def avg_mood(key):
    if key == API_KEY:
        value = request.args.get('playlist')

        playlist = playlist_str_to_ls(value)

        feats = default_mood(playlist)

        return jsonify(feats)


# http://127.0.0.1:5000/playlist_recs/0?playlist=['1h2vCbRUWpWnYEgb2hfQbi', '498ZVInMGDkmmNVpSWqHiZ', '3bidbhpOYeV4knp8AIu8Xn', '7B1QliUMZv7gSTUGAfMRRD', '2qYsSHsYkihWx043HVJQRV', '7x9Am1UW3C5yCZLSysEWxX', '7lWF2mVr1KKbVnaT2nSlPo', '4ycLiPVzE5KamivXrAzGFG', '05qCCJQJiOwvPQBb7akf1R', '1ONoPkp5XIuw3tZ1GzrNKZ', '3ZjnFYlal0fXN6t61wdxhl']
# http://127.0.0.1:5000/playlist_recs/0?playlist=['1h2vCbRUWpWnYEgb2hfQbi', '498ZVInMGDkmmNVpSWqHiZ', '3bidbhpOYeV4knp8AIu8Xn', '7B1QliUMZv7gSTUGAfMRRD', '2qYsSHsYkihWx043HVJQRV']
# http://127.0.0.1:5000/playlist_recs/0?playlist=['1h2vCbRUWpWnYEgb2hfQbi', '498ZVInMGDkmmNVpSWqHiZ', '3bidbhpOYeV4knp8AIu8Xn']
# Getting recomendations from playlist alone
@app.route('/playlist_recs/<key>')
def playlist_recs(key):
    if key == API_KEY:
        value = request.args.get('playlist')

        playlist = playlist_str_to_ls(value)

        recs = rec_data(playlist)
        li = [i['id'] for i in recs]
        features = get_all_features(li)
        feats = default_mood(playlist)
        feat_dict = songs_data(features)

        custom_style = fixed_style
        radar_chart = pygal.Radar(style=custom_style)


        radar_chart.x_labels = list(features.drop('id', axis=1).keys())

        for id, feature_vec in zip(features.id, features.drop('id', axis=1).values):
            radar_chart.add(spotify.track(id)['name'],
                            spot_scaler.transform([feature_vec])[0])

        graph_data = radar_chart.render_data_uri()
        graph_dict = [{'graph_uri':graph_data},feats,recs]

        return jsonify(graph_dict)


@app.route('/mood/<key>', methods=['GET'])
def mood_api(key):
    if key == API_KEY:
        mood_df = mood()

        feat_dict = {'acousticness': mood_df['acousticness'].iloc[0],
                    'danceability': mood_df['danceability'].iloc[0],
                    'duration_ms': mood_df['duration_ms'].iloc[0],
                    'energy': mood_df['energy'].iloc[0],
                    'instrumentalness': mood_df['instrumentalness'].iloc[0],
                    'key': mood_df['key'].iloc[0],
                    'liveness': mood_df['liveness'].iloc[0],
                    'loudness': mood_df['loudness'].iloc[0],
                    'mode': mood_df['mode'].iloc[0],
                    'speechiness': mood_df['speechiness'].iloc[0],
                    'tempo': mood_df['tempo'].iloc[0],
                    'time_signature': mood_df['time_signature'].iloc[0],
                    'valence': mood_df['valence'].iloc[0]}

        return jsonify(feat_dict)


@app.route('/mood_test/<key>/<value>', methods=['GET'])
def mood_rec_api(key, value):
    if key == API_KEY:
        recs = mood_playlist_recs([value])

        return jsonify(recs)


@app.route('/single_song_graph/<key>/<value>')
def sigle_song_graph(key, value):
    if key == API_KEY:

        features = get_all_features([value])

        custom_style = fixed_style
        radar_chart = pygal.Radar(style=custom_style)

        radar_chart.x_labels = list(features.drop('id', axis=1).keys())

        for id, feature_vec in zip(features.id, features.drop('id', axis=1).values):
            radar_chart.add(spotify.track(id)['name'],
                            spot_scaler.transform([feature_vec])[0])

        graph_data = radar_chart.render_data_uri()

        return jsonify({'graph_uri':graph_data})

if __name__ == '__main__':
    app.run()
