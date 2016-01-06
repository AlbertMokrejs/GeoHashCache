import sqlite3
import geohash
import generateDB
import hashlib
import time

def authenticate(username,password):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM login
    WHERE login.Username = '%s';""" % (username)
    result = c.execute(q)
    for r in result:
        if r[1] == password:
            return [True, r[2]]
    return [False, -1]
    
def updateCache(cacheID, lat, lon, Type, name, desc, stat):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """UPDATE caches 
    SET Latitude = %s, 
    Longitude = %s,
    Type = '%s',
    Name = '%s',
    Description = '%s', Status = %s
    WHERE caches.Cacheid = %s;""" % (lat, lon, Type, name, desc, stat, cacheID)
    c.execute(q)
    
def genNewCoord(cacheID,small):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT Latitude, Longitude
    FROM caches
    WHERE caches.Cacheid = %s;
    """ % (cacheID)
    result = c.execute(q)
    return geohash.geoHash(result[0],result[1],small)
    
def validateCache(cacheID, passcode):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM cacheIDs WHERE cacheIDs.Cacheid = %s;""" % (cacheID)
    result = c.execute(q)
    for r in result:
        if r[1] == passcode:
            return True
    return False
    
def makeNewCache(Latitude, Longitude, Type, Name, Description, Founder):
    cacheID = int(generateDB.greatestCacheID() + 1)
    print cacheID
    Date = time.strftime("%d-%m-%Y")
    print Date
    hashed = hashlib.sha224(str(cacheID) + Date).hexdigest()
    validID = int(str(int(hashed,16))[0:10])
    print validID
    generateDB.createCache(Latitude, Longitude, Type, Name, Description, cacheID, validID, Founder, Date)
    return [cacheID,validID]
    
def register(Uname,Pword):
    generateDB.createUser(Uname,Pword,generateDB.greatestUserID() + 1)
    
def getProfile(uid):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM login WHERE login.Uid = %s;""" % (uid)
    result = c.execute(q)
    for r in result:
        return marshal.loads(base64.b64decode(r[3]))

def setProfile(uid,blob):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """UPDATE login
        SET Profile = '%s'
        WHERE login.Uid = %s;""" % (base64.b64encode(marshal.dumps(blob)),uid)
    c.execute(q)

def appendProfile(uid,blob):
    setProfile(uid, getProfile(uid) + blob)

def Comment(Parentid, Content, Author):
    Commentid = lowestCommentID() - 1
    Date = time.strftime("%d-%m-%Y")
    generateDB.createComment(Parentid, Commentid, Content, Date, Author)
    
def makeQR(cacheID,validID):
    return ["https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=validateCache/" + str(cacheID) + "/" + str(validID),validID]
        
def cachesNear(lat, lon):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM caches
    WHERE abs(caches.Latitude - %s) < 1, abs(caches.Longitude - %s) < 1;
    """ % (lat, lon)
    result = c.execute(q)
    final = []
    for r in result:
        final.append([r[3],r[0],r[1]],r[5])
    return final

def getCache(uid):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM caches
    WHERE cacheID = %s;
    """ % (uid)
    result = c.execute(q)
    for r in result:
        final = {}
        final["lat"] = r[0]
        final["lon"] = r[1]
        final["type"] = r[2]
        final["name"] = r[3]
        final["desc"] = r[4]
        final["id"] = r[5]
        final["founder"] = r[7]
        final["date"] = r[8]
        final["stat"] = r[9]
        return final
    
    
