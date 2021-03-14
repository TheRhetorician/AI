import psycopg2
from tqdm import tqdm

def preprocess():
    conn = psycopg2.connect(database="final", user = "kriti", password = "root", host = "127.0.0.1", port = "5432")
    id_neigh={}

    cur1 = conn.cursor()
    cur1.execute(f"select nodes from planet_osm_ways ;")
    rows= cur1.fetchall()
    for row in tqdm(rows):
        for i in range(len(row[0])):
            if(i>0):
                if(row[0][i] in id_neigh):
                    id_neigh[row[0][i]].add(row[0][i-1])
                else:
                    id_neigh[row[0][i]] = set([row[0][i-1]])   
            if(i<len(row[0])-1):
                if(row[0][i] in id_neigh):
                    id_neigh[row[0][i]].add(row[0][i+1])
                else:
                    id_neigh[row[0][i]] = set([row[0][i+1]])
    conn.commit()
    conn.close()
    return id_neigh