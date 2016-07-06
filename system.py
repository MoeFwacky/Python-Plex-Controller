
import os
import getpass
import time
import sys
import requests
import sqlite3
import urllib3
import subprocess
import platform
import enchant

from os import listdir
from os.path import isfile, join

#top
user = getpass.getuser()

global file
global show
global play

#location of your TBN home directory

try:
	input = raw_input
except NameError:
	pass
	
MYDB = homedir + "myplex.db"
sql = sqlite3.connect(MYDB)
cur = sql.cursor()

global PLEXUN
global PLEXSVR
global PLEXCLIENT
global plex
global client


def plexlogin():
	global PLEXUN
	global PLEXSVR
	global PLEXCLIENT
	global plex
	global client
	global LOGGEDIN
	try:

		cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXUN\'')
		PLEXUN = cur.fetchone()
		PLEXUN = PLEXUN[0]

		cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXPW\'')
		PLEXPW = cur.fetchone()
		PLEXPW = PLEXPW[0]

		cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSVR\'')
		PLEXSVR = cur.fetchone()
		PLEXSVR = PLEXSVR[0]

		cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXCLIENT\'')
		PLEXCLIENT = cur.fetchone()
		PLEXCLIENT = PLEXCLIENT[0]
		try:
		
			cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERIP\'')
			PLEXSERVERIP = cur.fetchone()
			PLEXSERVERIP = PLEXSERVERIP[0]

			cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERPORT\'')
			PLEXSERVERPORT = cur.fetchone()
			PLEXSERVERPORT = PLEXSERVERPORT[0]

			cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERTOKEN\'')
			PLEXSERVERTOKEN = cur.fetchone()
			PLEXSERVERTOKEN = PLEXSERVERTOKEN[0]
		except Exception:
			print ("Local Variables not set. Run setup to use local access.")

		from plexapi.myplex import MyPlexAccount
		user = MyPlexAccount.signin(PLEXUN,PLEXPW)

		try:
			LOGGEDIN
		except Exception:
		
			try:
				from plexapi.server import PlexServer
				baseurl = 'http://' + PLEXSERVERIP + ':' + PLEXSERVERPORT
				token = PLEXSERVERTOKEN
				plex = PlexServer(baseurl, token)
			except Exception:
				print ("Local Fail. Trying cloud access.")
	
			plex = user.resource(PLEXSVR).connect()
			client = plex.client(PLEXCLIENT)
			LOGGEDIN = "YES"

	except IndexError:
		print ("Error getting necessary plex api variables. Run system_setup.py.")

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def muteaudio():
	global client
	plexlogin()
	client.setVolume(0, 'Video')

def unmuteaudio():
        global client
        plexlogin()
        client.setVolume(100, 'Video')

def lowaudio():
	global client
        plexlogin()
        client.setVolume(25, 'Video')

def mediumaudio():
	global client
        plexlogin()
        client.setVolume(50, 'Video')

def highaudio():
	global client
        plexlogin()
        client.setVolume(75, 'Video')

def maxaudio():
	global client
        plexlogin()
        client.setVolume(100, 'Video')
	



def listclients():
	daclients = []
	for client in plex.clients():
		daclients.append(client.title)
	print ("The Following Clients are available.")
	counter = 1
	for client in daclients:
		print (str(counter) + "- " + client.strip() + "\n")
		counter = counter + 1

def changeclient():
	daclients = []
	for client in plex.clients():
		daclients.append(client.title)
	print ("The Following Clients are available.")
	counter = 1
	for client in daclients:
		print (str(counter) + "- " + client.strip() + "\n")
		counter = counter + 1
	choice = int(input('New Client: '))
	try:
		client = daclients[choice-1].strip()
		cur.execute('DELETE FROM settings WHERE item LIKE \'PLEXCLIENT\'')
		sql.commit()
		cur.execute('INSERT INTO settings VALUES(?,?)',('PLEXCLIENT',client))
		sql.commit()
		cur.execute("SELECT * FROM settings WHERE item LIKE \'PLEXCLIENT\'")
		test = cur.fetchone()
		return ("Client successfully set to: " + client.strip())
	except Exception:
		return ("Error. Unable to update client. Please try again.")
		
	


def stopplay():
	client = plex.client(PLEXCLIENT)
	client.stop('video')

def pauseplay():
	client = plex.client(PLEXCLIENT)
	client.pause('video')

def whereat():
	client = plex.client(PLEXCLIENT)
	for mediatype in client.timeline():
		if int(mediatype.get('time')) != 0:
			check = mediatype.get('time')
			check2 = mediatype.get('duration')
			check = int(check)/60000
			check2 = int(check2)/60000
			say = ("We are at minute " + str(check) + " out of " + str(check2) + ".")
	return (say)

def skipahead():
	client = plex.client(PLEXCLIENT)
	client.stepForward('video')
	return ("Skip Ahead Complete.")

def skipback():
	client = plex.client(PLEXCLIENT)
	client.stepBack('video')
	return ("Skip Back Complete.")

def listwildcard():
	cur.execute('SELECT setting FROM settings WHERE item LIKE \'WILDCARD\'')
	wildcard = cur.fetchone()
	wildcard = wildcard[0]
	return wildcard

def changewildcard(show):
	currentw = listwildcard()
	print ("The Current Wild Card is: " + currentw + ".\n")
	if "none" in show:
		print ("What do you want to replace it with?")
		newwild = str(input('Show: '))
	else:
		newwild = show
	command = "SELECT TShow FROM shows WHERE TShow LIKE \'" + newwild + "\'"
	cur.execute(command)
	if not cur.fetchall():
		return ("Error. " + str(newwild) + " Not found in Library to set as wildcard.")
	else:
		cur.execute("DELETE FROM settings WHERE item LIKE \'WILDCARD\'")
		sql.commit()
		cur.execute("INSERT INTO settings VALUES(?,?)", ('WILDCARD', newwild))
		sql.commit()
		return (newwild + " has been set as the new Wildcard show.")

def getblockpackagelist():
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	command = 'SELECT Name FROM Blocks'
	cur.execute(command)
	list = cur.fetchall()
	xlist = []
	for item in list:
		xlist.append(item[0])
	return (xlist)
def ostype():
	ostype = platform.system()
	return ostype
	
def availstudiotv():
	if "Windows" in ostype():
		PLdir = homedir + 'Studio\\'
	else:
		PLdir = homedir + 'Studio/'
	from os import listdir
	from os.path import isfile, join
	showlist = [f for f in listdir(PLdir) if isfile(join(PLdir, f))]
	return showlist

def listtvstudio(studio):
	PLDir = homedir + 'Studio/' + studio + '.txt'
	with open (PLDir, 'r') as file:
		shows = file.readlines()
	file.close()
	return shows

def availgenretv():
	command = "SELECT Genre FROM TVshowlist ORDER BY Genre ASC"
	cur.execute(command)
	fgenres = cur.fetchall()
	xshowlist = []
	for genres in fgenres:
		genre = genres[0].split(";")
		for xgen in genre:
			if xgen not in xshowlist:
				xshowlist.append(xgen)
			
	#xshowlist = sorted(xshowlist)	
	#worklist(xshowlist)
	return (xshowlist)

def avalratingtv():
	command = "SELECT Rating FROM TVshowlist ORDER BY Genre ASC"
        cur.execute(command)
        fgenres = cur.fetchall()
        xshowlist = []
        for genres in fgenres:
                genre = genres[0].split(";")
                for xgen in genre:
                        if xgen not in xshowlist:
                                xshowlist.append(xgen)
	worklist(xshowlist)
	return("Done.")

def availgenremovie():
	command = "SELECT Genre FROM Movies"
	cur.execute(command)
	thelist = cur.fetchall()
	genres = []
	for item in thelist:
		item = item[0].split(' ')
		for gen in item:
			if gen not in genres:
				if gen == "":
					pass
				elif gen == "&":
					pass
				else:
					genres.append(gen)
	genres = sorted(genres)			
	worklist(genres)	
	return ("Done.")


def filenumlines(file):
	num_lines = sum(1 for line in open(file))
	#num_lines = num_lines - 1
	return num_lines

def helpme():
	link = homedir + "/help.txt"
	with open(link, 'r') as file:
		stuff = file.read()
	file.close()
	stuff = stuff.replace('\\','')
	return stuff

def explainblock(block):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	blist = getblockpackagelist()
	for item in blist:
		check = item
		if block == check:
			command = 'SELECT Items FROM Blocks WHERE Name LIKE \'' + block + '\''
			cur.execute(command)
			stuff = cur.fetchall()
			stuff = str(stuff)
			stuff = stuff.replace("[(u'","")
			stuff = stuff.replace("',)]","")
			stuff = stuff.replace("\\n","")
			stuff = stuff.split(';')

			for things in stuff:
				things = things.rstrip()
				if "Random_movie" in things:
					things = things.replace("Random_movie.", "A random ")
					things = things + " movie"
					things = things.replace(";","")
				elif "Random_tv" in things:
					things = things.replace("Random_tv.", "A Random ")
					things = things + " TV Show."
					things = things.replace(";","")
				try:
					tns = tns + things + "\n"
				except NameError:
					tns = things + "\n"
				tns = tns.replace("movie.", "the movie ")
			say = "The " + block + " plays the following:\n" + tns
			return say		
def addblock(name, title):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	command1 = 'SELECT Movie FROM Movies'
	command2 = 'SELECT TShow FROM TVshowlist'
	cur.execute(command1)
	mvcheck = cur.fetchall()
	cur.execute(command2)
	tcheck = cur.fetchall()
	mcheck = []
	tvcheck = []
	for mve in mvcheck:
		mcheck.append(mve[0])
	for tsh in tcheck:
		tvcheck.append(tsh[0])
	if (("none" not in name) and ("none" not in title)):
		blist = getblockpackagelist()
		title = titlecheck(title)
		title = mediachecker(title)
		if ("Quit." in title):
			return ("User Quit. No action taken.")
		if ("movie." in title) and ("random" not in title.lower()):
			title = title.split("movie.")
			title = title[1]
			for item in blist:
				#check = item.replace(".txt","").rstrip()
				check = str(item)
				if name == check:
					return ("Error. That block already exists. Pick a new name or use 'addtoblock' to update an existing block.")

			command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'' + title + '\''
			cur.execute(command)
			if not cur.fetchone():
				print ("Error: " + title + " not found.\n")
				xname = didyoumeanmovie(title)
				if ("Error" in xname):
					return(xname)
				elif ("Quit" in xname):
					return ("User quit. No action taken.")
			else:
				cur.execute(command)
				xname = cur.fetchone()
				xname = xname[0].strip()

			blname = str(name)
			adtitle = "movie." + str(xname) + ";"
			blcount = 0
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (blname, adtitle, blcount))
			sql.commit()
			blname = blname.replace("movie.", "The Movie ")
			say = (adtitle.rstrip() + " has been added to the " + blname + " .")

			return (say)
		elif ("random_movie." in title.lower()):
			rgenre = title.split("movie.")
			try:
				rgenre = rgenre[1]
			except IndexError:
				Return ("Error. No genre provided.")
			
			cur.execute('SELECT * FROM Movies WHERE Genre LIKE \'%' + rgenre + '%\'')
			if not cur.fetchone():
				return ("Sorry " + str(rgenre.strip()) + " not found as an available genre.")
			else:
				adtitle = title.strip() + ";"
				blcount = 0
				blname = str(name)
				cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (blname, adtitle, int(blcount)))
				sql.commit()
				say = title + " has been added to the " + name + " block."
				return (say)
		elif ("random_tv." in title.lower()):
			rgenre = title.split('tv.')
			try:
				rgenre = rgenre[1]
			except IndexError:
				Return ("Error. No genre provided.")
			print ("Checking " + rgenre)
			cgenre = availgenretv()
			cxgenre = []
			for items in cgenre:
				items = items.replace('.txt','')
				cxgenre.append(items)


			if rgenre not in cxgenre:
				return ("Sorry " + str(rgenre.strip()) + " not found as an available genre.")

			else:
				adtitle = bitems + "Random_tv." + rgenre.strip() + ";"
				blcount = 0
				cur.execute('DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\'')
				sql.commit()
				cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, adtitle, blcount))
				sql.commit()
				xname = "Random TV " + rgenre.strip() + " has been added to the block.\n"
				return (xname)
			
				
		else:
			for item in tvcheck:
				if (title.lower() == item.lower().rstrip()):
					xname = item
					mycheck = "True"
			try:
				mycheck
			except Exception:
				mycheck = "False"
			if "True" in mycheck:
				blname = str(name).strip()
				adtitle = str(xname).strip() + ";"
				blcount = 0
				cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (blname, adtitle, int(blcount)))
				sql.commit()
				blname = blname.replace("movie.", "The Movie ")
				say = (xname.rstrip() + " has been added to the " + blname + ".")
			else:
				print (xname +" not found in library. Did you mean: \n")
				for item in tvcheck:
					if (xname.lower() in item.lower().rstrip()):
						print (item)	
				say = "Done."
			return (say)
	else:
		print ("Command line options not present. Proceeding to querry mode.")	
		while True:
			say = ""
			print ("Enter New Block Name\n")
			name = str(input('Name: '))
			blist = getblockpackagelist()
			for item in blist:
				check = item
				if name == check:
					say = ("Error. Name already in use. Select new block name or edit the existing block.")
			if "Error" in say:
				print (say)
			else:
				break

		name = name.replace(",","")
		name = name.replace(";","")
		name = name.replace("+","")
		name = name.replace("=","")
		while True:
			cur.execute('SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + name + '\'')
			binfo = cur.fetchone()
			try:
				bname = binfo[0].rstrip()
				bitems = binfo[1].rstrip()
				bcount = binfo[2]
			except Exception:
				bname = name
				bitems = ""
				bcount = 0
			mycheck = ""
			choice = ""
			print ("Adding 1- Movie or 2- TV Show 3- Random Item Type to the list? 4- Quit.")
			try:
				choice = int(input('Choice: '))
			except Exception:
				choice = 4
			if choice == 1:
				xname = str(input('Movie Name:'))
				'''
				for item in mcheck:
					macheck = item.lower()
					if (xname.lower() == item.lower().rstrip()):
						xname = "movie." + item.rstrip()
						mycheck = "True"
				'''
				xname = titlecheck(xname.strip())
				xname = mediachecker(xname)
				if ("Quit." in xname):
					return ("User Quit. No action taken.")
				blname = str(name)
				adtitle = bitems+str(xname)+";"
				blcount = 0
				cur.execute('DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\'')
				sql.commit()
				cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, adtitle, bcount))
				sql.commit()
				xname = blname
				xname = xname.replace("movie.","")
				print (xname.rstrip() + " has been added to the block.")
			elif choice == 2:
				xname = str(input('TV Show Name:'))
				for item in tvcheck:
					if (xname.lower() == item.lower().rstrip()):
						xname = item.strip()
						mycheck = "True"
				try:
					mycheck
				except Exception:
					mycheck = "False"
				if "True" in mycheck:
					blname = str(name)
					adtitle = bitems+str(xname)+";"
					blcount = 0
					cur.execute('DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\'')
					sql.commit()
					cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, adtitle, bcount))
					sql.commit()
					xname = blname
					xname = xname.replace("movie.","")

					print (xname.rstrip() + " has been added to the block.")
				else:
					print (xname +" not found in library. Did you mean: \n")
					for item in tvcheck:
						if (xname.lower() in item.lower().rstrip()):
							print (item)
			elif choice == 3:
				rcheck = ""
				while "true" not in rcheck:
					try:
						print ("1 - Random Movie OR 2- Random TV Show\n")
						rtype = int(input('Random Type: '))
						if rtype == 1:
							rgenre = str(input('Genre:'))
							print ("Checking " + rgenre)
							cur.execute('SELECT * FROM Movies WHERE Genre LIKE \'%' + rgenre + '%\'')
							if not cur.fetchone():
								print ("Sorry " + str(rgenre.strip()) + " not found as an available genre.")
								
							else:
								print ("Pass. Adding now.")
								adtitle = bitems + "Random_movie." + rgenre.strip() + ";"
								blcount = 0
								cur.execute('DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\'')
								sql.commit()
								cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, adtitle, blcount))
								sql.commit()
								xname = "Random Movie " + rgenre.strip() + " has been added to the block.\n"
								rcheck = "true"
						elif rtype ==2:
							rgenre = str(input('Genre:'))
							print ("Checking " + rgenre)
							cgenre = availgenretv()
							cxgenre = []
							for items in cgenre:
								items = items.replace('.txt','')
								cxgenre.append(items)
							if rgenre not in cxgenre:
								print ("Sorry " + str(rgenre.strip()) + " not found as an available genre.")

							else:
								print ("Pass. Adding now.")
								adtitle = bitems + "Random_tv." + rgenre.strip() + ";"
								blcount = 0
								cur.execute('DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\'')
								sql.commit()
								cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, adtitle, blcount))
								sql.commit()
								xname = "Random TV " + rgenre.strip() + " has been added to the block.\n"
								rcheck = "true"
							rcheck = "true"
						else:
							print ("Error. You must choose one of the available options.")
					except Exception:
						print ("Error. You must choose one of the available options.")


			elif choice == 4:
				return ("Done.")
			else:
				print ("Error. You must select either 1- Movie OR 2- TV Show OR 3- Random Item OR 4- Quit.")
			
		say = ("block."+name+ " has been created.")
		return (say)

