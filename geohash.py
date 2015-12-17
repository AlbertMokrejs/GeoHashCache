
# go to 5 decimal places
# lat -90/90, long -180/180

import hashlib
import urllib2 

def Hash (lat, long):

url="https://api.bitcoinaverage.com/ticker/global/USD"
request = urllib2.urlopen(url)
result = request.read()
r = json.loads(result)
BTCval = r["last"]*r["ask"]

hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
