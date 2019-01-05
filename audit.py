import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# This pattern finds different types of streets in street names
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# The list of street types that we want to have
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# The list of dictionaries, containing street types that need to be changed to match the 'expected' list
mapping = { "St": "Street", "St.": "Street", "street": "Street",
            "Ave": "Avenue", "Ave.": "Avenue", "AVE": "Avenue,", "avenue": "Avenue",
            "Rd.": "Road", "Rd": "Road", "road": "Road",
            "Blvd": "Boulevard", "Blvd.": "Boulevard", "Blvd,": "Boulevard", "boulevard": "Boulevard",
            "broadway": "Broadway",
            "square": "Square", "square": "Square", "Sq": "Square",
            "way": "Way",
            "Dr.": "Drive", "Dr": "Drive",
            "ct": "Court", "Ct": "Court", "court": "Court",
            "cres": "Crescent", "Cres": "Crescent", "Ctr": "Center",
            "Hwy": "Highway", "hwy": "Highway",
            "Ln": "Lane", "Ln.": "Lane",
            "parkway": "Parkway" }

def audit_street_type(street_types, street_name):
	""" A function to match different types of streets with the expected list defined.

	This function is called from audit_name function.
	Args:
	-param1 street_types: list of dictionaries containing different street types.
		The key in the dictionary is the type of street (e.g. avenue, street),
		and the values are names of streets (e.g. Park avenue, 5th street).
	-param2 street_name: name of the street (i.e. tag.attrib['v']). This name is
		passed to this function from the audit_name function.
	
	street_type_re is the regex pattern and searches street_name to find any
	pattern that matches the constant list 'expected' which contains types of street.
	If any of the street types in the expected list matches the pattern, the function
	passes; if not, the function adds the street type as a key to street_types 
	dictionary and the street_name as a name to that street type list. (Example: 
	[Charles Ave. , Potreto Ave.] will change to
	street_types[Ave.]={'Charles Ave.','Potreto Ave.'})
	"""
    m = street_type_re.search(street_name) #searches for the regex pattern in the street name
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
	"""Returnes the attributes that equal street address"""

    return (elem.attrib['k'] == "addr:street")


def audit_name(osmfile):
	""" A function to audit different street types and create a list of dictionaries.

	Arg:
	-param1 osmfile: reads the OpenStreetMap data
	
	Iterates through the osmfile looking for starting tags (e.g. <node, <way). If the
	tag matches node or way, it iterates through their 'tag' tag, and calls
	audit_street_type with the street_types dictionary and tag.attrib['v'] attribute.
	This attribute contains the name of the street. It 

	Return:
	-returns the list of dictionaries containing list of street types with their
	corresponding street name.
	"""
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    # Iteratively parses the XML file
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # Iterates through the 'tag' tag of node and way tags
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_name(name, mapping):
	""" A function to correct the street types according to mappings

	Args:
	-param1 name: The street name coming from tag.attrib['v'] attribute. This 
		parameter is defined in shape_element function from shaping_csv.py file.
	-param2 mapping: Is the list of mapping created while auditing the street names
		in audit_street_type function
	The name is split by space and each word is compared to the mapping. If it
	exists in the mapping, it is changed to its expected pattern, and added to
	the output list. Output list contains all corrected street names.

	Return:
	-output: The list of corrected street names. (Example 5th street is separated
		to '5th' and 'street', and each is compared to mapping. For 'street' the
		mapping expects it to change to 'Street'. Function changes it to 'Street'
		and adds '5th Street' to the output list)
	"""
    output = list()
    parts = name.split(" ")
    for part in parts:
        if part in mapping:
            output.append(mapping[part])
        else:
            output.append(part)
    return " ".join(output)  
                       
def dicti(data, item):
	"""A dictionary to store postcodes.

	The dictionary key is the postcode and the dictionary value is the number of
	times the postcode is repeated in the data.
	"""
    data[item] += 1

def get_postcode(elem):
	"""Returns the attribute that equals to postcode"""
    return (elem.attrib['k'] == "addr:postcode")

def audit_postcode(osmfile):
	""" A function to audit different postcodes and create a list of dictionaries.

	Arg:
	-param1 osmfile: reads the OpenStreetMap data
	
	Iterates through the osmfile looking for starting tags (e.g. <node, <way). If the
	tag matches node or way, it iterates through their 'tag' tag, and calls
	get_postcode to find the postcode attribute. Then it calls the dicti function and 
	add the postcode to the dictionary.

	Return:
	-data: a dictionary containing postcodes and the number of times they have been
	repeated throughout the data. (Example: {'94122', '94122', '94122', '94611'} will
		give dicti{['94122']=3, ['94611']=1}
	"""
    osm_file = open(osmfile, "r")
    data = defaultdict(int)
    # Parsing the XML file
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        
        # Iterating through node and way elements.
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if get_postcode(tag):
                    dicti(data, tag.attrib['v'])
    return data

def update_postcode(digit):
	""" A function to correct the postcodes according to defined regex patterns.

	Arg:
	-param digit: The postcode coming from tag.attrib['v'] attribute. This 
		parameter is defined in shape_element function from shaping_csv.py file.

	Three regex patterns are defined according to the variety of postcodes gathered
	from audit_postcode function. 

	'^\D*(\d{5}$)' : Extract only 5 digits from the pattern. This regex asserts 
	position at start of the string ( ^ ) and matches any character that is NOT 
	a digit ( \D* ). The ( \d{5} ) matches a digit exactly 5 times. In case the
	postcode starts with letters (e.g. CA 12345), it gives two groups of output:
	One is 'CA' and the other is '12345'. Depending on which one is needed, the
	preferred group can be chosen.

	'^(\d{5})-\d{4}$': Extract the first 5 digits. This regex matches digits 5 
	times, is followed by a '-', and then matching digits exactly 4 times.

	'^\d{6}$': Find postcodes that are exactly 6-digit long. A 6-digit long 
	postcode is invalid; therefore, will be set to '00000'

	Defined another condition to deal with postcodes shorter than 5-digit long,
	or postcodes that equal to 'CA'. Both are invalid postcodes and will be set
	to '00000'

	Return:
	-output: Return a list of corrected postcodes

	"""
    output = list()
    
    first_category = re.compile('^\D*(\d{5}$)', re.IGNORECASE)
    second_category = re.compile('^(\d{5})-\d{4}$')
    third_category = re.compile('^\d{6}$')
    
    # For postcodes that are 5-digit long or are in this format 'CA 12345'
    if re.search(first_category, digit):
        new_digit = re.search(first_category, digit).group(1)
        output.append(new_digit)
    
    # For postcodes that are in this format '12345-6789'
    elif re.search(second_category, digit):
        new_digit = re.search(second_category, digit).group(1)
        output.append(new_digit)
    
    # For postcodes that are 6-digit long
    elif re.search(third_category, digit):
        third_output = third_category.search(digit)
        new_digit = '00000'
        output.append('00000')
    
    # For postcodes equal to 'CA' or shorter than 5-digit long
    elif digit == 'CA' or len(digit) < 5:
        new_digit = '00000'
        output.append(new_digit)

    return ', '.join(str(x) for x in output) 



