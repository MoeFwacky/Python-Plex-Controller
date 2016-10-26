import urllib3
import subprocess
import requests
import time
import os
import sys
import sqlite3
import platform
#top

try:
	input = raw_input
except NameError:
	pass

global favtv
global favmve
global tvgenres
global moviegenres
global pcount

favtv = []
favmve = []
tvgenres = []
moviegenres = []

MYDB = homedir + "myplex.db"
http = urllib3.PoolManager()

sql = sqlite3.connect(MYDB)
cur = sql.cursor()

FIXME = homedir + "fixme.txt"
PROBLEMS = homedir + "problems.txt"
with open (PROBLEMS, "w") as file:
	file.write('')
file.close()

ostype = platform.system()

cur.execute("SELECT setting FROM settings WHERE item LIKE \"PLEXSERVERIP\"")
wlink = cur.fetchone()[0]
cur.execute("SELECT setting FROM settings WHERE item LIKE \"PLEXSERVERPORT\"")
wip = cur.fetchone()[0]

def getsections():
        slink = "http://" + wlink + ":" + wip + "/library/sections/"
        response = http.urlopen('GET', slink, preload_content=False).read()
        response = str(response)
        response = response.split("Directory allowSync=")
        print ("The Following Sections are available off your server.")
        for item in response:
                name = item
                section = item
                try:
                        name = name.split("title=\"")
                        name = name[1]
                        name = name.split("\"")
                        name = name[0]

                        section = section.split("key=\"")
                        section = section[1]
                        section = section.split("\"")
                        section = section[0]

                        link = "http://" + wlink + ":" + wip + "/library/sections/" + section + "/all/"
                        print ("Name: " + name + "\nSection: " + section + "\nLink: " + link)
                except IndexError:
                        pass

cur.execute('CREATE TABLE IF NOT EXISTS settings(item TEXT, setting TEXT)')
sql.commit()

command = 'SELECT setting FROM settings WHERE item LIKE \'TVPART\''
cur.execute(command)
if not cur.fetchone():
	print ("Looks like you have never run the update DB script. Getting necessary links now.")
	#Example: http://192.168.1.134:32400/library/metadata/\n")
	#TVPART = str(input('Link:'))
	TVPART = "http://" + wlink + ":" + wip + "/library/metadata/"
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVPART",TVPART.strip()))
	sql.commit()
	print (TVPART + " has been added to the settings table. Moving on.")
else:
	cur.execute(command)
	test2 = cur.fetchone()[0]
	TVPART = test2

command = 'SELECT setting FROM settings WHERE item LIKE \'TVGET\''
cur.execute(command)
if not cur.fetchone():
	getsections()
	print ("Enter the link to your TV show tree.\nExample: http://192.168.1.134:32400/library/sections/1/all/ \n")
	TVGET = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVGET",TVGET.strip()))
	sql.commit()
	print (TVGET + " has been added to the settings table. Moving on.")
else:
	cur.execute(command)
	test1 = cur.fetchone()[0]
	TVGET = test1

command = 'SELECT setting FROM settings WHERE item LIKE \'MOVIEGET\''
cur.execute(command)
if not cur.fetchone():
	getsections()
	print ("Enter the link to your Movie tree.\nExample: http://192.168.1.134:32400/library/sections/2/all/ \n")
	MOVIEGET = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("MOVIEGET",MOVIEGET.strip()))
	sql.commit()
	print (MOVIEGET + " has been added to the settings table. Moving on.")
else:
	cur.execute(command)
	test = cur.fetchone()[0]
	MOVIEGET = test

print ("Database update starting...\n")	
try:
	cur.execute('DROP TABLE shows')
	sql.commit()
	print ("Obsolete shows table found and removed.\n")
except Exception:
	pass
