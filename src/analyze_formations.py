from get_formation_and_plot import get_formation
from collections import defaultdict

match_min_id  = 1
match_max_id = 25979



def analyze():
    away_formation_dict = defaultdict(int)
    home_formation_dict = defaultdict(int)
    for match_id in xrange(match_min_id, match_max_id):
        formations = get_formation(match_id)
        if(formations == None):
            continue
        home_formation = formations[0]
        away_formation = formations[1]
        home_formation_dict[home_formation] += 1
        away_formation_dict[away_formation] += 1

    return home_formation_dict, away_formation_dict

#home_dict, away_dict = analyze()
#print home_dict