def addtoblock(blockname, name):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	blist = getblockpackagelist()
	for item in blist:
		check = item.rstrip()
		if blockname == check:
			acheck = "True"
	try:
		acheck
	except Exception:
		acheck = "False"
	name = titlecheck(name.strip())
	name = mediachecker(name)
	if ("Quit." in name):
		return ("User Quit. No action Taken.")
	name = name.replace('movie.movie.','movie.')
	if ('movie.' in name):
		chname = name.split("movie.")
		chname = chname[1].strip()
		command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'' + chname + '\''
		cur.execute(command)
		if not cur.fetchone():
			name = didyoumeanmovie(chname)
			if ("Error" in name):
				return(name)
			elif ("Quit" in name):
				return ("User Quit. No action Taken.")
		#name = "movie." + name
	else:
		command = 'SELECT TShow FROM TVshowlist WHERE TShow LIKE \'' + name + '\''
		cur.execute(command)
		if not cur.fetchone():
			name = didyoumeanshow(name)
			if ("Error" in name):
				return(name)
			elif ("Quit" in name):
				return ("User Quit. No action Taken.")
	if "True" not in acheck:
		print (blockname +" not found in library. Did you mean:")
		for item in blist:
			if (blockname in item):
				if ("_count" in item):
					pass
				else:
					print (item)
		say = ("Add Failed. " + blockname + " not found.")
		return say
	else:
		cur.execute('SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + blockname + '\'')
		binfo = cur.fetchone()
		bname = binfo[0].rstrip()
		bitems = binfo[1].rstrip()
		aditem = bitems + name + ";"
		bcount = binfo[2]
		if ("movie." in name):
			blname = str(bname)
			adtitle = bitems + str(name) + ";"
			blcount = 0
			command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (blname, adtitle, blcount))
			sql.commit()
			blname = blname.replace("movie.", "The Movie ")
			say = (name.rstrip() + " has been added to the " + blname + " block.")
			return (say)

		else:
			xname = name
			blname = str(bname)
			adtitle = bitems + str(xname).strip() + ";"
			blcount = 0
			command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (blname, adtitle, int(blcount)))
			sql.commit()
			blname = blname.replace("movie.", "The Movie ")
			say = (xname.rstrip() + " has been added to the " + blname + " block.")
			return (say)
		return ("Done.")

def removefromblock(blockname, name):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	list = getblockpackagelist()
	for item in list:
		item = item.replace(".txt", "")
		if (item in blockname):
			xitem = item
			yitem = item + ".txt"
			xitem = xitem.replace('.txt','')
			command = 'SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + xitem + '\''
			cur.execute(command)
			binfo = cur.fetchone()
			bname = binfo[0]
			bitems = binfo[1]
			bcount = binfo[2]
			bxitems = bitems.split(';')
			ccheck = "fail"
			for item in bxitems:
				if name == item:
					ccheck = "pass"

			if ("pass" not in ccheck):
				return ("Error: " + name + " not found in " + blockname + " to remove")
			bitems = bitems.replace(name +";","", 1)
			command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, bitems, int(bcount)))
			sql.commit()
			say = name + " has been removed from " + blockname

			return say
	return ("Item not found to remove.")

def playblockpackage(play):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	list = getblockpackagelist()
	for item in list:
		item = item.replace(".txt", "")
		if (item in play):
			xitem = item
			yitem = item + ".txt"
			xitem = xitem.replace('.txt','')
			command = 'SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + xitem + '\''
			cur.execute(command)
			binfo = cur.fetchone()
			bname = binfo[0]
			bitems = binfo[1]
			bcount = binfo[2]
			bxitems = bitems.split(';')
			max_count = len(bxitems)
			play = bxitems[bcount]
			bcount = bcount + 1
			if int(bcount) == (int(max_count)-1):
				bcount = 0
				setplaymode("normal")
				print ("Playmode has been set to normal.")
			command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, bitems, int(bcount)))
			sql.commit()
			if "Random_movie." in play:
				type = play
				type = type.replace(";","")
				openmv = homedir + "tonights_movie.txt"
				with open(openmv, "r") as file:
					play = file.read()
				file.close()
				if not play:
					type = type.split("Random_movie.")
					type = type[1]
					type = type.replace(";","")
					play = suggestmovie(type)
					play = play.split("movie: ")
					play = play[1]
					play = play.split(" sound")
					play = play[0]
					play = "movie." + play
				play = play.rstrip()
				with open (openmv, "w") as file:
					file.write("")
				file.close()
			elif "Random_tv." in play:
				type = play
				type = type.replace(";","")
				tvopen = homedir + "random_tv_chooser.txt"
				with open(tvopen, "r") as file:
					play = file.read()
				file.close()
				if not play:
					type = type.split("Random_tv.")
					type = type[1]
					type = type.replace(";","")
					play = suggesttv(type)
					play = play.split("TV Show ")
					play = play[1]
					play = play.split(" sound")
					play = play[0]
				play = play.rstrip()
				with open(tvopen, "w") as file:
					file.write("")
				file.close()
			
			playshow(play)	


def availableshows():
	command = 'SELECT TShow FROM shows WHERE Tnum = 1'
	cur.execute(command)
	tshows = cur.fetchall()
	theshows = []
	for shows in tshows:
		theshows.append(shows[0])
	worklist(theshows)	
	return ("Done")

def worklist(thearray):
	movies = thearray
	mcount = 1
	mvcount = 0
	mmin = 0
	mmax = 9
	mpmin = 1
	if mmax > len(movies):
		mmax = int(len(movies)-1)
	exitc = ""
	while "quit" not in exitc:
		cls()
		try:
			print ("Error: " + Error + "\nThe Following Items Were Found:\n")
			del Error
		except NameError:
			print ("The Following Items Were Found:\n")
		while mmin <= mmax:
			print (movies[mmin])
			mmin = mmin + 1
		print ("\nShowing Items " + str(mpmin) + " out of " + str(mmax+1)+ " Total Found: " + str(len(movies)))
		mpmin = mmax + 1
		mmax = mmax + 10
		if (mmax > int(len(movies)-1)):
			mcheck = int(mmax) - int(len(movies)-1)
			if ((mcheck > 0) and (mcheck < 10)):
				mmax = mmax-mcheck
			elif mcheck > 10:
				return ("Done.")
		if (mmax == int(len(movies)+9)):
			return ("Done")
		print ("\nWould you like to see more?")
		getme = input('Yes or No?')
		if (("y" in getme.lower()) and ("letter" not in getme.lower())):
			mvcount = mvcount + 10
		elif ("letter" in getme.lower()):
			find = getme.lower().split("letter ")
			find = find[1][:1].strip()
			print ("Starting at the letter " + find + ".\n")
			lcount = 0
			lcheck = "go"
			try:
				while "stop" not in lcheck:
					lmcheck = movies[lcount][:1].lower()
					if find.lower() in lmcheck:
						lcheck = "stop"
					lcount = lcount + 1
				mmin = lcount
				mpmin = lcount + 1
				mmax = lcount + 10
				if (mmax > int(len(movies)-1)):
					mcheck = int(mmax) - int(len(movies)-1)
					if ((mcheck > 0) and (mcheck < 10)):
						mmax = mmax-mcheck
					elif mcheck > 10:
						return ("Done.")
					if (mmax == int(len(movies)+9)):
						return ("Done")
			except Exception:
				Error = "No items found containing " + find + ".\n"

			
		else:
			exitc = "quit"
		
			print ("\n")
			say = ""


def availableblocks():
	blocklist = getblockpackagelist()
	for item in blocklist: 
		try:
			blist = blist + item + "\n"
		except NameError:
			blist = item + "\n"
	return blist

def findmovie(movie):
	if ("genre." in movie.lower()):
		genre = movie.split("genre.")
		genre = genre[1]
		connsql = homedir + 'myplex.db'
		sql = sqlite3.connect(connsql)
		cur = sql.cursor()
		command = 'SELECT Movie FROM Movies WHERE Genre LIKE \'%' + genre + '%\' ORDER BY Movie ASC'
		cur.execute(command)
		#marker
		if not cur.fetchone():
                        return ("Error: No movies in the " + genre + " genre have been found.")
                else:
                        tlist = cur.fetchall()
                        mlist = []
                        for movie in tlist:
                                mlist.append(movie[0])
                        worklist(mlist)
	elif ("rating." in movie.lower()):
		from random import randint
		connsql = homedir + 'myplex.db'
                sql = sqlite3.connect(connsql)
                cur = sql.cursor()
		rating = movie.split('.')
		rating = rating[1].strip()
		command = "SELECT Movie FROM Movies WHERE Rating LIKE \'" + rating + "\'"
		cur.execute(command)
		if not cur.fetchone():
			return ("Error: No movies with a " + rating + " have been found.")
		else:
			tlist = cur.fetchall()
			mlist = []
			for movie in tlist:
				mlist.append(movie[0])
			worklist(mlist)
	elif ('actor.' in movie.lower()):
		from random import randint
                connsql = homedir + 'myplex.db'
                sql = sqlite3.connect(connsql)
                cur = sql.cursor()
                rating = movie.split('actor.')
                rating = rating[1].strip()
                command = "SELECT Movie FROM Movies WHERE Actors LIKE \'%" + rating + "%\'"
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: No movies starring " + rating + " have been found.")
                else:
                        tlist = cur.fetchall()
                        mlist = []
                        for movie in tlist:
                                mlist.append(movie[0])
                        worklist(mlist)
	else:
		connsql = homedir + 'myplex.db'
		sql = sqlite3.connect(connsql)
		cur = sql.cursor()
		command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'%' + movie + '%\''
		cur.execute(command)
		xep = cur.fetchall()
		try:
			print ("The Following Movies were found containing \'" + movie + "\':")
			for item in xep:
				print (item[0])
			print ("\n")
			say = ""
		except Exception:
			say = "No results found for " + movie + ". Did you mean:\n"

		if xep == []:
			movie = movie.split(' ')
			for title in movie:
				print ("Found containing " + title + "\n")
				command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'%' + title + '%\''
				cur.execute(command)
				xep = cur.fetchall()
				try:
					for item in xep:
						print (item[0])
					print ("\n")
					say = ""
				except Except:
					print ("No items found containing " + title)



		return (say)

