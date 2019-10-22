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
    return(render_template('home.html'))


@app.route('/songs/<key>/<value>')
def song_search(key, value):
    if key == API_KEY:
        songs = Rec_Helper().get_songs(value)
        return(jsonify(songs))


@app.route('/features/<key>/<value>')
def song_features(key, value):
    if key == API_KEY:
        features = Rec_Helper().get_features(value)
        return(jsonify(features))


@app.route('/recs/<key>/<value>')
def recommendations(key, value):
    if key == API_KEY:
        recs = Rec_Helper().rec_data(value)

        return(jsonify(recs))


@app.route('/embed/<key>/<value>')
def embed(key, value):
    if key == API_KEY:
        recs = Rec_Helper().rec_data(value)

        return(render_template('embed.html', recs=recs))


@app.route('/graph/<key>/<value>')
def graph(key, value):
    if key == API_KEY:
        rec_helper = Rec_Helper()
        recs = rec_helper.top_recs(value)

        features = pd.concat([rec_helper.get_all_features([value]), recs])

        radar_chart = pygal.Radar()
        radar_chart.title = ('Comparison of Recommendations for \"' +
                             rec_helper.spotify.track(value)['name'] + '\"')
        radar_chart.x_labels = list(features.keys())

        for id, feature_vec in zip(features.id, features.drop('id', axis=1).values):
            radar_chart.add(rec_helper.spotify.track(id)['name'],
                            rec_helper.spot_scaler.transform([feature_vec])[0])

        graph_data = radar_chart.render_data_uri()

        return(render_template('radar.html',
                                graph_data=graph_data,
                                title='Song Feature Graph'))

@app.route('/graph_data/<key>/<value>')
def graph_data(key, value):
    if key == API_KEY:
        rec_helper = Rec_Helper()
        recs = rec_helper.top_recs(value)

        features = pd.concat([rec_helper.get_all_features([value]), recs])

        feat_dict = rec_helper.songs_data(features)
        radar_chart = pygal.Radar()
        radar_chart.title = ('Comparison of Recommendations for \"' +
                             rec_helper.spotify.track(value)['name'] + '\"')
        radar_chart.x_labels = list(features.keys())

        for id, feature_vec in zip(features.id, features.drop('id', axis=1).values):
            radar_chart.add(rec_helper.spotify.track(id)['name'],
                            rec_helper.spot_scaler.transform([feature_vec])[0])

        graph_data = radar_chart.render_data_uri()
        graph_dict = [{'graph_uri':graph_data},feat_dict]
        return(jsonify(graph_dict))


@app.route('/mood/<key>', methods=['GET'])
def mood(key):
    if key == API_KEY:
        rec_helper = Rec_Helper()
        recs = rec_helper.mood()


        return(jsonify(recs))

if __name__ == '__main__':
    app.run()
