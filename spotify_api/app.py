from flask import Flask, render_template, request, url_for, redirect, jsonify

from decouple import config
from dotenv import load_dotenv
from work_data import *
from flask_cors import CORS
import pygal

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

        radar_chart = pygal.Radar()
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
        radar_chart = pygal.Radar()
        radar_chart.title = ('Comparison of Recommendations for \"' +
                             spotify.track(value)['name'] + '\"')
        radar_chart.x_labels = list(features.drop('id', axis=1).keys())

        for id, feature_vec in zip(features.id, features.drop('id', axis=1).values):
            radar_chart.add(spotify.track(id)['name'],
                            spot_scaler.transform([feature_vec])[0])

        graph_data = radar_chart.render_data_uri()
        graph_dict = [{'graph_uri':graph_data},feat_dict]
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



if __name__ == '__main__':
    app.run()
