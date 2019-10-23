# Spotify Song Recommender

The scope of this project was to build an application that uses the Spotify API along with Machine Learning techniques to recommend songs that users are likely to enjoy. 

### Available Data

We initially took a look at the [Spotify Audio Feature dataset on Kaggle.](https://www.kaggle.com/tomigelo/spotify-audio-features) This dataset has 17 features in total, 13 of which are actual audio features. 

![alt text](https://github.com/bw-spotify-oct/ds/blob/master/img/feat.png "Logo Title Text 1")

For the purpose of creating a model, we dropped “artist_name”, “track_name”, and “popularity”. Popularity is an interesting feature due to the fact that it does hold predictive power but is not entirely useful for our model because it is not a constant variable. Songs that have a high popularity score today may not have the same score tomorrow.

#### Here is a rundown of the features we used:

**duration_ms** - The duration of the track

**key** - The estimated overall key of the track.

**mode** - Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived.

**time_signature** - An estimated overall time signature of a track

**acousticness** - A confidence measure from 0.0 to 1.0 of whether the track is acoustic

**danceability** - Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.

**energy** - Energy is a measurement that represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.

**instrementalness** - Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”.

 **liveness** - Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live

**loudness** - Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude).

**speechiness** - Speechiness detects the presence of spoken words in a track.

**valence** - A measurement describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

**tempo** - In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.

### Creating a Neural Network 

Ian can fill this section out 

### RESTful API with Flask 

To power the Data Science aspect of this project, we needed to build a platform that received calls from the user application, collected data from the Spotify API, implemented our model, and then return rendered data back to the user application. 


![alt text](https://github.com/bw-spotify-oct/ds/blob/master/img/api.png "Logo Title Text 1")

#### Here are a few important calls we created for the API:
**Song search functionality** - Returns seven songs related to the user search query.

~~~
https://spotify-api-helper.herokuapp.com/songs/<api_key>/<user_query>
~~~

**Returns**
~~~
[
{"artist":"Florida Georgia Line","id":"498ZVInMGDkmmNVpSWqHiZ","song_name":"May We All","uri":"spotify:track:498ZVInMGDkmmNVpSWqHiZ"},
{"artist":"Florida Georgia Line","id":"58zWN3BNikOH7zVP6QGBZp","song_name":"May We All - Acoustic","uri":"spotify:track:58zWN3BNikOH7zVP6QGBZp"},
{"artist":"Florida Georgia Line","id":"6RHDliBPKS2TShFp7UIHF0","song_name":"May We All","uri":"spotify:track:6RHDliBPKS2TShFp7UIHF0"},
{"artist":"Florida Georgia Line","id":"6GIei0QWZjbrNWNwtTpiQL","song_name":"May We All - Commentary","uri":"spotify:track:6GIei0QWZjbrNWNwtTpiQL"},
{"artist":"Crooks UK","id":"37KWDhJ3fyBAFVcC0Hutan","song_name":"May Be","uri":"spotify:track:37KWDhJ3fyBAFVcC0Hutan"},
{"artist":"Florida Georgia Line","id":"0ONccS8Kchy2jgbhF5lg1i","song_name":"May We All","uri":"spotify:track:0ONccS8Kchy2jgbhF5lg1i"},
{"artist":"Roky Erickson","id":"6VbF4Hm5LTYgKH9R7ss2zZ","song_name":"We Are Never Talking","uri":"spotify:track:6VbF4Hm5LTYgKH9R7ss2zZ"}
]
~~~

**Graph URI & Recommended Song Data** - Returns the graph URI and five recommended songs based on a single song ID. 

~~~
https://spotify-api-helper.herokuapp.com/graph_data/<api_key>/<track_id>
~~~

**Returns**
~~~
[
{"graph_uri":"data:image/svg+xml;charset=utf-8;base64,PD94b...2c+PC9zdmc+"},
[{"artist":"Florida Georgia Line","id":"498ZVInMGDkmmNVpSWqHiZ","large_image":"https://i.scdn.co/image/205ec78bebfdc739bb3bb91076306e24f03c7d2c","med_image":"https://i.scdn.co/image/9ce932460729587fd8dccdac9214d741e127e162","small_image":"https://i.scdn.co/image/edc3a84866acc208acb5dbca21f05dda9a7eae99","song_name":"May We All","uri":"spotify:track:498ZVInMGDkmmNVpSWqHiZ"},
{"artist":"Maren Morris","id":"58spuRyMUsjKHQHEGwLC99","large_image":"https://i.scdn.co/image/ab67616d0000b2738bd4a20032a613d28e909109","med_image":"https://i.scdn.co/image/ab67616d00001e028bd4a20032a613d28e909109","small_image":"https://i.scdn.co/image/ab67616d000048518bd4a20032a613d28e909109","song_name":"80s Mercedes","uri":"spotify:track:58spuRyMUsjKHQHEGwLC99"},
{"artist":"Dustin Lynch","id":"2YMhrXQYKkm4kXLcXKKd5z","large_image":"https://i.scdn.co/image/ab67616d0000b2734686b4078ad5eb92315d28e0","med_image":"https://i.scdn.co/image/ab67616d00001e024686b4078ad5eb92315d28e0","small_image":"https://i.scdn.co/image/ab67616d000048514686b4078ad5eb92315d28e0","song_name":"Small Town Boy","uri":"spotify:track:2YMhrXQYKkm4kXLcXKKd5z"},
{"artist":"Maren Morris","id":"4H0vNUFcHPz5lytcLjwqkr","large_image":"https://i.scdn.co/image/ab67616d0000b2738bd4a20032a613d28e909109","med_image":"https://i.scdn.co/image/ab67616d00001e028bd4a20032a613d28e909109","small_image":"https://i.scdn.co/image/ab67616d000048518bd4a20032a613d28e909109","song_name":"Rich","uri":"spotify:track:4H0vNUFcHPz5lytcLjwqkr"},
{"artist":"Cole Swindell","id":"3y1t2sEahs8idFz2tiYNPO","large_image":"https://i.scdn.co/image/ab67616d0000b2734f239e3ce20b8e350244e84a","med_image":"https://i.scdn.co/image/ab67616d00001e024f239e3ce20b8e350244e84a","small_image":"https://i.scdn.co/image/ab67616d000048514f239e3ce20b8e350244e84a","song_name":"Let Me See Ya Girl","uri":"spotify:track:3y1t2sEahs8idFz2tiYNPO"},
{"artist":"Jon Pardi","id":"0bPnT6i9H1p8Vd85GS6Z7I","large_image":"https://i.scdn.co/image/ab67616d0000b2730504a96f206bc32ebe198b83","med_image":"https://i.scdn.co/image/ab67616d00001e020504a96f206bc32ebe198b83","small_image":"https://i.scdn.co/image/ab67616d000048510504a96f206bc32ebe198b83","song_name":"Night Shift","uri":"spotify:track:0bPnT6i9H1p8Vd85GS6Z7I"}]
]
~~~

**This is what the rended URI of the chart looks like.**
![alt text](https://github.com/bw-spotify-oct/ds/blob/master/img/chart.png "Logo Title Text 1")
