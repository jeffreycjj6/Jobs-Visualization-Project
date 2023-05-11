import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#views and webapp cannot be placed inside data_analysis folder for some reason, so data reading requires different locations
#index_col = 0 to remove the unamed initial column that shows index
df = pd.read_csv('data_analysis/mainData.csv', index_col = 0)
dfStates = pd.read_csv('data_analysis/aggregateData.csv', index_col = 0)

df.to_html('templates/mainData.html')
dfStates.to_html('templates/aggregateData.html')

states = {
    'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','HI': 'Hawaii','IA': 'Iowa',
    'ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MS': 'Mississippi',
    'MT': 'Montana','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania',
    'RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia', 'WY': 'Wyoming'
}

#Inverts all the states
states = {v: k for k, v in states.items()}


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
    df = pd.read_csv('data_analysis/mainData.csv', index_col = 0)
    dfStates = pd.read_csv('data_analysis/aggregateData.csv', index_col = 0)

    args = request.args
    currState = args.get('state')

    #Generate a dynamic state image by casting the curr state's name to a string and making it into a file directory
    image = "stateimages/" + str(currState) + ".jpg"

    #Uses the initials of the state to reduce the dataframes to only be of the current state
    currStateInitials = states.get(str(currState))
    df = df[df['state'] == currStateInitials]
    dfStates = dfStates[dfStates['State'] == currStateInitials]
    js = df['title'].value_counts()

    # Use this def info to generate the html page for each individual state
    return render_template("state.html", state=currState, stateData=dfStates, stateJobs = df, jobSeries = js, stateJobsHTML=(df.to_html()), stateImageURL=image)

@data.route("/jobdata")
def jobdata():
    return render_template("mainData.html")

@data.route("/aggregatedata")
def aggregatedata():
    return render_template("aggregateData.html")
