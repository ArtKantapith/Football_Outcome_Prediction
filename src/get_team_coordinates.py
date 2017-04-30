import sqlite3
from get_database_connection import get_connection_object


def get_team_coordinates(conn, match_id, plot_formation = False):
    cur = conn.cursor()
    sql = 'SELECT * From MATCH  WHERE id=?'
    cur.execute(sql, (match_id,))
    match = cur.fetchone()
    if(match == None):
        return None
    #print("match", match)
    home_players_api_id = list()
    away_players_api_id = list()
    home_players_x = list()
    away_players_x = list()
    home_players_y = list()
    away_players_y = list()


    for i in range(1, 12):
        home_players_api_id.append(match['home_player_%d' % i])
        away_players_api_id.append(match['away_player_%d' % i])
        home_players_x.append(match['home_player_X%d' % i])
        away_players_x.append(match['away_player_X%d' % i])
        home_players_y.append(match['home_player_Y%d' % i])
        away_players_y.append(match['away_player_Y%d' % i])

    #print('Example, home players api id: ')
    #print(home_players_api_id)
    players_api_id = [home_players_api_id, away_players_api_id]
    players_api_id.append(home_players_api_id)  # Home
    players_api_id.append(away_players_api_id)  # Away
    players_names = [[None] * 11, [None] * 11]

    for i in range(2):
        players_api_id_not_none = [x for x in players_api_id[i] if x is not None]
        sql = 'SELECT player_api_id,player_name FROM Player'
        sql += ' WHERE player_api_id IN (' + ','.join(map(str, players_api_id_not_none)) + ')'
        cur.execute(sql)
        players = cur.fetchall()
        for player in players:
            idx = players_api_id[i].index(player['player_api_id'])
            name = player['player_name'].split()[-1]  # keep only the last name
            players_names[i][idx] = name

    #print('Home team players names:')
    #print(players_names[0])
    #print('Away team players names:')
    #print(players_names[1])
    home_players_x = [5 if x == 1 else x for x in home_players_x]
    away_players_x = [5 if x == 1 else x for x in away_players_x]
    import matplotlib.pyplot as plt

    # Home team (in blue)
    plt.subplot(2, 1, 1)
    plt.rc('grid', linestyle="-", color='black')
    plt.rc('figure', figsize=(12, 20))
    plt.gca().invert_yaxis()  # Invert y axis to start with the goalkeeper at the top

    for label, x, y in zip(players_names[0], home_players_x, home_players_y):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-20, 20),
            textcoords='offset points', va='bottom')


    plt.scatter(home_players_x, home_players_y, s=480, c='blue')
    plt.grid(True)

    # Away team (in red)
    plt.subplot(2, 1, 2)
    plt.rc('grid', linestyle="-", color='black')
    plt.rc('figure', figsize=(12, 20))
    plt.gca().invert_xaxis()  # Invert x axis to have right wingers on the right
    for label, x, y in zip(players_names[1], away_players_x, away_players_y):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-20, 20),
            textcoords='offset points', va='bottom')

    plt.scatter(away_players_x, away_players_y, s=480, c='red')
    plt.grid(True)

    ax = [plt.subplot(2, 2, i + 1) for i in range(0)]
    for a in ax:
        a.set_xticklabels([])
        a.set_yticklabels([])
    plt.subplots_adjust(wspace=0, hspace=0)

    if(plot_formation):
        plt.show()
    from collections import Counter

    players_y = [home_players_y, away_players_y]
    formations = [None] * 2
    for i in range(2):
        formation_dict = Counter(players_y[i]);
        sorted_keys = sorted(formation_dict)
        formation = ''
        for key in sorted_keys[1:-1]:
            y = formation_dict[key]
            formation += '%d-' % y
        formation += '%d' % formation_dict[sorted_keys[-1]]
        formations[i] = formation

    #print('Home team formation: ' + formations[0])
    #print('Away team formation: ' + formations[1])

    return home_players_x, home_players_y, home_players_api_id, away_players_x, away_players_y, away_players_api_id
