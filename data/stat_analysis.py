#temp
def f1 (x, y):
    print (x+y)
    return x + y

def f2(a, b):
    return[["a", "b"], [a,b]]


import csv, sqlite3

def build_nhl_database():
    conn = sqlite3.connect(":memory:")

    create_game_table(conn)

def create_game_table(conn):
    cur = conn.cursor()
    cur.execute("create table game (game_id,season,type,date_time,\
                 away_team_id,home_team_id,away_goals,home_goals,outcome,\
                 home_rink_side_start,venue,venue_link,venue_time_zone_id,\
                 venue_time_zone_offset,venue_time_zone_tz)")
    with open('data/game.csv', 'rb') as fin:
        data_read = csv.reader(fin)
        for row in data_read:
            print row
            return


    
