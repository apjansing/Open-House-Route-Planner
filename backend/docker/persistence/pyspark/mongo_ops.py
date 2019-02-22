import json
import datetime
import pandas as pd
import pymongo as pm

import requests
from bs4 import BeautifulSoup

import os

try:
    # Python 3.x
    from urllib.parse import quote_plus
except ImportError:
    # Python 2.x
    from urllib import quote_plus

username = os.environ['MONGO_INITDB_ROOT_USERNAME']
password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
host = "mongo:27017"

uri = "mongodb://%s:%s@%s" % (
    quote_plus(username), quote_plus(password), host)


def drop_table(collection):
    collection.drop()

def create_loc_index(collection, name = "geometry", location_type = "2dsphere"):
    collection.create_index([(name,  location_type)])

def get_location_information(address):
    url = 'http://esri:5000/get_geocode/%s' % quote_plus(address)
    try:
        r = requests.get(url)
    except Exception as e:
        return "proxy service error: " + str(e), 503
    soup = BeautifulSoup(r.content, "html.parser")
    address_info = json.loads(str(soup))
    address_info['address'] = address
    return address_info

def load_location_information(collection, data):
    collection.insert_one(data)

def search_collection(collection, search_val = None, limit = 10):
    if limit != None:
        return collection.find(search_val).limit(limit)
    else:
        return collection.find(search_val)

def address_info_in_database(collection, address):
    search_val = {"address" : address}
    cursor = search_collection(collection, search_val = search_val, limit=1)
    return cursor.count() > 0

if __name__ == '__main__':
    connection = pm.MongoClient(uri)
    homes_collection = connection.homes_collection
    create_loc_index(homes_collection.homes)
    data = get_location_information("415 Van Dyke Rd, Liverpool, NY 13088")
    load_location_information(homes_collection.homes, data)
    search_collection(homes_collection.homes)
    print(address_info_in_database(homes_collection.homes, "415 Van Dyke Rd, Liverpool, NY 13088"))
    print(address_info_in_database(homes_collection.homes, "4807 Bear Rd, Liverpool, NY"))