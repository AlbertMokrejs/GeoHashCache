# go to 5 decimal places
# lat -90/90, long -180/180

import hashlib
import urllib2 
import time
import json

def geoHash (lat, lon, smallBool):
    if(abs(lat) > 90 and abs(lon) > 90):
        print "Error: Invalid"
        return [lat, lon]
    if(abs(lat) > 90):
        print "Wrong Order: Correcting"
        return coordGen(lon, lat, smallBool)
    return coordGen(lat, lon, smallBool)

def coordGen (lat, lon, smallBool):
    Date = time.strftime("%d-%m-%Y %H:%M:%S")
    url="https://api.bitcoinaverage.com/ticker/global/USD"
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    BTCval = r["last"]*r["ask"]*3.1415

    print BTCval
    print Date
    
    hashed = hashlib.sha224(str(BTCval) + Date).hexdigest()
    tempvalue = int(hashed,16)
    
    shorter = str(tempvalue)[0:20]
    longer = str(tempvalue)[len(str(tempvalue))-20:len(str(tempvalue))]
    
    print shorter
    print longer
    
    if smallBool:
        lat = lat - lat% 0.01
        lon = lon - lon% 0.01
    else:
        lat = lat - lat% 0.1
        lon = lon - lon% 0.1
    
    lat = float(str(lat) + str(shorter)) 
    lon = float(str(lon) + str(longer))
    lat = lat - lat % 0.00001
    lon = lon - lon % 0.00001
    
    print lat 
    print lon 
    return [lat, lon]
    
print geoHash(40.7245678,-73.8457658,True)
print geoHash(40.7245678,-73.8457658,False)
print geoHash(-73.8457658,40.7245678,True)
