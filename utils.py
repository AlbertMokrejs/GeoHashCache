import sqlite3
import geohash
import generateDB

def authenticate(username,password):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM login
    WHERE login.Username = '%s'
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
    return geohash.geoHash(result[0],result[1],small)
    
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
    generateDB.createCache(Latitude, Longitude, Type, Name, Description, cacheID, validID, Founder, Date)
    return cacheID
    
def register(Uname,Pword):
    generateDB.createUser(Uname,Pword,generateDB.greatestUserID() + 1)
    
def getProfile(uid):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM login WHERE Uid = '%s'""" % (uid)
    result = c.execute(q)
    for r in result:
        return marshal.loads(r[3])

def setProfile(uid,blob):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """UPDATE login
        SET Profile = '%s'
        WHERE Uid = '%s'""" % (marshal.dumps(blob),uid)
    c.execute(q)

def appendProfile(uid,blob):
    setProfile(uid, getProfile(uid) + blob)

def Comment(Parentid, Content, Author):
    Commentid = lowestCommentID() - 1
    Date = time.strftime("%d-%m-%Y")
    generateDB.createComment(Parentid, Commentid, Content, Date, Author)
    
def makeQR(cacheID):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM cacheIDs WHERE Cacheid = '%s'""" % (cacheID)
    result = c.execute(q)
    for r in result:
        return "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=validateCache/" + cacheID + "/" + r[1]
        
def cachesNear(lat, lon):
        conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM caches
    WHERE abs(caches.Latitude - '%s') < 1, abs(caches.Longitude - '%s') < 1
    """ % (lat, lon)
    result = c.execute(q)
    final = []
    for r in result
        final.append([r[3],r[0],r[1]],r[5])
    return final



