import sqlite3

def get_player_attributes(conn, player_id):
    cur = conn.cursor()
    sql = 'SELECT * FROM Player_Attributes'
    sql += ' WHERE player_api_id IN (' + ','.join(map(str, [player_id])) + ')'
    cur.execute(sql)
    player_data = cur.fetchall()
    print player_data
    return player_data