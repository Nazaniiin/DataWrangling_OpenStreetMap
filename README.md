# OpenStreetMap Data Wrangling Process

## A Short Introduction on OpenStreetMap
OpenStreetMap (OSM) foundation is building free and editable map of the world, enabling the development of freely-reusable geospatial data. The data from OpenStreetMap is being used by many applications such as GoogleMaps, Foursquare and Craigslist.

OpenStreetMap data structure has four core elements: Nodes, Ways, Tags, and Relations

- Nodes are points with a geographic position stored as lon (longitude) and lan (latitude). They are used to show points on the map such as points of interest.
- Ways are ordered list of nodes, representing a polyline or a polyline if they make a closed loop. They are used to show streets, rivers, and area such as parks, lakes, etc.
- Relations are ordered list of nodes, ways and relations (called 'members') where each members can have a 'role' (a string). They are used to show the relation between nodes and ways such as restrictions on roads.
- Tags are pairs of Keys and Values. They are used to store metdata of the map such as address, type of building, or any sort of physical property. Tags are always attached to a node, way or relation and are not stand-alone elements.

To look at the map, or download your area of interest, you can visit http://www.openstreetmap.org website. 

For more information you can check their wiki which includes all the necessary information and documentation:
https://en.wikipedia.org/wiki/OpenStreetMap

Users can add points on the map, create relations of the nodes and ways, and assign properties such as address or type to them. The data can be stored in OSM format, and can be access in different formats. For the purpose of this project, I use the OSM XML format.
http://wiki.openstreetmap.org/wiki/OSM_XML

In this project, I will work with the raw data from an area. Since the data is put by different users, I suppose it can be quite messy; therefore, I will use cleaning and auditing functions to make the data look clean for analysis. I will export the data into CSV format and use this format to create tables in my SQLite database. Then I run queries on the database to extract information such as number of nodes and ways, most contributing users, top points of interest, etc. I will conclude the project by discussing benefits as well as some anticipated problems in implementing the improvement.

## Area Chosen for Analysis

For this project, I chose San Francisco area in the US. I chose this area as it is a point of interest for me with its big IT corporations; also, it is a place I want to travel to one day. I decided to download the file locally to my machine.  
https://mapzen.com/data/metro-extracts/metro/san-francisco_california/

The 'metro extracts' will provide the map of the metropolian area (i.e. where you can find more elements to work with)

The original file is about 1.01GB in size; however, I use a sample file about 50MB to perform my initial analysis on. Once I am satisfied with the code, I run it on the original file to create the CSV files for my database. 

The data analyzed in this Jupyter notebook is from the sample file to be able to show shorter results from my analysis. I have included all the functions here, as well as the function to create CSV files, in separate .py files in my repository. Using those you can run the code on the original file. 
https://github.com/Nazaniiin/OpenStreetMap_DataWrangling

## Exploring the Data a bit

Let's start going through the data, find its problems and clean them. First, we'll take a look into the dataset and parse through using ElementTree and extract information such as different types of elements (nodes,ways,etc.) in the OSM XML file.

Using ET.iterparse (i.e. iterative parsing) is efficient here since the original file is too large for processing the whole thing. So iterative parsing will parse the file as it builds it.  
http://stackoverflow.com/questions/12792998/elementtree-iterparse-strategy

In this code, I will iterate through different tags in the XML (nodes,ways,relations,member,...) and count them, put them in a dictionary with the key being the tag name.
