import arcgis.network as network
import arcgis.geocoding as geocoding

from arcgis.gis import *
from arcgis.geometry import Point
from arcgis.geocoding import geocode, reverse_geocode
from arcgis.features.feature import FeatureSet, Feature

import json
import datetime
import pandas as pd

from flask import Flask
import requests

import os

app = Flask(__name__)

username = os.environ['ESRI_USERNAME']
password = os.environ['ESRI_PASSWORD']

gis = GIS('https://www.arcgis.com', username, password)
route_service_url = gis.properties.helperServices.route.url
route_layer = network.RouteLayer(route_service_url, gis=gis)
start_time = int(datetime.datetime.now().timestamp() * 1000)

@app.route('/get_directions/<locations>')
def get_directions(locations):
    locations = json.loads(locations)
    my_point1 = geocode(address=locations["source"], as_featureset=True).features[0].as_dict
    # my_point1 = json.loads(requests.post("http://localhost:5000/get_geocode/%s" % locations["source"]))
    my_point2 = geocode(address=locations["destination"], as_featureset=True).features[0].as_dict
    # my_point2 = json.loads(requests.post("http://localhost:5000/get_geocode/%s" % locations["destination"]))
    result = route_layer.solve(stops='''%f,%f; %f,%f'''%(my_point1['geometry']['x'], 
                                                     my_point1['geometry']['y'],
                                                     my_point2['geometry']['x'], 
                                                     my_point2['geometry']['y'],
                                                    ),
                           directions_language='en-US', return_routes=False,
                           return_stops=False, return_directions=True,
                           directions_length_units='esriNAUMiles',
                           return_barriers=False, return_polygon_barriers=False,
                           return_polyline_barriers=False, start_time=start_time,
                           start_time_is_utc=True)
    
    records = []
    travel_time, time_counter = 0, 0
    distance, distance_counter = 0, 0

    for i in result['directions'][0]['features']:
        time_of_day = datetime.datetime.fromtimestamp(i['attributes']['arriveTimeUTC'] / 1000).strftime('%H:%M:%S')
        time_counter = i['attributes']['time']
        distance_counter = i['attributes']['length']
        travel_time += time_counter
        distance += distance_counter
        records.append( (time_of_day, i['attributes']['text'], 
                        round(travel_time, 2), round(distance, 2))  )
        
    pd.set_option('display.max_colwidth', 100)
    df = pd.DataFrame.from_records(records, index=[i for i in range(1, len(records) + 1)], 
                                columns=['Time of day', 'Direction text', 
                                            'Duration (min)', 'Distance (miles)'])
    foo = json.loads(df.to_json(orient='index'))
    F = []
    for bar in foo:
        F += [foo[bar]]
    print('Trip took %f minutes.' % F[-1]['Duration (min)'])

    return json.dumps(F)

@app.route('/get_geocode/<address>')
def get_geocoded(address):
    return json.dumps(geocode(address=address, as_featureset=True).features[0].as_dict)

@app.route('/')
def hello():
    return "Open House Route Planner Landing Page"

if __name__ == '__main__':
    app.run(host="0.0.0.0")