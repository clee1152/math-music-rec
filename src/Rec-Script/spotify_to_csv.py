import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

def extract_tracks_from_playlist(sp=None, playlist=None):
    if not playlist or not sp: 
        print("Parameter error: extract_tacks_from_playlist()")
        return
    tracks = []
    while playlist:
        for item in playlist['items']:
            tracks.append(item['track'])            
        playlist = sp.next(playlist) if playlist['next'] else None
    return tracks

def get_track_metadata(sp=None, tracks=[]):
    if not sp or not tracks:
        print("Parameter error: get_track_data()")
        return
    track_data = []
    for item in tracks:
        track = {}
        track['name'], track['id']= item['name'], item['id']
        artists, id_artists = [], []
        for artist in item['artists']:
            artists.append(artist['name'])
            id_artists.append(artist['id'])
        track['artists'], track['id_artists'] = artists, id_artists
        genres = []
        flag = False
        for id in id_artists:
            if id == None:
                flag = True
                break
            artist = sp.artist(id)
            genres.append(artist['genres'])
        track['genres'] = genres
        if not flag: track_data.append(track)
        print('Appended', track['name'], 'by', track['artists'])

    return track_data

def get_track_features(sp=None, track_data=[]):
    if not sp or not track_data:
        print("Parameter error: get_track_features()")
        return
    feature_list = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    for track in track_data:
        track_id = track['id']
        features = sp.audio_features(track_id)[0]
        for feature in feature_list:
            track[feature] = features[feature]
    return track_data

def to_csv(track_features=[]):
    if not track_features:
        print("Parameter error: to_csv()")
        return
    f = open('./my_tracks.csv', 'w')
    writer = csv.writer(f)
    features = ['id','name','artists','id_artists','genres','danceability','energy', 'key','loudness','mode','speechiness',
        'acousticness','instrumentalness','liveness','valence','tempo','time_signature']
    writer.writerow(features)
    for track in track_features:
        row = []
        for feature in features:
            row.append(track[feature])
        writer.writerow(row)
    f.close()
    print("\nWritten track data to my_tracks.csv successfully.\n")

def spotify_to_csv(ID, SECRET, URI, PLAYLIST_ID=None):

    if not PLAYLIST_ID:
        print("Not a valid playlist.")
        return
    scope = ['user-library-read']
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ID,client_secret=SECRET,redirect_uri=URI,scope=scope))
    playlist = sp.user_playlist_tracks(playlist_id=PLAYLIST_ID) 
    tracks = extract_tracks_from_playlist(sp, playlist)
    track_data = get_track_metadata(sp, tracks)
    track_features = get_track_features(sp, track_data)
    to_csv(track_features)
    return sp

def get_sp():
    file = open('creds.txt', 'r')
    ID = file.readline()[:-1]
    SECRET = file.readline()[:-1]
    URI = file.readline()[:-1]
    file.close()
    scope = ['user-library-read', 'user-read-currently-playing', 'user-read-playback-state', 'user-top-read']
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ID,client_secret=SECRET,redirect_uri=URI,scope=scope))
    return sp