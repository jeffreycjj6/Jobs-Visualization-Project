import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

from geopy.geocoders import Nominatim

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


from flask import Blueprint, render_template, request, redirect, url_for
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
    image = "stateheatmaps/" + str(currState) + ".html"

    #Uses the initials of the state to reduce the dataframes to only be of the current state
    currStateInitials = states.get(str(currState))
    df = df[df['state'] == currStateInitials]
    dfStates = dfStates[dfStates['State'] == currStateInitials]
    js = df['title'].value_counts().to_frame(name='Listings Found')
    ls = df['location'].value_counts().to_frame(name='Occurences')

    '''geolocater = Nominatim(user_agent="MyApp", timeout=None)
    df['extraLocation'] = geolocater.geocode(df['location'])

    for index, row in df.iterrows():
        #Row is the current row of the df, currentCity simply isolates it to that row only
        currentCity = row['location']
        location = geolocater.geocode(currentCity)
        df.at[index, 'extraLocation'] = location'''

    # Use this def info to generate the html page for each individual state
    return render_template("state.html", state=currState, stateData=dfStates, stateJobs = df, locationSeries = ls.to_html(), jobSeries = js.to_html(), stateJobsHTML=(df.to_html()), stateImageURL=image)

@data.route("/jobdata")
def jobdata():
    return render_template("mainData.html")

@data.route("/aggregatedata")
def aggregatedata():
    return render_template("aggregateData.html")

@data.route("/credits")
def credits():
    return render_template("credits.html")

@data.route("/moredata")
def moredata():
    return render_template("moredata.html")

@data.route("/salarymaps")
def salarymaps():
    return render_template("salarymaps.html")

@data.route("/choropleth", methods=["POST", "GET"])
def choropleth():
    if request.method == "POST":
        title = request.form.get("title")
        scaleVal = request.form.get("scale")
        mapType = request.form.get("type")
        if title == '' or mapType == '' or mapType == 0:
            return render_template("errorpage.html")
        if scaleVal == '': #default scaleVal or for a percentage map
            scaleVal = 1
        return redirect(url_for('data.choroplethMap', job=title, scale=scaleVal, mpType=mapType))
    else:
        copy = pd.read_csv('data_analysis/mainData.csv', index_col = 0)
        allJ = copy['title'].value_counts().to_frame(name='Occurences')
        return render_template("choroplethPage.html", allJobs=allJ.to_html())


@data.route("/choropleth/<job><scale><mpType>")
def choroplethMap(job, scale, mpType):
    #args = request.args
    #job = args.get('jobtitle')
    
    states3 = [
    'AL',
    'AK',
    'AZ',
    'AR',
    'CA',
    'CO',
    'CT',
    'DE',
    'FL',
    'GA',
    'HI',
    'ID',
    'IL',
    'IN',
    'IA',
    'KS',
    'KY',
    'LA',
    'ME',
    'MD',
    'MA',
    'MI',
    'MN',
    'MS',
    'MO',
    'MT',
    'NE',
    'NV',
    'NH',
    'NJ',
    'NM',
    'NY',
    'NC',
    'ND',
    'OH',
    'OK',
    'OR',
    'PA',
    'RI',
    'SC',
    'SD',
    'TN',
    'TX',
    'UT',
    'VT',
    'VA',
    'WA',
    'WV',
    'WI',
    'WY'
    ]
    usa = gpd.read_file("data_analysis/us-states.json")
    usa.plot()

    if int(mpType) == 1:
        jobType = pd.DataFrame()
        for i in range(50):
            #drop all states except for the current one
            #iterate through the new reduced-state-specific job dataframe
            #then drop all entries except for the current job type being analyzed
            reducedJobDataframe = df[df['state'] == states3[i]]
            reducedJobDataframe = reducedJobDataframe[reducedJobDataframe['title'] == job] #testing business analyst
            jobType.loc[i, 'listings'] = len(reducedJobDataframe.index) #assign the number of entires found


        usa['listings'] = jobType['listings']
        usa = usa[~usa['name'].isin(['Alaska', 'Hawaii'])]

        numListings = usa['listings'].max()
        if numListings == 0:
            return render_template("errorpage.html")
        #scale = 1
        ax = usa.boundary.plot(edgecolor='gray', linewidth=0.3, figsize=(15.36,10.24))
        ax.set_title('Total ' + str(job) + ' Job Listings Across US States', size=15, weight='bold')
        usa.plot(ax=ax, vmax=numListings/int(scale), column='listings', cmap='YlGn', legend=True, legend_kwds={'shrink':1, 'orientation':'horizontal'})

        imageName = "static/usachoroplethmaps/" + str(job) + ".jpg"
        plt.savefig(imageName)
        imageName = "usachoroplethmaps/" + str(job) + ".jpg" #need to reupdate name to remove static so that html displays correctly

        return render_template("choroplethMap.html", imageSRC=imageName, jobTitle=job, maxListings=(numListings/int(scale)).round(), theType = mpType)
    else:
        jobType = pd.DataFrame()
        for i in range(50):
            #drop all states except for the current one
            #iterate through the new reduced-state-specific job dataframe
            #then drop all entries except for the current job type being analyzed
            reducedJobDataframe = df[df['state'] == states3[i]]
            totalStateJobs = len(reducedJobDataframe.index)
            reducedJobDataframe = reducedJobDataframe[reducedJobDataframe['title'] == job]
            if totalStateJobs == 0:
                jobType.loc[i, 'listings'] = 0
            else:
                jobType.loc[i, 'listings'] = (len(reducedJobDataframe.index) / totalStateJobs) * 100 #generate job percentage


        usa['listings'] = jobType['listings']
        usa = usa[~usa['name'].isin(['Alaska', 'Hawaii'])]

        numListings = usa['listings'].max()
        if numListings == 0:
            return render_template("errorpage.html")
        ax = usa.boundary.plot(edgecolor='gray', linewidth=0.3, figsize=(15.36,10.24))
        ax.set_title('Percent of ' + str(job) + ' Jobs Within US States', size=16, weight='bold')
        usa.plot(ax=ax, column='listings', cmap='YlGn', legend=True, legend_kwds={'shrink':1, 'orientation':'horizontal', 'format': '%.1f%%'})

        imageName = "static/usachoroplethmaps/" + str(job) + ".jpg"
        plt.savefig(imageName)
        imageName = "usachoroplethmaps/" + str(job) + ".jpg" #need to reupdate name to remove static so that html displays correctly

        return render_template("choroplethMap.html", imageSRC=imageName, jobTitle=job, maxListings=str(numListings.round()) + "%", theType = mpType)