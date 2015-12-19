import sqlite3
import geohash
import generateDB

def authenticate(username,password):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT Username, Password
    FROM logins
    WHERE logins.Username = '%s'
    """ % (username)
    result = c.execute(q)
    for r in result:
        if r[1] == password:
            return [True, r[2]]
    return [False, -1]
    
def updateCache(cacheID, lat, lon, Type, name, desc, stat):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """UPDATE caches 
    SET Latitude = '%s', 
    Longitude = '%s',
    Type = '%s',
    Name = '%s',
    Description = '%s', Status = '%s'
    WHERE Cacheid = '%s';""" % (lat, lon, Type, name, desc, stat, cacheID)
    c.execute(q)
    
def genNewCoord(cacheID,small):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT Latitude, Longitude
    FROM caches
    WHERE caches.Cacheid = '%s'
    """ % (cacheID)
    result = c.execute(q)
    return geoHash(result[0],result[1],small)
    
def validateCache(cacheID, passcode):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM cacheIDs WHERE Cacheid = '%s'""" % (cacheID)
    result = c.execute(q)
    for r in result:
        if r[1] == passcode:
            return True
    return False
    
def makeNewCache(Latitude, Longitude, Type, Name, Description, Founder):
    cacheID = greatestCacheID() + 1
    Date = time.strftime("%d-%m-%Y")
    hashed = hashlib.sha224(str(cacheID) + Date).hexdigest()
    validID = str(int(hashed,16))[0:10]
    createCache(Latitude, Longitude, Type, Name, Description, cacheID, validID, Founder, Date)

def makeComment(Parentid, Content, Author):
    Commentid = lowestCommentID() - 1
    Date = time.strftime("%d-%m-%Y")
    comment(Parentid, Commentid, Content, Date, Author)
    
def makeQR(cacheID):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM cacheIDs WHERE Cacheid = '%s'""" % (cacheID)
    result = c.execute(q)
    for r in result:
        return "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=validateCache/" + cacheID + "/" + r[1]
