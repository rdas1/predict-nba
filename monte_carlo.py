import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from datetime import datetime

games = pd.read_csv('nba_data/FiveThirtyEight/nba_elo.csv').filter(['date', 'season', 'playoff', 'team1', 'team2', 'score1', 'score2'])
upcoming_games = games[games.score1.isnull()]
games = games[games.score1.notnull()]

def simulate_game(teamA_mean_pts, teamA_sd_pts, teamA_mean_against, teamA_sd_against, teamB_mean_pts, teamB_sd_pts, teamB_mean_against, teamB_sd_against):
    teamA_score = ( random.gauss(teamA_mean_pts, teamA_sd_pts) + random.gauss(teamB_mean_against, teamB_sd_against) ) / 2
    teamB_score = ( random.gauss(teamB_mean_pts, teamB_sd_pts) + random.gauss(teamA_mean_against, teamA_sd_against) ) / 2
    delta = teamA_score - teamB_score
    return delta

def simulate_matchup(teamA, teamB, n=20000, season=datetime.now().year, only_regular_season=True):
    games_season = games[games.season == season]
    if only_regular_season:
        games_season = games_season[games_season.playoff.isnull()]

    teamA_scores = []
    teamA_against = []

    teamB_scores = []
    teamB_against = []

    for idx, teamA_game in games_season[ (games_season.team1 == teamA) | (games_season.team2 == teamA)].iterrows():
        if teamA_game.team1 == teamA:
            teamA_scores.append(teamA_game.score1)
            teamA_against.append(teamA_game.score2)
        else:
            teamA_scores.append(teamA_game.score2)
            teamA_against.append(teamA_game.score1)

    for idx, teamB_game in games_season[ (games_season.team1 == teamB) | (games_season.team2 == teamB)].iterrows():
        if teamB_game.team1 == teamB:
            teamB_scores.append(teamB_game.score1)
            teamB_against.append(teamB_game.score2)
        else:
            teamB_scores.append(teamB_game.score2)
            teamB_against.append(teamB_game.score1)

    teamA_mean_pts = np.mean(teamA_scores)
    teamA_sd_pts = np.std(teamA_scores)
    teamA_mean_against = np.mean(teamA_against)
    teamA_sd_against = np.std(teamA_against)

    teamB_mean_pts = np.mean(teamB_scores)
    teamB_sd_pts = np.std(teamB_scores)
    teamB_mean_against = np.mean(teamB_against)
    teamB_sd_against = np.std(teamB_against)

    simulations = []
    teamA_wins = 0
    teamB_wins = 0
    ties = 0
    for i in range(n):
        gm = simulate_game(teamA_mean_pts, teamA_sd_pts, teamA_mean_against, teamA_sd_against, teamB_mean_pts, teamB_sd_pts, teamB_mean_against, teamB_sd_against)
        simulations.append(gm)
        if gm > 0:
            teamA_wins += 1
        elif gm < 0:
            teamB_wins += 1
        else:
            ties += 1

    print("{}: {}%\n{}: {}%".format(teamA, (teamA_wins * 100 / n), teamB, (teamB_wins * 100 / n)))
    return simulations
    #return ( (teamA_wins * 100 / n), (teamB_wins * 100 / n) )

simulate_matchup("LAC", "LAL", season=2020)

for idx, matchup in upcoming_games.iterrows():
    print("{} vs {}".format(matchup.team1, matchup.team2))
    simulate_matchup(matchup.team1, matchup.team2)
    print("-" * 30)
print("DONE")