def listepisodes(show):
	command = "SELECT TShow, Episode, Season, Enum FROM shows WHERE TShow LIKE \'" + show + "\'"
	cur.execute(command)
	if not cur.fetchall():
		return ("The Show " + show + " not found.")
	else:
		cur.execute(command)
		episodes = cur.fetchall()
		for item in episodes:
			addme = " Season: " + str(item[2]) + " Episode: " + str(item[3]) + "\nName: " + item[1].strip()
			#addme = "Episode: " + item[1] + " Season: " + str(item[2]) + " Ep Number: " + str(item[3])
			try:
				eplist = eplist + " | " + addme
			except NameError:
				eplist = addme
		eplist = eplist.split(" | ")
		emax = 10
		if emax > int(len(eplist)):
			emax = int(len(eplist))
		emin = 0
		epmin = 1
		exitc = ""
		echoice = 1
		while "quit" not in exitc:
			cls()
			print ("The Following Episodes where found for the show " + show + ": \n")
			while emin <= emax-1:
				print (str(echoice) + ":" +eplist[emin])
				emin = emin + 1
				echoice = echoice + 1
			print ("\nShowing Items " + str(epmin) + " out of " + str(emax) + "\nTotal Number of Episodes: " + str(len(eplist)))
			print ("\nPick a number to see the episode details.\nOr\nWould you like to see more?")
			getme = input('1-10 / Yes or No?')
			try:
				choice = int(getme) + epmin-1
				choice = episodes[choice-1]
				say = epdetails(str(choice[0]), str(choice[2]), str(choice[3]))
				print ("Episode Details:\n" + say + "\n\nEnter 'Yes' to proceed.\n")
				readyc = input('Yes?' )
				if "y" in readyc.lower():
					epmin = emax + 1
					emax = emax + 10
					echoice = 1
					if (emax > int(len(eplist)-1)):
						echeck = int(emax) - int(len(eplist)-1)
						if ((echeck >0) and (echeck <10)):
							emax = emax - echeck+1
						elif echeck > 10:
							return ("Done.")
					if (emax == int(len(eplist)+9)):
						return ("Done.")
					if ('n' in getme.lower()):
						exitc = "quit"
			except Exception:
				epmin = emax + 1
				emax = emax + 10
				echoice = 1
				if (emax > int(len(eplist)-1)):
					echeck = int(emax) - int(len(eplist)-1)
					if ((echeck >0) and (echeck <10)):
						emax = emax - echeck+1
					elif echeck > 10:
						return ("Done.")
				if (emax == int(len(eplist)+9)):
					return ("Done.")
				if ('n' in getme.lower()):
					exitc = "quit"
	return ("Done.")				


def findshow(show):
        connsql = homedir + 'myplex.db'
        sql = sqlite3.connect(connsql)
        cur = sql.cursor()
	#marker
	if ("genre." in show.lower()):
		genre = show.split("genre.")
		genre = genre[1].strip().lower()
		command = 'SELECT TShow from TVshowlist WHERE Genre LIKE \'%' + genre + '%\''
	elif ("rating." in show.lower()):
		rating = show.split("rating.")
		rating = rating[1].strip()
		command = 'SELECT TShow FROM TVshowlist WHERE Rating LIKE \'' + rating + '\''
	elif ("duration." in show):
		duration = show.split("duration.")
		duration = int(duration[1].strip())
		command = 'SELECT TShow FROM TVshowlist WHERE Duration LIKE \'' + str(duration) + '\''
	else:
		command = 'SELECT TShow FROM shows WHERE TShow LIKE \'%' + show + '%\' AND Tnum = 1'
        cur.execute(command)
        xep = cur.fetchall()
	foundme = []
        try:
                for item in xep:
                       foundme.append(item[0])
		foundme = sorted(foundme)
		worklist(foundme)
		say = ("Done.")
        except Exception:
                say = "No results found. Please try again."
        return (say)

def epdetails(show, season, episode):
	connsql = homedir + 'myplex.db'
	sql = sqlite3.connect(connsql)
	cur = sql.cursor()
	test = show
	Ssn = season
	Epnum = episode
	command = 'SELECT Episode, Summary FROM shows WHERE TShow LIKE \'' + test + '\' and Season LIKE \'' + Ssn + '\' and Enum LIKE \'' + Epnum + '\''
	cur.execute(command)
	xep = cur.fetchone()
	ep = str(xep[0])
	summary = str(xep[1])
	summary = summary.replace("&apos;", "'")
	summary = summary.replace("&#xA;", "")
	showplay = ep + " The Plot Summary is " + summary
	return showplay

def moviedetails(movie):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	command = 'SELECT Movie, Summary, Rating, Tagline, Summary FROM Movies WHERE Movie LIKE \'' + movie + '\''
	cur.execute(command)
	xep = cur.fetchone()
	ep = str(xep[0])
	summary = str(xep[1])
	summary = summary.replace("&apos;", "'")
	summary = summary.replace("&#xA;", "")
	xmovie = "movie." + movie.strip()
	leftoff = whereleftoff(xmovie)

	showplay = "Movie: " + ep + "\nRated: " + str(xep[2]) + "\nTagline: " + str(xep[3]) + "\nSummary: " + summary + "\n\nResume from minute option: " + str(leftoff) + "."
	return showplay

def showdetails(show):
	command = 'SELECT * FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: " + show + " not found. Check title and try again.")
	else:
		cur.execute(command)
		stuff = cur.fetchone()
		name = stuff[0]
		summary = stuff[1]
		summary = summary.replace('&apos;','\'')
		try:
			genres = stuff[2]
		except Exception:
			genres = "N/A"
		genres = genres.replace(";", ", ")
		rating = stuff[3]
		duration = stuff[4]
		total = stuff[5]
		sayme = "For the show: " + name + "\nSummary: " + summary + "\nGenre: " + genres + "\nRating: " + rating + "\nDuration: " + str(duration) + " minutes\nNumber of Episodes: " + str(total)
		return (sayme)

def movietagline(movie):
	command = 'SELECT Tagline FROM Movies WHERE Movie LIKE \'' + movie + '\''
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: " + movie + " not found in DB. Please try again.")
	else:
		try:
			cur.execute(command)
			found = cur.fetchone()[0]
			return found
		except Exception:
			return ("The Move " + movie + " has no tagline.")

def movietlgame_gettagline():
	command = 'SELECT Tagline FROM Movies'
	cur.execute(command)
	tgs = cur.fetchall()
	taglines = []
	for tags in tgs:
		taglines.append(tags)
	max = int(len(taglines)-1)
	from random import randint, shuffle
	shuffle(taglines)
	getme = randint(0,max)
	found = taglines[getme]
	return (found[0])

def movietlgame_intro():
	command = 'SELECT State FROM States WHERE Option LIKE \'Tagline\''
	cur.execute(command)
	if not cur.fetchone():
		print ("Readying Game Board.")
		tagline = movietlgame_gettagline()
		cur.execute('INSERT INTO States VALUES(?,?)',('Tagline',tagline))
		sql.commit()
	cur.execute(command)
	tagline = cur.fetchone()[0]
	command = 'SELECT Movie FROM Movies WHERE Tagline LIKE \'' + tagline.strip() + '\''
	cur.execute(command)
	movie = cur.fetchone()[0]
	command = 'SELECT State FROM States WHERE Option LIKE \'TLG_TOTAL_Guesses\''
	cur.execute(command)
	try:
		tguesses = cur.fetchone()[0]
	except Exception:
		tguesses = 0
	tguesses = int(tguesses) + 1
	command = 'DELETE FROM States WHERE Option LIKE \'TLG_TOTAL_Guesses\''
	cur.execute(command)
	sql.commit()
	cur.execute('INSERT INTO States VALUES (?,?)',('TLG_TOTAL_Guesses', str(tguesses)))
	sql.commit()
	
	print ("Beginning Game...\nThis movies tagline is: " + tagline)
	guess = str(raw_input('Guess '))
	if ("i give up" in guess.lower()):
		command = 'DELETE FROM States WHERE Option LIKE \'Tagline\''
                cur.execute(command)
                sql.commit()
		command = 'DELETE FROM States WHERE Option LIKE \'TLG_Hints\''
                cur.execute(command)
                sql.commit()
		cur.execute('INSERT INTO States VALUES (?,?)',('TLG_Hints', '0'))
                sql.commit()
		command = 'SELECT State FROM States WHERE Option LIKE \'TLG_TOTAL_Losses\''
		cur.execute(command)
		try:
			tguesses = cur.fetchone()[0]
		except Exception:
			tguesses = 0
		tguesses = int(tguesses) + 1
		command = 'DELETE FROM States WHERE Option LIKE \'TLG_TOTAL_Losses\''
		cur.execute(command)
		sql.commit()
		cur.execute("INSERT INTO States VALUES(?,?)",('TLG_TOTAL_Wins',str(tguesses)))
		sql.commit()
		print ("\nThe tagline was for the movie " + movie + "\n")
		return ("What a Loser. You\'re like a L - 7 Weeney. ... I have cleared the board. Do better next time, if you can, Loser.")
	elif ("give hint" in guess.lower()):
		command = "SELECT State FROM States WHERE Option LIKE \'TLG_Hints\'"
		cur.execute(command)
		hints = cur.fetchone()[0]
		hints = int(hints)
		command = 'SELECT State FROM States WHERE Option LIKE \'TLG_TOTAL_Hints\''
		cur.execute(command)
		if not cur.fetchone():
			thints = 0
		else:
			try:
				thints = cur.fetchone()[0]
			except Exception:
				thints = 0
		thints = int(thints) + 1
		command = "DELETE FROM States WHERE Option LIKE \'TLG_TOTAL_Hints\'"
		cur.execute(command)
		sql.commit()
		cur.execute("INSERT INTO States VALUES(?,?)",('TLG_TOTAL_Hints',str(thints)))
		sql.commit()	
		
		if hints == 0:
			command = 'SELECT Rating FROM Movies WHERE Movie LIKE \'' + movie + '\''
			cur.execute(command)
			the_hints = cur.fetchall()[0]
			the_hints = the_hints[0]
			hints = hints + 1
			command = "DELETE FROM States WHERE Option LIKE \'TLG_Hints\'"
			cur.execute(command)
			sql.commit()
			cur.execute("INSERT INTO States VALUES(?,?)",('TLG_Hints',str(hints)))
			sql.commit()
			return ("This movie is rated: " + the_hints + "\n")
		elif hints == 1:
			command = 'SELECT Genre FROM Movies WHERE Movie LIKE \'' + movie + '\''
                        cur.execute(command)
                        the_hints = cur.fetchall()[0]
                        the_hints = the_hints[0]
                        hints = hints + 1
                        command = "DELETE FROM States WHERE Option LIKE \'TLG_Hints\'"
                        cur.execute(command)
                        sql.commit()
                        cur.execute("INSERT INTO States VALUES(?,?)",('TLG_Hints',str(hints)))
                        sql.commit()
			return ("This movie is in the following genres: " + the_hints + "\n")
		elif hints == 2:
			command = 'SELECT Director FROM Movies WHERE Movie LIKE \'' + movie + '\''
                        cur.execute(command)
                        the_hints = cur.fetchall()[0]
                        the_hints = the_hints[0]
			hints = hints + 1
                        command = "DELETE FROM States WHERE Option LIKE \'TLG_Hints\'"
                        cur.execute(command)
                        sql.commit()
                        cur.execute("INSERT INTO States VALUES(?,?)",('TLG_Hints',str(hints)))
                        sql.commit()
                        return ("This movie was directed by: " + the_hints + "\n")
		elif hints == 3:
                        command = 'SELECT Actors FROM Movies WHERE Movie LIKE \'' + movie + '\''
                        cur.execute(command)
                        the_hints = cur.fetchall()[0]
                        the_hints = the_hints[0]
                        hints = hints + 1
                        command = "DELETE FROM States WHERE Option LIKE \'TLG_Hints\'"
                        cur.execute(command)
                        sql.commit()
                        cur.execute("INSERT INTO States VALUES(?,?)",('TLG_Hints',str(hints)))
                        sql.commit()
                        return ("This movie starred: " + the_hints + "\n")
		elif hints == 4:
			print ("WARNING: This is your very last hint. If you can't get it off this you are in bad shape.\n")
                        command = 'SELECT Summary FROM Movies WHERE Movie LIKE \'' + movie + '\''
                        cur.execute(command)
                        the_hints = cur.fetchall()[0]
                        the_hints = the_hints[0]
                        hints = hints + 1
                        command = "DELETE FROM States WHERE Option LIKE \'TLG_Hints\'"
                        cur.execute(command)
                        sql.commit()
                        cur.execute("INSERT INTO States VALUES(?,?)",('TLG_Hints',str(hints)))
                        sql.commit()
                        return ("This movie's summary is: " + the_hints + "\n")
		else:
			command = "DELETE FROM States WHERE Option LIKE \'TLG_Hints\'"
                        cur.execute(command)
                        sql.commit()
                        cur.execute("INSERT INTO States VALUES(?,?)",('TLG_Hints','0'))
			sql.commit()
			return ("Sorry, but you have reached the maximum number of hints. I have reset the hits couner, but your overall counter will continue to increase as you use this command.")

	else:
		mvcheck = guess.lower()
		command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'' + mvcheck + '\''
		cur.execute(command)
		if not cur.fetchone():
			guess = didyoumeanmovie(mvcheck)
		if guess.lower() in movie.lower():
			command = 'DELETE FROM States WHERE Option LIKE \'Tagline\''
			cur.execute(command)
			sql.commit()
			command = "DELETE FROM States WHERE Option LIKE \'TLG_Hints\'"
			cur.execute(command)
			sql.commit()
			cur.execute("INSERT INTO States VALUES(?,?)",('TLG_Hints','0'))
			sql.commit()
			command = 'SELECT State FROM States WHERE Option LIKE \'TLG_TOTAL_Wins\''
			cur.execute(command)
			try:
				tguesses = cur.fetchone()[0]
			except Exception:
				tguesses = 0
			tguesses = int(tguesses) + 1
			command = 'DELETE FROM States WHERE Option LIKE \'TLG_TOTAL_Wins\''
			cur.execute(command)
			sql.commit()
			cur.execute("INSERT INTO States VALUES(?,?)",('TLG_TOTAL_Wins',str(tguesses)))
                        sql.commit()
			
			return ("WINNER WINNER CHICKEN DINNER!!!!")
		else:
			return ("We're Sorry, but that guess is incorrect. Please try again.")

	

def movierating(movie):
	command = 'SELECT Rating FROM Movies WHERE Movie LIKE \'' + movie + '\''
        cur.execute(command)
        if not cur.fetchone():
                return ("Error: " + movie + " not found in DB. Please try again.")
        else:
		try:
			cur.execute(command)
			found = cur.fetchone()[0]
			if "none" in found:
				return ("The Movie " + movie + " has no rating.")
			else:
				return ("The Movie " + movie + " has a " + found + " rating.")
		except Exception:
			return "The Movie " + movie + " has no rating specified." 

