import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import ParameterGrid
from sklearn.cluster import KMeans
from sklearn import metrics
import heapq
import csv

def transform_data():
    features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    data = pd.read_csv('./my_tracks.csv')
    tracks_data = data.copy()[features]
    tracks_data[tracks_data.columns] = StandardScaler().fit_transform(tracks_data)
    return data, tracks_data

def pca_kmeans_centroids(tracks_data=None):

    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(tracks_data)
    print()
    print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
    print('Cumulative variance explained by 3 principal components: {:.2%}'.format(np.sum(pca.explained_variance_ratio_)))

    parameters = [i for i in range(2,max(2,int(np.sqrt(tracks_data.shape[0]))))]
    parameter_grid = ParameterGrid({'n_clusters': parameters})
    best_score = -1
    kmeans_model = KMeans()
    silhouette_scores = []
    for p in parameter_grid:
        kmeans_model.set_params(**p) 
        kmeans_model.fit(tracks_data)          
        ss = metrics.silhouette_score(tracks_data, kmeans_model.labels_)
        silhouette_scores += [ss]
        if ss > best_score:
            best_score = ss
            best_grid = p
    

    kmeans = KMeans(n_clusters=best_grid['n_clusters'])
    kmeans.fit(tracks_data)
    centroids = kmeans.cluster_centers_
    centroids_pca = pca.transform(centroids)
    x = pca_result[:, 0]
    y = pca_result[:, 1]
    z = pca_result[:, 2]

    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(silhouette_scores)
    ax1.set_xlabel('number of clusters')
    ax1.set_ylabel('silhouette score')
    ax1.title.set_text('n_cluster\'s silhouette scores')
    ax2 = fig.add_subplot(1,2,2, projection='3d')
    ax2.scatter3D(centroids_pca[:, 0], centroids_pca[:, 1], centroids_pca[:, 2], marker='X', s=200, linewidths=1.5,
                color='red', edgecolors="black", lw=1.5)
    ax2.scatter3D(x, y, z, c=kmeans.labels_, alpha=0.5, s=200)
    ax2.set_xlabel("PC 1")
    ax2.set_ylabel("PC 2")
    ax2.set_zlabel("PC 3")
    ax2.title.set_text('track clusters')

    return centroids

def get_centroid_tracks(centroids=[], data=None, tracks_data=None):
    copy = data.copy(deep=True)
    features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    for feature in features:
        copy[feature] = tracks_data[feature]
    centroid_entries, tracks = [], []
    copy = copy.values.tolist()
    for centroid in centroids:
        points = []
        for entry in copy:
            dist = 0   
            for i in range(len(centroid)):
                dist += (abs(entry[i + 5] - centroid[i]) ** 2)
            points.append([dist, entry])
        heapq.heapify(points)
        dist, entry = heapq.heappop(points)
        centroid_entries.append(entry)
    identifiers = ['id', 'name', 'artists', 'id_artists', 'genres']
    for entry in centroid_entries:
        track = {}
        for i in range(len(identifiers)):
            track[identifiers[i]] = entry[i]
        tracks.append(track)
    data = data.values.tolist()
    for track in tracks:
        for item in data:
            if track['id'] == item[0]:
                for i in range(len(features)):
                    track[features[i]] = item[i + 5]
    return tracks

def filter_tracks(popularity=0):
    if popularity > 100 or popularity < 0:
        print("Popularity score must be between 0 and 100 inclusive.")
        return
    
    with open('tracks.csv', 'r') as inp, open('track_recs.csv', 'w') as out:
        writer = csv.writer(out)
        for i, row in enumerate(csv.reader(inp)):
            if i == 0: continue
            if int(row[3]) >= popularity: 
                writer.writerow(row)
    inp.close()
    out.close()

def get_recommendations(num_recs=5):
    data, tracks_data = transform_data()
    all_tracks = pd.read_csv('./track_recs.csv')
    my_tracks = pd.read_csv('./my_tracks.csv')['id'].to_list()
    centroids = pca_kmeans_centroids(tracks_data)
    centroid_tracks = get_centroid_tracks(centroids, data, tracks_data)
    all_tracks = all_tracks.values.tolist()
    recommendations = []
    features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    for centroid in centroid_tracks:
            points = []
            centroid_genres = centroid['genres'].replace('[', '').replace(']', '').replace("'", "").split(", ")
            for entry in all_tracks:
                if entry[0] == 'id': continue
                dist = 0   
                for i, feature in enumerate(features):
                    dist += (abs(entry[i + 9] - abs(centroid[feature])) ** 2)
                entry_genres = entry[len(entry) - 1].replace('[', '').replace(']', '').replace("'", "").split(", ")
                for genre in entry_genres:
                    if genre in centroid_genres and entry[1] not in my_tracks:
                        points.append([dist, entry, centroid])
                        break
            heapq.heapify(points)
            for i in range(num_recs):
                if len(points) < 3: continue
                dist, entry, centroid = heapq.heappop(points)
                recommendation = [entry, centroid]
                recommendations.append(recommendation)
    
    return num_recs, recommendations

def get_genres(sp, start_from, end=600000):

    tracks = pd.read_csv('./tracks.csv')
    id_artists = tracks['id_artists'].tolist()
    for i, each in enumerate(id_artists):
        each = each[1:len(each)-1].replace("'","").split(", ")
        id_artists[i] = each
        
    f = open('./genres.csv', 'a')
    writer = csv.writer(f)
    for i in range(start_from-2, min(len(id_artists), end)):
        genres = []
        for j in range(len(id_artists[i])):
            artist = sp.artist(id_artists[i][j])
            for genre in artist['genres']:
                genres.append(genre)
        genres = genres if len(genres) > 0 else ['none']
        writer.writerow([id_artists[i], genres])
        print("%6d %s %s" % (i, id_artists[i], genres))
    f.close()

def append_genres():
    tracks = pd.read_csv('tracks.csv')
    genres = pd.read_csv('genres.csv')['genres']
    new_tracks = tracks.join(genres)
    new_tracks.to_csv('modified_tracks.csv')

def print_recs(recommendations, popularity, num_recs):
    print("\n-------------------- Mathematical Music Recommendations --------------------\n")
    print("---------- Drawn from songs with a score of %2d out of 100 popularity --------\n" % (popularity))
    for i in range(0, len(recommendations), num_recs):
        recommendations[i][1]['artists'] = recommendations[i][1]['artists'][1:len(recommendations[i][1]['artists'])-1].replace("'","")
        print(recommendations[i][1]['name'].ljust(40), 'by', recommendations[i][1]['artists'], 'recommends...\n')
        for j in range(i, i + num_recs):
            if j < len(recommendations):
                count = j % num_recs
                recommendations[j][0][6] = recommendations[j][0][6].replace("'", "").replace("[","").replace("]","")
                print("%3d:" % (count + 1), recommendations[j][0][2].ljust(40), 'by', recommendations[j][0][6])
        print()
    print("--------------------------------------------------------------------------------\n")
        
    plt.show()