cur.execute('CREATE TABLE IF NOT EXISTS Movies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
sql.commit()
cur.execute('CREATE TABLE IF NOT EXISTS TVshowlist(TShow TEXT, Summary TEXT, Genre TEXT, Rating TEXT, Duration INT, Totalnum INT)')
sql.commit()

def progress(num):
	num = int(num)
	global pcount
	try:
		pcount
	except NameError:
		pcount = 0
	pcount = pcount + 1
	perc = round((float(pcount) / float(num)) * 100, 1)
	sys.stdout.write("\r" + str(perc) + "%")
	sys.stdout.flush()

def clearprogress():
	global pcount
	pcount = 0

def getshows():	
	print ("Getting TVshowlist now.")
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	shows = response.split('<Directory ratingKey=')
	counter = 1
	xnum = int(len(shows))-1

	while counter <= int(len(shows)-1):

		show = shows[counter]
		
		genres = show
		studio = show
		
		
		title = show
		title = title.split('title="')
		title = title[1]
		title = title.split('"')
		title = title[0]
		
		title = title.replace('&apos;','\'')
		title = title.replace('&amp;','&')
		title = title.replace('?','')
		title = title.replace('/',' ')
		title = title.replace("&#39;","'")
		
		summary = show
		rating = show
		duration = show
		totalnum = show
		
		summary = show
		summary = summary.split('summary="')
		summary = summary[1]
		summary = summary.split('"')
		summary = summary[0]
		summary = summary.replace('\'','')
		
		rating = show
		try:
			rating = rating.split('contentRating="')
			rating = rating[1]
			rating = rating.split('"')
			rating = rating[0]
		except Exception:
			rating = 'N\A'
		duration = show
		duration = duration.split('duration="')
		duration = duration[1]
		duration = duration.split('"')
		duration = duration[0]
		duration = int(duration)/60000
		
		totalnum = show
		totalnum = totalnum.split(' leafCount="')
		totalnum = totalnum[1]
		totalnum = totalnum.split('"')
		totalnum = totalnum[0]
		
		name = title
		TShow = name
				
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
		
			
			
		studio = studio.split("studio=\"")
		try:
			studio = studio[1]
			studio = studio.split("\"")
			studio = studio[0]
		except IndexError:
			studio = "None"
		TShow = TShow.replace("'","''")
		summary = summary.replace("&#39;","'")
		summary = summary.replace("'","''")
		summary = str(summary.decode('ascii','ignore')).strip()
		cur.execute("SELECT * FROM TVshowlist WHERE TShow LIKE \"" + TShow + "\"")
		try:
			if not cur.fetchone():
				cur.execute("INSERT INTO TVshowlist VALUES(?, ?, ?, ?, ?, ?)", (TShow, summary, genre, rating, int(duration), int(totalnum)))
				sql.commit()
				#marker
				progress(xnum)
		except IndexError: 
			print ("\nError adding " + TShow)
			with open(PROBLEMS, 'a') as file:
				file.write(TShow + "\n")
			file.close()
				
		
		counter = counter + 1

	clearprogress()	
	print ("\n\nTV Show List Generated.")


def getmovies():
	print ("Getting Movies now.")
	response = http.urlopen('GET', MOVIEGET, preload_content=False).read()
	response = str(response)
	shows = response.split('<Video ratingKey=')
	xnum = int(len(shows))-1
	counter = 1

	while counter <= int(len(shows)-1):

		ashow = shows[counter]
		ashow = ashow.split("key=\"/library/metadata/")
		ashow = ashow[1]
		ashow = ashow.split("\"")
		ashow = ashow[0]
		ashow = TVPART + ashow.strip()
		show = http.urlopen('GET', ashow, preload_content=False).read()

		genres = show
		studio = show
		directors = show
		actors = show
		rating = show
		summary = show
		tagline = show
		
		title = show
		title = title.split('" title="')
		title = title[1]
		title = title.split('"')
		title = title[0]
		
		title = title.replace('&apos;','\'')
		title = title.replace('&amp;','&')
		title = title.replace("&#39;","'")
		
		name = title

		try:
			genres = genres.split("</Media>")
			genres = genres[1]
			genres = genres.split("<Director")
			genres = genres[0]
			genres = genres.split('tag="')
			bgenre = ""
			for genre in genres:
				genre = genre.split('"')
				genre = genre[0]
				genre = genre.replace("&amp;","&")
				if ("\"" in genre):
					pass
				elif (("<Genre id=" in genre) or ("<Media videoResolution=" in genre)):
					pass
				else:
					bgenre = bgenre + " " + genre
		except IndexError:
			bgenre = "None"
		try:
			directors = directors.split("</Media>")
			directors = directors[1]
			directors = directors.split("<Writer")
			directors = directors[0]
			directors = directors.split("<Director")
			#print directors
			dict = ""
			cnt = 0
			for director in directors:
				if cnt == 0:
					pass
				else:
					director = director.split("tag=\"")
					director = director[1]
					director = director.split("\"")
					director = director[0]
					dict = dict + director + " "
				cnt = cnt + 1
			directors = dict.strip()
		except Exception:
			directors = ""
		
		try:	
			bactors = ""
			actors = actors.split("<Role id=\"")
			cnt = 0
			for actor in actors:
				if cnt == 0:
					pass
				else:
					actor = actor.split("tag=\"")
					actor = actor[1]
					actor = actor.split("\"")
					actor = actor[0]
					bactors = bactors + " " + actor
				cnt = cnt + 1
			bactors = bactors.strip()
		except Exception:
			bactors = ""
		
		rating = rating.split("contentRating=\"")
		try:
			rating = rating[1]
			rating = rating.split("\"")
			rating = rating[0]
		except IndexError:
			#print ("No Rating Available. Skipping " + name)
			rating = "none"
		
		tagline = tagline.split("tagline=\"")
		try:
			tagline = tagline[1]
			tagline = tagline.split("\" ")
			tagline = tagline[0]
		except IndexError:
			#print ("No Tagline Available. Skipping " + name)
			tagline = "none"
			
		summary = summary.split("summary=\"")
		try:
			summary = summary[1]
			summary = summary.split("\"")
			summary = summary[0]
		except IndexError:
			#print ("No Summary Available. Skipping " + name)
			summary = "none"

		summary = summary.replace('&apos;','\'')
		summary = summary.replace('&amp;','&')
		summary = summary.replace("&#39;","'")
		summary = summary.replace(',', ' ')	
		summary = summary.replace('\'','')
		try:
			summary = summary.decode("ascii", "ignore")
		except Exception:
			pass
		name = name.replace('&apos;','\'')
		name = name.replace('&amp;','&')
		name = name.replace(',', ' ')
		name = name.replace("'","''")
		tagline = tagline.replace('&apos;','')
		tagline = tagline.replace('&amp;','&')
		tagline = tagline.replace(',', ' ')
		tagline = tagline.replace('\'','')
		try:
			tagline = tagline.decode("ascii", "ignore")
		except Exception:
			pass
		directors = directors.replace('&apos;','')
		directors = directors.replace('&amp;','&')
		directors = directors.replace(',', ' ')
		directors = directors.replace('\'','')
		try:
			directors = directors.decode("ascii", "ignore")
		except Exception:
			pass
		bgenre = bgenre.replace('&apos;','')
		bgenre = bgenre.replace('&amp;','&')
		bgenre = bgenre.replace(',', ' ')
		bgenre = bgenre.replace("none", "")
		bactors = bactors.replace('&apos;','')
		bactors = bactors.replace('\'','')
		bactors = bactors.replace('&amp;','&')
		bactors = bactors.replace(',', ' ')
		try:
			bactors = bactors.decode("ascii", "ignore")
		except Exception:
			pass
		
		try:
			cur.execute('SELECT * FROM Movies WHERE Movie LIKE \'' + name + '\'')
			if not cur.fetchone():
				cur.execute('INSERT INTO Movies VALUES(?, ?, ?, ?, ?, ?, ?)', (name, summary, rating, tagline, bgenre, directors, bactors))
				sql.commit()
		except Exception:
			print ("\nError adding " + name)
			with open(PROBLEMS, 'a') as file:
				file.write(name.decode("ascii", "ignore") + " " + bactors + "\n")
			file.close()
		progress(xnum)
		counter = counter + 1
	clearprogress()
	print ("\nDone.")

def getcommercials():
	cur.execute("CREATE TABLE IF NOT EXISTS commercials(name TEXT, duration INT)")
	sql.commit()
	command = "SELECT setting FROM settings WHERE item LIKE \"COMPART\""
	cur.execute(command)
	if not cur.fetchone():
		getsections()
		print ("You need to supply the link to find your commercials.\nExample: http://192.168.1.134:32400/library/metadata/\n")
		COMPART = str(input('Link:'))
		cur.execute("INSERT INTO settings VALUES(?,?)", ("COMPART",COMPART.strip()))
		sql.commit()
		print (COMPART + " has been added to the settings table. Moving on.")
	else:
		cur.execute(command)
		COMPART = cur.fetchone()[0]

	cur.execute("DELETE FROM commercials")
	sql.commit()
	
	response = http.urlopen('GET', COMPART, preload_content=False).read()
	response = str(response)
	commercials = response.split("<Video ratingKey=")
	counter = 1

	while counter <= int(len(commercials)-1):
		comc = commercials[counter]
		duration = comc

		comc = comc.split("title=\"")
		comc = comc[1]
		comc = comc.split("\"")
		comc = comc[0].strip()

		duration = duration.split("duration=\"")
		duration = duration[1]
		duration = duration.split("\"")
		duration = duration[0].strip()
		duration = int(duration)/1000
		cur.execute("SELECT * FROM commercials WHERE name LIKE \"" + comc + "\"")
		if not cur.fetchone():
			cur.execute("INSERT INTO commercials VALUES (?,?)", (comc, duration))
			sql.commit()
			#print ("New Commercial Found: " + comc)
		counter = counter + 1
	
	print ("Done")

def getprerolls():
        cur.execute("CREATE TABLE IF NOT EXISTS prerolls(name TEXT, duration INT)")
        sql.commit()
        command = "SELECT setting FROM settings WHERE item LIKE \"PREROLLPART\""
        cur.execute(command)
        if not cur.fetchone():
		getsections()
                print ("You need to supply the link to find your prerolls.\nExample: http://192.168.1.134:32400/library/metadata/\n")
                PREROLLPART = str(input('Link:'))
                cur.execute("INSERT INTO settings VALUES(?,?)", ("PREROLLPART",PREROLLPART.strip()))
                sql.commit()
                print (PREROLLPART + " has been added to the settings table. Moving on.")
        else:
                cur.execute(command)
                PREROLLPART = cur.fetchone()[0]

	cur.execute("DELETE FROM prerolls")
	sql.commit()

        response = http.urlopen('GET', PREROLLPART, preload_content=False).read()
        response = str(response)
        commercials = response.split("<Video ratingKey=")
        counter = 1

        while counter <= int(len(commercials)-1):
                comc = commercials[counter]
                duration = comc

                comc = comc.split("title=\"")
                comc = comc[1]
                comc = comc.split("\"")
                comc = comc[0].strip()

                duration = duration.split("duration=\"")
                duration = duration[1]
                duration = duration.split("\"")
                duration = duration[0].strip()
                duration = int(duration)/1000
                cur.execute("SELECT * FROM prerolls WHERE name LIKE \"" + comc + "\"")
                if not cur.fetchone():
                        cur.execute("INSERT INTO prerolls VALUES (?,?)", (comc, duration))
                        sql.commit()
                        #print ("New preroll Found: " + comc)
                counter = counter + 1

        print ("\nDone")

def getcustomsection(name):
	sname = "CUSTOM_" + name.lower().strip()
	command = "CREATE TABLE IF NOT EXISTS "+ sname + "(name TEXT, duration INT, type TEXT)"
	cur.execute(command)
        sql.commit()
        command = "SELECT setting FROM settings WHERE item LIKE \"" + sname + "\""
        cur.execute(command)
        if not cur.fetchone():
		getsections()
                print ("You need to supply the link to find your " + name.strip() + " section.\nExample: http://192.168.1.134:32400/library/sections/9/all/\n")
                PREROLLPART = str(input('Link:'))
                cur.execute("INSERT INTO settings VALUES(?,?)", (sname,PREROLLPART.strip()))
                sql.commit()
                print (PREROLLPART + " has been added to the settings table. Moving on.")
        else:
                cur.execute(command)
                PREROLLPART = cur.fetchone()[0]

        cur.execute("DELETE FROM " + sname)
        sql.commit()

        response = http.urlopen('GET', PREROLLPART, preload_content=False).read()
        response = str(response)
	type = response
	type = type.split("librarySectionTitle=\"")
	type = type[1]
	type = type.split("\"")
	type = type[0].strip()
	
        commercials = response.split("<Video ratingKey=")
        counter = 1

        while counter <= int(len(commercials)-1):
                comc = commercials[counter]
                duration = comc

                comc = comc.split("title=\"")
                comc = comc[1]
                comc = comc.split("\"")
                comc = comc[0].strip().strip()
		comc = comc.replace("&#39;","''")
		comc = comc.replace("&amp;","&")

                duration = duration.split("duration=\"")
                duration = duration[1]
                duration = duration.split("\"")
                duration = duration[0].strip()
                duration = int(duration)/1000
		
                cur.execute("SELECT * FROM " + sname + " WHERE name LIKE \"" + comc + "\"")
                if not cur.fetchone():
                        cur.execute("INSERT INTO " + sname + " VALUES (?,?,?)", (comc, duration, type))
                        sql.commit()
                        #print ("New " + sname + " Found: " + comc)
                counter = counter + 1

        print ("\nDone")

def startupactiontv():
	cur.execute("DELETE FROM TVshowlist")
	sql.commit()
	print ("TV Tables purged and ready for data.")

def startupactionmovie():
	cur.execute("DELETE FROM Movies")
	sql.commit()
        print ("Movie Tables purged and ready for data.")

def getfavorites():
	global favtv
	global favmve
	cur.execute("SELECT Movie FROM Movies WHERE Genre LIKE \"%favorite%\"")
	mlist = cur.fetchall()
	for mve in mlist:
		mve = mve[0]
		if mve.strip() not in favmve:
			favmve.append(mve)

	cur.execute("SELECT TShow FROM TVshowlist WHERE Genre LIKE \"%favorite%\"")
	tvlist = cur.fetchall()
	for item in tvlist:
		item = item[0]
		if item not in favtv:
			favtv.append(item)

	print ("Favorites Acquired. Moving On.")

def restorefavorites():
	global favtv
        global favmve
	cmdtv = "python ./system.py addfavoriteshow "
	cmdmv = "python ./system.py addfavoritemovie "
	
	for show in favtv:
		command = cmdtv + "\"" + show.strip() + "\""
		os.system(command)
	
	for movie in favmve:
		command = cmdmv + "\"" + movie.strip() + "\""
		os.system(command)

	print ("Favorites Restored.")

def getgenrestv():
	global tvgenres
	command = "SELECT Genre FROM TVshowlist ORDER BY Genre ASC"
        cur.execute(command)
        fgenres = cur.fetchall()
        xshowlist = []
        for genres in fgenres:
                genre = genres[0].split(";")
                for xgen in genre:
                        if xgen not in xshowlist:
                                xshowlist.append(xgen)
	for genre in xshowlist:
		genre = genre.strip()
		command = "SELECT TShow from TVshowlist where Genre LIKE \"%" + genre + "%\""
		cur.execute(command)
		shows = cur.fetchall()
		for show in shows:
			show = show[0]

			try:
				writeme = writeme + "," + show
			except NameError:
				writeme = genre + ":" + show
		tvgenres.append(writeme)
		del writeme
	print ("TV Genres Saved.")

def getgenresmovie():
	global moviegenres
	command = "SELECT Genre FROM Movies ORDER BY Genre ASC"
	cur.execute(command)
	fgenres = cur.fetchall()
	xmovies = []
	for genres in fgenres:
		genre = genres[0].split(" ")
		for xgen in genre:
			if ((xgen not in xmovies) and (xgen != "")):
				xmovies.append(xgen)
	for genre in xmovies:
		if genre == " ":
			pass
		else:
			genre = genre.strip()
			command = "SELECT Movie FROM Movies WHERE Genre LIKE \"%" + genre + "%\""
			cur.execute(command)
			movies = cur.fetchall()
			for movie in movies:
				movie = movie[0]
				try:
					writeme = writeme + "," + movie
				except NameError:
					writeme = genre + ":" + movie
				moviegenres.append(writeme)
				del writeme
	print ("Movie Genres Saved.")
	
def restoregenrestv():
	print ("\nRestoring Custom TV Genres Now.")
	global tvgenres
	xnum = int(len(tvgenres))-1
	for genre in tvgenres:
		genre = genre.split(":")
		shows = genre[1]
		genre = genre[0]
		shows = shows.split(",")
		for show in shows:
			show = show.strip()
			say = addgenreshow(show,genre)
		progress(xnum)
	clearprogress()
	print ("\nTV Genres Restored.")

def restoregenremovies():
	print ("\nRestoring Custom Movie Genres.")
	global moviegenres
	xnum = int(len(moviegenres))-1
	for gre in moviegenres:
		if gre == " ":
			pass
		else:
			gre = gre.split(":")
			shows = gre[1]
			genre = gre[0]
			shows = shows.split(",")
			for show in shows:
				show = show.strip()
				say = addgenremovie(show, genre)
		progress(xnum)
	clearprogress()
        print ("\nMovie Genres Restored.")

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
        if genre.lower() in genres.lower():
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
		say = "Error restoring genre " + genre + " to movie " + movie
		return ("Error restoring genre " + genre + " to movie " + movie)
        cur.execute(command)
        stuff = cur.fetchone()
        title = stuff[0]
        summary = stuff[1]
        rating = stuff[2]
        tagline = stuff[3]
        genres = stuff[4]
        director = stuff[5]
        actor = stuff[6]
        if genre.lower() in genres.lower():
                return("Error: " + genre + " is already associated with the movie " + movie)
        genres = genres.strip() + " " + genre
        command = 'DELETE FROM Movies WHERE Movie LIKE \'' + movie + '\''
        cur.execute(command)
        sql.commit()
        cur.execute('INSERT INTO Movies VALUES(?,?,?,?,?,?,?)',(title, summary, rating, tagline, genres, director, actor))
        sql.commit()
        return (genre + " successfully associated with the movie " + movie )
	
try:
	if "Windows" not in ostype:
		option = str(sys.argv[1])
	else:
		print ("Notice: For Windows, the update db script may default to 'all' when there is an argument failure.\n")
		option = "all"
	#getsections()
	#commands
	if ("updatetv" in option):
		bcmd = "python " + homedir + "system.py backuptvdb"
		os.system(bcmd)
		getgenrestv()
		try:
			getgenrestv()
			startupactiontv()
			getshows()
			restoregenrestv()
		except KeyboardInterrupt:
			print ("Cancel request received. Restoring tables.")
			cmd = "python " + homedir + "system.py restoretvdb"
			os.system(cmd)
			print("Cancelled.")
	elif ("updatemovies" in option):
		bcmd = "python " + homedir + "system.py backupmoviedb"
		os.system(bcmd)
		try:
			getgenresmovie()
			startupactionmovie()
			getmovies()
			restoregenremovies()
		except KeyboardInterrupt:
			print ("Cancel request received. Restoring tables.")
                        cmd = "python " + homedir + "system.py restoremoviedb"
                        os.system(cmd)
                        print("Cancelled.")
	elif ("all" in option):
		bcmd = "python " + homedir + "system.py backuptvdb"
                os.system(bcmd)
		bcmd = "python " + homedir + "system.py backupmoviedb"
                os.system(bcmd)
		try:
			getgenrestv()
			getgenresmovie()
			startupactiontv()
			startupactionmovie()
			getshows()
			getmovies()
			restoregenrestv()
			restoregenremovies()
		except KeyboardInterrupt:
			print ("Cancel request received. Restoring tables.")
                        cmd = "python " + homedir + "system.py restoremoviedb"
                        os.system(cmd)
			cmd = "python " + homedir + "system.py restoretvdb"
                        os.system(cmd)
                        print("Cancelled.")
	elif ("getcommercials" in option):
		getcommercials()
		print ("Commercial Get Finished.")
	elif ("getprerolls" in option):
		getprerolls()
		print ("Preroll Get Finished.")
	elif ("getcustomsection" in option):
		try:
			option = str(sys.argv[2])
			getcustomsection(option)
			print ("Get Custom Done.")
		except IndexError:
			print ("Error: You must supply a section name to use this command.")
	elif ("getsections" in option):
		getsections()

except TypeError:
	print ("No option specified. Use 'updatetv' or 'updatemovies' or 'all' to update your db.")		
print ("Done")
