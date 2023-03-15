import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys, math, random


pd.set_option("display.max_rows", None, "display.max_columns", None)
team1 = pd.read_csv("csv/" + sys.argv[1] + ".csv")
team2 = pd.read_csv("csv/" + sys.argv[2] + ".csv")
d1AvgOffTempo = 104.7
d1AvgPoss = 67.7
luckFactor = 2

def calcEfg(*, verbose=False):
    # calulate effective field goal percentage for team1
    # eFG% = (FG + .5* 3P) / FGA
    a = (team1.loc[0]["FG"] + 0.5 * team1.loc[0]["3P"]) / team1.loc[0]["FGA"]
    if verbose:
        print(f"{sys.argv[1]} eFG%: {a:.2f}")

    # calulate effective field goal percentage for team2
    # eFG% = (FG + .5* 3P) / FGA
    b = (team2.loc[0]["FG"] + 0.5 * team2.loc[0]["3P"]) / team2.loc[0]["FGA"]
    if verbose:
        print(f"{sys.argv[2]} eFG%: {b:.2f}")

    return a, b

def calcOffTempo(*, verbose=False):
    a = (team1.loc[0]["FGA"] + (0.475 * team1.loc[0]["FTA"]) - team1.loc[0]["ORB"] + team1.loc[0]["TOV"])
    if verbose:
        print(f"{sys.argv[1]} Offensive Tempo: {a:.2f}")

    b = (team2.loc[0]["FGA"] + (0.475 * team2.loc[0]["FTA"]) - team2.loc[0]["ORB"] + team2.loc[0]["TOV"])
    if verbose:
        print(f"{sys.argv[2]} Offensive Tempo: {b:.2f}")

    return a, b

def calcDefTempo(*, verbose=False):
    a = (team1.loc[1]["FGA"] + (0.475 * team1.loc[1]["FTA"]) - team1.loc[1]["ORB"] + team1.loc[1]["TOV"])
    if verbose:
        print(f"{sys.argv[1]} Defensive Tempo: {a:.2f}")

    b = (team2.loc[1]["FGA"] + (0.475 * team2.loc[1]["FTA"]) - team2.loc[1]["ORB"] + team2.loc[1]["TOV"])
    if verbose:
        print(f"{sys.argv[2]} Defensive Tempo: {b:.2f}")

    return a, b

def calcOffEff(*, verbose=False):
    a = team1.loc[0]["PTS"]/calcOffTempo()[0]*100
    if verbose:
        print(f"{sys.argv[1]} Offensive Efficiency: {a:.2f}")
    
    b = team2.loc[0]["PTS"]/calcOffTempo()[1]*100
    if verbose:
        print(f"{sys.argv[2]} Offensive Efficiency: {b:.2f}")

    return a, b

def calcDefEff(*, verbose=False):
    a = team1.loc[1]["PTS"]/calcDefTempo()[0]*100
    if verbose:
        print(f"{sys.argv[1]} Defensive Efficiency: {a:.2f}")
    
    b = team2.loc[1]["PTS"]/calcDefTempo()[1]*100
    if verbose:
        print(f"{sys.argv[2]} Defensive Efficiency: {b:.2f}")

    return a, b

def calcAdjustedOffEff(*, verbose=False):
    a = ((calcOffEff()[0]-d1AvgOffTempo)+(calcDefEff()[1]-d1AvgOffTempo))+d1AvgOffTempo
    if verbose:
        print(f"{sys.argv[1]} Adjusted Offensive Efficiency: {a:.2f}")
    
    b = ((calcOffEff()[1]-d1AvgOffTempo)+(calcDefEff()[0]-d1AvgOffTempo))+d1AvgOffTempo
    if verbose:
        print(f"{sys.argv[2]} Adjusted Offensive Efficiency: {b:.2f}")

    return a, b

def calcAdjustedPoss(*, verbose=False):
    a = (calcOffTempo()[0]-d1AvgPoss+calcDefTempo()[1]-d1AvgPoss)+d1AvgPoss
    if verbose:
        print(f"{sys.argv[1]} Adjusted # Poss: {a:.2f}")
    
    b = (calcOffTempo()[1]-d1AvgPoss+calcDefTempo()[0]-d1AvgPoss)+d1AvgPoss
    if verbose:
        print(f"{sys.argv[2]} Adjusted # Poss: {b:.2f}")

    return a, b

def calcAdjustedScore(*, verbose=False):
    a = calcAdjustedOffEff()[0] * calcAdjustedPoss()[0] / 100
    if verbose:
        print(f"{sys.argv[1]} Adjusted Score: {math.floor(a)}")
    
    b = calcAdjustedOffEff()[1] * calcAdjustedPoss()[1] / 100
    if verbose:
        print(f"{sys.argv[2]} Adjusted Score: {math.floor(b)}")

    return a, b

# 
def calcAdjustedLuckScore(*, verbose=False):
    r = random.randint(-luckFactor, luckFactor)
    a = calcAdjustedScore()[0] + r
    if verbose:
        print(f"{sys.argv[1]} Adjusted Luck Score: {math.floor(a)}")
    
    b = calcAdjustedScore()[1] + r
    if verbose:
        print(f"{sys.argv[2]} Adjusted Luck Score: {math.floor(b)}")

    return a, b

def winner(*, verbose=False, luck=False):
    print(f"luck: {luck}")
    if luck:
        a = calcAdjustedLuckScore()[0]
        b = calcAdjustedLuckScore()[1]
        if a > b:
            print(f"{sys.argv[1]} wins by {a-b:.0f} points.")
            return a
        elif a < b:
            print(f"{sys.argv[2]} wins by {b-a:.0f} points.")
            return b
        else:
            print(f"{sys.argv[1]} and {sys.argv[2]} tie with {a:.0f} points")
            return None
    else:
        a, b = calcAdjustedScore()
        if a > b:
            print(f"{sys.argv[1]} wins by {a-b:.0f} points.")
            return a
        elif a < b:
            print(f"{sys.argv[2]} wins by {b-a:.0f} points.")
            return b
        else:
            print(f"{sys.argv[1]} and {sys.argv[2]} tie with {a:.0f} points")
            return None

calcEfg(verbose=True)
calcOffTempo(verbose=True)
calcDefTempo(verbose=True)
calcOffEff(verbose=True)
calcDefEff(verbose=True)
calcAdjustedOffEff(verbose=True)
calcAdjustedPoss(verbose=True)
calcAdjustedScore(verbose=True)
calcAdjustedLuckScore(verbose=True)

winner(verbose=True, luck=False)
winner(verbose=True, luck=True)