def moviesummary(movie):
        command = 'SELECT Summary FROM Movies WHERE Movie LIKE \'' + movie + '\''
        cur.execute(command)
        if not cur.fetchone():
                return ("Error: " + movie + " not found in DB. Please try again.")
        else:
                try:
                        cur.execute(command)
                        found = cur.fetchone()[0]
                        if "none" in found:
                                return ("The Movie " + movie + " has no Summary.")
                        else:
                                return ("The Movie " + movie + " 's summary is: " + found)
                except Exception:
                        return "The Movie " + movie + " has no summary in the database."



def setnextep(show, season, episode):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	test = show
	Ssn = season
	Epnum = episode
	command = 'SELECT Episode, Tnum FROM shows WHERE TShow LIKE \'' + test + '\' and Season LIKE \'' + Ssn + '\' and Enum LIKE \'' + Epnum + '\''
	cur.execute(command)
	ep = cur.fetchall()
	Episode = ep[0]
	xshow = Episode[0]
	Episode = Episode[1]
	ep = int(Episode)
	command = 'DELETE FROM TVCounts WHERE Show LIKE \'' + show + '\''
	cur.execute(command)
	sql.commit()
	cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, ep))
	sql.commit()
	say = "The Next episode of " + show + " has been set to - " + xshow 
	say = say.rstrip()
	return say



def playspshow(show, season, episode):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	test = show
	Ssn = season
	Epnum = episode
	command = 'SELECT Episode FROM shows WHERE TShow LIKE \'' + test + '\' and Season LIKE \'' + Ssn + '\' and Enum LIKE \'' + Epnum + '\''
	cur.execute(command)
	ep = cur.fetchall()
	for item in ep:
		theep = item[0]

	shows = plex.library.section('TV Shows')
	the_show = shows.get(show)
	#showplay = the_show.rstrip()
	epx = the_show.get(theep)
	client = plex.client("RasPlex")
	client.playMedia(epx)
	nowplaywrite("TV Show: " + show + " Episode: " + theep)
	showsay = 'Playing ' + theep + ' From the show ' + show + ' Now, Sir'

	return showsay

def playshow(show):
	consql = homedir + 'myplex.db'
	tvshowlist = homedir + 'tvshowlist.txt'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	with open(tvshowlist, 'r') as file:
		showlist = file.readlines()
	file.close()
	command = 'SELECT Episode FROM shows WHERE TShow LIKE \'' + show + '\''
	cur.execute(command)
	if not cur.fetchone():
		schecker = "lost"
	else:
		schecker = "found"

	try:
		schecker
	except NameError:
		schecker = "lost"
		
	if ("found" in schecker):
		try:
			command = 'SELECT Number FROM TVCounts WHERE Show LIKE \'' + show + '\''
			cur.execute(command)
			thecount = cur.fetchone()
			thecount = thecount[0]
		except Exception:
			print ("Item not found in DB. Adding")
			thecount = 1 
			cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecount))
			sql.commit()

		if thecount == 0:
			thecount = 1
		
		command = 'SELECT Episode FROM shows WHERE TShow LIKE \'' + show + '\' and Tnum LIKE \'' + str(thecount) + '\''
		cur.execute(command)
		sql.commit()
		xshow = cur.fetchone()
		xshow = xshow[0].rstrip()
		thecountx = (thecount + 1)
		command = 'SELECT Episode FROM shows WHERE TShow LIKE \'' + show + '\' and Tnum LIKE \'' + str(thecountx) + '\''
		cur.execute(command)
		check = cur.fetchone()
		if not check:
			thecountx = 1
		command = 'DELETE FROM TVCounts WHERE Show LIKE \'' + show + '\''
		cur.execute(command)
		cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecountx))
		sql.commit()	
		thecount = str(thecount)
	
		shows = plex.library.section('TV Shows')
		the_show = shows.get(show)
		#showplay = the_show.rstrip()
		ep = the_show.get(xshow)
		client = plex.client("RasPlex")
		client.playMedia(ep)
		nowplaywrite("TV Show: " + show + " Episode: " + xshow)
		showsay = 'Playing ' + xshow + ' From the show ' + show + ' Now, Sir' 
		
		return showsay
	elif ("movie." in show):
		show = show.replace("movie.", "")
		command = 'SELECT Movie FROM Movies WHERE Movie like\'' + show + '\''
		cur.execute(command)
		movies = cur.fetchall()
		for mvs in movies:
			if mvs[0].lower() == show.lower():
				show = mvs[0]
				show = show.rstrip()
				movie = plex.library.section('Movies').get(show)
				client = plex.client(PLEXCLIENT)
				client.playMedia(movie)
				#playfile(show)
				showplay = show
				nowplaywrite("Movie: " + showplay)
				
				return ("Playing the movie " + show + " now, Sir.") 
		return ("Error. " + show + " Not found!")
	elif ("block." in show):
		playblockpackage(show)
		show = show.replace("_", " ")
		return ("Starting the " + show)
	else:
		
		return ("Media not found to launch. Check the title and try again.")

def whereleftoff(item):
	global plex
	if "movie." in item:
		plexlogin()
		item = item.replace("movie.","")
		command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'' + item.strip() + '\''
		cur.execute(command)
		movie = cur.fetchone()
		try:
			movie = movie[0]
		except Exception:
			return ("Error: movie not found. Please try again.")
		mve = plex.library.section('Movies').get(movie)
		whereleftoff = mve.viewOffset
		whereleftoff = whereleftoff / 60000
		return (whereleftoff)
	else:
		if "block." in item:
			thing = item.replace("block.","").strip()
			command = "SELECT Count FROM Blocks WHERE Name LIKE \'" + thing + "\'"
			cur.execute(command)
			foundc = cur.fetchone()[0]
			if not foundc:
				return ("Block not found. Try again.")
			else:
				command = "SELECT Items FROM Blocks WHERE Name Like \'" + thing + "\'"
				cur.execute(command)
				items = cur.fetchone()[0]
				items = items.split(';')
				found = items[foundc]
				return ("Up next is item " + str(foundc + 1) + ":\n" + found)
		print ("Sorry. This feature only currently supports movies. Starting your request from the beginning.")
		return (0)

def playwhereleftoff(show):
	leftoff = int(whereleftoff(show)) * 60000
	consql = homedir + 'myplex.db'
	tvshowlist = homedir + 'tvshowlist.txt'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	with open(tvshowlist, 'r') as file:
		showlist = file.readlines()
	file.close()
	command = 'SELECT Episode FROM shows WHERE TShow LIKE \'' + show + '\''
	cur.execute(command)
	if not cur.fetchone():
		schecker = "lost"
	else:
		schecker = "found"

	try:
		schecker
	except NameError:
		schecker = "lost"
	if ("found" in schecker):
		try:
			command = 'SELECT Number FROM TVCounts WHERE Show LIKE \'' + show + '\''
			cur.execute(command)
			thecount = cur.fetchone()
			thecount = thecount[0]
		except Exception:
			print ("Item not found in DB. Adding")
			thecount = 1 
			cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecount))
			sql.commit()
			print ("added")

		if thecount == 0:
			thecount = 1
		
		command = 'SELECT Episode FROM shows WHERE TShow LIKE \'' + show + '\' and Tnum LIKE \'' + str(thecount) + '\''
		cur.execute(command)
		sql.commit()
		xshow = cur.fetchone()
		xshow = xshow[0].rstrip()
		thecountx = (thecount + 1)
		command = 'SELECT Episode FROM shows WHERE TShow LIKE \'' + show + '\' and Tnum LIKE \'' + str(thecountx) + '\''
		cur.execute(command)
		check = cur.fetchone()
		if not check:
			thecountx = 1
		command = 'DELETE FROM TVCounts WHERE Show LIKE \'' + show + '\''
		cur.execute(command)
		cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecountx))
		sql.commit()	
		thecount = str(thecount)
	
		shows = plex.library.section('TV Shows')
		the_show = shows.get(show)
		#showplay = the_show.rstrip()
		ep = the_show.get(xshow)
		client = plex.client("RasPlex")
		client.playMedia(ep, leftoff)
		nowplaywrite("TV Show: " + show + " Episode: " + xshow)
		showsay = 'Playing ' + xshow + ' From the show ' + show + ' Now, Sir' 
		
		return showsay
	elif ("movie." in show):
		show = show.replace("movie.", "")
		command = 'SELECT Movie FROM Movies WHERE Movie like\'' + show + '\''
		cur.execute(command)
		movies = cur.fetchall()
		for mvs in movies:
			if mvs[0].lower() == show.lower():
				show = mvs[0]
				show = show.rstrip()
				movie = plex.library.section('Movies').get(show)
				client = plex.client(PLEXCLIENT)
				client.playMedia(movie, offset=leftoff)
				#playfile(show)
				showplay = show
				nowplaywrite("Movie: " + showplay)
				
				return ("Playing the movie " + show + " now, Sir.") 
		return ("Error. " + show + " Not found!")
	elif ("block." in show):
		playblockpackage(show)
		show = show.replace("_", " ")
		return ("Starting the " + show)
	else:
		
		return ("Media not found to launch. Check the title and try again.")
	
		


def queueadd(addme):
        title = addme.strip()
        if (("numb3rs" not in title.lower()) and ("se7en" not in title.lower())):
                title = titlecheck(title).strip()
		title = title.replace("'","")
		link = homedir + 'myplex.db'
		sql = sqlite3.connect(link)
		cur = sql.cursor()
		type = "queue"
		xname = title
		xname = xname.replace('movie.','')
		if ("addrand" in addme):
			say = queuefill()
		elif ("Quit." in addme):
			say = "User quit. No action taken."
			return (say)
		name = mediachecker(xname)
	else:
		name = mediachecker(title)

	if ("movie." in name):
		xname = name + ";"
		command = 'SELECT State FROM States WHERE Option LIKE \'' + type + '\''
		cur.execute(command)
		queue = cur.fetchone()
		queue = queue[0]
		if not queue:
			queue = xname
		else:
			queue = queue + xname
		command = 'DELETE FROM States WHERE Option LIKE \'' + type + '\''
		cur.execute(command)
		sql.commit()
		cur.execute('INSERT INTO States VALUES(?,?)', (type, queue))
		sql.commit()	
		xname = xname.replace("movie.","")
		say = ("The Movie " + xname.rstrip() + " has been added to the queue.")
		return say	
	else:
		xname = name
		xname = xname + ";"
		command = 'SELECT State FROM States WHERE Option LIKE \'' + type + '\''
		cur.execute(command)
		queue = cur.fetchone()
		queue = queue[0]
		if not queue:
			queue = xname
		else:
			queue = queue + xname
		command = 'DELETE FROM States WHERE Option LIKE \'' + type + '\''
		cur.execute(command)
		cur.execute('INSERT INTO States VALUES(?,?)', (type, queue))
		sql.commit()

		say = ("The TV Show " + xname.rstrip() + " has been added to the queue.")
		return say

def nowplaywrite(showplay):
	cur.execute('DELETE FROM States WHERE Option LIKE \'Nowplaying\'')
	sql.commit()
	cur.execute('INSERT INTO States VALUES (?,?)',('Nowplaying',showplay))
	sql.commit()

def nowplaying():
	cur.execute('SELECT State FROM States WHERE Option LIKE \'Nowplaying\'')
	title = cur.fetchone()
	title = title[0]
	global plex
	plexlogin()
	psess = plex.sessions()
	for sess in psess:
		if (sess.player.title == PLEXCLIENT):
			if "Episode:" in title:
				ctitle = title.split("Episode: ")
				ctitle = ctitle[1].strip()
			elif ("Movie: " in title):
				ctitle = title.split("Movie: ")
				ctitle = ctitle[1].strip()
		
			if ctitle in sess.title:
				say = "Now Playing: " + title
			else:
				say = "Content Type: " + sess.type + ".\n Title: " + sess.title + "."
	return (say)



def queueget():
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	name = "queue"
	command = 'SELECT State FROM States WHERE Option LIKE \'' + name + '\''
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]

	
	if (queue == ""):
		queue = queuefill()

	queue = queue.replace(";", ", and then ")
	queue = queue.replace("movie.", "The Movie ")
	queue = queue.replace(' has been added to the queue.',', and then ')

	queue = "Up next we have: " + queue + "Agent Smith will find content to watch, Sir."
	
	return queue;

def queuefix():
	command = 'DELETE FROM States WHERE Option LIKE \'queue\''
	cur.execute(command)
	sql.commit()
	queue = listwildcard() + ";"
	cur.execute('INSERT INTO States VALUES(?,?)',('queue',queue))
	sql.commit()
	
	return ("The Queue has been rebuilt.")

def queuefill():
	from random import randint, shuffle
	playme = randint(1,7)
	#random TV show
	if ((playme == 1) or (playme ==5) or (playme == 7)):
		if (playme == 1):
			command = "SELECT TShow FROM TVshowlist"
			cur.execute(command)
		else:
			print ("Using Favorites TV")
			command = "SELECT TShow FROM TVshowlist WHERE Genre LIKE \'%Favorite%\'"
			cur.execute(command)
			lcheck = cur.fetchall()
			if (int(len(lcheck)) <25):
				command = "SELECT TShow FROM TVshowlist"
			cur.execute(command)
		tvlist = cur.fetchall()
		tlist = []
		for shw in tvlist:
			tlist.append(shw[0])
		shuffle(tlist)
		max = int(len(tlist))-1
		min = 0
		playc = randint(min,max)
		addme = tlist[playc]
	#random Movie
	if ((playme == 2) or (playme ==4) or (playme == 6)):
		if ((playme == 2) or (playme == 6)):
			command = "SELECT Movie FROM Movies WHERE Genre LIKE \'%favorite%\'"
			print ("Using Favorites.")
		else:
			command = "SELECT Movie FROM Movies"
                cur.execute(command)
		mvlist = cur.fetchall()
		mlist = []
		for mve in mvlist:
			mlist.append(mve[0])
		shuffle(mlist)
		max = int(len(mlist))-1
		min = 0
		playc = randint(min,max)
		play = mlist[playc]
		addme = "movie." + play
	if (playme == 3):
		cur.execute('SELECT setting FROM settings WHERE item LIKE \'WILDCARD\'')
		addme = cur.fetchone()
		addme = addme[0]
	#addme = "The Big Bang Theory"
	return queueadd(addme)

