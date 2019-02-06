# infutor_nhl_challenge
coding challenge from infutor, Paul Spears

Basic instruction for how to use my implemention of answers to the coding challenge:

Note: github prevented all data files from uploading due to size restraints, 
  complete collection of data files can be found at https://www.kaggle.com/martinellis/nhl-game-data

Start a python idle and load the included "stat_analysis.py"
Before processing need to load the database to a connection: conn = build_nhl_database()

Now a variety of commands can be run to get statistics on the data, commands are of the form as follows:

shifts_per_game(conn, player_first_name, player_last_name, season)
time_per_shift(conn, player_first_name, player_last_name, season)
shots_per_game(conn, player_first_name, player_last_name, season)
goals_per_game(conn, player_first_name, player_last_name, season)
power_play_percentage(conn, team_location, team_mascot, season)
net_turnover_avg(conn, team_location, team_mascot, season)
visualize_player_shots_over_season(conn, player_first_name, player_last_name, season)
visualize_player_hits_over_season(conn, player_first_name, player_last_name, season)
visualize_team_shots_over_season(conn, team_location, team_mascot, season)
visualize_team_hits_over_season(conn, team_location, team_mascot, season)

the first 4 functions provide direct answers to question 1.
a) Patrick Kane: 23.5823, Alex Ovechkin: 21.7191
b) Patrick Kane: 54.8867, Alex Ovechkin: 51.1542
c) Patrick Kane:  3.9873, Alex Ovechkin:  4.0674
d) Patrick Kane:  0.4430, Alex Ovechkin:  0.4297
the next 2 function provide direct answers to question 3
a) Washington Capitals: 24.1379%
b) Washington Capitals: -3.0566
The remaining visualization functions produce the requested graphs on command as scatter plots, tracking stats over the course of a season


For reference the following commands were used to get the result for all questions:
> conn = build_nhl_database()
> shifts_per_game(conn, "Patrick", "Kane", "20162017")
23.582278481012658
> time_per_shift(conn, "Patrick", "Kane", "20162017")
54.88674181427805
> shots_per_game(conn, "Patrick", "Kane", "20162017")
3.9873417721518987
> goals_per_game(conn, "Patrick", "Kane", "20162017")
0.4430379746835443
> shifts_per_game(conn, "Alex", "Ovechkin", "20162017")
21.719101123595507
> time_per_shift(conn, "Alex", "Ovechkin", "20162017")
51.15416451112261
> shots_per_game(conn, "Alex", "Ovechkin", "20162017")
4.067415730337078
> goals_per_game(conn, "Alex", "Ovechkin", "20162017")
0.42696629213483145
> power_play_percentage(conn, "Washington", "Capitals", "20172018")
'24.1379310345%'
> net_turnover_avg(conn, "Washington", "Capitals", "20172018")
-3.056603773584906
> visualize_player_shots_over_season(conn, "Patrick", "Kane", "20162017")
> visualize_player_hits_over_season(conn, "Patrick", "Kane", "20162017")
> visualize_player_shots_over_season(conn, "Alex", "Ovechkin", "20162017")
> visualize_player_hits_over_season(conn, "Alex", "Ovechkin", "20162017")
> visualize_team_shots_over_season(conn, "Washington", "Capitals", "20172018")
> visualize_team_hits_over_season(conn, "Washington", "Capitals", "20172018")
>
