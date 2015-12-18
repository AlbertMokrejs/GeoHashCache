import hashlib
import urllib2 
import time
import json

#geoHash: Meant for direct access.
#
#Returns: A List containing a Latitude and Longitude.
#
#Params: A Latitude and Longitude, as well as a boolean indicating if the area should be reduced.
#
#It will attempt to correct inverted coordinate pairs before passing to coordGen.
def geoHash (lat, lon, smallBool):
    if(abs(lat) > 90 and abs(lon) > 90):
        print "Error: Invalid"
        return [lat, lon]
    if(abs(lat) > 90):
        print "Wrong Order: Correcting"
        return coordGen(lon, lat, smallBool)
    return coordGen(lat, lon, smallBool)

#coordGen: Used by geoHash. 
#
#Returns: A List containing a Latitude and Longitude.
#
#Params: A Latitude and Longitude, as well as a boolean indicating if the area should be reduced.
#
#It accesses the current time, and the latest BTC:USD value call on BitAverage to make a long string of text. This text is
#then hashed and converted to decimal values, with the front 20 digits being appended to the first 3 or 4 of the Latitude
#and the last 20 being appended to the first 3 or 4 of the Longitutde. This pair is then truncated at 5 decimal places and
#returned.
def coordGen (lat, lon, smallBool):
    #Get the date string.
    Date = time.strftime("%d-%m-%Y %H:%M:%S")
    
    #Get the BTC-Value string.
    url="https://api.bitcoinaverage.com/ticker/global/USD"
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    BTCval = r["last"]*r["ask"]*3.1415
    
    #Hash the strings, and convert to an integer.
    hashed = hashlib.sha224(str(BTCval) + Date).hexdigest()
    tempvalue = int(hashed,16)
    
    #Split off the front 20 and last 20 digits of the tempvalue.
    shorter = str(tempvalue)[0:20]
    longer = str(tempvalue)[len(str(tempvalue))-20:len(str(tempvalue))]
    
    #Depending on the size parameter, truncate the original coordinates to 1 or 2 decimals.
    if smallBool:
        lat = lat - lat% 0.01
        lon = lon - lon% 0.01
    else:
        lat = lat - lat% 0.1
        lon = lon - lon% 0.1
    
    #Append the values and truncate to 5 decimal places.
    lat = float(str(lat) + str(shorter)) 
    lon = float(str(lon) + str(longer))
    lat = lat - lat % 0.00001
    lon = lon - lon % 0.00001
    
    #Clear rounding errors and return the coordinate pair.
    return [float(str(lat)[0:8]),float(str(lon)[0:8])]
    