def queueremove(item):
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	name = "queue"
	command = 'SELECT State FROM States WHERE Option LIKE \'' + name + '\''
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]
	queue = queue.replace(';;',';')
	oqueue = queue
	queue = queue.split(';')
	if (item == "None"):
		removeme = queue[0]
	else:
		removeme = mediachecker(item)
	removeme = removeme + ";"
	if (removeme in oqueue):
		newqueue = oqueue.replace(removeme, "")
		newqueue = newqueue.replace("movie.';","")
		newqueue = newqueue.lstrip()
		cur.execute('DELETE FROM States WHERE Option LIKE \'Queue\'')
		sql.commit()
		cur.execute('INSERT INTO States VALUES(?,?)', (name, newqueue))
		sql.commit()
		upnext()
		


def queueremovenofill():
	sqlcon = homedir + "myplex.db"
	sql = sqlite3.connect(sqlcon)
	cur = sql.cursor()
	name = "queue"
	command = 'SELECT State FROM States WHERE Option LIKE \'' + name + '\''
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]
	oqueue = queue
	queue = queue.split(';')
	removeme = queue[0]
	removeme = removeme + ";"
	newqueue = oqueue.replace(removeme, "")
	newqueue=newqueue.lstrip()
	cur.execute('DELETE FROM States WHERE Option LIKE \'Queue\'')
	sql.commit()
	cur.execute('INSERT INTO States VALUES(?,?)', (name, newqueue))
	sql.commit()
	

def upnext():
	sqlcon = homedir + 'myplex.db'
	sql = sqlite3.connect(sqlcon)
	cur = sql.cursor()
	command = 'SELECT State FROM States WHERE Option LIKE \'Playmode\''
	cur.execute(command)
	playmode = cur.fetchone()
	playmode = playmode[0]
	try:
		option = str(sys.argv[2])
		if "normal" in option:
			playmode = option
	except Exception:
		pass
	queue = openqueue()
	if (("normal" in playmode) or ("binge." in playmode)):	
		queue = queue.split(";")
		try:
			playme = queue[0]
			playme = playme.lstrip()
			if "block." in playme:
				skipthat()
				setplaymode(playme)
				playme = upnext()
				return (playme)
		except IndexError:
			queuefill()
			queue= openqueue()
			queue = queue.split(';')
			playme = queue[0]
		if ("binge." in playmode):
			playme = playmode.split("binge.")
			playme = playme[1].strip()
		else:
			playme = playme.replace(";"," ")	
			playme = playme.rstrip()
	elif "block" in playmode:
		playme = playmode
	elif "marathon." in playmode:
		show = playmode.split("marathon.")
		show = show[1]
		playme = show

	return playme

def seriesskipback(show):
	command = "SELECT Number from TVCounts WHERE Show LIKE \'" + show + "\'"
	cur.execute(command)
	if not cur.fetchone():
		command = "SELECT TShow FROM shows WHERE TShow LIKE \'" + show + "\'"
		cur.execute(command)
		if not cur.fetchone():
			return ("Error. " + show + " not found.")
		else:
			cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, 1))
			sql.commit()
			return ("Show " + show + " has been set to the first episode in the series.")
	else:
		cur.execute(command)
		nowat = cur.fetchone()
		nowat = nowat[0]
		if nowat == 1:
			return ("Show " + show + " is already at the first episode in the series. Unable to go back.")
		else:
			nowat = int(nowat) - 1
			cur.execute('DELETE FROM TVCounts WHERE show LIKE \'' + show + '\'')
			sql.commit()
			cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, nowat))
                        sql.commit()
			sayme = nextep(show)
			return (sayme)

def seriesskipahead(show):
        command = "SELECT Number from TVCounts WHERE Show LIKE \'" + show + "\'"
        cur.execute(command)
        if not cur.fetchone():
                command = "SELECT TShow FROM shows WHERE TShow LIKE \'" + show + "\'"
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error. " + show + " not found.")
                else:
                        cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, 1))
                        sql.commit()
                        return ("Show " + show + " has been set to the first episode in the series.")
        else:
                cur.execute(command)
                nowat = cur.fetchone()
                nowat = nowat[0]
		command = "SELECT tnum FROM shows WHERE TShow LIKE \'" + show + "\'"
		cur.execute(command)
		max = cur.fetchall()
		max = len(max) - 1
                if nowat == max:
                        return ("Show " + show + " is already at the last episode. Unable to skip ahead.")
                else:
                        nowat = int(nowat) + 1
                        cur.execute('DELETE FROM TVCounts WHERE show LIKE \'' + show + '\'')
                        sql.commit()
                        cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, nowat))
                        sql.commit()
                        sayme = nextep(show)
                        return (sayme)
	

def playmode():
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	command = 'SELECT State FROM States WHERE Option LIKE \'Playmode\''
	cur.execute(command)
	playmode = cur.fetchone()
	playmode = playmode[0]
	playmode = playmode.replace("marathon.","Marathon Mode- ")
	if "binge." in playmode:
		option = playmode.split("binge.")
		option = option[1].strip()
		option = option.replace("movie.", "The Movie ")
		return ("We are binge  watching: " + option)
	return playmode

def setplaymode(mode):
	from random import randint
	mode = mode.replace("block_","block.")
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	command = 'DELETE FROM States WHERE Option LIKE \'Playmode\''
	cur.execute(command)
	name = 'Playmode'
	queue = mode	
	cur.execute('INSERT INTO States VALUES(?,?)', (name, queue))
	sql.commit()
	if "block.randommovieblock" in mode:
		xmode = mode.split('.')
		xmode = xmode[1]
		command = 'SELECT Movie from Movies'
		cur.execute(command)
		movielist = cur.fetchall()
		moviemax = len(movielist)
		movie1 = movielist[randint(0,moviemax)]
		movie1 = movie1[0]
		movie2 = movielist[randint(0,moviemax)]
		movie2 = movie2[0]
		movie3 = movielist[randint(0,moviemax)]
		movie3 = movie3[0]
		bname = "randommovieblock"
		command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
		cur.execute(command)
		sql.commit()
		block = "movie."+movie1 + ";movie." + movie2 + ";movie." + movie3 + ";"
		blcount = 0
		cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, block, blcount))
		sql.commit()
		say = movie1 + ", and then " + movie2 + ", and finally " + movie3
		mode = "Random " + xmode + " movie block. This one will play: " + say
		
		return "Playmode has been set to "+ mode

def getblockpackage(play):
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	list = getblockpackagelist()
	play = play.replace("block.","")
	for item in list:
		item = item.replace(".txt", "")
		if (item in play):
			command = 'SELECT Items, Count FROM Blocks WHERE Name LIKE \'' + play + '\''
			cur.execute(command)
			stuff = cur.fetchone()
			plays = stuff[0]
			plays = plays.split(";")
			name = play
			count = stuff[1]
			play = plays[count]
			play = play.rstrip()
	return play

def mediachecker(title):
	check1 = "start"
        check2 = "start"
        ctitle = title.replace("movie.","")
        cur.execute('SELECT Movie FROM Movies WHERE Movie LIKE \'' + ctitle + '\'')
        if not cur.fetchone():
                check1 = "fail"
        else:
                check1 = "pass"
                newt = "movie." + title
        cur.execute('SELECT TShow FROM TVshowlist WHERE TShow LIKE \'' + title + '\'')
        if not cur.fetchone():
                check2 = "fail"
        else:
                check2 = "pass"
        if ((check1 == "fail") and (check2 == "fail")):
                addme = didyoumeanboth(title)
                if "Quit." in addme:
                        return ("User Quit. No Action Taken.")
                else:
                        title = addme
        elif ((check1 == "pass") and (check2 == "pass") and ("Fail" not in externalcheck())):
                addme = didyoumeanboth(title)
                if "Quit." in addme:
                        return ("User Quit. No Action Taken.")
                else:
                        title = addme
        elif ((check1 == "pass") and (check2 == "fail")):
                title = newt
	return (title)

def setupnext(title):
	title = title.strip()
	if (("numb3rs" not in title.lower()) and ("se7en" not in title.lower())):
		title = titlecheck(title).strip()
	title = title.replace("'","")
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	check1 = "start"
	check2 = "start"
	ctitle = title.replace("movie.","")
	cur.execute('SELECT Movie FROM Movies WHERE Movie LIKE \'' + ctitle + '\'')
        if not cur.fetchone():
		check1 = "fail"
	else:
		check1 = "pass"
		newt = "movie." + title
	cur.execute('SELECT TShow FROM TVshowlist WHERE TShow LIKE \'' + title + '\'')
	if not cur.fetchone():
		check2 = "fail"
	else:
		check2 = "pass"
	if ((check1 == "fail") and (check2 == "fail")):
		addme = didyoumeanboth(title)
		if "Quit." in addme:
			return ("User Quit. No Action Taken.")
		else:
			title = addme
	elif ((check1 == "pass") and (check2 == "pass") and ("Fail" not in externalcheck())):
		addme = didyoumeanboth(title)
                if "Quit." in addme:
                        return ("User Quit. No Action Taken.")
                else:
                        title = addme
	elif ((check1 == "pass") and (check2 == "fail")):
		title = newt

	if ("movie." in title):
		ctitle = title.replace("movie.","")
		command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'' + ctitle + '\''
		cur.execute(command)
		if not cur.fetchone():
			return ("Error. Title not found to add to play queue.")
	else:
		command = 'SELECT TShow FROM shows WHERE TShow LIKE \'' + title + '\''
		cur.execute(command)
		if not cur.fetchone():
			say = didyoumeanshow(title)
			if ("Quit" in say):
				return ("Done")
			elif ("Error" in say):
				return ("Error. Title not found to add to play queue.")
			else:
				say = setupnext(say)
				return (say)

	command = 'SELECT State FROM States WHERE Option LIKE \'Queue\''
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]
	writeme = title + ";"
	command = 'DELETE FROM States WHERE Option LIKE \'Queue\''
	cur.execute(command)
	queue = writeme + queue
	name = "queue"
	cur.execute('INSERT INTO States VALUES(?,?)', (name, queue))
	sql.commit()
	title = title.replace("movie.", "The movie ")

	return (title + " will play next from the queue.")

def addfavoritemovie(title):
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	command = 'SELECT * FROM Movies WHERE Movie LIKE \'' + title + '\''
	cur.execute(command)
	if not cur.fetchone():
		#say = findmovie(title)
		say = didyoumeanmovie(title)
		if "Error" not in say:
			command = 'SELECT * FROM Movies WHERE Movie LIKE \'' + say.strip() + '\''
			cur.execute(command)
		else:
			return (say)
	else:
		cur.execute(command)
	try:
		found = cur.fetchone()
		movie = found[0]
		summary = found[1]
		rating = found[2]
		tagline = found[3]
		genre = found[4]
		if ("favorite" not in genre.lower()):
			genre = genre + " favorite"
			director = found[5]
			actors = found[6]
			command = 'DELETE FROM Movies WHERE Movie LIKE \'' + title + '\''
			cur.execute(command)
			cur.execute('INSERT INTO Movies VALUES(?,?,?,?,?,?,?)', (movie, summary, rating, tagline, genre, director, actors))
			sql.commit()

			return (movie + " has been added to the favorites list.")
		else:
			return (movie + " is already in the favorites list. No action taken.")
	except IndexError:
		return ("Error adding " + movie + " to the favorites list.")

def addgenreshow(show, genre):
	command = 'SELECT * FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: " + show + " not found. Check title and try again.")
	cur.execute(command)
	stuff = cur.fetchone()
	TShow = stuff[0]
	summary = stuff[1]
	try:
		genres = stuff[2]
	except Exception:
		genres = ""
	rating = stuff[3]
	duration = stuff[4]
	totalnum = stuff[5]
	if genre in genres:
		return("Error: " + genre + " is already associated with the show " + show)
	genres = genres + " " + genre
	command = 'DELETE FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
	cur.execute(command)
	sql.commit()
	cur.execute('INSERT INTO TVshowlist VALUES(?,?,?,?,?,?)',(TShow, summary, genres, rating, int(duration), int(totalnum)))
	sql.commit()
	return (genre + " has been associated with " + show)

def addgenremovie(movie, genre):
	command = 'SELECT * FROM Movies WHERE Movie LIKE \'' + movie + '\''
	cur.execute(command)
	if not cur.fetchone():
		say = didyoumeanmovie(movie)
		command = 'SELECT * FROM Movies WHERE Movie LIKE \'' + say + '\''
	cur.execute(command)
	stuff = cur.fetchone()
	title = stuff[0]
	summary = stuff[1]
	rating = stuff[2]
	tagline = stuff[3]
	genres = stuff[4]
	director = stuff[5]
	actor = stuff[6]
	if genre in genres:
		return("Error: " + genre + " is already associated with the movie " + movie)
	genres = genres + genre + ';'
	command = 'DELETE FROM Movies WHERE Movie LIKE \'' + movie + '\''
	cur.execute(command)
	sql.commit()
	cur.execute('INSERT INTO Movies VALUES(?,?,?,?,?,?,?)',(title, summary, rating, tagline, genres, director, actor))
	sql.commit()
	return (genre + " successfully associated with the movie " + movie ) 	

def addfavoriteshow(show):
	genre = "Favorite"
	command = 'SELECT * FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
        cur.execute(command)
        if not cur.fetchone():
		say = didyoumeanshow(show)
		if ("Quit" in say):
			return ("Done.")
		elif ("Error" in say):
			return ("Error: " + show + " not found. Check title and try again.")
		else:
			command = 'SELECT * FROM TVshowlist WHERE TShow LIKE \'' + say + '\''
			show = say
        cur.execute(command)
        stuff = cur.fetchone()
        TShow = stuff[0]
        summary = stuff[1]
        try:
                genres = stuff[2]
        except Exception:
                genres = ""
        rating = stuff[3]
        duration = stuff[4]
        totalnum = stuff[5]
        if genre in genres:
                return("Error: " + genre + " is already associated with the show " + show)
        genres = genres + genre + ";"
        command = 'DELETE FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
        cur.execute(command)
        sql.commit()
        cur.execute('INSERT INTO TVshowlist VALUES(?,?,?,?,?,?)',(TShow, summary, genres, rating, int(duration), int(totalnum)))
        sql.commit()
        return (genre + " has been associated with " + show)

def externalcheck():
	try:
		check = str(sys.argv[2])
		return ("Pass")
	except Exception:
		if str(sys.argv[1]) == "addblock":
			return ("Pass")
		return ("Fail")

