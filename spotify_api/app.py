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

if __name__ == '__main__':
    app.run()
