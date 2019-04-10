import json
import numpy as np
from pprint import pprint
from os import listdir
from os.path import isfile, join
from MongoOps import MongoOps
from ICSParser import ICSParser
from make_directions_matrix import DirectionsMatrix
import random


def random_combination(iterable, r):
    '''
    This function helps test different scenarios.
    '''
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)


class Graph(object):
    """ 
    A Python Class
    A simple Python graph class, demonstrating the essential 
    facts and functionalities of graphs.
    Original implementation from https://www.python-course.eu/graphs_python.php
    Changes to include weighted edges from https://towardsdatascience.com/to-all-data-scientists-the-one-graph-algorithm-you-need-to-know-59178dbb1ec2
    Some functions have been removed because they are not 
    going to be used, and I would like to protect future 
    users from using this graph object incorrectly.
    """
    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict
        self.__vertices = self.vertices()

    def vertex_ids(self):
        """ returns the vertices of a graph """
        vertices = []
        for val in self.__graph_dict:
            vertices += [val['ID']]
        self.__vertices = vertices
        return list(self.__vertices)
    
    def vertices(self):
        """ returns the vertices of a graph """
        vertices = []
        for val in self.__graph_dict:
            ver = self.__removekey(val, 'edges')
            vertices += [ver]
        self.__vertices = vertices
        return list(self.__vertices)
    
    def get_vertex_from_vid(self, vid):
        ''' 
        returns the vertex given its id.
        I would LIKE to assume that the vertex's id will match its location in
        graph_dict, but I won't in the case that someone passes in an irregualar
        graph_dict to the Graph object.
        '''
        vertex = None
        for val in self.__graph_dict:
            if val['ID'] == vid:
                vertex = val
        if vertex == None:
            raise Exception('Vertex ID provided not found.')
        return vertex

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()
    
    def get_edges_from_vid(self, vid):
        ''' 
        returns the edges from a vertex, given its id.
        '''
        vertex = self.get_vertex_from_vid(vid)
        edges = self.get_edges(vertex)
        return edges

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            edges += self.get_edges(vertex)
        return edges

    def get_edges(self, vertex):
        """
        returns the edges of a vertex dictionary
        """
        edges = []
        for neighbour in vertex['edges']:
            weight = neighbour[1]
            n = neighbour[0]
            v = vertex['ID']
            if [v, n, weight] not in edges:
                edges.append([v, n, weight])
        return edges
    
    def __str__(self):
        res = "vertices:\n"
        for k in self.__vertices:
            res += str(k) + " \n"
        res += "\nedges:\n"
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def adj_mat(self):
        return self.__graph_dict
    
    def __removekey(self, d, key):
        r = dict(d)
        del r[key]
        return r

