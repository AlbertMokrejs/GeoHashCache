from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from random import randint

import generateDB
import utils
import geohash

generateDB.checkGenerate()

##

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	if "user" in session.keys() and "uid" in session.keys():
		return render_template("home.html", Username = session["user"])
	return render_template("home.html")
	
@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="GET":
        	return render_template("login.html")
        else:
        	uname = request.form['username']
        	pword = request.form['password']
        	if utils.authenticate(uname,pword)[0]:
        		session["user"] = uname
        		session["uid"] = utils.authenticate(uname,pword)[1]
        		return redirect("/home")
        	else:
            		session["user"] = ""
            		session["uid"] = -1
            		error = "Bad username or password"
            		return render_template("login.html",error=error)

@app.route("/register",methods=["GET","POST"])
def registerPage():
	if request.method=="GET":
        	return render_template("register.html")
        else:
        	uname = request.form['username']
        	pword = request.form['password']
        	if pword == request.form["confirm"]:
        		utils.register(uname,pword)
        		session["user"] = uname
        		session["uid"] = utils.authenticate(uname,pword)[1]
        		return redirect("/home")
        	else:
            		session["user"] = ""
            		session["uid"] = -1
            		error = "Passwords do not match"
            		return render_template("register.html",error=error)


@app.route("/logout")
def logout():
	session["user"] = ""
	session["uid"] = -1
	return redirect("/home")
	
##



@app.route("/moveCache/<cacheID>")
def moveCache(cacheID = 0):
	return genNewCoord(cacheID, False)
  

@app.route("/closeMoveCache/<cacheID>")
def moveCacheB(cacheID = 0):
	return genNewCoord(cacheID, True)
	
@app.route("/checkCache/<cacheID>/<validID>")
def checkCache(cacheID = 0, validID = 0):
	return validateCache(cacheID, validID)



if (__name__ == "__main__"):
        app.debug = True
        app.secret_key = "secret"
        app.run(host='0.0.0.0', port=8000)
