import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#views and webapp cannot be placed inside data_analysis folder for some reason, so data reading requires different locations
df = pd.read_csv('data_analysis/mainData.csv')
dfStates = pd.read_csv('data_analysis/aggregateData.csv')

df.to_html('templates/mainData.html')
dfStates.to_html('templates/aggregateData.html')

from flask import Blueprint, render_template, request
#%store -r dfStates



test = Blueprint(__name__, "test")
data = Blueprint(__name__, "data")

#Establishes one possible route from start page
@test.route("/")
def home():
    return render_template("map.html")

@data.route("/info")
def info():
    args = request.args
    currState = args.get('state')
    return render_template("state.html", state=currState)

@data.route("/jobdata")
def jobdata():
    return render_template("mainData.html")

@data.route("/aggregatedata")
def aggregatedata():
    return render_template("aggregateData.html")
