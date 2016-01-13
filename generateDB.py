import sqlite3, os.path
import base64
import marshal

#Checks if there is a database. Makes one if there isn't.
#
#
def checkGenerate():
   #Checks if there is a database file.
   x = os.path.isfile("GeoHashCache.db")
   
   if not x:
      #Makes tables.
      connect = sqlite3.connect("GeoHashCache.db")
      curs = connect.cursor()
      List = ["""
   CREATE TABLE login(
      Username TEXT,
      Password TEXT,
      Uid REAL,
      Profile BLOB,
      Email TEXT,
      Last TEXT
   );""","""CREATE TABLE caches(
      Latitude REAL, 
      Longitude REAL,
      Type TEXT,
      Name TEXT,
      Description TEXT,
      Cacheid REAL,
      Validid REAL,
      Founder TEXT,
      Date TEXT,
      Status REAL
   );""","""CREATE TABLE comments(
      Parentid REAL,
      Commentid REAL,
      Content TEXT,
      Date TEXT,
      Author TEXT
   );
   """,
   """CREATE TABLE cacheIDs(
      Cacheid REAL,
      Validid REAL);
   """]
      for q in List:
         curs.execute(q)
         connect.commit()

#Finds the ID of the latest Cache as IDs are sequential. 
def greatestCacheID():
    #Gets all caches.
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q="""SELECT * FROM caches;
    	"""
    result = c.execute(q)
    #Loops through all IDs to find the greatest, starting at 0.
    x = 0
    print result
    for r in result:
        if r[5] > x:
            x = r[5]
    print x
    return x

#Finds the ID of the latest comment.
def lowestCommentID():
    #Gets all comments.
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q="""SELECT * FROM comments;
    	"""
    result = c.execute(q)
    #Loops through all IDs to find the lowest, starting at -1.
    x = -1
    for r in result:
        if r[1] < x:
            x = r[1]
    return x
    
def greatestUserID():
    #Gets all caches.
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q="""SELECT * FROM login;
    	"""
    result = c.execute(q)
    #Loops through all IDs to find the greatest, starting at 0.
    x = 0
    for r in result:
        if r[2] > x:
            x = r[2]
    return x

def createUser(username,password,uid,email,date):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """insert into login values ('%s','%s',%s,'%s','%s','%s');""" % (username,password,uid,base64.b64encode(str(marshal.dumps([]))),email,date )
    c.execute(q)
    conn.commit()
    
def createCache(Latitude, Longitude, Type, Name, Description, Cacheid, Validid, Founder, Date):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """insert into caches values (%s,%s,'%s','%s','%s',%s,%s,'%s','%s',%s);""" % (Latitude, Longitude, Type, Name, Description, Cacheid, Validid, Founder, Date, 0)
    print q
    c.execute(q)
    conn.commit()
    q = """insert into cacheIDs values (%s,%s);""" % (Cacheid, Validid)
    print q
    c.execute(q)
    conn.commit
    
def createComment(Parentid, Commentid, Content, Date, Author):
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q = """insert into comments values (%s,%s,'%s','%s','%s');""" % (Parentid, Commentid, Content, Date, Author)
    c.execute(q)
    conn.commit()




