
'''
After I have audited and cleaned the data and transfered everything into table in my database, I can start running queries on it. 
The queries answer many questions such as:
	Number of nodes
	Number of way
	Number of unique users
	Most contributing users
	Number of users who contributed only once
	Top 10 amenities in San Fracisco
	Cuisines in San Francisco
	Shops in San Francisco
	Users who added amenities
	List of postcodes
'''

from pprint import pprint
import os
from hurry.filesize import size
import sqlite3
import csv
from pprint import pprint

# Change the path for sqlite_file and dirpath according to your data
sqlite_file = 'openstreetmap_sf_db.sqlite'
dirpath = '/Users/nazaninmirarab/Desktop/Data Science/P3/Project/Sizes'

files_list = []
for path, dirs, files in os.walk(dirpath):
    files_list.extend([(filename, size(os.path.getsize(os.path.join(path, filename)))) for filename in files])

for filename, size in files_list:
    print '{:.<40s}: {:5s}'.format(filename,size)


con = sqlite3.connect(sqlite_file)
cur = con.cursor()

def number_of_nodes():
    output = cur.execute('SELECT COUNT(*) FROM nodes')
    return output.fetchone()[0]

print 'Number of nodes: \n' , number_of_nodes()

def number_of_ways():
    output = cur.execute('SELECT COUNT(*) FROM ways')
    return output.fetchone()[0]

print 'Number of ways: \n' , number_of_ways()

def number_of_unique_users():
    output = cur.execute('SELECT COUNT(DISTINCT e.uid) FROM \
                         (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e')
    return output.fetchone()[0]

print 'Number of unique users: \n' , number_of_unique_users()

def most_contributing_users():
    
    output = cur.execute('SELECT e.user, COUNT(*) as num FROM \
                         (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
                         GROUP BY e.user \
                         ORDER BY num DESC \
                         LIMIT 10 ')
    pprint(output.fetchall())
    return output.fetchall()

print 'Most contributing users: \n', most_contributing_users()

def number_of_users_contributed_once():
    
    output = cur.execute('SELECT COUNT(*) FROM \
                             (SELECT e.user, COUNT(*) as num FROM \
                                 (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
                                  GROUP BY e.user \
                                  HAVING num = 1) u')
    
    return output.fetchone()[0]
                         
print 'Number of users who have contributed once: \n', number_of_users_contributed_once()

def top_ten_amenities_in_sf():
    output = cur.execute('SELECT value, COUNT(*) as num FROM nodes_tags\
                            WHERE key="amenity" \
                            GROUP BY value \
                            ORDER BY num DESC \
                            LIMIT 10' )
    pprint(output.fetchall())
    return output.fetchall()

print 'Top ten amenities: \n', top_ten_amenities_in_sf()

def cuisines_in_sf():
    output = cur.execute ('SELECT value, COUNT(*) as num FROM ways_tags \
                           WHERE key="cuisine" \
                           GROUP BY value \
                           ORDER BY num DESC \
                           LIMIT 10')
    pprint(output.fetchall())
    return output.fetchall()

print 'Top 10 cuisines: \n', cuisines_in_sf()

def shops_in_sf():
    output = cur.execute('SELECT value, COUNT(*) as num FROM nodes_tags\
                            WHERE key="shop" \
                            GROUP BY value \
                            ORDER BY num DESC' )
    pprint.pprint(output.fetchall())
    return output.fetchall()

print 'Different types of shops: \n', top_ten_amenities_in_sf()

def users_who_added_amenity():
    output = cur.execute('SELECT DISTINCT(nodes.user), nodes_tags.value FROM \
                            nodes join nodes_tags \
                            on nodes.id=nodes_tags.id \
                            WHERE key="amenity" \
                            GROUP BY value \
                            LIMIT 10' ) # Remove this part to get the whole list
    pprint(output.fetchall())
    return output.fetchall()

print 'Users who added amenity to the map: \n', users_who_added_amenity()

def list_of_postcodes():
    output = cur.execute('SELECT e.value, COUNT(*) as num FROM \
                            (SELECT value FROM nodes_tags WHERE key="postcode"\
                             UNION ALL SELECT value FROM ways_tags WHERE key="postcode") e \
                            GROUP BY e.value \
                            ORDER BY num DESC \
                            LIMIT 5' ) # Remove this limit to see the complete list of postcodes
    pprint(output.fetchall())
    return output.fetchall()

print 'List of postcodes: \n'
list_of_postcodes()

def amenities_around_94122():
    output = cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
                          FROM nodes_tags \
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE key="amenity") AS amenities \
                            ON nodes_tags.id = amenities.id \
                            WHERE nodes_tags.key="amenity"\
                            GROUP BY nodes_tags.value \
                            ORDER BY num DESC \
                            LIMIT 20' ) # Remove this limit to see the complete list of postcodes
    pprint(output.fetchall())
    return output.fetchall()

print 'Amenities around 94122 postcode: \n'
amenities_around_94122()

def most_popular_cafes():
    output = cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
                          FROM nodes_tags \
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="coffee_shop") AS cafes \
                            ON nodes_tags.id = cafes.id \
                            WHERE nodes_tags.key="name"\
                            GROUP BY nodes_tags.value \
                            ORDER BY num DESC \
                            LIMIT 10' ) # Remove this limit to see the complete list of postcodes
    pprint(output.fetchall())
    return output.fetchall()

print 'Most popular cafes in San Francisco: \n'
most_popular_cafes()
