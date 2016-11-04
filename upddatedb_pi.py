import urllib3
import subprocess
import requests
import time
import os
import sys
import sqlite3
import platform
#top

global pcount
global TVGET
global LOGGEDIN
try:
	input = raw_input
except NameError:
	pass

MYDB = homedir + "myplex.db"
http = urllib3.PoolManager()

sql = sqlite3.connect(MYDB)
cur = sql.cursor()

def getsections():
	plexlogin()
	xlibrary = plex.library.sections()
	foundsect = []
	print ("The Following Sections are available off your server.")
	for lib in xlibrary:
		print lib.title
		foundsect.append(lib.title)
	return foundsect

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
		except Exception:
			print ("Local Variables not set. Run setup to use local access.")
		from plexapi.myplex import MyPlexAccount
		try:
			LOGGEDIN
		except Exception:
			try:
				from plexapi.server import PlexServer
				baseurl = 'http://' + PLEXSERVERIP + ':' + PLEXSERVERPORT
				plex = PlexServer(baseurl)
			except Exception:
				print ("Local Fail. Trying cloud access.")
				user = MyPlexAccount.signin(PLEXUN,PLEXPW)
				plex = user.resource(PLEXSVR).connect()
			client = plex.client(PLEXCLIENT)
			LOGGEDIN = "YES"
	except IndexError:
		print ("Error getting necessary plex api variables. Run system_setup.py.")

def getmovies():
	mcheck = "fail"
	command = "SELECT setting FROM settings WHERE item LIKE \"MOVIEGET\""
	cur.execute(command)
	if not cur.fetchone():
		mcheck = "fail"
	else:
		cur.execute(command)
		MOVIEGET = cur.fetchone()[0]
		if "http" in MOVIEGET:
			cur.execute("DELETE FROM settings WHERE item LIKE \"MOVIEGET\"")
			sql.commit()
		else:
			mcheck = "pass"
	if "fail" in mcheck:
		print ("We need to update your settings to use the new movieget function. Input the name of the section that is your \"Movies\" section.")
		foundsect = getsections()
		MOVIEGET = str(input('Enter Section Name: '))
		MOVIEGET = MOVIEGET.strip()
		if MOVIEGET in foundsect:
			print (MOVIEGET.strip())
			cur.execute("INSERT INTO settings VALUES (?,?)",("MOVIEGET",MOVIEGET))
			sql.commit()
		else:
			print ("Error: " + MOVIEGET + " not found as an available section in your library.")
	else:
		print ('Using the following movie library: ' + MOVIEGET)
	plexlogin()
	movies = []
	mlist = plex.library.section(MOVIEGET)
	mxlist = mlist.search("")
	count = 0
	xnum = int(len(mxlist)-1)
	for video in mxlist:
		try:
			name = str(video.title)
		except Exception:
			name = video.title
			name = name.encode("utf8")
			name = str(name)
		name = name.replace("'","''")
		summary = video.summary
		try:
			summary = str(summary)
		except Exception:
			summary = summary.encode("ascii", "ignore")
		rating = str(video.contentRating)
		try:
			tagline = str(video.tagline)
		except Exception:
			try:
				tagline = tagline.decode("ascii", "ignore")
			except Exception:
				tagline = ""
		tagline = tagline.replace("'","''")
		agenre = video.genres
		gcmd = "SELECT Genre FROM backupmovies WHERE Movie LIKE \"" + name + "\""
		cur.execute(gcmd)
		if not cur.fetchone():
			gcheck = []
		else:
			cur.execute(gcmd)
			gcheck = cur.fetchone()[0]
			gcheck = gcheck.split(' ')

		for item in agenre:
			if item == " ":
				pass
			elif (item not in gcheck):
				try:
					bgenre = bgenre + " " + item.tag
				except NameError:
					bgenre = item.tag
		try:
			bgenre
		except NameError:
			bgenre = ""
		for item in gcheck:
			if item == " ":
				pass
			elif ((item not in agenre) and (item not in bgenre)):
				try:
					bgenre = bgenre + " " + item.strip()
				except NameError:
					bgenre = item.strip()
		bgenre = bgenre.strip()

		directors = video.directors
		for dt in directors:
			try:
				xdt = xdt + " " + dt.tag
			except NameError:
				xdt = dt.tag
		try:
			directors = xdt
			del xdt
		except Exception:
			directors = ""
		try:
			directors = str(directors)
		except Exception:
			directors = str(directors.encode("ascii", "ignore"))

		actors = video.roles
		for act in actors:
			try:
				xact = xact + " " + act.tag
			except NameError:
				xact = act.tag
		try:
			bactors = xact
			del xact
		except Exception:
			bactors = ""
		try:
			bactors = str(bactors)
		except Exception:
			bactors = str(bactors.encode("ascii", "ignore"))
		try:
			cur.execute('SELECT * FROM Movies WHERE Movie LIKE \'' + name + '\'')
			if not cur.fetchone():
				cur.execute('INSERT INTO Movies VALUES(?, ?, ?, ?, ?, ?, ?)', (name, summary, rating, tagline, bgenre, directors, bactors))
				sql.commit()
		except IndexError:
			print ("\nError adding " + name)
			with open(PROBLEMS, 'a') as file:
				file.write(name.decode("ascii", "ignore") + " " + bactors + "\n")
			file.close()
		progress(xnum)
		del bgenre
	clearprogress()
	print ("\nDone.")

