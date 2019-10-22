from flask import Flask, render_template, request, url_for, redirect,jsonify
from decouple import config
from dotenv import load_dotenv
from work_data import *
import pygal


load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/songs/<value>')
def song_search(value):
    songs = Rec_Helper().get_songs(value)
    return(jsonify(songs))

@app.route('/features/<value>')
def song_features(value):
    features = Rec_Helper().get_features(value)
    return(jsonify(features))

@app.route('/recs/<value>')
def recommendations(value):
    recs = Rec_Helper().feedback(value)

    return(jsonify(recs))

@app.route('/embed/<value>')
def embed(value):
    recs = Rec_Helper().feedback(value)

    return(render_template('embed.html', recs=recs))

@app.route('/graph/<value>')
def graph(value):
    rec_helper = Rec_Helper()
    recs = rec_helper.top_recs(value)

    features = pd.concat([rec_helper.get_all_features([value]), recs])

    radar_chart = pygal.Radar()
    radar_chart.title = 'Comparison of Recommendations for \"' + rec_helper.spotify.track(value)['name'] + '\"'
    radar_chart.x_labels = list(features.keys())

    for name, feature_vec in zip(features.id, features.drop('id', axis=1).values):
        radar_chart.add(rec_helper.spotify.track(name)['name'],
                        rec_helper.spot_scaler.transform([feature_vec])[0])

    graph_data = radar_chart.render_data_uri()

    return(render_template('radio.html', graph_data = graph_data, title='Song Feature Graph'))

if __name__ == '__main__':
    app.run()
