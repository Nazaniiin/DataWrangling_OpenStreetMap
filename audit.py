
'''This code is part of the final project

In this code I audit and clean the data for street names and postcodes.

For the Street Names:
- I audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
  the unexpected street types to the appropriate ones in the expected list.
  I add mappings only for the actual problems I find in this OSMFILE,
  not a generalized solution, since that may and will depend on the particular area you are auditing.
- I write the update_name function, to actually fix the street name.
  The function takes a string with street name as an argument and should return the fixed name
  
For Postcodes:
- I audit the OSMFILE and find any variation of postcodes entered by users.
  I create a dictionary and store all the variations of postcodes in it.
  I come up with regular expressions to find those patterns.
- I write the update_postcode function, applying the regular expression patterns to fix the issues

Later, I need to import this code to the 'shaping_csv.py' file so that I can audit the data before the CSV files are created.
'''

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# the list of street types that we want to have
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

#The list of dictionaries, containing street types that need to be changed to match the expected list
mapping = { "St": "Street",
            "St.": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "AVE": "Avenue,",
            "avenue": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "road": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Blvd,": "Boulevard",
            "boulevard": "Boulevard",
            "broadway": "Broadway",
            "square": "Square",
            "way": "Way",
            "Dr.": "Drive",
            "Dr": "Drive",
            "ct": "Court",
            "Ct": "Court",
            "court": "Court",
            "Sq": "Square",
            "square": "Square",
            "cres": "Crescent",
            "Cres": "Crescent",
            "Ctr": "Center",
            "Hwy": "Highway",
            "hwy": "Highway",
            "Ln": "Lane",
            "Ln.": "Lane",
            "parkway": "Parkway"
            }

# Audit and clean street types
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_name(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    # parses the XML file
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # iterates through the 'tag' element of node and way elements
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def update_name(name, mapping):
    output = list()
    parts = name.split(" ")
    for part in parts:
        if part in mapping:
            output.append(mapping[part])
        else:
            output.append(part)
    return " ".join(output)  
            
# Audit and clean postcodes           
def dicti(data, item):
    data[item] += 1

def get_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_postcode(osmfile):
    osm_file = open(osmfile, "r")
    data = defaultdict(int)
    # parsing the XML file
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        
        # iterating through node and way elements.
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if get_postcode(tag):
                    dicti(data, tag.attrib['v'])
    
    return data

def update_postcode(digit):
    output = list()
    
    first_category = re.compile(r'^\D*(\d{5}$)', re.IGNORECASE)
    
    second_category = re.compile('^(\d{5})-\d{4}$')
    
    third_category = re.compile('^\d{6}$')
    
    if re.search(first_category, digit):
        new_digit = re.search(first_category, digit).group(1)
        output.append(new_digit)
        
    elif re.search(second_category, digit):
        new_digit = re.search(second_category, digit).group(1)
        output.append(new_digit)
    
    elif re.search(third_category, digit):
        third_output = third_category.search(digit)
        new_digit = '00000'
        output.append('00000')
    
    # this condition matches the third category for the other two types of postcodes
    elif digit == 'CA' or len(digit) < 5:
        new_digit = '00000'
        output.append(new_digit)

    return ', '.join(str(x) for x in output) 



