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
	return genNewCoord(cacheID, False)
  

@app.route("/closeMoveCache/<cacheID>")
def moveCache(cacheID = 0):
	return genNewCoord(cacheID, True)

if (__name__ == "__main__"):
        app.debug = True
        app.secret_key = "secret"
        app.run(host='0.0.0.0', port=8000)
