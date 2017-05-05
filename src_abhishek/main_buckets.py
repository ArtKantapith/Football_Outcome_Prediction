import pandas
import numpy
import scipy
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import numpy as np


match = pandas.read_csv("..\data\MatchCleaned.csv")
player_attributes = pandas.read_csv("..\data\Player_Attributes.csv")
matchid = match["id"].values.astype(int)
label = match.values[:,-1].astype(int)
playerid = player_attributes["player_api_id"].values.astype(int)
home_players_api_id = match.values[:,47:58]
home_players_x = match.values[:,3:14]
home_players_y = match.values[:,25:36]
away_players_api_id = match.values[:,58:69]
away_players_x = match.values[:,14:25]
away_players_y = match.values[:,36:47]
player_feature_dict = dict()
num_features = player_attributes.shape[1]-2

def analyze_player(player_id):

    if player_id not in player_feature_dict:
        player_feature_dict[player_id] = player_attributes.values[playerid==player_id,1:-1].astype(int).reshape(num_features)
    return player_feature_dict[player_id]

def bucket(match_id, bx, by):


    bucket_size_x = int(np.ceil(9.0/bx))
    bucket_size_y = int(np.ceil(11.0/by))
    home_x = home_players_x[matchid==match_id,:].reshape(11)
    home_y = home_players_y[matchid==match_id,:].reshape(11)
    away_x = away_players_x[matchid==match_id,:].reshape(11)
    away_y = away_players_y[matchid==match_id,:].reshape(11)

    print home_x, home_y
    print away_x, away_y

    home_x_buckets = np.floor(home_x/bx).astype(int)
    home_y_buckets = np.floor(home_y/by).astype(int)
    away_x_buckets = np.floor(away_x/bx).astype(int)
    away_y_buckets = np.floor(away_y/by).astype(int)

    print 'buckets'
    print home_x_buckets, home_y_buckets
    print away_x_buckets, away_y_buckets
    cluster_home = (home_x_buckets  + home_y_buckets * bucket_size_x)
    cluster_away = (away_x_buckets  + away_y_buckets * bucket_size_x)

    print cluster_home, cluster_away
    return cluster_home, cluster_away


def aggregate_feature_vectors(match_id, bucket_size_x, bucket_size_y):
    cluster_home, cluster_away = bucket( match_id, bucket_size_x, bucket_size_y )
    bucket_num_x = int(np.ceil(9.0 / bucket_size_x))
    bucket_num_y = int(np.ceil(11.0 / bucket_size_y))

    cluster_ids = bucket_num_x * bucket_num_y

    feature_home = numpy.zeros([11,num_features]).astype(int)
    feature_away = numpy.zeros([11,num_features]).astype(int)

    for (i,home_id) in enumerate(home_players_api_id[matchid==match_id,:].reshape(11)):
        feature_home[i,:] = numpy.asarray(analyze_player(home_id))
    feature_home = numpy.concatenate([feature_home,numpy.asarray(cluster_home).reshape([11,1])],axis = 1)

    for (i,away_id) in enumerate(away_players_api_id[matchid==match_id,:].reshape(11)):
        feature_away[i,:] = numpy.asarray(analyze_player(away_id))
    feature_away = numpy.concatenate([feature_away,numpy.asarray(cluster_away).reshape([11,1])],axis = 1)

    feature_home_final = numpy.zeros([cluster_ids,num_features]).astype(int)
    feature_away_final = numpy.zeros([cluster_ids,num_features]).astype(int)
    for i in xrange(0,cluster_ids):
        feature_home_final[i,:] = numpy.sum(feature_home[feature_home[:,36]==i,:-1],axis = 0).astype(int)
        feature_away_final[i,:] = numpy.sum(feature_away[feature_away[:,36]==i,:-1],axis = 0).astype(int)

    feature_home_final = feature_home_final.reshape([1,cluster_ids * num_features])
    feature_away_final = feature_away_final.reshape([1,cluster_ids * num_features])
    #print(feature_home_final.shape)
    print feature_home_final#, feature_away_final
    return feature_home_final, feature_away_final

bucket_size_x = int(np.ceil(9.0 / 3))
bucket_size_y = int(np.ceil(11.0 / 4))
cluster_ids = bucket_size_x * bucket_size_y
matchdata = numpy.zeros([match.shape[0], 2 * cluster_ids * num_features])

#aggregate_feature_vectors(10767, 3, 3)
'''
for (i,id) in enumerate(matchid):
    print i
    feature_home,feature_away = aggregate_feature_vectors(id, 3, 4)
    matchdata[i,:] = numpy.concatenate([feature_home,feature_away],axis = 1)

alldata = numpy.concatenate([matchdata,label.reshape([label.shape[0],1])],axis = 1)
numpy.savez("alldata_buckets_4x3.npz",alldata)

'''
