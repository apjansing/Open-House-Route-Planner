import json
import numpy as np
from os import listdir
from MongoOps import MongoOps
from ICSParser import ICSParser
from os.path import isfile, join


class DirectionsMatrix():
    def __init__(self, locations = [], mops = MongoOps()):
        self.locations = locations
        self.directions_matrix = None
        self.mops = mops
    
    def get_directions_matrix(self):
        directions_matrix = []
        for location1 in locations:
            loc1_row = []
            for location2 in locations:
                if location1['location'] != location2['location']:
                    loc1_loc2_directions = self.mops.safe_query_for_directions(start = location1, stop = location2)
                    loc1_row += [loc1_loc2_directions]
                else:
                    loc1_row += [None]
            directions_matrix += [loc1_row]
        self.directions_matrix = np.array(directions_matrix)

    def generate_simplified_directions_matrix(self):
        try:
            if self.directions_matrix == None:
                self.get_directions_matrix()
        except:
            pass
        simplified_directions_matrix = []
        for i in range(len(self.directions_matrix)):
            row_data = self._get_start_location_info(i)
            simplified_directions_matrix += [self._get_time_between_points(i, row_data)]
        self.simplified_directions_matrix = np.array(simplified_directions_matrix)

    def _get_start_location_info(self, row):
        start = ''
        if self.directions_matrix[row][0] != None:
            start = self.directions_matrix[row][0]['start']
        else:
            start = self.directions_matrix[row][1]['start']
        return self.mops.safe_query_for_location_info(start)

    def _get_time_between_points(self, row, simplified_directions_row):
        durations = []
        for j in range(len(self.directions_matrix[row])):
            if self.directions_matrix[row][j] == None:
                durations += [[j, -1]]
            else:
                duration = self.directions_matrix[row][j]['directions'][-1]['Duration (min)']
                durations += [[j, duration]]
        simplified_directions_row['durations'] = durations
        return simplified_directions_row


if __name__ == "__main__":
    sample_data_files = [f for f in listdir("/data") if isfile(join("/data", f))]
    mops = MongoOps()
    locations = []
    for open_house_file in sample_data_files:
        parser = ICSParser("/data/%s" % open_house_file)
        event = parser.to_dict()
        # print(event)
        result = mops.safe_query_for_location_info(event)
        locations += [result]
    dir_mx = DirectionsMatrix(locations, mops)
    # dir_mx.get_directions_matrix()
    dir_mx.generate_simplified_directions_matrix()
    # print(dir_mx.directions_matrix[0][1])
    # print(dir_mx.directions_matrix.shape)
    print(dir_mx.simplified_directions_matrix)
    