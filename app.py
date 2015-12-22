from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from random import randint

import generateDB
import utils
import geohash

generateDB.checkGenerate()

##
##
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
        		if session["redir"] and session["redir"] != "":
        			redir = session["redir"]
        			session["redir"] = ""
        			return redirect(redir)
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
        		if session["redir"] and session["redir"] != "":
        			redir = session["redir"]
        			session["redir"] = ""
        			return redirect(redir)
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
	
@app.route("/found",methods=["GET","POST"])
def foundCache():
	if request.method=="GET":
		if not (session["user"] and session["user"] != ""):
			session["redir"] = "/found"
			return redirect("/login")
		return render_template("found.html")
	else:
		if "Latitude" in request.form.keys() and "Longitude" in request.form.keys() and "Type" in request.form.keys() and "Name" in request.form.keys() and "Desc" in request.form.keys():
			Founder = session["user"]
			Latitude = request.form['Latitude']
			Longitude = request.form['Longitude']
			Type = request.form['Type']
			Description = request.form['Desc']
			Name = request.form["Name"]
			newID = utils.makeNewCache(Latitude, Longitude, Type, Name, Description, Founder)
			return render_template("found.html", name = Name, IMG = utils.makeQR(newID)[0], validID = utils.makeQR(newID)[1])
		return render_template("found.html", Error = "Please Fill Out The Form Completely")
			
@app.route("/cache/<uid>")
def cacheProfile( uid = 0):
        return render_template( "cache.html", utils.getCache( uid ))
	
## ------ app.py API code, accessed only by local file -------- ##


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
