from collections import defaultdict
from get_database_connection import get_connection_object
from get_player_attributes import get_player_attributes

player_min_id  = 1
player_max_id = 25979



def analyze_player():

    conn = get_connection_object()
    player_data = get_player_attributes(conn, 505942)
    if(player_data == None):
        return

analyze_player()
#print home_dict