class OpenHouseGraph(Graph):
    """
    OpenHouseGraph extends the Graph Object. Base Graph object was inspired by,
    https://towardsdatascience.com/to-all-data-scientists-the-one-graph-algorithm-you-need-to-know-59178dbb1ec2
    """

    def visit_next(self, current_vertex, arrival_time, visited, trip = [], average_time_at_each_house = 30):
        """
        Recursive function, given by a starting vertex, iterate over outbound 
        edges to travel to every house and determine what the time would be
        after getting to a destination. 
        """
        acyclic_edges = self.get_acyclic_edges(self.get_edges(current_vertex), visited)
        for a_edge in acyclic_edges:
            
            # Determine when you leave at the next house.
            departure_time = arrival_time + average_time_at_each_house

            # Determine when you 'arrive' at the next house.
            next_arrival_time = departure_time + a_edge[2]

            idx = a_edge[1]
            a_vertex = self.get_vertex_from_vid(idx)
            opened, closed = self.open_and_closed(next_arrival_time, a_vertex)
            wait_function = self.get_wait_function(opened, closed)
            next_arrival_time = wait_function(a_vertex['start'], next_arrival_time)

            # If you're not too late, continue with this path
            if next_arrival_time > 0:
                step = visited + [idx]
                trip += self.visit_next(a_vertex, next_arrival_time, step)
        return [visited] if len(visited) > 1 else trip


    def flatten(self, trips):
        results = []
        for i in range(len(trips)):
            if isinstance(trips[i], int):
                return trips
            else:
                if len(trips[i]) > 0:
                    results += [trips[i]]
        return results

    def get_acyclic_edges(self, edges, visited):
        """
        Gets edges out of a vertex that have not been visited.
        """
        E = []
        for edge in edges:
            idx = edge[1]
            if self.been_visited(visited, idx):
                continue
            else:
                E += [edge]
        return E
            
    def been_visited(self, visited, v):
        '''
        Checks to make sure you're not going back to a node that has already 
        been visited.
        '''
        return v in visited

    def open_and_closed(self, arrival_time, next_vertex):
        """
        Determines whether an open house has started/ended when you arrive.
        """
        opened = arrival_time >= next_vertex['start']
        closed = arrival_time >= next_vertex['end']
        return [opened, closed]

    def get_wait_function(self, opened, closed):
        """
        Given the combination of booleans opened and closed, set the wait variable
        to a given set of values. Return the lambda function corresponding key equal
        to the wait variable.
        """
        if not opened:
            wait = "Wait"
        elif not closed:
            wait = "No need to wait"
        elif closed:
            wait = "Too late"
        else:
            wait = "Time doesn't work that way!"
        wait_function = {
            "No need to wait" : lambda opens_at, current_time : current_time,
            "Wait" : lambda opens_at, current_time : opens_at,
            "Too late" : lambda opens_at, current_time : -1,
            "Time doesn't work that way!" : lambda opens_at, current_time : -1
        }
        return wait_function[wait]
        
    def convert_mins_to_time(self, time):
        """
        Converts a time in the form of 600 to its more recognisable form.
        600 corresponding to 10:00 (or 600 minutes from midnight).
        """
        hours_minutes = str(time / 60).split('.')
        hours_minutes[0] = hours_minutes[0]
        hours_minutes[1] = str(float('0.'+hours_minutes[1]) * .6)[2:4]
        return hours_minutes[0], hours_minutes[1]

if __name__ == "__main__":
    
    locations = []
    mops = MongoOps()
    sample_data_files = [f for f in listdir("/data") if isfile(join("/data", f)) and f != '.DS_Store' ]
    for open_house_file in sample_data_files:
        try:
            parser = ICSParser("/data/%s" % open_house_file)
            event = parser.to_dict()
            result = mops.safe_query_for_location_info(event)
            locations += [result]
        except:
            pass

    random_locations = random_combination(locations, len(locations))
    DM = DirectionsMatrix(random_locations, mops)
    DM.generate_simplified_directions_matrix()
    sdm = DM.simplified_directions_matrix


    # Showing off EST/EDT time of day of the open houses and the conversion to minutes from midnight that day
    for i in range(len(sdm)):
        start = str(int(sdm[i]['dtstart'][9:-3])-400)
        start_minutes = int(start[:-2])*60 + int(start[-2:])
        end = str(int(sdm[i]['dtend'][9:-3])-400)
        end_minutes = int(end[:-2])*60 + int(end[-2:])
        sdm[i]['start_minutes'] = start_minutes
        sdm[i]['end_minutes'] = end_minutes
    
    vertices = []
    V = None
    for i in range(len(sdm)):
        V = {'ID' : i, 
                'start' : sdm[i]['start_minutes'], 
                'end' : sdm[i]['end_minutes'], 
                'edges' : sdm[i]['durations'],
                'address_hash' : sdm[i]['address_hash'],
                'address' : sdm[i]['location']['address']}
        vertices += [V]
    ohg = OpenHouseGraph(vertices)

    paths = []
    for v in ohg.vertices():
        starting_id = v['ID']
        starting_vertex = ohg.get_vertex_from_vid(starting_id)
        start_time = starting_vertex['start']
        path = ohg.visit_next(starting_vertex, start_time, [starting_id])
        if len(path) > 0:
            for p in path:
                if p not in paths:
                    paths += [p]
    paths = np.array(paths)

    pprint(paths)
    
    max_len = max([len(path) for path in paths])
    print('max_len:', max_len)
    P = []
    for path in paths:
        if len(path) >= max_len:
            P += [path]
    print(P)
    pprint(vertices)
    for path in P:
        print('------------------------- Showing path for {}'.format(path))
        for p in path:
            print(vertices[p]['address'])
    print('\n')
