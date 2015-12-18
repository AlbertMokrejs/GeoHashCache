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

def GreatestStoryID():
    conn = sqlite3.connect("StoryBase.db")
    c = conn.cursor()
    q="""SELECT * FROM Stories;
    	"""
    result = c.execute(q)
    x = 0
    for r in result:
        if r[3] > x:
            x = r[3]
    return x

def register(username,password):
    conn = sqlite3.connect("StoryBase.db")
    c = conn.cursor()
    q = """insert into Login values ('%s','%s');""" % (username,password)
    c.execute(q)
    conn.commit()
    
def comment(storyID, CContent, Date):
    conn = sqlite3.connect("StoryBase.db")
    c = conn.cursor()
    q = """insert into comments values ('%s','%s','%s');""" % (storyID, CContent, Date)
    c.execute(q)
    conn.commit()
    
def addStory(Content, Name, Username, ID, Date):
    conn = sqlite3.connect("StoryBase.db")
    c = conn.cursor()
    q = """insert into Stories values ('%s','%s','%s','%s','%s');""" % (Content,Name,Username,ID,Date)
    c.execute(q)
    conn.commit()

