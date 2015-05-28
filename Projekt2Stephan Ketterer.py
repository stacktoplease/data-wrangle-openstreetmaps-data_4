import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r"^([a-z]|_)*$")
lower_colon = re.compile(r"^([a-z]|_)*:([a-z]|_)*$")
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    node["created"]={}
    node["pos"]=[]
    node["address"]={}
    node["node_refs"]=[]
    #creating all the necessary dictionaries and lists 
    if element.tag == "node" or element.tag == "way" :
        #filtering out only node and way elements
        for secondlevel in element:
            if secondlevel.tag=="nd":
                node["node_refs"].append(secondlevel.attrib["ref"])        
            if "k" in secondlevel.attrib:
                if re.search(problemchars,secondlevel.attrib["k"]):
                    #if any of the problemchars occur, most likely the information is faulty and we have to ignore it
                    pass                 
                else:
                    if secondlevel.attrib["k"].count(":")==2:
                        #if there are 2 ":" in the adress it is most likely invalid, so ignore it
                        pass
                    elif secondlevel.attrib["k"].count(":")==1:
                        if secondlevel.attrib["k"].startswith("addr:"):
                            stripped=secondlevel.attrib["k"].replace("addr:","")
                            node["address"][stripped]=secondlevel.attrib["v"]
                            #getting rid of "addr" as a needless start of the information, because we already have it in the dictionary key
                    else:
                        node[secondlevel.attrib["k"]]=secondlevel.attrib["v"]
            if "postcode" in node["address"]:
                help=node["address"]["postcode"].replace("NV","")
                node["address"]["postcode"]=help
                #solves the Problem with the "NV" that sometimes is put into the zipcode
            if "city" in node["address"]:
                help=node["address"]["city"].replace("NV","")
                node["address"]["city"]=help
                #takes care of "NV" in the city
        for x in CREATED:
            if x in element.attrib:
                node["created"][x]=element.attrib[x]
                # fill up the sub dictionary created with the corresponding values
        node["id"]=element.attrib["id"]
        #since not every key is in every part of the data, we will check if it exists, if it does, create the key/value pair, if not just pass and move on
        try:
            node["visible"]=element.attrib["visible"]
        except:
            pass
        try:
            node["amenity"]=element.attrib["amenity"]
        except :
            pass
        try:
            node["cuisine"]=element.attrib["cuisine"]
        except :
            pass        
        try:
            node["name"]=element.attrib["name"]
        except :
            pass
        try:
            node["phone"]=element.attrib["phone"]
        except :
            pass 
        try:
            node["type"]=element.tag
        except :
            pass
        try:
            node["pos"].append(float(element.attrib["lat"]))
            node["pos"].append(float(element.attrib["lon"]))
            #we need to use float() for conversion to not lose important decimal data
            if node["address"]=={}:
                del node["address"]
            if node["node_refs"]==[]:
                del node["node_refs"]
                return node
            else:
                return node                    
        except:
            if node["address"]=={}:
                del node["address"]
            if node["node_refs"]==[]:
                del node["node_refs"]
                return node 
            else:
                return node  
            #the last few lines check if the key adress and node_refs have actual corresponding values, and if not, the key gets deleted              
            pass
        else:
            return None

def audit():
    osm_file = open("c:\Users\Stephan\Downloads\lasvegas.osm", "r")
    with open("c:\Users\Stephan\Downloads\lasvegas2.txt", "w+") as outfile:
        for event, elem in ET.iterparse(osm_file, events=("start",)):   
            if elem.tag == "node" or elem.tag == "way":
                json.dump(shape_element(elem),outfile)
                elem.clear()

audit()