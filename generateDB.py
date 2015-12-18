import sqlite3, os.path

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
