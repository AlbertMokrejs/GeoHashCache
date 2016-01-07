from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import sys
from random import randint

import urllib2
import json

import generateDB
import utils
import geohash

from .geodata import get_geodata

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
	if "redir" in session.keys() and session["redir"] != "":
        			redir = session["redir"]
        			session["redir"] = ""
	if request.method=="GET":
        	return render_template("login.html")
        else:
        	uname = request.form['username']
        	pword = request.form['password']
        	if utils.authenticate(uname,pword)[0]:
        		session["user"] = uname
        		session["uid"] = utils.authenticate(uname,pword)[1]
        		if "redir" in locals():
        			return redirect(redir)
        		return redirect("/home")
        	else:
            		session["user"] = ""
            		session["uid"] = -1
            		error = "Bad username or password"
            		return render_template("login.html",error=error)

@app.route("/register",methods=["GET","POST"])
def registerPage():
	if "redir" in session.keys() and session["redir"] != "":
        			redir = session["redir"]
        			session["redir"] = ""
	if request.method=="GET":
        	return render_template("register.html")
        else:
        	uname = request.form['username']
        	pword = request.form['password']
        	if pword == request.form["confirm"]:
        		utils.register(uname,pword)
        		session["user"] = uname
        		session["uid"] = utils.authenticate(uname,pword)[1]
        		if 'redir' in locals():
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
		if not ("user" in session.keys() and session["user"] != ""):
			session["redir"] = "/found"
			return redirect("/login")
		return render_template("found.html", Username = session["user"])
	else:
		try:
			Founder = session["user"]
			Latitude = float(request.form['Latitude'])
			Longitude = float(request.form['Longitude'])
			Type = request.form['Type']
			Description = request.form['Desc']
			Name = request.form["Name"]
			BODGE = utils.makeNewCache(Latitude, Longitude, Type, Name, Description, Founder)
			print sys.exc_info()[0]
			print BODGE
			IMG = utils.makeQR(BODGE[0],BODGE[1])[0]
			print IMG
			validID = BODGE[1]
			print validID
			print sys.exc_info()[0]
			return render_template("found.html", name = Name, IMG = IMG, validID = validID, Username = session["user"])
		except:
			e = sys.exc_info()[0]
			print e
			return render_template("found.html", Error = "Please Fill Out The Form Completely", Username = session["user"])
			
@app.route("/cache/<uid>",methods=["GET","POST"])
def cacheProfile( uid = 0):
	if request.method=="GET":
		data = utils.getCache( uid )
		if data["stat"] == 0:
			data["stat"] = "Normal"
		if data["stat"] == 1:
			data["stat"] = "Being Relocated"
		if data["stat"] == 2:
			data["stat"] = "Lost"
		if data["stat"] == 3:
			data["stat"] = "Damaged"
        	return render_template( "cache.html", data = data, Username = session["user"])
        else:
        	if "status" in request.form.keys():
        		stat = request.form['status']
        		if stat == "Lost":
        			stat = 2
        		if stat == "Damaged":
        			stat = 3
        		data = utils.getCache( uid )
        		utils.updateCache(uid, data["lat"], data["lon"], data["type"], data["name"], data["desc"], stat)
        		data = utils.getCache( uid )
        		if data["stat"] == 0:
				data["stat"] = "Normal"
			if data["stat"] == 1:
				data["stat"] = "Being Relocated"
			if data["stat"] == 2:
				data["stat"] = "Lost"
			if data["stat"] == 3:
				data["stat"] = "Damaged"
		 	return render_template( "cache.html", data = data, Error = "Report Processed", Username = session["user"])
		else:
		 	return redirect("/validatecache/" + uid + "/" + request.form["validID"])
        

@app.route("/validatecache/<cacheID>/<validID>", methods=["GET","POST"])
def cache(cacheID = 0, validID = 0):
	if request.method=="POST":
 +		validID=request.form["validID"]
	result = utils.validateCache(int(cacheID), int(validID))
	if not ("user" in session.keys() and session["user"] != ""):
		session["redir"] = "/validateCache/" + cacheID + "/" + validID
		return redirect("/login")
	else:
		if result:
			data = utils.getCache(cacheID)
			utils.appendProfile(session["uid"],[data["name"],data["lat"],data["lon"]])
			## TEMPORARY
			if data["stat"] == 0:
				data["stat"] = "Normal"
			if data["stat"] == 1:
				data["stat"] = "Being Relocated"
			if data["stat"] == 2:
				data["stat"] = "Lost"
			if data["stat"] == 3:
				data["stat"] = "Damaged"
	  		return render_template("validatecache.html", cacheID = "/validatecache/" + cacheID + "/" + validID, data = data, Error = "Succesfully Validated", Username = session["user"])
		else:	
			data = utils.getCache(cacheID)
			Error = "Failed To Validate"
			if validID == 0:
				Error = ""
			## TEMPORARY
			if data["stat"] == 0:
				data["stat"] = "Normal"
			if data["stat"] == 1:
				data["stat"] = "Being Relocated"
			if data["stat"] == 2:
				data["stat"] = "Lost"
			if data["stat"] == 3:
				data["stat"] = "Damaged"
	  		return render_template("validatecache.html", cacheID = "/validatecache/" + cacheID + "/" + validID, data = data, Error = Error, Username = session["user"])

@app.route("/find")
def localCache():
	ip_address = request.access_route[0] or request.remote_addr
    	geodata = get_geodata(ip_address)
    	latitude=geodata.get("latitude"),
        longitude=geodata.get("longitude"),
	data = utils.cachesNear(latitude, longitude)
	LocList = []
	for r in data:
		LocList.append(['<a href="/validatecache/' + r[1] +'/0">' + r[0][0] + '</a>', r[0][1], r[0][2]])
	return render_template("find.html", LocList = LocList Username = session["user"])
	
	
## ------ app.py API code, accessed only by local file -------- ##


@app.route("/moveCache/<cacheID>")
def moveCache(cacheID = 0):
	return utils.genNewCoord(cacheID, False)
  

@app.route("/closeMoveCache/<cacheID>")
def moveCacheB(cacheID = 0):
	return utils.genNewCoord(cacheID, True)
	
@app.route("/checkCache/<cacheID>/<validID>")
def checkCache(cacheID = 0, validID = 0):
	return utils.validateCache(cacheID, validID)
        

if (__name__ == "__main__"):
        app.debug = True
        app.secret_key = "secret"
        app.run(host='0.0.0.0', port=8000)
