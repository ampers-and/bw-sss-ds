# Spotify Song Recommender

The scope of this project was to build an application that uses the Spotify API along with Machine Learning techniques to recommend songs that users are likely to enjoy. 

###Available Data

We initially took a look at the [Spotify Audio Feature dataset on Kaggle.](https://www.kaggle.com/tomigelo/spotify-audio-features) This dataset has 17 features in total, 13 of which are actual audio features. 

![alt text](https://github.com/bw-spotify-oct/ds/blob/master/img/feat.png "Logo Title Text 1")

For the purpose of creating a model, we dropped “artist_name”, “track_name”, and “popularity”. Popularity is an interesting feature due to the fact that it does hold predictive power but is not entirely useful for our model because it is not a constant variable. Songs that have a high popularity score today may not have the same score tomorrow.

####Here is a rundown of the features we used:

duration_ms - The duration of the track

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

