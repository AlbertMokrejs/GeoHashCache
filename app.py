from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from random import randint
import generateDB
import utils

checkGenerate()

##

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/moveCache/<cacheID>")
def moveCache(cacheID = 0):
  c = conn.cursor()
  q = """
    SELECT Latitude, Longitude
    FROM caches
    WHERE caches.Cacheid = '%s'
    """ % (cacheID)
  result = c.execute(q)
  return geoHash(result[0],result[1],False)

@app.route("/closeMoveCache/<cacheID>")
def moveCache(cacheID = 0):
  c = conn.cursor()
  q = """
    SELECT Latitude, Longitude
    FROM caches
    WHERE caches.Cacheid = '%s'
    """ % (cacheID)
  result = c.execute(q)
  return geoHash(result[0],result[1],True)

if (__name__ == "__main__"):
        app.debug = True
        app.secret_key = "secret"
        app.run(host='0.0.0.0', port=8000)
