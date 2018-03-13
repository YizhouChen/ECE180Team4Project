import gmaps
import pandas as pd
import numpy as np
from mapsplotlib import mapsplot as mplt
mplt.register_api_key('AIzaSyAVpjvREbvsAGnHlwC5v-YJKegctJMD6EI')

business = pd.read_json('business.json', lines=True)


gmaps.configure(api_key="AIzaSyAVpjvREbvsAGnHlwC5v-YJKegctJMD6EI") # Your Google API key

data = []
new_lat = []
new_lon = []
location=[]

lat = list(business['latitude'])
lon = list(business['longitude'])
city = list(business['city'])
for i in range(len(city)):
    if (city[i] == 'Las Vegas'):
        data.append(i)
for x in data:
    new_lat.append(lat[x])
    new_lon.append(lon[x])

for i in range (len(new_lat)):
    location.append((new_lat[i],new_lon[i]))


fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(locations))
fig