def titlecheck(title):
	title = title.replace("movie.","")
	title = title.lower()
	check = "fail"
	cur.execute("SELECT Movie FROM Movies")
	mlist = cur.fetchall()
	mvlist = []
	for item in mlist:
		#mvlist.append(str(item[0].lower()))
		if title in item[0].lower():
			check = "pass"
	#if title in mvlist:
		#check = "pass"
	
	cur.execute("SELECT TShow FROM TVshowlist")
	tvlist = cur.fetchall()
	tvxlist = []
	for item in tvlist:
		tvxlist.append(str(item[0].lower()))
	if title in tvxlist:
		check = "pass"
	if "fail" in check:	
		d = enchant.Dict("en_US")
		options = []
		newt = ""
		ccount = 0
		fail = "no"
		for word in title.split(" "):
			if d.check(word) is True:
				newt = newt + word + " "
			else:
				clist = d.suggest(word)
				word = clist[ccount]
				newt = newt + word + " "
				fail = "yes"
		if "yes" in fail:
			print ("Assuming you meant " + newt )
	else:
		newt = title
	return (newt)

def didyoumeanboth(title):
	#title = titlecheck(title).strip()
	movie = title
	movie = movie.replace("movie.","")
	passcheck = ['the', 'and', 'a', 'to', 'of', 'for', 'an', 'on', 'with', '&', 'from']
	found = []
	#darker
	if "Fail" not in externalcheck():
		tshow = movie
		show = movie
		checks = []
		if (" " in show):
			show = show.split(' ')
			for item in show:
				if item.lower() not in passcheck:
					checks.append(item)
		else:
			checks.append(show)
		for item in checks:
			command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'%' + item + '%\''
			cur.execute(command)
			if cur.fetchall():
				cur.execute(command)
				foundme = cur.fetchall()
				for items in foundme:
					if items[0].strip().lower() not in found:
						found.append('movie.' + items[0].strip().lower())
		del checks
	show = title
	tshow = show
        checks = []
        show = show.split(' ')
        for item in show:
                if item.lower() not in passcheck:
                        checks.append(item)
        for item in checks:
                command = 'SELECT TShow FROM TVshowlist WHERE TShow LIKE \'%' + item + '%\''
                cur.execute(command)
                if cur.fetchall():
                        cur.execute(command)
                        foundme = cur.fetchall()
                        for items in foundme:
                                if items[0].strip() not in found:
                                        found.append(items[0].strip())
        if not found:
                return ("Error: " + tshow + ", nor anything close was found in your library.")
        choicecount = 1
        max = int(len(found))
	print ("Did you mean:\n")
        for item in found:
                print (str(choicecount) + ":" + item.replace("movie.","The Movie ") + "\n")
                choicecount = choicecount + 1
        print (str(choicecount) + ": Quit")
        cchecker = 'false'
        while cchecker == 'false':
                try:
                        watchme = int(raw_input('Choice: '))
                        if watchme == max+1:
                                return("Quit.")
                        else:
                                play = found[int(watchme)-1]
                                return (play)
                except TypeError:
                        print ("Error: You must choose one of the available options to proceed.")

def didyoumeanshow(show):
	passcheck = ['the', 'from', 'and', 'a', 'to', 'of', 'for', 'an', 'on', 'with', '&']
	tshow = show
	checks = []
	found = []
	show = show.split(' ')
	for item in show:
		if item.lower() not in passcheck:
			checks.append(item)
	print (tshow + " not found. Did you mean on of the following, perhaps:\n")
	for item in checks:
		command = 'SELECT TShow FROM TVshowlist WHERE TShow LIKE \'%' + item + '%\''
		cur.execute(command)
		if cur.fetchall():
			cur.execute(command)
			foundme = cur.fetchall()
			for items in foundme:
				if items[0].strip() not in found:
					found.append(items[0].strip())
	if not found:
		return ("Error: " + tshow + ", nor anything close was found in your library.")
	choicecount = 1
	max = int(len(found))
	for item in found:
		print (str(choicecount) + ":" + item + "\n")
		choicecount = choicecount + 1
	print (str(choicecount) + ": Quit")
	cchecker = 'false'
	while cchecker == 'false':
		try:
			watchme = int(raw_input('Choice: '))
			if watchme == max+1:
				return("Quit")
			else:
				play = found[int(watchme)-1]
				return (play)
		except TypeError:
			print ("Error: You must choose one of the available options to proceed.")

		
def didyoumeanmovie(movie):
	passcheck = ['the', 'from', 'and', 'a', 'to', 'of', 'for', 'an', 'on', 'with', '&']
        tshow = movie
	show = movie
        checks = []
        found = []
        show = show.split(' ')
        for item in show:
                if item.lower() not in passcheck:
                        checks.append(item)
        print (tshow + " not found. Did you mean on of the following, perhaps:\n")
        for item in checks:
                command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'%' + item + '%\''
                cur.execute(command)
                if cur.fetchall():
                        cur.execute(command)
                        foundme = cur.fetchall()
                        for items in foundme:
                                if items[0].strip() not in found:
                                        found.append(items[0].strip())
        if not found:
                return ("Error: " + tshow + ", nor anything close was found in your library.")
        choicecount = 1
        max = int(len(found))
        for item in found:
                print (str(choicecount) + ":" + item + "\n")
                choicecount = choicecount + 1
        print (str(choicecount) + ": Quit")
        cchecker = 'false'
        while cchecker == 'false':
                try:
                        watchme = int(raw_input('Choice: '))
                        if watchme == max+1:
                                return("Quit")
                        else:
                                play = found[int(watchme)-1]
                                return (play)
                except TypeError:
                        print ("Error: You must choose one of the available options to proceed.")
 
def whatsafterthat():
	check = playmode()
	if "normal" in check:
		name = "queue"
		command = 'SELECT State FROM States WHERE Option LIKE \'' + name + '\''
		cur.execute(command)
		queue = cur.fetchone()
		queue = queue[0]
		queue = queue.split(";")
		if queue[1] == '':
			print ("Generating after that now, sir.")
			furst = queue[0]
			skipthat()
			sayme = whatupnext()
			sayme = sayme.split("we have ")
			sayme = sayme[1]
			sayme = sayme.replace("movie.", "The movie ")
			setupnext(furst)
			furst = furst.replace("movie.", "The movie ")
			return (sayme + " will play after " + furst)
		else:
			sayme = whatupnext()
			sayme = sayme.split("we have ")
			sayme = sayme[1]
			
			upnext = queue[1]
			upnext = upnext.replace("movie.", "The movie ")
			return ("After " + sayme + " we have: " + upnext + ".")

	else:
		return("Sorry, whatsafterthat only currenly supports normal playback.")
	return ("Done.")	

def whatupnext():
	sqlcon = homedir + 'myplex.db'
	sql = sqlite3.connect(sqlcon)
	cur = sql.cursor()
	command = 'SELECT State FROM States WHERE Option LIKE \'Playmode\''
	cur.execute(command)
	playmode = cur.fetchone()
	playmode = playmode[0]

	if (("normal" in playmode) or ("binge." in playmode)):
		queue = openqueue()
		if queue == " ":
			print ("First run situation detected. Taking approprate action.\n")
			queuefix()
			#skipthat()
			queue = openqueue()
		queue = queue.split(';')
		upnext = queue[0]
		upnext = upnext.replace(";", "")
		upnext = upnext.replace("movie.", "The Movie ")
		upnext = upnext.rstrip()
		if "binge." in playmode:
			upnext = playmode.split("binge.")
			upnext = upnext[1].strip()
			upnext = upnext.replace("movie.", "The Movie ")
		playme = upnext
	
		if ('The Movie'  in playme):
			goon = "yes"
		elif ("block." in playme):
			skipthat()
			setplaymode(playme)
			say = whatupnext()
			return (say)
		else:

			playme = playme.strip()
			playme = playme.rstrip()
			try:
				command = 'SELECT Number FROM TVCounts WHERE Show LIKE \'' + playme + '\''
				cur.execute(command)
				thecount = cur.fetchone()
				thecount = thecount[0]
			except Exception:
				thecount = 1
				cur.execute('INSERT INTO TVCounts VALUES(?,?)', (playme, thecount))
				sql.commit()
			if thecount ==0:
				thecount = 1
			epnum = str(thecount)
			command1 = 'SELECT Season, Enum, Episode FROM shows WHERE TShow LIKE \'' + playme + '\' and Tnum LIKE \'' + epnum + '\''
			sqlcon = homedir + 'myplex.db'
			sql = sqlite3.connect(sqlcon)
			cur = sql.cursor()
			cur.execute(command1)
			ep = cur.fetchone()

			ssn = str(ep[0])
			xep = str(ep[1])
			episode = str(ep[2])
			playme = "The TV Show " + playme +" Season " + ssn + " Episode " + xep + ", " + episode
			playme = playme.rstrip()

		upnext = "Up next we have " + playme
	elif ("block." in playmode):
		block = getblockpackage(playmode)
		if ("Random_movie." in block):
			title = block.split("Random_movie.")
			title = title[1]
			title = title.replace(";","")
			title = title.rstrip()
			upnext = "Up next is a random " + title + " movie. Tonights selection is: "
			tnmv = homedir + 'tonights_movie.txt'
			with open(tnmv, "r") as file:
				play = file.read()
			file.close()
			if not play:
				play = suggestmovie(title)
				play = play.split("movie: ")
				play = play[1]
				play = play.split(" sound")
				play = play[0]
				with open(tnmv, "w") as file:
					file.write("movie."+play)
				file.close()
			play = play.replace("movie.", "\nThe Movie ")
			upnext = upnext + play
			#upnext = upnext.replace("movie.", "The movie ")
		elif ("Random_tv." in block):
			title = block.split("Random_tv.")
			title = title[1]
			title = title.replace(";","")
			title = title.rstrip()
			upnext = "Up next is a random " + title + " Show. The current selection is: "
			rdtv = homedir + 'random_tv_chooser.txt'
			with open(rdtv, "r") as file:
				play = file.read()
			file.close()
			if not play:
				play = suggesttv(title.rstrip())
				play = play.split("TV Show ")
				play = play[1]
				play = play.split(" sound")
				play = play[0]
				with open(rdtv, "w") as file:
					file.write(play)
				file.close()
			upnext = upnext + play
			upnext = upnext.replace("movie.", "The movie ")
		else:
			if ("movie." in block):
				episode = block.split("movie.")
				episode = episode[1].rstrip()
				episode = "The Movie " + episode
			else:
				episode = nextep(block)
				block = playmode.replace("block.","")
			upnext = "Up next we have " + episode
			upnext = upnext.replace("For the show ", "")
			upnext = upnext.replace("Up next is ", "")
			upnext = upnext.replace(" we have the", ",")
	elif ("marathon." in playmode):
		show = playmode.split("marathon.")
		show = show[1]
		episode = nextep(show)
		episode = episode.rstrip()
		upnext = "Up next we have " + episode
		upnext = upnext.replace("For the show ", "")
		upnext = upnext.replace(" we have the", ",")


	return upnext

def idtonightsmovie():
	mode = playmode()
	if "block." in mode:
		mode = mode.split("block.")
		mode = mode[1].strip()
		command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
		cur.execute(command)
		blocki = cur.fetchone()[0]
		blocki = blocki.split(';')
		for block in blocki:
				
			if ("Random_movie." in block):
				title = block.split("Random_movie.")
				title = title[1]
				title = title.replace(";","")
				title = title.rstrip()
				tnmv = homedir + "tonights_movie.txt"
				with open(tnmv, "r") as file:
					play = file.read()
				file.close()
				if not play:
					play = suggestmovie(title)
					play = play.split("movie: ")
					play = play[1]
					play = play.split(" sound")
					play = play[0]
					with open(tnmv, "w") as file:
						file.write("movie."+play)
					file.close()
		play = play.replace("movie.","")
		play = "Tonights scheduled film is: " + play
	else:
		play = "No movie currently scheduled."
	return play

def settonightsmovie(movie):
	tnmv = homedir + "tonights_movie.txt"
	command = "SELECT Movie FROM Movies WHERE Movie LIKE \'" + movie + "\'"
	cur.execute(command)
	if not cur.fetchone():
		return ("Error. Movie not found.")
	moview = "movie." + movie.strip()		
	with open(tnmv, "w") as file:
		file.write(moview)
	file.close()
	return ("Tonights movie has been set to " + movie)
		

def nextep(show):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	try:
		command = 'SELECT Number FROM TVCounts WHERE Show LIKE \'' + show + '\''
		cur.execute(command)
		thecount = cur.fetchall()
		thecount = thecount[0]
	except Exception:
		thecount = 1
		cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecount))
		sql.commit()

	if thecount == 0:
		thecount = 1
	try:
		epnum = thecount[0]
	except Exception:
		epnum = thecount
	#epnum = str(epnum)
	command1 = 'SELECT Season, Enum, Episode FROM shows WHERE TShow LIKE \'' + str(show) + '\' and Tnum LIKE \'' + str(epnum) + '\''
	sqlcon = homedir + "myplex.db"
	sql = sqlite3.connect(sqlcon)
	cur = sql.cursor()
	cur.execute(command1)
	ep = cur.fetchone()
	ssn = str(ep[0])
	xep = str(ep[1])
	episode = str(ep[2])
	episode = "For the show " + show + ", Up next is Season " + ssn + ", Episode " + xep + ", " + episode
	episode = episode.rstrip()

	return episode


def removeblock(block):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	say = availableblocks()
	if "none" in block:
		print("Block Package to Remove?")
		print (say + "\n\n")
		block = str(input('Block: '))
	if block in say:
		print ("Removing the " + block + " block now.")
	else:
		return ("Error, block not found to remove. Please try check and try again.")
	bname = block.strip()
	command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
	cur.execute(command)
	sql.commit()
	return ("Block " + block + " has been successfully removed.")

