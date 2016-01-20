import sqlite3
import geohash
import generateDB
import hashlib
import time
import marshal
import base64
import smtplib

#------------------
#Tests for the validity of the coordinates

#Input: Latitude and Longitude
#Output: Whether the coordinates are valid and returns 
def validCoord(lat,lon):
    if(abs(lat) > 90 and abs(lon) > 90):
        print "Error: Invalid"
        return [9000,9000]
    if(abs(lat) > 90):
        print "Wrong Order: Correcting"
        return [lon,lat]
    return [lat,lon]

#Sends email receipt to the intended recipient

#Input: Recipient email address, subject title, and body of email
#Output: Sends email and, if applicable, error message.
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

#Congratulations message

#Input: User ID, intended user, and username
#Output: Congratulatory message by team on the successful discovery of user's GeoCache
def collectCache(uid,user,username):
    dataU = findUserData(user)
    dataC = getCache(uid)
    subject = "" + dataC["name"] + " was found by " + username + "!"
    body = "Dear " + dataU[0] + ",\nYour cache, " + dataC["name"] + ", was found by " + username + """ today! The cache'll be moved promptly. 
    Meanwhile, why not spend a day GeoCaching yourself? \n Sincerely, The GeoHashCache Team."""
    recipient = dataU[3]
    send_email(dataU[4],subject,body)

#Login authentication into database of GeoCaches and user accounts

#Input: Login credentials
#Output: Boolean value indicating success and, if true, account information
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

#Quick way to find if username is already taken

#Input: Username
#Output: Presence of user in database (boolean)
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

#Finding user ID attached to username

#Input: Username
#Output: User ID
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

#Accessing actual user data

#Input: Username
#Output: Relevant user data under username
def findUserData(username):
    UID = findUserID(username)
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """
    SELECT *
    FROM login
    WHERE login.Uid = %s;""" % (UID)
    result = c.execute(q)
    for r in result:
        return [r[0],r[1],r[2],r[4],r[5]]
    return ["","",0,"",""]

#Updating overall cache data in database

#Input: Cache ID, latitude, longitude, name, description, and status
#Ouput: None. Updates database
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

#Generate coordinates based on cache ID in database

#Input: Cache ID and type of cache
#Output: Information relevant to cache
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

#Finds validity of cache according to passcode (authentication), if it is already taken or not

#Input: cacheID and passcode
#Output: Boolean value of availability
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

#Make a new cache and set a place for it in database

#Input: Latitude, longitude, type of cache, name, short description, and the user/founder
#Output: Creating database slot for said cache
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

#Create new account

#Input: Username, Password, email
#Output: Generates database slot for account
def register(Uname,Pword,email):
    generateDB.createUser(Uname,Pword,generateDB.greatestUserID() + 1,email,time.strftime("%d-%m-%Y"))

#Gets user's profile information based on user ID

#Input: user ID
#Output: User info
def getProfile(uid):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """SELECT * FROM login WHERE login.Uid = %s;""" % (uid)
    result = c.execute(q)
    for r in result:
        print marshal.loads(base64.b64decode(r[3]))
        return marshal.loads(base64.b64decode(r[3]))
    return [["ERRORCODE",0,0]]

#Sets profile to GeoHashCache database

#Input: User ID and potential random binary data
#Output: Makes slot in database with user ID, filtering the random binaries
def setProfile(uid,blob):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """UPDATE login
        SET Profile = '%s'
        WHERE login.Uid = %s;""" % (base64.b64encode(marshal.dumps(blob)),uid)
    c.execute(q)
    conn.commit()

#Appends profile onto database using "setProfile"

#Input: User ID
#Output: Same as setProfile, except just adding onto the database
def appendProfile(uid,blob):
    setProfile(uid, getProfile(uid) + blob)

#Insert comment into particular database slot for later access

#Input: Parent ID, actual comment, and the author (user)
#Output: Database slot generated, no graphical output.
def Comment(Parentid, Content, Author):
    Commentid = generateDB.lowestCommentID() - 1
    Date = time.strftime("%d-%m-%Y")
    generateDB.createComment(Parentid, Commentid, Content, Date, Author)

#API connection with QR, checks for validity of cache

#Input: Cache ID and a valid ID
#Output: QR Server https link to said cache
def makeQR(cacheID,validID):
    return ["https://api.qrserver.com/v1/create-qr-code/?size=640x640&data=validateCache/" + str(cacheID) + "/" + str(validID),validID]

#Finds local caches near a certain global location

#Input: Latitude, Longitude
#Output: Cache information array
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

#Get cache information based on user ID

#Input: User ID
#Output: Every bit of profile information about the cache
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
    
    
