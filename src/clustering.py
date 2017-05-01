from get_team_coordinates import get_team_coordinates
import sqlite3
from get_database_connection import get_connection_object
import numpy
from sklearn.cluster import KMeans
from get_player_feature_vector import analyze_player

def clusterPlayers(db, match_id):
    home_x, home_y, home_player_ids, away_x, away_y, away_player_ids = get_team_coordinates(db,match_id)

    home_x = numpy.asarray(home_x)
    home_y = numpy.asarray(home_y)
    away_x = numpy.asarray(away_x)
    away_y = numpy.asarray(away_y)

    kmeans_home = KMeans(n_clusters=3, random_state=0).fit(home_y[1:].reshape([-1,1]))
    kmeans_away = KMeans(n_clusters=3, random_state=0).fit(away_y[1:].reshape([-1,1]))


    centres = kmeans_away.cluster_centers_

    order = [0,1,2]
    if centres[0] <= centres [1 ] and centres[1] <= centres[2]:
        order = [0,1,2]
    elif centres[0] <= centres [1 ] and centres[2] <= centres[1]:
        order = [0,2,1]
    elif centres[0] >= centres[1] and centres[2] >= centres[0]:
        order = [1,0,2]
    elif centres[0] >= centres [1] and centres[0] >= centres[2]:
        order = [1,2,0]
    elif centres[0] >= centres [2] and centres[1] >= centres[0]:
        order = [2,0,1]
    else:
        order = [2,1,0]


    kmeans_away = [ order[x] for x in kmeans_away.labels_]

    centres = kmeans_home.cluster_centers_

    order = [0,1,2]

    if centres[0] <= centres [1 ] and centres[1] <= centres[2]:
        order = [0,1,2]
    elif centres[0] <= centres [1 ] and centres[2] <= centres[1]:
        order = [0,2,1]
    elif centres[0] >= centres[1] and centres[2] >= centres[0]:
        order = [1,0,2]
    elif centres[0] >= centres [1] and centres[0] >= centres[2]:
        order = [1,2,0]
    elif centres[0] >= centres [2] and centres[1] >= centres[0]:
        order = [2,0,1]
    else:
        order = [2,1,0]



    kmeans_home = [ order[x] for x in kmeans_home.labels_]

    kmeans_home = [3]+kmeans_home
    kmeans_away = [3]+kmeans_away

    return home_player_ids, kmeans_home, away_player_ids, kmeans_away

'''
def aggregate_feature_vectors(db,match_id):

    home_player_ids, kmeans_home, away_player_ids, kmeans_away = clusterPlayers(db,match_id)
    feature_home = numpy.zeros([11,36])
    feature_away = numpy.zeros([11,36])
    for (i,home_id) in enumerate(home_player_ids):
        feature_home[i,:] = numpy.asarray(get_player_feature_vector(home_id))
    for (i,away_id) in enumerate(away_player_ids):
        feature_away[i,:] = numpy.asarray(get_player_feature_vector(away_id))
'''

db = get_connection_object()
match_id = 25579
#aggregate_feature_vectors(db,match_id)
clusterPlayers(db, 25579)