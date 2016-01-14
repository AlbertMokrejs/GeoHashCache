import sqlite3
import geohash
import generateDB
import hashlib
import time
import marshal
import base64
import smtplib

def send_email(recipient, subject, body):
    user = "GeoHashCache@gmail.com"
    pwd = "NuclearPotato"
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        print "error"

def authenticate(username,password):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM login
    WHERE Username = '%s';""" % (username)
    result = c.execute(q)
    for r in result:
        if r[1] == password:
            Date = time.strftime("%d-%m-%Y")
            q = """UPDATE login SET Last = '%s' WHERE Username = '%s';""" %(Date,username)
            c.execute(q)
            conn.commit()
            return [True, r[2],r[4]]
    return [False, -1,""]
    
def findUser(username):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM login
    WHERE login.Username = '%s';""" % (username)
    result = c.execute(q)
    for r in result:
        return True
    return False
    
def findUserID(username):
    if findUser(username):
        conn = sqlite3.connect("GeoHashCache.db")
        c = conn.cursor()
        q = """
    SELECT *
    FROM login
    WHERE login.Username = '%s';""" % (username)
        result = c.execute(q)
        for r in result:
            return r[2]
    return 0
    
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
    conn.commit()
    
def genNewCoord(cacheID,small):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT Latitude, Longitude
    FROM caches
    WHERE caches.Cacheid = %s;
    """ % (cacheID)
    result = c.execute(q)
    for r in result:
        return geohash.geoHash(r[0],r[1],small)
    
def validateCache(cacheID, passcode):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT Cacheid,Validid FROM caches
    WHERE caches.Cacheid = %s;
    """ % (cacheID)
    result = c.execute(q)
    for r in result:
        if r[1] == passcode and r[0] == cacheID:
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
    
def register(Uname,Pword,email):
    generateDB.createUser(Uname,Pword,generateDB.greatestUserID() + 1,email,time.strftime("%d-%m-%Y"))
    
def getProfile(uid):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM login WHERE login.Uid = %s;""" % (uid)
    result = c.execute(q)
    for r in result:
        print marshal.loads(base64.b64decode(r[3]))
        return marshal.loads(base64.b64decode(r[3]))
    return [["ERRORCODE",0,0]]

def setProfile(uid,blob):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """UPDATE login
        SET Profile = '%s'
        WHERE login.Uid = %s;""" % (base64.b64encode(marshal.dumps(blob)),uid)
    c.execute(q)
    conn.commit()

def appendProfile(uid,blob):
    setProfile(uid, getProfile(uid) + blob)

def Comment(Parentid, Content, Author):
    Commentid = generateDB.lowestCommentID() - 1
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
    WHERE (((caches.Latitude - %s) * (caches.Latitude - %s)) + ((caches.Longitude - %s) * (caches.Longitude - %s))) < 25.1;
    """ % (lat, lat, lon, lon)
    result = c.execute(q)
    final = []
    for r in result:
        final.append([[r[3],r[0],r[1]],int(r[5])])
    return final

def getCache(uid):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM caches
    WHERE Cacheid = %s;
    """ % (uid)
    result = c.execute(q)
    for r in result:
        final = {}
        final["lat"] = r[0]
        final["lon"] = r[1]
        final["type"] = r[2]
        final["name"] = r[3]
        final["desc"] = r[4]
        final["id"] = int(r[5])
        final["founder"] = r[7]
        final["date"] = r[8]
        final["stat"] = r[9]
        return final
    
    
