from flask import Flask, render_template, request, url_for, redirect,jsonify
from get_data import *
from decouple import config
from dotenv import load_dotenv
from work_data import *

load_dotenv()

API_KEY = config("API_KEY")

app = Flask(__name__)


@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/songs/<key>/<value>')
def song_search(key,value):
    if key == API_KEY:
        songs = get_songs(value)
        return(jsonify(songs))

@app.route('/features/<key>/<value>')
def song_features(key,value):
    if key == API_KEY:
        features = get_features(value)
        return(jsonify(features))

@app.route('/recs/<key>/<value>')
def recommendations(key,value):
    if key == API_KEY:
        recs = Five_recs(value)
        all_recs = recs.get_100()
        feature_df = recs.get_all_features(all_recs)
        target_song = recs.get_all_features(value)
        five_recs_df = recs.top_recs(feature_df, target_song)
        five_recs = recs.feedback(five_recs_df)

        return(jsonify(five_recs))


@app.route('/embed/<key>/<value>')
def embed(key,value):

    if key == API_KEY:
        recs = Five_recs(value)
        all_recs = recs.get_100()
        feature_df = recs.get_all_features(all_recs)
        target_song = recs.get_all_features(value)
        five_recs_df = recs.top_recs(feature_df, target_song)
        five_recs = recs.feedback(five_recs_df)
        return(render_template('embed.html', five_recs=five_recs))

if __name__ == '__main__':
    app.run()
