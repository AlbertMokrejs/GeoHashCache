import sqlite3, os.path

def generateGhcDB():
   x = os.path.isfile("GeoHashCache.db")
   if not x:
      connect = sqlite3.connect("GeoHashCache.db")
      curs = connect.cursor()
      List = ["""
   CREATE TABLE logins(
      Username TEXT,
      Password TEXT,
      Uid REAL
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
   );""","""CREATE TABLE comments(
      Parentid REAL,
      Commentid REAL,
      Content TEXT,
      Date TEXT,
      Author TEXT,
   );
   """,
   """CREATE TABLE cacheIDs(
      Cacheid REAL,
      Validid REAL);
   """]
      for q in List:
         curs.execute(q)
         connect.commit()

def greatestCacheID():
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q="""SELECT * FROM caches;
    	"""
    result = c.execute(q)
    x = 0
    for r in result:
        if r[5] > x:
            x = r[5]
    return x
    
def lowestCommentID():
    conn = sqlite3.connect("GeoHashCache.db")
    c = conn.cursor()
    q="""SELECT * FROM caches;
    	"""
    result = c.execute(q)
    x = -1
    for r in result:
        if r[1] < x:
            x = r[1]
    return x

def register(username,password,uid):
    conn = sqlite3.connect("StoryBase.db")
    c = conn.cursor()
    q = """insert into login values ('%s','%s','%s');""" % (username,password,uid)
    c.execute(q)
    conn.commit()