def skipthat():
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	mode = playmode()
	try:
		option = str(sys.argv[2])
		if "normal" in option:
			print ("Skip Enabled")
	except Exception:
		option = ""
	if (("normal" in mode) or ("normal" in option)):
		command = 'SELECT State FROM States WHERE Option LIKE \'Queue\''
		cur.execute(command)
		queue = cur.fetchone()
		queue = queue[0]
		queue = queue.split('\n')
		try:
			check1 = queue[0]
			check1 = check1.replace(';','')
			queueremove('None')
			playme = upnext()
			check2 = playme
			if check1 == check2:
				skipthat()
			else:
				playme = playme.replace("movie.", "The Movie ")
				playme = "The next item in the queue has been set to: " + playme
				return playme
		except IndexError:
			return "No queue to skip."	
	elif ("binge." in mode):

		return ("We are in binge mode. Change playmodes to use this option or add 'normal' to your command to skip what is up next in the queue.")
	else:
		play = upnext()
		consql = homedir + 'myplex.db'
		sql = sqlite3.connect(consql)
		cur = sql.cursor()
		list = getblockpackagelist()
		for item in list:
			item = item.replace(".txt", "")
			if (item in play):
				xitem = item
				yitem = item + ".txt"
				xitem = xitem.replace('.txt','')
				command = 'SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + xitem + '\''
				cur.execute(command)
				binfo = cur.fetchone()
				bname = binfo[0]
				bitems = binfo[1]
				bcount = binfo[2]
				bxitems = bitems.split(';')
				max_count = len(bxitems)
				play = bxitems[bcount]
				bcount = bcount + 1
				if int(bcount) == (int(max_count)-1):
					bcount = 0
					setplaymode("normal")
					print ("Playmode has been set to normal.")
				command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
				cur.execute(command)
				sql.commit()
				cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, bitems, int(bcount)))
				sql.commit()
		say = whatupnext()
		return (say)

def findsomethingelse():
	queue = openqueue()
	Readfiletv = homedir + 'tvshowlist.txt'
	Readfilemov = homedir + 'movielist.txt'
	try:
		queue = queue.split(';')
		queue[0]
		queueremovenofill()
		from random import randint
		playme = randint(1,5)
		if ((playme == 1) or (playme ==5)):
			with open(Readfiletv, "r") as file:
				playfiles = file.readlines()
			file.close()
			min = 0
			max = filenumlines(Readfiletv)
			playc = randint(min,max)
			play = playfiles[playc]
			play = play.rstrip()
			addme = play
			playme = setupnext(addme)

		elif ((playme == 2) or (playme ==4)):
			with open(Readfilemov, "r") as file:
				playfiles = file.readlines()
			file.close()
			min = 0
			max = filenumlines(Readfilemov)
			playc = randint(min,max)
			play = playfiles[playc]
			play = play.rstrip()
			addme = "movie." + play
			playme = setupnext(addme)

			#set this to be whatever you want your wild card to be. 
		elif (playme == 3):
			addme = "The Big Bang Theory"
			playme=setupnext(addme)
			#return (playme)
	except IndexError:
		playme = queuefill()
	return (playme)

def findnewmovie():
	tonightsmovie = homedir + "tonights_movie.txt"
	with open(tonightsmovie, "w") as file:
		file.write("")
	file.close()
	say = whatupnext()
	return(say)
	with open(tonightsmovie, "w") as file:
		file.write("")
	file.close()
	say = whatupnext()
	return(say)


def openqueue():
	name = "queue"
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	command = 'SELECT State FROM States WHERE Option LIKE \'' + name + '\''
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]
	if not queue:
		queue = queuefill()
	return queue

def restartblock(block):
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	if block == "none":
		block = playmode()
		block = block.replace("block.","")
	try:	
		command = 'SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + block + '\''
		cur.execute(command)
		binfo = cur.fetchone()
		bname = binfo[0]
		bitems = binfo[1]
		bcount = "0"
	except TypeError:
		return ("Block not found to restart.")
	else:
		command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
		cur.execute(command)
		sql.commit()
		cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, bitems, int(bcount)))
		sql.commit()

	return ("Done")
def randommovieblock(genre):
	openme = homedir + 'random_movie_block.txt'
	with open(openme, "w") as file:
		file.write("")
	file.close()
	movie1 = suggestmovieblockuse(genre)
	movie2 = suggestmovieblockuse(genre)
	if movie2 == movie1:
		movie2 = suggestmovieblockuse(genre)
	movie3 = suggestmovieblockuse(genre)
	if ((movie2 == movie3) or (movie1 == movie3)):
		movie3 = suggestmovieblockuse(genre)
	say = "I have generated the following " + genre + " movie block: \n" + movie1 + "\n" + movie2 + "\n" + movie3
	movie1 = "movie." + movie1
	movie2 = "movie." + movie2
	movie3 = "movie." + movie3
	movie1 = movie1.rstrip()
	movie2 = movie2.rstrip()
	movie3 = movie3.rstrip()
	mode1 = "randommovieblock"
	mode = "block.randommovieblock"
	addme = movie1 + ";" + movie2 + ";" + movie3 + ";"
	cur.execute('DELETE FROM Blocks WHERE Name LIKE \'' + mode1 + '\'')
	sql.commit()
	cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (mode1, addme, "0"))
	sql.commit()
	cur.execute('DELETE FROM States WHERE Option LIKE \'Playmode\'')
	sql.commit()
	cur.execute('INSERT INTO States VALUES(?,?)', ('Playmode', mode))
	sql.commit()
	return (say)

def suggestmovieblockuse(genre):
	openp = homedir + 'pending_queue.txt'
	from random import randint
	if (genre == "none"):
		readfilemov = homedir + 'movielist.txt'
		with open(readfilemov, "r") as file:
			playfiles = file.readlines()
		file.close()
		min = 0
		max = filenumlines(readfilemov)
		playc = randint(min,max)
		play = playfiles[playc]
		play = play.rstrip()
		addme = "movie." + play
		openp = homedir + 'pending_queue.txt'
		with open (openp,'w') as file:
			file.write(addme)
		file.close()
	else:
		genre = genre.rstrip()
		cur.execute('SELECT Movie FROM Movies WHERE Genre LIKE \'%' + genre + '%\'')
		found = cur.fetchall()
		min = 0
		max = int(len(found))
		playc = randint(min,max)
		play = found[playc]
		play = play[0]
	return play

def suggestmovie(genre):
	link = homedir + 'myplex.db'
	sql = sqlite3.connect(link)
	cur = sql.cursor()
	from random import randint
	if (genre == "none") or (genre == "all"):
		command = 'SELECT Movie from Movies WHERE Genre LIKE \'%favorite%\''
		cur.execute(command)
		mvlist = cur.fetchall()
		if ((int(len(mvlist)) < 9) or (genre == "all")):
			command = 'SELECT Movie FROM Movies'
			cur.execute(command)
			mvlist = cur.fetchall()
		min = 0
		max = int(len(mvlist)-1)
		playc = randint(min,max)
		play = mvlist[playc]
		play = play[0].rstrip()
		#command = 'SELECT Movie from Movies WHERE Movie LIKE\'' + play + '\''
		#cur.execute(command)
		#mvlist = cur.fetchall()
		for mvs in mvlist:
			if mvs[0].lower() == play.lower():
				play = mvs[0]	
		addme = "movie." + play

		command = 'DELETE from States WHERE Option LIKE \'Pending\''
		cur.execute(command)
		sql.commit()
		cur.execute('INSERT INTO States VALUES(?,?)', ('Pending',addme))
		sql.commit()
		
	elif ("rating." in genre):
                rating = genre.split("rating.")
                rating = rating[1].strip()
                command = 'SELECT Movie FROM Movies WHERE Rating LIKE \'' + rating + '\''
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: No Movies found with a " + rating + " rating.")
                else:
                        mlist = cur.fetchall()
                        min = 0
                        max = int(len(mlist)-1)
                        from random import randint
                        mcount = randint(min,max)
                        play = mlist[mcount][0]
                        addme = "movie." + play
			command = 'DELETE from States WHERE Option LIKE \'Pending\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO States VALUES(?,?)', ('Pending',addme))
			sql.commit()
	elif ("actor." in genre):
		rating = genre.split("actor.")
                rating = rating[1].strip()
                command = 'SELECT Movie FROM Movies WHERE Actors LIKE \'%' + rating + '%\''
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: No Movies found starring " + rating + ".")
                else:
                        mlist = cur.fetchall()
                        min = 0
                        max = int(len(mlist)-1)
                        from random import randint
                        mcount = randint(min,max)
                        play = mlist[mcount][0]
                        addme = "movie." + play
			command = 'DELETE from States WHERE Option LIKE \'Pending\''
                        cur.execute(command)
                        sql.commit()
                        cur.execute('INSERT INTO States VALUES(?,?)', ('Pending',addme))
                        sql.commit()

	else:
		genre = genre.rstrip()
		cur.execute('SELECT Movie FROM Movies WHERE Genre LIKE \'%' + genre + '%\'')
		found = cur.fetchall()
		min = 0
		max = int(len(found))
		playc = randint(min,max)
		play = found[playc]
		play = play[0].rstrip()
		addme = "movie." + play
		command = 'DELETE from States WHERE Option LIKE \'Pending\''
		cur.execute(command)
		sql.commit()
		cur.execute('INSERT INTO States VALUES(?,?)', ('Pending',addme))
		sql.commit()

	return "How does the movie: " + play + " sound, Sir?"

def suggesttv(genre):
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	if (genre == "none"):
		readfiletv = homedir + 'tvshowlist.txt'
		
		from random import randint
		with open(readfiletv, "r") as file:
			playfiles = file.readlines()
		file.close()
		min = 0
		max = filenumlines(readfiletv)
		playc = randint(min,max)
		play = playfiles[playc]
		play = play.rstrip()
		addme = play
	elif("rating." in genre):
		rating = genre.split("rating.")
		rating = rating[1].strip()
		command = 'SELECT TShow FROM TVshowlist WHERE Rating LIKE \'' + rating + '\''
		cur.execute(command)
		if not cur.fetchall():
			return("Error: Rating " + rating + " not found in library. Check and try again.")
		else:
			cur.execute(command)
			foundt = cur.fetchall()
                        max = len(foundt)
                        max = int(max) - 1
                        from random import randint
                        pcnt = randint(0, max)
                        play = foundt[pcnt][0]
	elif("duration." in genre):
                rating = genre.split("duration.")
                rating = rating[1].strip()
                command = 'SELECT TShow FROM TVshowlist WHERE Duration LIKE \'' + rating + '\''
                cur.execute(command)
                if not cur.fetchall():
                        return("Error: Duration length " + rating + " not found in library. Check and try again.")
                else:
                        cur.execute(command)
                        foundt = cur.fetchall()
                        max = len(foundt)
                        max = int(max) - 1
                        from random import randint
                        pcnt = randint(0, max)
                        play = foundt[pcnt][0]
	else:
		command = 'SELECT TShow FROM TVshowlist WHERE Genre LIKE \'%' + genre + ';%\''
		cur.execute(command)
		if not cur.fetchall():
			return("Error. Genre: " + genre + " not found. Please try again.")
		else:
			cur.execute(command)
			foundt = cur.fetchall()
			max = len(foundt)
			max = int(max) - 1
			from random import randint
			pcnt = randint(0, max)
			play = foundt[pcnt][0]
	play = play.rstrip()
	command = 'DELETE FROM States WHERE Option LIKE \'Pending\''
	cur.execute(command)
	sql.commit()
	cur.execute('INSERT INTO States VALUES(?,?)', ('Pending',play))
	sql.commit()

	return "How does the TV Show " + play + " sound, Sir?"

def listshows(genre):
	command = 'SELECT TShow from TVshowlist WHERE Genre LIKE \'%' + genre + ';%\''
	cur.execute(command)
	if not cur.fetchall():
		return("Error: " + " No shows were found in the " + genre + " genre.")
	cur.execute(command)
	play = cur.fetchall()
	shows = []
	for item in play:
		shows.append(item[0].strip())
	shows = sorted(shows)
	worklist(shows)	

	return ("Done.")

def listmovies():
	cur.execute("SELECT Movie FROM Movies")
	thelist = cur.fetchall()
	movies = []
	for movie in thelist:
		movies.append(movie[0])
	worklist(movies)

	return ("Done.")
		
def whatispending():
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	command = 'SELECT State FROM States WHERE Option LIKE \'Pending\''
	cur.execute(command)
	if not cur.fetchone():
		return ("Nothing is pending.")
	else:
		cur.execute(command)
		pending = cur.fetchone()
		pending = pending[0].replace("movie.","The Movie ")
		return (pending + " is currently in the pending queue.")
	

def addsuggestion():
	consql = homedir + 'myplex.db'
	sql = sqlite3.connect(consql)
	cur = sql.cursor()
	command = 'SELECT State FROM States WHERE Option LIKE \'Pending\''
	cur.execute(command)
	if not cur.fetchone():
		return ("Nothing is pending.")
	else:
		cur.execute(command)
		pending = cur.fetchone()
		pending = pending[0]
	if pending == "":
		return ("Nothing pending to add.")
	else:

		queueadd(pending)

		pending = pending.replace('movie.', 'The Movie ')
		
		say = pending + " has been added to the queue."
		command = 'DELETE FROM States WHERE Option LIKE \'Pending\''
		cur.execute(command)
		sql.commit()

		return say

def readlist(list):
	for item in list:
		item = item.rstrip()
		try:
			say = say + item + "\n"
		except NameError:
			say = item + "\n"
	say = say.replace('.txt', '')
	return say
def playcheckstop():
	openme = homedir + 'playstatestatus.txt'
	with open(openme, "w") as file:
		file.write("Off")
	file.close()

def playcheckstart():
        openme = homedir + 'playstatestatus.txt'
        with open(openme, "w") as file:
		file.write("On")
        file.close()