def getgenres(show):
	global TVGET
	command = "SELECT setting FROM settings WHERE item LIKE \"TVGENREFIX\""
	cur.execute(command)
	if not cur.fetchone():
		cur.execute("SELECT setting FROM settings WHERE item LIKE \"PLEXSERVERIP\"")
		wlink = cur.fetchone()[0]
		cur.execute("SELECT setting FROM settings WHERE item LIKE \"PLEXSERVERPORT\"")
		wip = cur.fetchone()[0]
		slink = "http://" + wlink + ":" + wip + "/library/sections/"
		response = http.urlopen('GET', slink, preload_content=False).read()
		response = str(response)
		response = response.split("Directory allowSync=")
		#print ("The Following Sections are available off your server.")
		sctsn = []
		for item in response:
			try:
				name = item
				section = item
				name = name.split("title=\"")
				name = name[1]
				name = name.split("\"")
				name = name[0]

				section = section.split("key=\"")
				section = section[1]
				section = section.split("\"")
				section = section[0]

				link = "http://" + wlink + ":" + wip + "/library/sections/" + section + "/all/"
				sctsn.append(link)
				if name == TVGET:
					TVGENREFIX = link
			except IndexError:
				pass
		print TVGENREFIX
		if TVGENREFIX.strip() not in sctsn:
			Print ("Error: Invalid Selection Choice. Alternate Method Will Fail!")
		else:
			cur.execute("INSERT INTO settings VALUES (?,?)",("TVGENREFIX",TVGENREFIX))
			sql.commit()
	cur.execute(command)
	TVGENREFIX = cur.fetchone()[0]
	response = http.urlopen('GET', TVGENREFIX, preload_content=False).read()
	response = str(response)
	shows = response.split('<Directory ratingKey=')
	counter = 1
	xnum = int(len(shows))-1
	while counter <= int(len(shows)-1):
		xshow = shows[counter]
		genres = xshow	
		title = xshow
		title = title.split('title="')
		title = title[1]
		title = title.split('"')
		title = title[0]
		
		title = title.replace('&apos;','\'')
		title = title.replace('&amp;','&')
		title = title.replace('?','')
		title = title.replace('/',' ')
		title = title.replace("&#39;","'")	
		if (title == show):
			genres = genres.split("<Genre tag=\"")
			try:
				genre = genres[1]
			except IndexError:
				genre = "none"
			try:
				genre2 = genres[2]
				genre2 = genre2.split('" />')
				genre2 = genre2[0]
			except IndexError:
				genre2 = "none"
			try:
				genre3 = genres[3]
				genre3 = genre3.split('" />')
				genre3 = genre3[0]
			except IndexError:
				genre3 = "none"
			genre = genre.split('" />')
			
			genre = genre[0] + ";" + genre2 + ";" + genre3 + ";"
			genre = genre.replace('none;','')
			genre = genre.split(";")
			return genre
		counter = counter + 1
	return ("")

