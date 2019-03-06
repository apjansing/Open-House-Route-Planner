import os
import re
import json
import pprint
import string
import requests
import datetime
import pandas as pd
import pymongo as pm
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
# from ICSParser import ICSParser

class MongoOps():
    # def __init__(self, username=os.environ['MONGO_INITDB_ROOT_USERNAME'], 
    #                 password=os.environ['MONGO_INITDB_ROOT_PASSWORD'], 
    #                 host="mongo:27017"):
    def __init__(self, username="admin", 
                    password="admin", 
                    host="mongo:27017"):                    
        self.username = username
        self.password = password
        self.host = host
        self.uri = "mongodb://%s:%s@%s" % (quote_plus(self.username), 
                                        quote_plus(self.password), self.host)
        self.connection = pm.MongoClient(self.uri)
        self.homes_database = self.connection.homes_database
        self.create_loc_index(self.homes_database.homes)
        self.create_loc_index(self.homes_database.directions)

    def drop_table(self, collection):
        collection.drop()

    def create_loc_index(self, collection, name = "geometry", location_type = "2dsphere"):
        collection.create_index([(name,  location_type)])


    def load_location_information(self, collection, data):
        collection.insert_one(data)

    def search_collection(self, collection, search_val = None, limit = 10):
        if limit != None:
            return collection.find(search_val).limit(limit)
        else:
            return collection.find(search_val)

    def address_info_in_database(self, collection, address):
        address = self.format_address(address)
        search_val = {"location.address" : address}
        cursor = self.search_collection(collection, search_val = search_val, limit=1)
        return cursor.count() > 0

    def format_address(self, address):
        formatted_address = address.lower()
        remove_spaces = lambda s : remove_spaces(re.sub("  ", " ", s)) if "  " in s else s
        whitelist = string.ascii_lowercase + string.digits + ' '
        formatted_address = remove_spaces(formatted_address)
        formatted_address = ''.join(c for c in formatted_address if c in whitelist)
        return formatted_address

    def _query_for_location_info(self, address):
        address = self.format_address(address)
        url = 'http://esri:5000/get_geocode/%s' % quote_plus(address)
        try:
            r = requests.get(url)
        except Exception as e:
            return "proxy service error: " + str(e), 503
        soup = BeautifulSoup(r.content, "html.parser")
        address_info = json.loads(str(soup))
        address_info['address'] = address
        return address_info

    def safe_query_for_location_info(self, event):
        address = ""
        if type(event)==dict:
            address = event["location"]
        elif type(event)==str:
            address = event
        if not self.address_info_in_database(self.homes_database.homes, address):
            print("Address not found! Gathering data from Esri.")
            data = self._query_for_location_info(address)
            if type(event)==dict:
                event["location"] = data
            elif type(event)==str:
                event = {"location": data}
            self.load_location_information(self.homes_database.homes, event)
            result = self.search_collection(self.homes_database.homes, {"location.address" : self.format_address(address)}).next()
            return result
        else:
            print("Address found! Gathering data from MongoDB.")
            result = self.search_collection(self.homes_database.homes, {"location.address" : self.format_address(address)}).next()
            return result

# def run_tests():
#     mops = MongoOps()
#     mops.safe_query_for_location_info("415 Van    DyKe Rd., Utica, NY 13502")
#     mops.safe_query_for_location_info("999 cOuntY   roUTe 85, OSWego,  NY 13126")
#     mops.safe_query_for_location_info("6906 Quail Lake Drive, San Antonio, TX")

#     parser = ICSParser("../data/6jan18/download.ics")
#     event = parser.to_dict()
#     pprint.pprint(mops.safe_query_for_location_info(event))

# if __name__ == '__main__':
#     run_tests()