try:	
	show = str(sys.argv[1])
	show = show.replace("+"," ")
	if ("addfavoritemovie" in show):
		title = str(sys.argv[2])
		say = addfavoritemovie(title)
	elif ("addfavoriteshow" in show):
		title = str(sys.argv[2])
		say = addfavoriteshow(title)
	elif ("addgenreshow" in show):
		try:
			show = str(sys.argv[2])
			genre = str(sys.argv[3])
			say = addgenreshow(show, genre)
		except Exception:
			say = "Error: A Show and Genre are required to use this command."
	elif ("addgenremovie" in show):
		try:
			movie = str(sys.argv[2])
			genre = str(sys.argv[3])
			say = addgenremovie(movie, genre)
		except Exception:
			say = "Error: Both a Movie and a Show are required to use this command."
	elif ("queueadd" in show):
		addme = str(sys.argv[2])
		say = queueadd(addme)
		#sayx = say + " has been added to the queue."
		#saythat(say)
	elif ("whereat" in show):
		plexlogin()
		nowp = nowplaying()
		say = whereat()
		say = "For " + nowp + "- " + say 
	elif ("listwildcard" in show):
		say = listwildcard()
	elif ("changewildcard" in show):
		try:
			show = str(sys.argv[2])
		except Exception:
			show = "none"
		say = changewildcard(show)
	elif ("idtonightsmovie" in show):
		say = idtonightsmovie()
	elif ("settonightsmovie" in show):
		try:
			movie = str(sys.argv[2])
			say = settonightsmovie(movie)
		except IndexError:
			say = "Error: You must provide a movie to use this command."
	elif ("findnewmovie" in show):
		say = findnewmovie()
	elif ("randommovieblock" in show):
		genre = str(sys.argv[2])
		say = randommovieblock(genre)
	elif ("listclients" in show):
		plexlogin()
		listclients()
		say = ""
	elif ("changeclient" in show):
		plexlogin()
		say = changeclient()
	elif ("stopplay" in show):
		plexlogin()
		stopplay()
		say = "Playback has been stopped. A new program will start unless you have already stopped playstatus.py"
	elif ("pauseplay" in show):
		plexlogin()
		pauseplay()
		say = "Playback has been paused."
	elif (("skipahead" in show) and ("series" not in show)):
		plexlogin()
		say = skipahead()
	elif (("skipback" in show) and ("series" not in show)):
		plexlogin()
		say = skipback()
	elif ("playcheckstart" in show):
		playcheckstart()
		say = "Playback State Checking has been Enabled."
	elif ("playcheckstop" in show):
		playcheckstop()
		say = "Playback State Checking has been Stopped."
	elif ("playchecksleep" in show):
		openme = homedir + 'playstatestatus.txt'
		with open(openme, "w") as file:
				file.write("Sleep")
		file.close()
		say = "Playback State Checking will stop, and the system will sleep when the current program ends. Be well, Sir."
	elif ("queueshow" in show):
		say = queueget()
		#saythat(say)
	elif ("queuefix" in show):
		say = queuefix()
	elif ("queueremove" in show):
		try:
			item = str(sys.argv[2])
		except IndexError:
			item = "None"
		name = "queue"
		command = 'SELECT State FROM States WHERE Option LIKE \'' + name + '\''
		cur.execute(command)
		queue = cur.fetchone()
		queue = queue[0]
		if item == "None":
			say = upnext()
			queueremove('None')
			say = say + " has been removed from the queue."
		else:
			if item in queue:
				queueremove(item)
				say = item + " has been removed from the queue."
			else:
				say = item + " not found in queue to remove."
	elif ("whatupnext" in show):
		say = whatupnext()
	elif ("whatsafterthat" in show):
		say = whatsafterthat()
	elif ("startnextprogram" in show):
		openme = homedir + 'playstatestatus.txt'
		with open(openme, "r") as file:
			checkme = file.read()
		file.close()
		if "On" in checkme:
			playcheckstop()
		plexlogin()
		show = upnext()
		say = playshow(show)
		if (("block." or "binge.") not in say):
			skipthat()
		say = say + "\n"
		if "On" in checkme:
			time.sleep(5)
			playcheckstart()
	elif ("skipthat" in show):
		say = skipthat()
		if "No queue to skip." in say:
			say = queuefill()
		#saythat(say)
	elif ("seriesskipback" in show):
		try:
			show = str(sys.argv[2])
			say = seriesskipback(show)
		except Exception:
			sayx = whatupnext()
			
			pmode = playmode()
			try:
				if ("normal" not in pmode):
					say = sayx.split('we have ')
				else:
					say = sayx.split("The TV Show ")
				say = say[1]
				if ("normal" not in pmode):
					say = say.split(', Season')
				else:
					say = say.split(" Season ")
				show = say[0]
			except Exception:
				say = "A movie is currently up next, and no show was specified. No action has been taken.\n"
			if ('A movie' not in say):
				say = seriesskipback(show)
			
	elif ("seriesskipahead" in show):
                try:
                        show = str(sys.argv[2])
			say = seriesskipahead(show)
                except Exception:
                        sayx = whatupnext()

                        pmode = playmode()

                        try:
                                if ("normal" not in pmode):
                                        say = sayx.split('we have ')
                                else:
                                        say = sayx.split("The TV Show ")
                                say = say[1]
                                if ("normal" not in pmode):
                                        say = say.split(', Season')
                                else:
                                        say = say.split(" Season ")
                                show = say[0]
                        except Exception:
                                say = "A movie is currently up next, and no show was specified. No action has been taken.\n"
			if ('A movie' not in say):
				say = seriesskipahead(show)
	
	elif ("findsomethingelse" in show):
		say = findsomethingelse()
		#queue = queue.split(';')
	elif ("suggestmovie" in show):
		try:
			genre = str(sys.argv[2])
		except IndexError:
			genre = "none"
		say = suggestmovie(genre)
		#saythat(say)
	elif ("suggesttv" in show):
		try:
			genre = str(sys.argv[2])
		except IndexError:
			genre = "none"
		say = suggesttv(genre)
		#saythat(say)
	elif ("listshows" in show):
		try:
			genre = str(sys.argv[2])
			say = listshows(genre)
		except IndexError:
			show = availableshows()
			say = show
	elif ("listepisodes" in show):
		try:
			show = str(sys.argv[2])
			say = listepisodes(show)
		except IndexError:
			say = "Specificy a show to use this command."
	elif ("listmovies" in show):
		say = listmovies()

	elif ("addsuggestion" in show):
		say = addsuggestion()
		#saythat(say)
	elif ("whatispending" in show):
		say = whatispending()
		#saythat(say)
	elif ("availableblocks" in show):
		try:
			say = availableblocks()
			say = "The Following Blocks are available:\n" + say
		except NameError:
			say = "You must first create a block to use this command. Use 'addblock' for more information."

	elif ("restartblock" in show):
		try:
			block = str(sys.argv[2])
		except Exception:
			block = "none"
		say = restartblock(block)
	elif ("explainblock" in show):
		block = str(sys.argv[2])
		say = explainblock(block)
		#saythat(say)
	elif ("addblock" in show):
		try:
			name = str(sys.argv[2])
		except Exception:
			name = "none"
		try:
			title = str(sys.argv[3])
		except Exception:
			title = "none"

		say = addblock(name, title)
	elif ("removeblock" in show):
		try:
			block = str(sys.argv[2])
		except Exception:
			block = "none"
		say = removeblock(block)
		
	elif ("addtoblock" in show):
		try:
			block = str(sys.argv[2])
			item = str(sys.argv[3])
		except Exception:
			say = "You must provide both a block name and movie/show title to use this command."
		say = addtoblock(block, item)
	elif ("removefromblock" in show):
		try:
			block = str(sys.argv[2])
			item = str(sys.argv[3])
			say = removefromblock(block,item)
		except Exception:
			say = "You must provide both a block name and movie/show title to use this command."
	
	elif ("setupnext" in show):
		title = str(sys.argv[2])
		say = setupnext(title)
	elif ("featuredone" in show):
		plexlogin()
		show = upnext()
		say = playshow(show)
		skipthat()
		say = "Sir, the last feature has ended, starting " + say
		
	elif ("blockplay" in show):
		plexlogin()
		play = str(sys.argv[2])
		say = playblockpackage(play)
	elif ("nextep" in show)and ("setnextep" not in show):
		show = str(sys.argv[2])
		say = nextep(show)

	elif ("getplaymode" in show):
		say = playmode()
	elif ("setplaymode" in show):
		try:
			mode = str(sys.argv[2])
		except Exception:
			mode = show.split("setplaymode ")
			mode = mode[1]
		setplaymode(mode)
		say = whatupnext()
		say = say.replace("is active.", "is now active.")

	elif ("epdetails" in show):
		try:
			show = str(sys.argv[2])
			try:
				season = str(sys.argv[3])
				episode = str(sys.argv[4])
				say = epdetails(show, season, episode)
			except Exception:
				command = 'SELECT Number FROM TVCounts WHERE Show LIKE \'' + show + '\''
				cur.execute(command)
				if not cur.fetchone():
					command = 'SELECT Summary FROM shows WHERE TShow LIKE \'' + show + '\' AND Season = 1 AND Enum = 1'
				else:
					cur.execute(command)
					Tnum = cur.fetchone()[0]
					Tnum = int(Tnum)
					command = "SELECT Summary FROM shows WHERE TShow LIKE \'" + show + "\' AND Tnum = " + str(Tnum)
				presay = nextep(show)
				cur.execute(command)
				say = presay + "\n" + cur.fetchone()[0]
				if len(say) > 350:
					say = say[:350] + " ..."
		except IndexError:
			say2 = "Assuming you ment the next up show or movie.\n"
			unext = upnext()
			if ("block." in unext):
				block = unext.split('block.')[1].strip()
				command = 'SELECT Items, Count FROM Blocks WHERE Name LIKE \'' + block + '\''
				cur.execute(command)
				found = cur.fetchone()
				items = found[0]
				count = found[1]
				items = items.split(';')
				item = items[int(count)]
				command = 'SELECT Number FROM TVCounts WHERE Show LIKE \'' + item + '\''
                                cur.execute(command)
                                if not cur.fetchone():
                                        command = 'SELECT Summary FROM shows WHERE TShow LIKE \'' + item + '\' AND Season = 1 AND Enum = 1'
                                else:
                                        cur.execute(command)
                                        Tnum = cur.fetchone()[0]
                                        Tnum = int(Tnum)
                                        command = "SELECT Summary FROM shows WHERE TShow LIKE \'" + item + "\' AND Tnum = " + str(Tnum)
			elif ("movie." in unext):
				command = 'SELECT Summary FROM Movies WHERE Movie LIKE \'' + unext.split('movie.')[1].strip() + '\''
			else:
				command = 'SELECT Summary FROM shows WHERE TShow LIKE \'' + unext.strip() + '\''
			cur.execute(command)
			say3 = cur.fetchone()[0] + " ..."
			wsay = whatupnext()
			if len(say3) > 350:
				say3 = say3[:350] + " ..."
			wsay = whatupnext()
			say = say2 + "\n" + wsay + "\n" + say3
	elif ("moviedetails" in show):
		movie = str(sys.argv[2])
		say = moviedetails(movie)
	elif ("showdetails" in show):
		show = str(sys.argv[2])
		say = showdetails(show)
	elif ("findmovie" in show):
		movie = str(sys.argv[2])
		say = findmovie(movie)
	elif ("findshow" in show):
		show = str(sys.argv[2])
		say = findshow(show)
	elif ("setnextep" in show):
		show = str(sys.argv[2])
		season = str(sys.argv[3])
		episode = str(sys.argv[4])
		say = setnextep(show, season, episode)

	elif "nowplaying" in show:
		say = nowplaying()

	elif "moviegenres" in show:

		say = availgenremovie()

	elif "tvgenres" in show:
		xshowlist = availgenretv()
		xshowlist = sorted(xshowlist)
                worklist(xshowlist)
		say = "Done."
	elif "tvratings" in show:
		say = avalratingtv()
	elif "tvstudios" in show:
		say = availstudiotv()
		say = readlist(say)
	elif "listtvstudio" in show:
		studio = str(sys.argv[2])
		say = listtvstudio(studio)
		say = readlist(say)
	elif (("whereleftoff" in show) and ("play" not in show)):
		try:
			item = str(sys.argv[2])
			say = whereleftoff(item)
			if (("block." not in item) and ("Error" not in str(say))):
				say = "You left off at minute " + str(say) + "."
		except IndexError:
			say = "Error. You must specify an item to use this command."
	elif (("playwhereleftoff" in show) or ("resumeplay" in show)):
		try:
			openme = homedir + 'playstatestatus.txt'
			with open(openme, "r") as file:
				checkme = file.read()
			file.close()
			if "On" in checkme:
				playcheckstop()
			item = str(sys.argv[2])
			say = playwhereleftoff(item)
			time.sleep(5)
			if "On" in checkme:
				playcheckstart()
		except IndexError:
			say = "Error. You must specify a movie or show to use this command."

	elif "mtagline" in show:
		try:
			movie = str(sys.argv[2])
			say = movietagline(movie)
		except IndexError:
			say = "Error: You  muist specify a movie to use this command."
	elif "mrating" in show:
		try:
                        movie = str(sys.argv[2])
                        say = movierating(movie)
                except IndexError:
                        say = "Error: You  muist specify a movie to use this command."
	elif "msummary" in show:
                try:
                        movie = str(sys.argv[2])
                        say = moviesummary(movie)
                except IndexError:
                        say = "Error: You  muist specify a movie to use this command."
	elif "taglinegame" in show:
		say = movietlgame_intro()
	elif (("muteaudio" in show) and ("unmute" not in show)):
		muteaudio()
		say = "Audio has been muted."
	elif "unmuteaudio" in show:
		unmuteaudio()
		say = "Audio has been restored."
	elif ("lowaudio" in show):
		lowaudio()
		say = "Audio has been set to 25%"
	elif ("mediumaudio" in show):
		mediumaudio()
		say = "Audio has been set up 50%"
	elif ("highaudio" in show):
		highaudio()
		say = "Audio has been set up 75%"
	elif ("maxaudio" in show):
		maxaudio()
		say = "Audio has been set to 100%"
	elif ("titlecheck" in show):
		try:
			title = str(sys.argv[2])
			say = titlecheck(title)
			
		except IndexError:
			say = "Error."
	#marker
	else:
		plexlogin()
		show = mediachecker(show)
		openme = homedir + 'playstatestatus.txt'
                with open(openme, "r") as file:
                        checkme = file.read()
                file.close()
                if "On" in checkme:
                        playcheckstop()
		try:
			season = str(sys.argv[2])
			episode = str(sys.argv[3])
			say = playspshow(show, season, episode)
		
		except IndexError:
				
			say = playshow(show)
                if "On" in checkme:
			time.sleep(5)
                        playcheckstart()
	print (say)
except IndexError:
	show = "We're Sorry, but either that command wasn't recognized, or no input was received. Please try again."  
 
	print (show)