def getshows():
	global TVGET
	tcheck = "fail"
	command = "SELECT setting FROM settings WHERE item LIKE \"TVGET\""
	cur.execute(command)
	if not cur.fetchone():
		tcheck = "fail"
	else:
		cur.execute(command)
		TVGET = cur.fetchone()[0]
		if "http" in TVGET:
			cur.execute("DELETE FROM settings WHERE item LIKE \"TVGET\"")
			sql.commit()
		else:
			tcheck = "pass"
	if "fail" in tcheck:
		print ("We need to update your settings to use the new tvget function. Input the name of the section that is your \"TV Shows\" section.")
		foundsect = getsections()
		TVGET = str(input('Enter Section Name: '))
		TVGET = TVGET.strip()
		if TVGET in foundsect:
			print (TVGET.strip())
			cur.execute("INSERT INTO settings VALUES (?,?)",("TVGET",TVGET))
			sql.commit()
		else:
			print ("Error: " + TVGET + " not found as an available section in your library.")
	else:
			print ('Using the following TV Show library: ' + TVGET)	
	plexlogin()
	tlist = plex.library.section(TVGET)
	tvlist = tlist.search("")
	xnum = int(len(tvlist))-1
	for show in tvlist:
		name = str(show.title)
		summary = show.summary
		summary = str(summary.encode('ascii','ignore')).strip()
		rating = str(show.contentRating)
		rating = rating.replace("__NA__","NA")
		duration =  int(show.duration)/60000
		agenre = show.genres
		try:
			agenre = str(agenre)
			if agenre == "__NA__":
				agenre = ""
				#print ("Genre Get Failed. Trying alternate method")
				agenre = getgenres(name)
		except IndexError:
			print ("Genre Get Failed.")
			agenre = getgenres(name)
		gcmd = "SELECT Genre FROM backshowlist WHERE TShow LIKE \"" + name + "\""
		cur.execute(gcmd)
		if not cur.fetchone():
			gcheck = []
		else:
			cur.execute(gcmd)
			gcheck = cur.fetchone()[0]
			gcheck = gcheck.replace(";"," ")
			gcheck = gcheck.split(' ')
		for item in agenre:
			if ((item == " ") or (item == "")):
				pass
			elif (item not in gcheck):
				try:
					bgenre = bgenre + " " + item
				except NameError:
					bgenre = item
		try:
			str(bgenre)
		except NameError:
			bgenre = ""
		for item in gcheck:
			if item == " ":
				pass
			elif (item not in bgenre):
				try:
					bgenre = bgenre + " " + item.strip()
				except NameError:
					bgenre = item.strip()
		bgenre = bgenre.strip()
		totalnum = int(show.leafCount)
		cur.execute("SELECT * FROM TVshowlist WHERE TShow LIKE\"" + name + "\"")
		if not cur.fetchone():
			cur.execute("INSERT INTO TVshowlist VALUES (?,?,?,?,?,?)",(name,summary,bgenre,rating,duration,totalnum))
			sql.commit()
			
		progress(xnum)
		del bgenre
	clearprogress()

def getcustom(section):
	if ("preroll" in section.lower()):
		cur.execute("CREATE TABLE IF NOT EXISTS prerolls(name TEXT, duration INT)")
		sql.commit()
		mcheck = "fail"
		command = "SELECT setting FROM settings WHERE item LIKE \"PREROLLPART\""
		cur.execute(command)
		if not cur.fetchone():
			mcheck = "fail"
		else:
			cur.execute(command)
			PREROLLPART = cur.fetchone()[0]
			if "http" in PREROLLPART:
				cur.execute("DELETE FROM settings WHERE item LIKE \"PREROLLPART\"")
				sql.commit()
			else:
				mcheck = "pass"
		if "fail" in mcheck:
			print ("We need to update your settings to use the new preroll get function. Input the name of the section that is your \"Pre Rolls\" section.")
			foundsect = getsections()
			PREROLLPART = str(input('Enter Section Name: '))
			PREROLLPART = PREROLLPART.strip()
			if PREROLLPART in foundsect:
				print (PREROLLPART.strip())
				cur.execute("INSERT INTO settings VALUES (?,?)",("PREROLLPART",PREROLLPART))
				sql.commit()
			else:
				print ("Error: " + PREROLLPART + " not found as an available section in your library.")
		else:
			print ('Using the following Preroll library: ' + PREROLLPART)
		USEME = PREROLLPART
		USETABLE = "prerolls"
	elif ("commercial" in section.lower()):
		cur.execute("CREATE TABLE IF NOT EXISTS commercials(name TEXT, duration INT)")
		sql.commit()
		mcheck = "fail"
		command = "SELECT setting FROM settings WHERE item LIKE \"COMPART\""
		cur.execute(command)
		if not cur.fetchone():
			mcheck = "fail"
		else:
			cur.execute(command)
			COMPART = cur.fetchone()[0]
			if "http" in COMPART:
				cur.execute("DELETE FROM settings WHERE item LIKE \"COMPART\"")
				sql.commit()
			else:
				mcheck = "pass"
		if "fail" in mcheck:
			print ("We need to update your settings to use the new Commercial get function. Input the name of the section that is your \"Commercials\" section.")
			foundsect = getsections()
			COMPART = str(input('Enter Section Name: '))
			COMPART = COMPART.strip()
			if COMPART in foundsect:
				print (COMPART.strip())
				cur.execute("INSERT INTO settings VALUES (?,?)",("COMPART",COMPART))
				sql.commit()
			else:
				print ("Error: " + COMPART + " not found as an available section in your library.")
		else:
			print ('Using the following Commercial library: ' + COMPART)
		USEME = COMPART
		USETABLE = "commercials"
	elif ("custom." in section.lower()):
		section = section.lower()
		section = section.replace("custom.","").strip()
		item = "CUSTOM_" + section
		cur.execute("CREATE TABLE IF NOT EXISTS " + item + "(name TEXT, duration INT, type TEXT)")
		sql.commit()
		command = "SELECT setting FROM settings WHERE item LIKE \"" + item + "\""
		mcheck = "fail"
		cur.execute(command)
		if not cur.fetchone():
			mcheck = "fail"
		else:
			cur.execute(command)
			COMPART = cur.fetchone()[0]
			if "http" in COMPART:
				cur.execute("DELETE FROM settings WHERE item LIKE \"" + item + "\"")
				sql.commit()
			else:
				mcheck = "pass"
		if "fail" in mcheck:
			print ("We need to update your settings to use the new Custom get function. Input the name of the section that is your \"" + item + "\" section.")
			foundsect = getsections()
			COMPART = str(input('Enter Section Name: '))
			COMPART = COMPART.strip()
			if COMPART in foundsect:
				print (COMPART.strip())
				cur.execute("INSERT INTO settings VALUES (?,?)",(item,COMPART))
				sql.commit()
			else:
				print ("Error: " + COMPART + " not found as an available section in your library.")
		else:
			print ('Using the following Custom library: ' + COMPART)
		USEME = COMPART
		USETABLE = item
        plexlogin()
	mlist = plex.library.section(USEME)
	mxlist = mlist.search("")
        count = 0
        xnum = int(len(mxlist)-1)
        for video in mxlist:
		try:
			name = str(video.title)
		except Exception:
			name = video.title
			name = name.encode("utf8")
			name = str(name)
		name = name.replace("'","''")
		duration = int(video.duration)/1000
		cur.execute("SELECT * FROM " + USETABLE + " WHERE name LIKE \"" + name + "\"")
		if not cur.fetchone():
			if (("prerolls" in USETABLE) or ("commercials" in USETABLE)):
				cur.execute("INSERT INTO " + USETABLE + " VALUES (?,?)",(name, duration))
				sql.commit()
				#print ("Found and added: " + name + ".")
			elif ("CUSTOM_" in USETABLE):
				cur.execute("INSERT INTO " + USETABLE + " VALUES (?,?,?)",(name, duration, USEME))
				sql.commit()
				#print ("Found and added: " + name + ".")
		progress(xnum)
	clearprogress()
	print ("Done.")

