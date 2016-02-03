# -*- coding: utf-8 -*-
# File: download_data.py
# Description: Download data from ESPN's NBA database
# Author:
# Email:

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


###############################################################################
# UTILITY FUNCTIONS
###############################################################################

def BS(html):
    """
    Overcome annoying warning message: set the html parser
    """
    return BeautifulSoup(html, "lxml")


def soup_link(link):
    """
    Input:
        link: a string, a valid url
    Returns:
        a BeautifulSoup object representing the HTML content of the url
    """
    content = urlopen(link).read()
    soup = BS(content)
    return soup


def parse_distance(string):
    """
    Get the distance from a report line. Example: an input "25-foot jumper"
    should result in an output 25 (an integer).

    Input:
        string: a string to be analyzed
    Returns:
        if the string contains distance information, return the distance as
        an integer. else return nothing ("return None")
    """
    # write the pattern
    pp = # fill in here
    result = pp.search(string)
    if # fill in here
        # turn the result to an integer and return it
        dist =
        return dist
    else:
        return None


def parse_points_scored(string):
    """
    Determine the number of points scored.

    Input:
        string: a string to be analyzed
    Returns:
        1, 2 or 3: how many points were scored
    """
    if # fill in here
    elif # fill in here
    else:
        return 2


def parse_shot_success(string):
    """
    Determine if the shot was successful.

    Input:
        string: a string to be analyzed
    Returns:
        "scores" or "misses" or "not a shot" based on
        the shot success.
    """
    if # fill in here
    elif # fill in here
    else:
        return "not a shot"


def get_player_in_action(string, list_players):
    """
    Determine which player was in action

    Inputs:
        string: a string to be analyzed
        list_players: a list of players among whom we are looking for the
            active player
    Returns:
        The player in action. If none of the players in list_players was
        in action, return "Not in team"
    """
    for player in list_players:
        # write the pattern
        begin_pattern =
        if begin_pattern.search(string):
            return player
        if "blocks" in string:
            # write the pattern
            pattern =
            # take out the first word (name of player blocked)
            trimmed_string =
            if pattern.search(trimmed_string):
                return player

    return "Not in team"


###############################################################################
# SCRAPING FUNCTIONS
###############################################################################

def get_players(team_id, year):
    """
    Get a list of players in a team in a given year.

    Inputs:
        team_id: string, a three-letter id of the team
        year: integer, a year

    Returns:
        a list of strings that are the players' names
    """
    link = "http://espn.go.com/nba/team/stats/_/name/{}/year/{}/".format(team_id, year)
    soup = soup_link(link)

    # find the first occurence of tr with class "colhead"
    # use soup.find for the first occurence
    game_stat_row =

    player_names = []
    for # fill in here
        player_names.append(name)

    return player_names


def extract_gamelog_row(row, list_players, home_or_away):
    """
    Extract information from a gamelog row.

    Inputs:
        row: a gamelog row (Beautiful Soup object)
        list_players: a list of players

    Returns:
        a dictionary containing information about the gamelog row
    """
    pieces = list(row.children)
    info_dict = {}

    # filter rows of timeout, end of quarter
    if # fill in here
        return info_dict

    if home_or_away == "away":
        game_event = # fill in here
    else:
        game_event = # fill in here


    text = # fill in here
    # get rid of initial spaces
    text = # fill in here

    info_dict["text"] = text

    info_dict["player"] = # fill in here
    info_dict["shot_success"] = # fill in here

    if # fill in here
        info_dict["points_scored"] = # fill in here
    else:
        info_dict["points_scored"] = 0

    # distance
    info_dict["distance"] = parse_distance(text)

    # certain shot types are assigned a fixed distance
    if not(info_dict["distance"]):
        if "dunk" in text:
            info_dict["distance"] = 0
        if "layup" in text:
            info_dict["distance"] = 1
        if "tip shot" in text:
            info_dict["distance"] = 1
        if "three point" in text:
            info_dict["distance"] = 23

    return info_dict


def structure_gamelog_info(game_id, list_players, home_or_away):
    """
    Parse information from gamelog.

    Inputs:
        game_id: string, the id of the game
        list_players: a list of strings, the players of the team
        home_or_away: string, "home" or "away"

    Returns:
        Pandas data frame that contains information from the gamelog's rows
    """
    game_link = "http://espn.go.com/nba/playbyplay?gameId={}&period=0".format(game_id)
    gamelog = # fill in here, soup the link

    report_lines = gamelog.findAll # fill in here

    list_info_dicts = []

    for line in report_lines:
        info_dict = # fill in here

        # filter lines that are not meaningful or relevant
        if  # fill in here
            continue
        if # fill in here
            continue

        info_dict["game_id"] = game_id
        # fill in here: add info_dict to list_info_dicts
        list_info_dicts.append(info_dict)

    df = pd.DataFrame(list_info_dicts)
    return df


def parse_all_games(df_game_ids, list_players):
    list_dfs = []
    for ix, row in df_game_ids.iterrows():
        game_id = row["game_id"]
        home_or_away = row["home_or_away"]
        print(game_id)
        df = structure_gamelog_info(game_id, list_players, home_or_away)
        list_dfs.append(df)
        time.sleep(1)    # wait for one second

    df_all = pd.concat(list_dfs)
    return df_all


###############################################################################
# RUN THE SCRAPING
###############################################################################

# ---- define parameters

team_id = "por"
year = 2015
DATA_FOLDER = "../data"

# ---- get the players
list_players = get_players(team_id, year)

# ---- scrape one game for testing purposes
GAME_ID = 400579510
home_or_away = "away"
df_game = structure_gamelog_info(GAME_ID, list_players, home_or_away)
# sum the points scored. Is it really the same that the team scored in the game?

# ---- scrape all games
# -------- read the game ids
df_game_ids = pd.read_csv(DATA_FOLDER + "/gameids_{}_{}.csv".format(team_id, year))
# -------- run the parser
df_all = parse_all_games(df_game_ids, list_players)
# -------- output the result
df_all.to_csv(DATA_FOLDER + "/all_games_{}_{}.csv".format(team_id, year),
              index = False)
