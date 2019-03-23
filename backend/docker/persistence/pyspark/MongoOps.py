import os
import re
import json
import string
import hashlib
import requests
import datetime
import pandas as pd
import pymongo as pm
from bson import Binary
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

class MongoOps():
    """
    docstring for MongoOps
    """
    def __init__(self, username="admin", 
                    password="admin", 
                    host="mongo:27017",
                    testing=False):
        self.username = username
        self.password = password
        self.host = host
        self.uri = "mongodb://%s:%s@%s" % (quote_plus(self.username), 
                                        quote_plus(self.password), self.host)

        self.connection = pm.MongoClient(self.uri)
        self.homes_database = self.connection.homes_database

        self.homes_collection = self.homes_database.homes
        self.directions_collection = self.homes_database.directions

        self.create_loc_index(self.homes_collection)
        self.create_loc_index(self.directions_collection)
        self.testing = testing

    def drop_table(self, collection):
        collection.drop()

    def create_loc_index(self, collection, name = "geometry", location_type = "2dsphere"):
        collection.create_index([(name,  location_type)])


    def load_dict(self, collection, data):
        collection.insert_one(data)

    def search_collection(self, collection, search_val = None, limit = 10):
        if limit != None:
            return collection.find(search_val).limit(limit)
        else:
            return collection.find(search_val)

    def address_info_in_database(self, collection, address_hash):
        search_val = {"address_hash" : address_hash}
        cursor = self.search_collection(collection, search_val = search_val, limit=1)
        return cursor.count() > 0

    def format_address(self, address):
        formatted_address = address.lower()
        remove_spaces = lambda s : remove_spaces(re.sub("  ", " ", s)) if "  " in s else s
        whitelist = string.ascii_lowercase + string.digits + ' '
        formatted_address = remove_spaces(formatted_address)
        formatted_address = ''.join(c for c in formatted_address if c in whitelist)
        return formatted_address

    def flask_request(self, url):
        try:
            r = requests.get(url)
        except Exception as e:
            return "proxy service error: " + str(e), 503
        soup = BeautifulSoup(r.content, "html.parser")
        address_info = json.loads(str(soup))
        return address_info

    def _query_for_location_info(self, address):
        address = self.format_address(address)
        url = 'http://esri:5000/get_geocode/%s' % quote_plus(address)
        r = self.flask_request(url)
        r['address'] = address
        return r

    def safe_query_for_location_info(self, event):
        address = ""
        if type(event)==dict:
            address = event["location"]
        elif type(event)==str:
            address = event
        address = self.format_address(address)
        address_hash = self.get_hash(address)
        if not self.address_info_in_database(self.homes_database.homes, address_hash):
            self.print_test("%s not found! Gathering data from Esri." % address)
            data = self._query_for_location_info(address)
            if type(event)==dict:
                event["location"] = data
                event["address_hash"] = address_hash
            elif type(event)==str:
                event = {"location": data, "address_hash": address_hash}
            self.load_dict(self.homes_database.homes, event)
        else:
            self.print_test("%s found! Gathering data from MongoDB." % address)
        result = self.search_collection(self.homes_database.homes, {"address_hash" : address_hash}).next()
        return result

    def get_hash(self, strings):
        hasher = hashlib.sha1()
        string = "".join(strings)
        hasher.update(string.encode('utf-8'))
        hashed_directions = hasher.digest()
        return hashed_directions

    def get_address_from_loc_data(self, loc):
        if isinstance(loc, dict):
            try:
                loc_str = loc["location"]["address"]
            except:
                print("Dict passed is not properly formatted. Should have {\"location\": {..., \"address\": <address>}} format.")
                return None
        elif isinstance(loc, str):
            try:
                loc_str = json.loads(loc).get("location.address", loc.get("location", loc.get("address")))
            except:
                loc_str = loc
        else:
            print("Location data not string or dict.")
            return None
        return loc_str.strip()

    def get_directions(self, start, stop):
        """
        get_directions is designed to receive jsons for the following schema.
        A schema checker may be added at some point in the future.
            {"geometry": {"x" : <float>, "y": <float> }, *}
        """
        start_str = json.dumps(start, skipkeys=True)
        stop_str = json.dumps(stop, skipkeys=True)

        directions_json = {}

        url_path = 'get_directions/{ "location_1": %s, "location_2": %s }' % (start_str, stop_str)
        url = 'http://esri:5000/%s' % url_path

        directions = self.flask_request(url)
        directions_json['directions'] = directions

        hashed_directions = hashed_directions = self.get_hash([start_str, stop_str])

        directions_json["directions_hash"] = hashed_directions

        return directions_json
    
    def direction_in_database(self, collection, direction_hash):
        search_val = {"directions_hash": Binary(data = direction_hash)}
        cursor = self.search_collection(collection, search_val = search_val, limit=1)
        return cursor.count() > 0

    def _query_for_directions(self, start, stop):
        directions = self.get_directions(start, stop)
        return directions
        
        
    def safe_query_for_directions(self, start, stop):
        start_str = self.get_address_from_loc_data(start)
        start_data = self.safe_query_for_location_info(start_str)

        stop_str = self.get_address_from_loc_data(stop)
        stop_data = self.safe_query_for_location_info(stop_str)

        directions_hash = self.get_hash([start_str, stop_str])
        if not self.direction_in_database(self.directions_collection, directions_hash):
            self.print_test("Directions from %s to %s not found! Gathering data from Esri." % (start_str, stop_str))
            directions = self._query_for_directions(start_data["location"], stop_data["location"])
            directions["directions_hash"] = directions_hash
            directions["start"] = start_data["location"]["address"]
            directions["stop"] = stop_data["location"]["address"]
            
            self.load_dict(self.directions_collection, directions)
        else:
            self.print_test("Directions from %s to %s found! Gathering data from MongoDB." % (start_str, stop_str))
            directions = self.search_collection(self.directions_collection, {"directions_hash": directions_hash}).next()
        return directions

    def print_test(self, string):
        if self.testing:
            print(string)    

if __name__ == "__main__":
    from ICSParser import ICSParser
    mops = MongoOps()
    ics = ICSParser()
    
    ics.parse_ics("/data/download.ics")
    start = mops.safe_query_for_location_info(ics.to_dict())

    ics.parse_ics("/data/download (1).ics")
    stop = mops.safe_query_for_location_info(ics.to_dict())

    print(mops.safe_query_for_directions(start, stop))