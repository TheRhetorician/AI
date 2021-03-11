from heapq import heappush, heappop, heapify
import psycopg2
from time import time
from id_coord import *
from preprocess_2 import *


class Node:
    def __init__(self, node_id, latitude, longitude, parent_id, gn):
        self.node_id = node_id
        self.parent_id = parent_id
        self.latitude = latitude
        self.longitude = longitude
        self.gn = gn

    def get_hn(self, target_latitude, target_longitude):
        latitude = self.latitude
        longitude = self.longitude
        diff = abs(target_latitude - latitude) + abs(target_longitude-longitude) 
        self.hn = diff
        return diff


def search_neighbours(node_id):
    if(id_neigh[node_id]):
        return list(id_neigh[node_id])
    return []

def create_node(node_id, parent_id = None, latitude = None , longitude = None, gn = 0):
    latitude, longitude = node_coord[node_id][0] , node_coord[node_id][1]
    node = Node(node_id, latitude, longitude, parent_id, gn)
    return node

def give_id(lat, lon):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM planet_osm_nodes WHERE lat={lat} AND lon={lon};")
    rows = cur.fetchall()
    return rows[0][0]


def distance(node_id, new_latitude, new_longitude):
    latitude, longitude = node_coord[node_id][0] , node_coord[node_id][1]
    diff = abs(latitude - new_latitude) + abs(longitude-new_longitude)
    return diff


def path_search(latitude, longitude, target_latitude, target_longitude):
    prior_queue = []
    seen = set()
    node_id = give_id(latitude, longitude)
    start_id = node_id
    node = create_node(node_id, None, latitude, longitude, 0)
    hn = node.get_hn(target_latitude, target_longitude)
    id_node = {}

    heappush(prior_queue, (hn, 0, node))
    k=1
    print("Searching for optimal path ...")
    while True:
        if not prior_queue:
            print('Path not found!!!')
            break

        node = heappop(prior_queue)[2]

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
        neighbours = search_neighbours(node.node_id)

        for neighbour in neighbours:
            if neighbour not in seen:	
                new_node = create_node(neighbour, node.node_id, gn = node.gn + distance(neighbour, latitude, longitude)) 
                new_hn = new_node.get_hn(target_latitude, target_longitude)
                heappush(prior_queue, (new_hn + new_node.gn, k, new_node))
                k = k + 1

    route = []
    node_id = target_id
    while True:
        node = id_node[node_id]
        route.append(node)
        node_id = node.parent_id
        if node_id==start_id:
            route.append(id_node[start_id])
            break
    route = list(reversed(route))
    return route

if __name__ == '__main__' :
    t1= time()
    conn = psycopg2.connect(database="final", user = "kriti", password = "root", host = "127.0.0.1", port = "5432")
    
    latitude = 172405060
    longitude = 784258271
    target_latitude = 175469351
    target_longitude = 785726514

    node_coord = makeDict()
    id_neigh = preprocess()
    route = path_search(latitude, longitude, target_latitude, target_longitude)
    
    for node in route :
        print(node.latitude, node.longitude)

    print(len(route))
    conn.commit()
    conn.close()
    t2=time()
    print()
    print()
    print(t2-t1)
# 172405060  784258271
# 175469351  785726514