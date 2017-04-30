from get_formation_and_plot import get_formation

match_min_id  = 1
match_max_id = 25979

def analyze():
    for match_id in xrange(match_min_id, match_max_id):
        formations = get_formation(match_id)
    print formations

analyze()