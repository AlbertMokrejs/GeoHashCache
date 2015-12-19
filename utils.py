import sqlite3

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

