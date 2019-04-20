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

@app.route('/get_directions/<coordinates>')
def get_directions(coordinates):
    """
    get_directions is designed to receive jsons for the following schema.
    A schema checker may be added at some point in the future.
    {
        "location_1": { "geometry": {"x" : <float>, "y": <float> }, * },
        "location_2": { "geometry": {"x" : <float>, "y": <float> }, * }
    }
    """
    coordinates = json.loads(coordinates)
    result = route_layer.solve(stops='''%f,%f; %f,%f'''%(coordinates["location_1"]['geometry']['x'],
        coordinates["location_1"]['geometry']['y'],
        coordinates["location_2"]['geometry']['x'],
        coordinates["location_2"]['geometry']['y']),
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
        tod_token = i['attributes']['arriveTimeUTC']
        time_of_day = datetime.datetime.fromtimestamp(tod_token / 1000).strftime('%H:%M:%S')
        time_counter = i['attributes']['time']
        distance_counter = i['attributes']['length']
        travel_time += time_counter
        distance += distance_counter
        records.append( (time_of_day, i['attributes']['text'], 
                        round(travel_time, 2), round(distance, 2))  )
        
    pd.set_option('display.max_colwidth', 100)
    directions_dataframe = pd.DataFrame.from_records(records, index=[i for i in range(1, len(records) + 1)], 
        columns=['Time of day', 'Direction text', 'Duration (min)', 'Distance (miles)'])
    directions_json = json.loads(directions_dataframe.to_json(orient='index'))
    directions_json_array = []
    for bar in directions_json:
        directions_json_array += [directions_json[bar]]
    return json.dumps(directions_json_array)

@app.route('/get_geocode/<address>')
def get_geocoded(address):
    """
    get_geocode expects and address (i.e. 100 Seymour Ave, Utica, NY 13502) in the URL and will return the a json in a form as shown below.
    {
    "geometry": {
        "x": -75.23401051692672,
        "y": 43.08877505712876,
        "spatialReference": {
            "wkid": 4326,
            "latestWkid": 4326
        }
    },
    "attributes": {
        "Loc_name": "World",
        "Status": "M",
        "Score": 95.18,
        "Match_addr": "Seymour Ave, Utica, New York, 13501",
        "LongLabel": "Seymour Ave, Utica, NY, 13501, USA",
        "ShortLabel": "Seymour Ave",
        "Addr_type": "StreetName",
        "Type": "",
        "PlaceName": "",
        "Place_addr": "Seymour Ave, Utica, New York, 13501",
        .
        .
        .
        "X": -75.23401051692672,
        "Y": 43.08877505712876,
        "DisplayX": -75.23401051692672,
        "DisplayY": 43.08877505712876,
        "Xmin": -75.23501051692672,
        "Xmax": -75.23301051692671,
        "Ymin": 43.08777505712876,
        "Ymax": 43.089775057128755,
        "ExInfo": "100",
        "OBJECTID": 1
    }
    """
    return json.dumps(geocode(address=address, as_featureset=True).features[0].as_dict)

@app.route('/')
@app.route('/<path:p>')
def wikiproxy(p = ''):
    import requests
    url = 'https://apjansing.github.io/Open-House-Route-Planner/{0}'.format(p)
    try:
        r = requests.get(url)
    except Exception as e:
        return "proxy service error: " + str(e), 503
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.content, "html.parser")
    return str(soup)

if __name__ == '__main__':
    app.run(host="0.0.0.0")