def progress(num):
        num = int(num)
        global pcount
        try:
		pcount
        except NameError:
		pcount = 0 
        perc = round((float(pcount) / float(num)) * 100, 1)
        sys.stdout.write("\r" + str(perc) + "%")
        sys.stdout.flush()
	pcount = pcount + 1

def clearprogress():
        global pcount
        pcount = 0

def startupactionmovie():
        command = "python " + homedir + "system.py backupmoviedb"
        os.system(command)
        cur.execute("DELETE FROM Movies")
        sql.commit()
        print ("Movie Table purged and ready for data.")

def startupactiontv():
	command = "python " + homedir + "system.py backuptvdb"
        os.system(command)
        cur.execute("DELETE FROM TVshowlist")
        sql.commit()
        print ("TV Table purged and ready for data.")

cur.execute('CREATE TABLE IF NOT EXISTS Movies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
sql.commit()
cur.execute('CREATE TABLE IF NOT EXISTS TVshowlist(TShow TEXT, Summary TEXT, Genre TEXT, Rating TEXT, Duration INT, Totalnum INT)')
sql.commit()

print ("Database update starting...\n")

try:
	if ("movie" in str(sys.argv)):
		tpe = "movie"
		startupactionmovie()
		getmovies()
	elif ("shows" in str(sys.argv)):
		tpe = "tv"
		startupactiontv()
		getshows()
	elif ("prerolls" in str(sys.argv)):
		tpe = "prerolls"
		getcustom("prerolls")
	elif ("commercials" in str(sys.argv)):
		tpe = "commercials"
		getcustom("commercials")
	elif ("custom." in str(sys.argv)):
		item = str(sys.argv[1])
		getcustom(item)
	elif("all" in str(sys.argv).lower()):
		tpe = "both"
		startupactionmovie()
		getmovies()
		startupactiontv()
		getshows()
except KeyboardInterrupt:
	print ("Cancel request received. Restoring tables.")
	if (("movie" in tpe) or ("both" in tpe)):
		cmd = "python " + homedir + "system.py restoremoviedb"
		os.system(cmd)
	elif (("show" in tpe) or ("both" in tpe)):
		cmd = "python " + homedir + "system.py restoretvdb"
		os.system(cmd)
	print("Cancelled.")
