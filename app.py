from flask import Flask, render_template, request, redirect, url_for, session
from random import randint
from geodata import get_geodata
import sqlite3
import sys
import urllib2
import json
import generateDB
import utils
import geohash



generateDB.checkGenerate("0")


##
##

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	if not "user" in session.keys():
		session["user"] = ""
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
        	email = request.form['email']
        	valid = (pword == request.form["confirm"])
        	error = ""
        	if not valid:
        		error = "Passwords do not match"
        	if valid:
        		valid = valid and not len(pword) < 8
        		if not valid:
        			error = "Passwords are too short"
        		if valid:
	        		valid = valid and not any(a for a in pword if a in """@;!'"?""")
        			if not valid:
        				error = """The following symbols are not allowed in passwords: @;.,!'"?"""
        			if valid:
        				valid = valid and not len(uname) < 8
        				if not valid:
        					error = "Passwords are too short"
        				if valid:
        					valid = valid and not any(a for a in uname if a in """@;!'"?""")
        					if not valid:
        						error = """The following symbols are not allowed in usernames: @;.,!'"?"""
        	if valid:
        		utils.register(uname,pword,email)
        		session["user"] = uname
        		session["uid"] = utils.authenticate(uname,pword)[1]
        		session["email"] = email
        		if 'redir' in locals():
        			return redirect(redir)
        		return redirect("/home")
        	else:
            		session["user"] = ""
            		session["uid"] = -1
            		return render_template("register.html",error=error)


@app.route("/logout")
def logout():
	session["user"] = ""
	session["uid"] = -1
	session["email"] = ""
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
		if "validID" in request.form.keys():
			validID=request.form["validID"]
		stat = 0
		if "Damaged" in request.form.keys():
			stat = 3
		if "Lost" in request.form.keys():
			stat = 2
		data = utils.getCache(cacheID)
		utils.updateCache(cacheID, data["lat"], data["lon"], data["type"], data["name"], data["desc"], stat)
		if "Comment" in request.form.keys():
			Comment =request.form["Comment"]
			if not ("user" in session.keys() and session["user"] != ""):
				session["redir"] = "/validatecache/%s/%s" % (cacheID, validID)
				return redirect("/login")
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
	  		return render_template("validatecache.html", valid = True, cacheID = "/validatecache/" + cacheID + "/" + validID, data = data, Error = "Succesfully Validated", Username = session["user"])
		else:	
			data = utils.getCache(cacheID)
			Error = "Failed To Validate"
			if int(validID) == 0:
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
	  		return render_template("validatecache.html", valid = False, cacheID = "/validatecache/" + cacheID + "/" + validID, data = data, Error = Error, Username = session["user"])

@app.route("/find")
def localCache():
	ip_address = request.access_route[0] 
	#or request.remote_addr
	print ip_address
    	geodata = get_geodata(ip_address)
    	latitude=geodata.get("latitude")
        longitude=geodata.get("longitude")
        print latitude
        print longitude
	data = utils.cachesNear(float(latitude), float(longitude))
	LocList = []
	for r in data:
		LocList.append(['<a href="/validatecache/' + str(r[1]) +'/0">' + str(r[0][0]) + '</a>', r[0][1], r[0][2]])
	print LocList
	return render_template("find.html", LocList = LocList, Username = session["user"], Lon = latitude, Lat = longitude)

@app.route("/user/<user>")
def userProfiles(user = 0):
	if not str(user).isdigit():
		user = utils.findUserID(user)
	data = utils.getProfile(user)
	if len(data) > 0 and len(data[0]) > 0 and data[0][0] == "ERRORCODE":
		Error = "Invalid User Account"
		return render_template("user.html", user = user, Error = Error, Username = session["user"])
	else:
		return render_template("user.html", user = user, Data = Data, Username = session["user"])
	
	
	
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
