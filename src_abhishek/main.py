import pandas
import numpy
import scipy
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder

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

def Clustering(match_id):

    home_x = home_players_x[matchid==match_id,:].reshape(11)
    home_y = home_players_y[matchid==match_id,:].reshape(11)
    away_x = away_players_x[matchid==match_id,:].reshape(11)
    away_y = away_players_y[matchid==match_id,:].reshape(11)

    kmeans_home = KMeans(n_clusters=3, random_state=0).fit(home_y[1:].reshape([-1,1]))
    kmeans_away = KMeans(n_clusters=3, random_state=0).fit(away_y[1:].reshape([-1,1]))

    centres = kmeans_away.cluster_centers_
    order = numpy.argsort(centres,axis = 0).reshape(3)
    away_dict = dict()
    for entry in order:
        away_dict[order[entry]] = entry

    centres = kmeans_home.cluster_centers_
    order = numpy.argsort(centres,axis = 0).reshape(3)
    home_dict = dict()

    for entry in order:
        home_dict[order[entry]] = entry
    kmeans_away = [away_dict[x]+1 for x in kmeans_away.labels_]
    kmeans_home = [home_dict[x]+1 for x in kmeans_home.labels_]

    kmeans_home = [0]+kmeans_home
    kmeans_away = [0]+kmeans_away
    return kmeans_home, kmeans_away



def aggregate_feature_vectors(match_id):
    kmeans_home, kmeans_away = Clustering(match_id)
    feature_home = numpy.zeros([11,num_features]).astype(int)
    feature_away = numpy.zeros([11,num_features]).astype(int)
    for (i,home_id) in enumerate(home_players_api_id[matchid==match_id,:].reshape(11)):
        feature_home[i,:] = numpy.asarray(analyze_player(home_id))
    feature_home = numpy.concatenate([feature_home,numpy.asarray(kmeans_home).reshape([11,1])],axis = 1)

    for (i,away_id) in enumerate(away_players_api_id[matchid==match_id,:].reshape(11)):
        feature_away[i,:] = numpy.asarray(analyze_player(away_id))
    feature_away = numpy.concatenate([feature_away,numpy.asarray(kmeans_away).reshape([11,1])],axis = 1)

    feature_home_final = numpy.zeros([4,num_features]).astype(int)
    feature_away_final = numpy.zeros([4,num_features]).astype(int)
    for i in xrange(1,4):
        feature_home_final[i,:] = numpy.mean(feature_home[feature_home[:,36]==i,:-1],axis = 0).astype(int)
        feature_away_final[i,:] = numpy.mean(feature_away[feature_away[:,36]==i,:-1],axis = 0).astype(int)

    feature_home_final[0,:] = feature_home[0,:-1].astype(int)
    feature_away_final[0,:] = feature_away[0,:-1].astype(int)
    feature_home_final = feature_home_final.reshape([1,4*num_features])
    feature_away_final = feature_away_final.reshape([1,4*num_features])
    return feature_home_final, feature_away_final

matchdata = numpy.zeros([match.shape[0],8*num_features])
for (i,id) in enumerate(matchid):
    print i
    feature_home,feature_away = aggregate_feature_vectors(id)
    matchdata[i,:] = numpy.concatenate([feature_home,feature_away],axis = 1)

alldata = numpy.concatenate([matchdata,label.reshape([label.shape[0],1])],axis = 1)
numpy.savez("alldata.npz",alldata)
