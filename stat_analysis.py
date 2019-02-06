# file to contain function pertaining to stat analysis of NHL data
#  Purpose: provide answers for questions in Infutor prompt in a method
#           that is generalized and reusable
#
# functions organized into different group
#   1) functions to create an sqlite database from csv copies of nhl data
#   2) functions to query created database and find statistics
#   3) functions to create visualizations

import csv, sqlite3, matplotlib.pyplot as plt

######################   Start of query functions for stats   ###################
######################              Player Stats              ###################

#calculate average shifts per game for a player
# input: conn - database connection
#        player_first_name
#        player_last_name
#        season - season, ex. 20162017
def shifts_per_game(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    try:
        player_id = cur.fetchone()[0]
    except:
        print("Failed to find that player in that season")
        return 0
    
    #need to select count of number of shifts during the season(s)
    # for which that player participated
    cur.execute("Select count(*) from\
                (Select game_id s \
                   from game_shifts \
                   inner join \
                   (Select game_id g from game where season=?) \
                   on s = g \
                 where player_id=?) "\
                ,(season,player_id,))
    try:
        total_shifts = cur.fetchone()[0]
    except:
        total_shifts = 0

    #need to select count of number of games during the season(s)
    # for which that player participated
    cur.execute("Select count(*) from\
                (Select game_id s from game_shifts\
                   inner join \
                   (Select game_id g from game where season=?) \
                   on s = g \
                   where player_id=? group by game_id)" \
                ,(season,player_id,))
    try:
        total_games = cur.fetchone()[0]
    except:
        print("That player played 0 games this season")
        return 0

    return total_shifts / (total_games*1.0)

    #also could have used only 1 query by grouping shift counts by game, and using
    #  sql AVG over the result

#calculate average time per shift across season
# input: conn - database connection
#        player_first_name
#        player_last_name
#        season - season, ex. 20162017
def time_per_shift(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    try:
        player_id = cur.fetchone()[0]
    except:
        print("Failed to find that player in that season")
        return 0
    
    #shift start and end are integers of seconds since start of game

    cur.execute("Select shift_start, shift_end \
                 from game_shifts s \
                 inner join (Select game_id g from game where season=?) \
                 on s.game_id = g \
                 where player_id=?",(season,player_id,))
    
    shifts = cur.fetchall()
    total_time = 0
    for shift in shifts:
        total_time += shift[1] - shift[0]

    if(len(shifts)==0):
        print("That player played 0 games this season")
        return 0
    
    return total_time / (len(shifts) * 1.0)

#calculate average number of shots per game for a player
# input: conn - database connection
#        player_first_name
#        player_last_name
#        season - season, ex. 20162017
def shots_per_game(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    try:
        player_id = cur.fetchone()[0]
    except:
        print("Failed to find that player in that season")
        return 0

    #collect data from game_skater_stats for total shots
    cur.execute("Select Sum(shots) from game_skater_stats  \
                    inner join (Select game_id g from game where season=?) \
                    on game_skater_stats.game_id=g \
                    where player_id=?",(season,player_id,))
    try:
        total_shots = cur.fetchone()[0]
    except:
        total_shots=0

    #need to select count of number of games during the season(s)
    # for which that player participated
    cur.execute("Select count(*) from\
                (Select game_id s from game_shifts\
                   inner join \
                   (Select game_id g from game where season=?) \
                   on s = g \
                   where player_id=? group by game_id)" \
                ,(season,player_id,))
    try:
        total_games = cur.fetchone()[0]
    except:
        print("That player played 0 games this season")
        return 0
    return total_shots / (total_games * 1.0)

    

#calculate average number of shots per game for a player
# input: conn - database connection
#        player_first_name
#        player_last_name
#        season - season, ex. 20162017
def goals_per_game(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    try:
        player_id = cur.fetchone()[0]
    except:
        print("Failed to find that player in that season")
        return 0

    #collect data from game_skater_stats for total goals
    #  effectively the same problem as total shots
    cur.execute("Select Sum(goals) from game_skater_stats  \
                    inner join (Select game_id g from game where season=?) \
                    on game_skater_stats.game_id=g \
                    where player_id=?",(season,player_id,))
    try:
        total_goals = cur.fetchone()[0]
    except:
        total_goals=0

    #need to select count of number of games during the season(s)
    # for which that player participated
    cur.execute("Select count(*) from\
                (Select game_id s from game_shifts\
                   inner join \
                   (Select game_id g from game where season=?) \
                   on s = g \
                   where player_id=? group by game_id)" \
                ,(season,player_id,))
    try:
        total_games = cur.fetchone()[0]
    except:
        print("That player played 0 games this season")
        return 0
    return total_goals / (total_games * 1.0)


#calculate average number of shots per game for which the player participated in the play
# input: conn - database connection
#        player_first_name
#        player_last_name
#        season - season, ex. 20162017
def shots_per_game_participation(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    player_id = cur.fetchone()[0]
    
    #look in game_plays table ---where event in ('Blocked Shot', 'Missed Shot', 'Shot')---
    #also need to join through game_plays_player to get to player_id from play_id
    cur.execute("Select count(*) from\
                (Select game_id g1_id, play_id p1_id \
                   from game_plays \
                   inner join (Select game_id g2_id from game where season=?) on g1_id=g2_id \
                   inner join (Select play_id p2_id from game_plays_players where player_id=?) on p1_id=p2_id\
                 where event in ('Blocked Shot', 'Missed Shot', 'Shot')) "\
                ,(season,player_id,))
    total_shots = cur.fetchone()[0]
    
    #need to select count of number of games during the season(s)
    # for which that player participated
    cur.execute("Select count(*) from\
                (Select game_id s from game_shifts\
                   inner join \
                   (Select game_id g from game where season=?) \
                   on s = g \
                   where player_id=? group by game_id)" \
                ,(season,player_id,))
    total_games = cur.fetchone()[0]
    return total_shots / (total_games * 1.0)

#calculate average number of goals per game for which a player participated in the play
# input: conn - database connection
#        player_first_name
#        player_last_name
#        season - season, ex. 20162017
def goals_per_game_participation(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    player_id = cur.fetchone()[0]
    
    #look in game_plays table ---where event like 'Goal'---
    #also need to join through game_plays_player to get to player_id from play_id
    #  This is essentially the same problem as shots per game
    cur.execute("Select count(*) from\
                (Select game_id g1_id, play_id p1_id \
                   from game_plays \
                   inner join (Select game_id g2_id from game where season=?) on g1_id=g2_id \
                   inner join (Select play_id p2_id from game_plays_players where player_id=?) on p1_id=p2_id\
                 where event='Goal') "\
                ,(season,player_id,))
    total_goals = cur.fetchone()[0]
    
    #need to select count of number of games during the season(s)
    # for which that player participated
    cur.execute("Select count(*) from\
                (Select game_id s from game_shifts\
                   inner join \
                   (Select game_id g from game where season=?) \
                   on s = g \
                   where player_id=? group by game_id)" \
                ,(season,player_id,))
    total_games = cur.fetchone()[0]
    return total_shots / (total_games * 1.0)


######################             Team Stats             ###################
def power_play_percentage(conn, team_location, team_mascot, season):
    cur = conn.cursor()
    # first figure out team_id
    cur.execute("Select team_id from team_info where shortName=? and teamName=?",
                (team_location, team_mascot))
    try:
        team_id = cur.fetchone()[0]
    except:
        print("That team does not exist")
        return 0

    cur.execute("Select sum(powerPlayOpportunities), sum(powerPlayGoals) \
                    from game_teams_stats \
                    inner join (select game_id g from game where season=?) \
                    on g=game_teams_stats.game_id \
                    where team_id=?",
                (season, team_id,))

    res = cur.fetchone()
    return str(100 * res[1] / (res[0] * 1.0)) + "%"
    

def net_turnover_avg(conn, team_location, team_mascot, season):
    cur = conn.cursor()
    # first figure out team_id
    cur.execute("Select team_id from team_info where shortName=? and teamName=?",
                (team_location, team_mascot))
    try:
        team_id = cur.fetchone()[0]
    except:
        print("That team does not exist")
        return 0

    cur.execute("Select sum(giveaways), sum(takeaways), count(1) \
                    from game_teams_stats \
                    inner join (select game_id g from game where season=?) \
                    on g=game_teams_stats.game_id \
                    where team_id=?",
                (season, team_id,))

    res = cur.fetchone()
    return (res[1] - res[0]) / (res[2] * 1.0)
    

######################  Start of visualization functions  ###################
def visualize_player_shots_over_season(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    try:
        player_id = cur.fetchone()[0]
    except:
        print("Failed to find that player in that season")
        return 0

    #collect data from game_skater_stats for total shots
    cur.execute("Select game_id, shots from game_skater_stats  \
                    inner join (Select game_id g from game where season=?) \
                    on game_skater_stats.game_id=g \
                    where player_id=? \
                    order by game_id asc",(season,player_id,))
    
    res = cur.fetchall()
    x = []
    y = []
    ctr = 0
    for item in res:
        ctr += 1
        x.append(ctr)
        y.append(item[1])
        
    fig, ax = plt.subplots()
    ax.scatter(x=x, y=y, marker='o', c='r', edgecolor='b')
    ax.set_xlabel('Game Number')
    ax.set_ylabel('Shots')
    ax.set_title("Shots by "+ player_first_name +" "+ player_last_name + " over " + season)
    plt.show()
    return

def visualize_player_hits_over_season(conn, player_first_name, player_last_name, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select player_id from player_info where firstName=? and lastName=?",
                (player_first_name, player_last_name))
    try:
        player_id = cur.fetchone()[0]
    except:
        print("Failed to find that player in that season")
        return 0

    #collect data from game_skater_stats for total shots
    cur.execute("Select game_id, hits from game_skater_stats  \
                    inner join (Select game_id g from game where season=?) \
                    on game_skater_stats.game_id=g \
                    where player_id=? \
                    order by game_id asc",(season,player_id,))
    
    res = cur.fetchall()
    x = []
    y = []
    ctr = 0
    for item in res:
        ctr += 1
        x.append(ctr)
        y.append(item[1])
        
    fig, ax = plt.subplots()
    ax.scatter(x=x, y=y, marker='o', c='r', edgecolor='b')
    ax.set_xlabel('Game Number')
    ax.set_ylabel('Hits')
    ax.set_title("Hits by "+ player_first_name +" "+ player_last_name + " over " + season)
    plt.show()
    return

def visualize_team_shots_over_season(conn, team_location, team_mascot, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select team_id from team_info where shortName=? and teamName=?",
                (team_location, team_mascot))
    try:
        team_id = cur.fetchone()[0]
    except:
        print("Failed to find that team in that season")
        return 0

    #collect data from game_skater_stats for total shots
    cur.execute("Select game_id, shots from game_teams_stats  \
                    inner join (Select game_id g from game where season=?) \
                    on game_teams_stats.game_id=g \
                    where team_id=? \
                    order by game_id asc",(season,team_id,))
    
    res = cur.fetchall()
    x = []
    y = []
    ctr = 0
    for item in res:
        ctr += 1
        x.append(ctr)
        y.append(item[1])
        
    fig, ax = plt.subplots()
    ax.scatter(x=x, y=y, marker='o', c='r', edgecolor='b')
    ax.set_xlabel('Game Number')
    ax.set_ylabel('Shots')
    ax.set_title("Shots by "+ team_location +" "+ team_mascot + " over " + season)
    plt.show()
    return

def visualize_team_hits_over_season(conn, team_location, team_mascot, season):
    cur = conn.cursor()
    # first figure out player_id
    cur.execute("Select team_id from team_info where shortName=? and teamName=?",
                (team_location, team_mascot))
    try:
        team_id = cur.fetchone()[0]
    except:
        print("Failed to find that team in that season")
        return 0

    #collect data from game_skater_stats for total shots
    cur.execute("Select game_id, hits from game_teams_stats  \
                    inner join (Select game_id g from game where season=?) \
                    on game_teams_stats.game_id=g \
                    where team_id=? \
                    order by game_id asc",(season,team_id,))
    
    res = cur.fetchall()
    x = []
    y = []
    ctr = 0
    for item in res:
        ctr += 1
        x.append(ctr)
        y.append(item[1])
        
    fig, ax = plt.subplots()
    ax.scatter(x=x, y=y, marker='o', c='r', edgecolor='b')
    ax.set_xlabel('Game Number')
    ax.set_ylabel('Hits')
    ax.set_title("Hits by "+ team_location +" "+ team_mascot + " over " + season)
    plt.show()
    return

######################   Start of db building functions   ###################
#unused
def create_table_from_headers(name, headers):
    ret_str = "create table " + name + "("
    for header in headers:
        ret_str += header + ","
    return ret_str[:-1] + ');'

#base function to help create sql statements when creating tables
def insert_vales_from_headers(name, headers):
    ret_str = "insert into " + name + "("
    for header in headers:
        ret_str += header + ","
    ret_str = ret_str[:-1] + ') values ('
    for header in headers:
        ret_str += "?,"
    return ret_str[:-1] + ');'

#wrapper for building the sqlite database
#  returns connection to the database
def build_nhl_database():
    conn = sqlite3.connect(":memory:")
    conn.text_factory = str
    cur = conn.cursor()

    #put all individual calls to build each table
    create_game_table(cur)
    conn.commit()
    create_game_goalie_stats_table(cur)
    conn.commit()
    create_game_plays_table(cur)
    conn.commit()
    create_game_plays_players_table(cur)
    conn.commit()
    create_game_shifts_table(cur)
    conn.commit()
    create_game_skater_stats_table(cur)
    conn.commit()
    create_game_teams_stats_table(cur)
    conn.commit()
    create_player_info_table(cur)
    conn.commit()
    create_team_info_table(cur)
    conn.commit()
    return conn


#definitions to build each table from incuded csv files
# note: limited data types in sqlite only using text and integer
def create_game_table(cur):
    table_name = "game"
    cur.execute("create table " + table_name + " (\
                    game_id INTEGER PRIMARY KEY,\
                    season INTEGER,\
                    type text,\
                    date_time text,\
                    away_team_id INTEGER,\
                    home_team_id INTEGER,\
                    away_goals INTEGER,\
                    home_goals INTEGER,\
                    outcome text,\
                    home_rink_side_start text,\
                    venue text,\
                    venue_link text,\
                    venue_time_zone_id text,\
                    venue_time_zone_offset INTEGER,\
                    venue_time_zone_tz text)")
    with open('data/game.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        #create_table_str = create_table_from_headers("game", headers)
        #cur.execute(create_table_str)
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_game_goalie_stats_table(cur):
    table_name = "game_goalie_stats"
    cur.execute("create table " + table_name + " (\
                    game_id integer,\
                    player_id integer,\
                    team_id integer,\
                    timeOnIce integer,\
                    assists integer,\
                    goals integer,\
                    pim integer,\
                    shots integer,\
                    saves integer,\
                    powerPlaySaves integer,\
                    shortHandedSaves integer,\
                    evenSaves integer,\
                    shortHandedShotsAgainst integer,\
                    evenShotsAgainst integer,\
                    powerPlayShotsAgainst integer,\
                    decision text,\
                    savePercentage integer,\
                    powerPlaySavePercentage text,\
                    evenStrengthSavePercentage text)")
    with open('data/game_goalie_stats.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_game_plays_table(cur):
    table_name = "game_plays"
    cur.execute("create table " + table_name + " (\
                    play_id text primary key,\
                    game_id integer,\
                    play_num integer,\
                    team_id_for text,\
                    team_id_against text,\
                    event text,\
                    secondaryType text,\
                    x text,\
                    y text,\
                    period integer,\
                    periodType text,\
                    periodTime integer,\
                    periodTimeRemaining integer,\
                    dateTime text,\
                    goals_away integer,\
                    goals_home integer,\
                    description text,\
                    st_x text,\
                    st_y text,\
                    rink_side text)")
    with open('data/game_plays.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_game_plays_players_table(cur):
    table_name = "game_plays_players"
    cur.execute("create table " + table_name + " (\
                    play_id text,\
                    game_id integer,\
                    play_num integer,\
                    player_id integer,\
                    playerType text)")
    with open('data/game_plays_players.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_game_shifts_table(cur):
    table_name = "game_shifts"
    cur.execute("create table " + table_name + " (\
                    game_id integer,\
                    player_id integer,\
                    period integer,\
                    shift_start integer,\
                    shift_end integer)")
    with open('data/game_shifts.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_game_skater_stats_table(cur):
    table_name = "game_skater_stats"
    cur.execute("create table " + table_name + " (\
                    game_id integer,\
                    player_id integer,\
                    team_id integer,\
                    timeOnIce integer,\
                    assists integer,\
                    goals integer,\
                    shots integer,\
                    hits integer,\
                    powerPlayGoals integer,\
                    powerPlayAssists integer,\
                    penaltyMinutes integer,\
                    faceOffWins integer,\
                    faceoffTaken integer,\
                    takeaways integer,\
                    giveaways integer,\
                    shortHandedGoals integer,\
                    shortHandedAssists integer,\
                    blocked integer,\
                    plusMinus integer,\
                    evenTimeOnIce integer,\
                    shortHandedTimeOnIce integer,\
                    powerPlayTimeOnIce integer)")
    with open('data/game_skater_stats.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_game_teams_stats_table(cur):
    table_name = "game_teams_stats"
    cur.execute("create table " + table_name + " (\
                    game_id integer,\
                    team_id integer,\
                    HoA text,\
                    won text,\
                    settled_in text,\
                    head_coach text,\
                    goals integer,\
                    shots integer,\
                    hits integer,\
                    pim integer,\
                    powerPlayOpportunities integer,\
                    powerPlayGoals integer,\
                    faceOffWinPercentage integer,\
                    giveaways integer,\
                    takeaways integer)")
    with open('data/game_teams_stats.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_player_info_table(cur):
    table_name = "player_info"
    cur.execute("create table " + table_name + " (\
                    player_id integer primary key,\
                    firstName text,\
                    lastName text,\
                    nationality text,\
                    birthCity text,\
                    primaryPosition text,\
                    birthDate text,\
                    link text)")
    with open('data/player_info.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return

def create_team_info_table(cur):
    table_name = "team_info"
    cur.execute("create table " + table_name + " (\
                    team_id integer primary key,\
                    franchiseId text,\
                    shortName text,\
                    teamName text,\
                    abbreviation text,\
                    link text)")
    with open('data/team_info.csv', 'rb') as fin:
        headers = next(fin).replace('"', '').split(',')
        data_read = csv.reader(fin)

        for row in data_read:
            cur.execute(insert_vales_from_headers(table_name, headers), row)
        return
                        

    
