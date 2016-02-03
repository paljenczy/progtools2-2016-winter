# -*- coding: utf-8 -*-
# File: analyze_shooting_data.py
# Description: Analyze shooting data
# Author:
# Email:

import pandas as pd
import matplotlib.pyplot as plt

def plot_freq_by_distance(df, filename):
    """
    Plots the frequencies for each distance.
    """
    freq_by_dist = # fill in here

    plt.cla()
    # plot here
    plt.savefig(filename)


def int_success(str_success):
    """
    Returns 1 if str_success is "scores" and 0 otherwise.
    """
    # fill in here

def plot_prob_success_by_distance(df, filename):
    """
    Plots the shooting success probability for each distance
    """
    df["is_shot_successful"] = # fill in here
    prob_shot_success = # fill in here

    plt.cla()
    # plot here
    plt.savefig(filename)


###############################################################################
# RUN THE ANALYSIS
###############################################################################

DATA_FOLDER = "../data"

# READ IN DATA AND SELECT ROWS OF INTEREST
df = pd.read_csv(DATA_FOLDER + "/all_games_por_2015.csv")
# select rows with non-null distance and copy the dataframe to a new one
df_distance = # fill in here
# turn distance to integer
df_distance["distance"] = # fill in here
# take shots only within 30 feet
df_distance = # fill in here

plot_freq_by_distance(df_distance, "../output/freq_by_dist.png")
plot_prob_success_by_distance(df_distance, "../output/prob_success_by_dist.png")
