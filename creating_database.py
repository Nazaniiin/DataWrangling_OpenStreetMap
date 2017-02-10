
'''
This code is part of the final project.

It creats SQL tables for nodes_tags, ways, ways_nodes, ways_tags and nodes.

'''
import sqlite3
import csv
from pprint import pprint

# Put the path to your sqlite database. If no database is available, a new one will be created
sqlite_file = 'openstreetmap_sf_db.sqlite'

# Connecting to the database
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

# Making sure a table that already exists does not get created
cur.execute('DROP TABLE IF EXISTS nodes')
conn.commit()

# Creating the nodes_tags table
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT)
''')
conn.commit()

with open('nodes_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    in_db = [(i['id'], i['key'], i['value'].decode('utf-8'), i['type']) for i in dr]
    
#insert the data
cur.executemany('INSERT INTO nodes_tags(id, key, value, type) VALUES(?, ?, ?, ?);', in_db)
conn.commit()

#creating the ways table
cur.execute('''
    CREATE TABLE ways(id INTEGER PRIMARY KEY, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp DATETIME)
''')
conn.commit()

with open('ways.csv', 'rb') as f:
    dr = csv.DictReader(f)
    in_db = [(i['id'], i['user'].decode('utf-8'), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]
    
#insert the data
cur.executemany('INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES(?, ?, ?, ?, ?, ?);', in_db)
conn.commit()

#creating the ways_nodes table
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
conn.commit()

with open('ways_nodes.csv', 'rb') as f:
    dr = csv.DictReader(f)
    in_db = [(i['id'], i['node_id'], i['position']) for i in dr]
    
#insert the data
cur.executemany('INSERT INTO ways_nodes(id, node_id, position) VALUES(?, ?, ?);', in_db)
conn.commit()

#creating the ways_tags table
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER , key TEXT, value TEXT, type TEXT)
''')
conn.commit()

with open('ways_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    in_db = [(i['id'], i['key'], i['value'].decode('utf-8'), i['type']) for i in dr]
    
#insert the data
cur.executemany('INSERT INTO ways_tags(id, key, value, type) VALUES(?, ?, ?, ?);', in_db)
conn.commit()

#creating the nodes table
cur.execute('''
            CREATE TABLE IF NOT EXISTS nodes(id INTEGER PRIMARY KEY, lat REAL, 
            lon REAL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp DATE)
        ''')
conn.commit()

with open('nodes.csv', 'rb') as f:
    dr = csv.DictReader(f)
    in_db = [(i['id'].decode('utf-8'), i['lat'],i['lon'],i['user'].decode('utf-8'), i['uid'],i['version'],i['changeset'],i['timestamp']) for i in dr]
    
#insert the data
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?,?, ?, ?, ?);", in_db)
conn.commit()
