This app has two components:

1. A ReactJS component. This component allows a user to get their playlist and their IDs.

2. A Python component in Rec-Script. This component gives recommendations based on the tracks in a user's playlist. The script takes 3 arguments: the playlist ID, the popularity of the recommendations they prefer on a scale of 1- 100, and the number of recommendations.

In order to run the python script, one must have the following Kaggle dataset downloaded into the Rec-Scripts directory:

https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks
