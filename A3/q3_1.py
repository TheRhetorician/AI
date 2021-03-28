from heapq import heappush, heappop, heapify
import psycopg2
from time import time
from id_coord import *
from preprocess_2 import *

conn = psycopg2.connect(database="final", user = "kriti", password = "root", host = "127.0.0.1", port = "5432")


class Node:
    ''' each node represented as an instance of this class'''
    def __init__(self, node_id, latitude, longitude, parent_id, gn):
        self.node_id = node_id
        self.parent_id = parent_id # also has parent node from which it was directed used for backtracking
        self.latitude = latitude
        self.longitude = longitude
        self.gn = gn

    # hn is crow flies or euclidean distance or straight line distance between 2 points
    def get_hn(self, target_latitude, target_longitude):
        latitude = self.latitude
        longitude = self.longitude
        diff = ((target_latitude - latitude)**2 + (target_longitude-longitude)**2)**0.5
        # diff = (abs(target_latitude - latitude) + abs(target_longitude-longitude))
        
        self.hn = diff
        return diff


def search_neighbours(node_id, id_neigh):
    '''returns list of neighbours of a particular node'''

    if(id_neigh[node_id]):
        return list(id_neigh[node_id])
    return []


def create_node(node_id, node_coord, parent_id = None, latitude = None , longitude = None, gn = 0):
    '''creates a node'''
    
    latitude, longitude = node_coord[node_id][0] , node_coord[node_id][1]
    node = Node(node_id, latitude, longitude, parent_id, gn)
    return node


def give_id(lat, lon):
    '''returns id for given latitude and longitude'''

    cur = conn.cursor()
    cur.execute(f"SELECT * FROM planet_osm_nodes WHERE lat={lat} AND lon={lon};")
    rows = cur.fetchall()
    return rows[0][0]


def distance(node_id, new_latitude, new_longitude, node_coord):
    '''gn calculation is crow flies or euclidean distance or straight line distance between 2 points'''

    latitude, longitude = node_coord[node_id][0] , node_coord[node_id][1]
    # diff = abs(latitude - new_latitude) + abs(longitude-new_longitude)
    diff = ((new_latitude - latitude)**2 + (new_longitude-longitude)**2)**0.5

    return diff


def path_search(latitude, longitude, target_latitude, target_longitude, node_coord, id_neigh):
    '''function to search path'''

    if(latitude ==target_latitude and longitude==target_longitude):
        return []

    # heap to sort and select next best node
    prior_queue = [] 

    #stores nodes that have been visited already
    seen = set()

    node_id = give_id(latitude, longitude)
    start_id = node_id
    node = create_node(node_id, node_coord, None, latitude, longitude, 0)
    hn = node.get_hn(target_latitude, target_longitude)
    id_node = {}

    heappush(prior_queue, (hn, 0, node))
    k=1
    print("Searching for optimal path ...")
    while True:

        #if priority queue empty
        if not prior_queue:
            print('Path not found!!!')
            break

        node = heappop(prior_queue)[2]
        
        #if node already seen
        while node in seen:
            if prior_queue:
                node = heappop(prior_queue)[2]
            else:
                print('Path not found!!!')
                break

        id_node[node.node_id] = node
        latitude = node.latitude
        longitude = node.longitude

        if latitude==target_latitude and longitude==target_longitude:
            print('Solution found')
            target_id = node.node_id
            break

        seen.add(node.node_id)
        neighbours = search_neighbours(node.node_id, id_neigh)

        #not the target node then check and push its neighbours to heap
        for neighbour in neighbours:
            if neighbour not in seen:	
                new_node = create_node(neighbour, node_coord, node.node_id, gn = node.gn + distance(neighbour, latitude, longitude,node_coord)) 
                new_hn = new_node.get_hn(target_latitude, target_longitude)
                heappush(prior_queue, (new_hn + new_node.gn, k, new_node)) # k is a variable used as tiebreaker in case 2 nodes have same fn
                k = k + 1

    route = []
    
    node_id = target_id
    
    #backtracking to source node to get the path
    while True:
        node = id_node[node_id]
        route.append(node)
        node_id = node.parent_id
        if node_id==start_id:
            route.append(id_node[start_id])
            break
    route = list(reversed(route))
    return route

def calc(slat, slong, dlat, dlong, node_coord, id_neigh):
    t1= time()
    latitude = slat
    longitude = slong
    target_latitude = dlat
    target_longitude = dlong

    route = path_search(latitude, longitude, target_latitude, target_longitude, node_coord, id_neigh)
    
    final_route=[]
    for node in route :
        final_route.append([node.latitude/10**7, node.longitude/10**7])

    t2=time()
    print("---------------------------------------")
    print("Calculation time\n")
    print(t2-t1)
    return final_route

# if __name__ == '__main__' :
#     node_coord = makeDict()
#     id_neigh = preprocess()
#     calc(172405060, 784258271, 175469351,  785726514, node_coord, id_neigh)
