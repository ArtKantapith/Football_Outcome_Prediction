from collections import defaultdict
from get_database_connection import get_connection_object
from get_player_attributes import get_player_attributes

def getAverage():
    string = '[73.460353168579573,"medium","medium",49.9210776337,57.2660230859,62.4296720577,49.4684357157,59.1751537059,52.9656745649,49.3809503009,57.0698802022,63.3888785751,67.6593572201,68.0512443896,65.9709099937,66.1037064136,65.1894960417,61.8084273405,66.9690453204,67.0385438621,67.4245285079,53.3394306058,60.9480457787,52.0092714943,55.786504461,57.8735497752,55.0039859781,46.7722423038,50.3512574942,48.001461948,14.7043933123,16.0636118422,20.9983619268,16.1321542847,16.4414388835]'
    av = eval(string)
    return av

def analyze_player(player_id):

    conn = get_connection_object()
    player_data = get_player_attributes(conn, player_id)
    ran = range(7,len(player_data))
    ran = [5] + ran
    feature =[]
    avvector = getAverage()
    for index in ran :
        feature.append(player_data[index])
    for i in xrange(0,len(feature)):
        if i in (1,2):
            if feature[i] not in ("high","medium","low"):
                feature[i] = 1
        else:
            if feature[i] == None:
                feature[i] = int(avvector[i])
    for i in (1,2):
        if feature[i]=="high":
            feature[i]=2
        if feature[i]=="medium":
            feature[i]=1
        if feature[i]=="medium":
            feature[i]=0
    return feature
