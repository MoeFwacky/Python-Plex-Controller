homedir = '/home/pi/hasystem/'

import os
import getpass
import time
import calendar
import sys
import requests
import sqlite3
import urllib3
import subprocess
import platform
try:
	import enchant
except Exception:
	print ("Warning: pyenchant no installed or has a path problem. Spell checking will not work.\n")

from os import listdir
from os.path import isfile, join
from random import randint, shuffle

#top
user = getpass.getuser()
http = urllib3.PoolManager()

global file
global show
global play
global pcmd
global pcount
global ttlchk
global commandcheck
global xlib
global PRINTMODE
commandcheck = "no"

ttlchk = ""

#SLEEPTIME = 20 
try:
	input = raw_input
except NameError:
	pass
	
MYDB = homedir + "myplex.db"
sql = sqlite3.connect(MYDB)
cur = sql.cursor()

cur.execute("SELECT State FROM States WHERE Option LIKE \"SLEEPTIME\"")
if not cur.fetchone():
	cur.execute("INSERT INTO States VALUES (?,?)",("SLEEPTIME","20"))
	sql.commit()
	cur.execute("SELECT State FROM States WHERE Option LIKE\"SLEEPTIME\"")
else:
	cur.execute("SELECT State FROM States WHERE Option LIKE\"SLEEPTIME\"")
SLEEPTIME = int(cur.fetchone()[0])

global PLEXSVR
global PLEXCLIENT
global plex
global client


def plexlogin():
	global PLEXSVR
	global PLEXCLIENT
	global plex
	global client
	global LOGGEDIN
	try:

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

		try:
			LOGGEDIN
		except Exception:
		
			try:
				from plexapi.server import PlexServer
				from plexapi.myplex import MyPlexUser
				baseurl = 'http://' + PLEXSERVERIP + ':' + PLEXSERVERPORT
				plex = PlexServer(baseurl)
			except IndexError:
				from plexapi.myplex import MyPlexAccount
				print ("Local Fail. Trying cloud access.")
				cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXUN\'')
				PLEXUN = cur.fetchone()
				PLEXUN = PLEXUN[0]
				try:	
					cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXPW\'')
					PLEXPW = cur.fetchone()
					PLEXPW = PLEXPW[0]
					import base64
					PLEXPW = str(base64.b64decode(PLEXPW))
				except Exception:
					print ("Your Plex Password is temporarly needed to proceed:\n")
					PLEXPW = str(getpass.getpass("Password: "))
				user = MyPlexAccount.signin(PLEXUN,PLEXPW)

				print ("\rSuccessfully logged into Plex cloud.\n")
				plex = user.resource(PLEXSVR).connect()
			if ("changeclient" not in sys.argv):
				try:
					client = plex.client(PLEXCLIENT)
				except Exception:
					print ("Retrying Client Get.\n")
					time.sleep(1)
					client = plex.client(PLEXCLIENT)
			LOGGEDIN = "YES"

	except IndexError:
		print ("Error getting necessary plex api variables. Run system_setup.py.")

		
def setsleeptime(num):
	num = str(num)
	cur.execute("DELETE FROM States WHERE Option LIKE \"SLEEPTIME\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("SLEEPTIME",num))
	sql.commit()
	return ("SLEEPTIME setting has been adjusted to: " + num + ".\n")

def gethonorific(): #Returns the value of the name the script will refer to the user by in certain outputs.
	command = "SELECT State FROM States WHERE Option LIKE \"CALLMETHIS\""
	cur.execute(command)
	if not cur.fetchone():
		CALLMETHIS = "Sir"
		cur.execute("INSERT INTO States VALUES (?,?)",("CALLMETHIS",CALLMETHIS))
		sql.commit()
	cur.execute(command)
	CALLMETHIS = cur.fetchone()[0]
	return (CALLMETHIS)

def sethonorific(myname): #Sets the name the script will refer to the user by. Defaults to "Sir"
	if myname == "none":
		print ("What shall I call thee?")
		CALLMETHIS = str(raw_input('TItle: ')).strip()
	else:
		CALLMETHIS = myname.strip()
	cur.execute("DELETE FROM States WHERE Option LIKE \"CALLMETHIS\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("CALLMETHIS",CALLMETHIS))
	sql.commit()
	return ("I shall now call thee " + CALLMETHIS + ". Good Day.")

def changeplexip(): #Changes the stored IP address for the Plex Server
	plexip = str(raw_input('Plex Server IP: '))
	plexip = plexip.strip()
	plexport = str(raw_input('Plex Port: '))
	plexport = plexport.strip()
	cur.execute("DELETE FROM settings WHERE item LIKE \'PLEXSERVERIP\'")
	sql.commit()
	cur.execute("DELETE FROM settings WHERE item LIKE \'PLEXSERVERPORT\'")
	sql.commit()
	cur.execute("INSERT INTO settings VALUES (?,?)",("PLEXSERVERIP",plexip))
	sql.commit()
	cur.execute("INSERT INTO settings VALUES (?,?)",("PLEXSERVERPORT",plexport))
	sql.commit()
	

def changeplexpw(password): #Changes the stored password for Plex. Obsolete as storing passwords is no longer needed
	password = password.strip()
	cur.execute("DELETE FROM settings WHERE item LIKE \'PLEXPW\'")
	sql.commit()
	password = str(password.encode('base64','strict'))
	cur.execute("INSERT INTO settings VALUES(?,?)",('PLEXPW',password))
	sql.commit()
	return ("The Plex PW has been changed.")

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def checkcustomtables(show): 
	command = "SELECT name FROM sqlite_master WHERE type='table'"
	cur.execute(command)
	list = cur.fetchall()
	for item in list:
		if ("CUSTOM_" in item[0]):
			command = "SELECT name, type FROM " + item[0] + " WHERE name LIKE \"" + show + "\""
			cur.execute(command)
			if not cur.fetchone():
				pass
			else:
				cur.execute(command)
				found = cur.fetchone()
				type = found[1]
				found = found[0]
				return ("CUSTOM."+found, type)
	return show

def checkprecomm(show):
	oshow = show
	if ((show == "playcommercial") or (show == "preroll")):
		return show
	show = show.replace("preroll.","")
	show = show.replace("playcommercial.","")
	com1 = "SELECT name FROM prerolls WHERE name LIKE \"" + show + "\""
	com2 = "SELECT name FROM commercials WHERE name LIKE \"" + show + "\""
	try:
		cur.execute(com1)
		if not cur.fetchone():
			pass
		else:
			cur.execute(com1)
			show = cur.fetchone()[0]
			show = "preroll." + show
			return show
		cur.execute(com2)
		if not cur.fetchone():
					pass
		else:
			cur.execute(com2)
			show = cur.fetchone()[0]
			show = "playcommercial." + show
			return show
		return oshow
	except sqlite3.OperationalError:
		return oshow

def getcustomtable(table):
	item = "CUSTOM_" + table.strip()
	command = "SELECT name FROM "+ item
	try:
		cur.execute(command)
	except Exception:
		try:
                        plexlogin()
                        ssec = plex.library.sections()
                        for lib in ssec:
                                if lib.title ==table:
                                        stuff = lib.search("")
                                        found = []
                                        for item in stuff:
                                                found.append(item.title)
                        return found
		except Exception:
			return ("Error: " + table + " not found.")

	stuff = []
	if not cur.fetchall():
		return ("Error: " + table + " not found.")
	else:
		cur.execute(command)
		found = cur.fetchall()
		for item in found:
			stuff.append(item[0])
		return stuff

def listcustomtables(): #Displays a list of custom Plex libraries imported into the controller database
	command = "SELECT name FROM sqlite_master WHERE type='table'"
	cur.execute(command)
	list = cur.fetchall()
	stuff = []
	for item in list:
		if ("CUSTOM_" in item[0]):
			stuff.append(item[0])
	return stuff

def muteaudio(): #Mutes the audio
	global client
	plexlogin()
	client.setVolume(0, 'Video')

def mutemusic(): #Mutes audio output to the music client
	plexlogin()
	PLEXMUSICCLIENT = musiccheck()
	client = plex.client(PLEXMUSICCLIENT)
	client.setVolume(0, 'music')

def unmutemusic(): #Unmutes audio output to the music client
        plexlogin()
        PLEXMUSICCLIENT = musiccheck()
        client = plex.client(PLEXMUSICCLIENT)
        client.setVolume(100, 'music')

def unmuteaudio(): #Unmutes audio 
        global client
        plexlogin()
        client.setVolume(100, 'Video')

def lowaudio(): #Sets volume to 25%
	global client
	plexlogin()
	client.setVolume(25, 'Video')

def mediumaudio(): #Sets volume to 50%
	global client
	plexlogin()
	client.setVolume(50, 'Video')

def highaudio(): #Sets volume to 75%
	global client
	plexlogin()
	client.setVolume(75, 'Video')

def maxaudio(): #Sets audio to 100%
	global client
	plexlogin()
	client.setVolume(100, 'Video')

def schedchecker(command):
	global commandcheck

	command = command.replace("system.py schedchecker ","")
	cmd = "SELECT name FROM help"
	cur.execute(cmd)
	xcmds = cur.fetchall()
	cmds = []
	for item in xcmds:
		cmds.append(item[0])
	ccheck = "no"
	for itm in cmds:
		if itm in command:
			#print ("Pass: Commands")
			commandcheck = "yes"
			return command
	if "no" in ccheck:	
		say = titlecheck(command)
		if ("ERROR:" in say):
			return ("ERROR: Command Fail. " + command + " does not appear to be valid. Check and try again.")
		else:
			#print ("Pass: Media")
			return ("\\\"" + say + "\\\"")
	

def addschedule(action, time, day): #Adds an item to the schedule. These must be done one at a time, to add in bulk, use a shell script
	action = action.strip()
	time = time.strip()
	day = day.strip()
	global commandcheck
	achk = schedchecker(action)
	if "ERROR:" in achk:
		return achk
	try:
		cur.execute("SELECT * FROM SCHEDULES")
	except sqlite3.OperationalError:
		cur.execute("CREATE TABLE IF NOT EXISTS SCHEDULES(action TEXT, time TEXT, day TEXT)")
		sql.commit()
	command = "SELECT * FROM SCHEDULES WHERE time LIKE \"" + time + "\" AND day LIKE \"" + day + "\""
	cur.execute(command)
	if not cur.fetchall():
		addme = []
		addme.append(action)
	else:
		cur.execute(command)
		addme = cur.fetchall()[0][0]
		addme = addme.split(";")
		addme.append(action)
		cur.execute("DELETE FROM SCHEDULES WHERE time LIKE \"" + time + "\" AND day LIKE \"" + day + "\"")
		sql.commit()
	for item in addme:
		if item == "":
			pass
		else:
			try:
				adme = adme + item + ";"
			except NameError:
				if ((len(addme) == 1) and ("yes" not in commandcheck)):
					item = "\"" + item + "\""
				adme = item + ";"
	cur.execute("INSERT INTO SCHEDULES VALUES(?,?,?)",(adme, time, day))
	sql.commit()
	return ("Successfully added item to schedule.")

def removeschedule(time, day): #Removes an item from the schedule
	command = "SELECT * FROM SCHEDULES WHERE time LIKE \"" + time + "\" AND day LIKE \"" + day + "\""
	cur.execute(command)
	if not cur.fetchall():
		return("Error: no schedules found for " + time + " on " + day + " found.")
	cur.execute(command)
	fnd = cur.fetchone()
	print ("Found:\n" + fnd[0] + "\n" + fnd[1] + "\n" + fnd[2] + "\n\nRemoving Now.\n")
	cur.execute("DELETE FROM SCHEDULES WHERE time LIKE \"" + time + "\" AND day LIKE \"" + day + "\"")
	sql.commit()
	return ("\nSuccessfully removed schedule for " + time + " on " + day + ".")

def argprocessor(thearg):
	try:
		xshow = show
	except Exception:
		sch = []
		for thing in sys.argv:
			if "system.py" in thing:
				pass
			elif thearg in thing:
				pass
			else:
				achk = schedchecker(thing)
				if "ERROR" not in achk:
					return achk
				#print achk
				sch.append(thing)
		if len(sch) == 1:
			xshow = sch[0]
		else:
			print ("\nARGUMENT ERROR: TAKING A BEST GUESS!!\n")
			xshow = sch[0]
		return xshow
	for thing in sys.argv:
		if "system.py" in thing:
			pass
		elif thearg in thing:
			pass
		elif xshow in thing:
			pass
		else:
			return thing

def viewschedules(): #Outputs the entire schedule list. Currently has pagination and will output the entire schedule at once.
	try:
		cur.execute("SELECT * FROM SCHEDULES")
	except sqlite3.OperationalError:
		cur.execute("CREATE TABLE IF NOT EXISTS SCHEDULES(action TEXT, time TEXT, day TEXT)")
		sql.commit()
	if (("-d" not in sys.argv) and ("-t" not in sys.argv) and ("-a" not in sys.argv)):
		command = "SELECT * FROM SCHEDULES"
		cur.execute(command)
		if not cur.fetchall():
			return ("Nothing is currently scheduled.")
		cur.execute(command)
		sched = cur.fetchall()
		for item in sched:
			print ("Action: " + item[0])
			print ("Time: " + item[1])
			print ("Day: " + item[2] + "\n")
	elif ("-t" in sys.argv):
		if len(sys.argv) == 3:
                        command = "SELECT time FROM SCHEDULES"
                        cur.execute(command)
                        list = cur.fetchall()
                        flist = []
                        for item in list:
                                itm = item[0]
                                if itm not in flist:
                                        flist.append(itm)

                        if len(flist) > 0:
                                print ("The Following Times have items scheduled:\n")
                                for item in flist:
                                        print (item)
		else:
			argv = argprocessor("-t")
			argv = timechecker(argv)
			command = "SELECT * FROM SCHEDULES WHERE time LIKE \"" + argv + "\""
                        cur.execute(command)
                        if not cur.fetchall():
                                return ("Error: No scheduled items found for time: " + argv)
                        cur.execute(command)
			flist = cur.fetchall()
                        print ("The following items were found for time " + argv + ":\n")
                        for item in flist:
                                print ("Action: " + item[0])
                                print ("Day: " + item[2] + "\n")
	elif ("-a" in sys.argv):
                if len(sys.argv) == 3:
                        command = "SELECT action FROM SCHEDULES"
                        cur.execute(command)
                        list = cur.fetchall()
                        flist = []
                        for item in list:
                                itm = item[0]
                                if itm not in flist:
                                        flist.append(itm)

                        if len(flist) > 0:
                                print ("The Following Actions are scheduled:\n")
                                for item in flist:
                                        print (item)
                else:
                        argv = argprocessor("-a")
                        command = "SELECT * FROM SCHEDULES WHERE action LIKE \"%" + argv + "%\""
                        cur.execute(command)
                        if not cur.fetchall():
                                return ("Error: No scheduled items found for action: " + argv)
                        cur.execute(command)
                        flist = cur.fetchall()
                        print ("The following items were found for action " + argv + ":\n")
                        for item in flist:
                                print ("Action: " + item[0])
				print ("Time: " + item[1])
                                print ("Day: " + item[2] + "\n")
	else:
		if len(sys.argv) == 3:
			command = "SELECT day FROM SCHEDULES"
			cur.execute(command)
			list = cur.fetchall()
			flist = []
			for item in list:
				itm = item[0]
				if itm not in flist:
					flist.append(itm)
			
			if len(flist) > 0:
				print ("The Following Days have items scheduled:\n")
				for item in flist:
					print (item)	
		else:
			argv = argprocessor("-d")
			command = "SELECT * FROM SCHEDULES WHERE day LIKE \"" + argv + "\""
			cur.execute(command)
			if not cur.fetchall():
				return ("Error: No scheduled items found for day: " + argv)
			cur.execute(command)
			flist = cur.fetchall()
			print ("The following items were found for day " + argv + ":\n")
			for item in flist:
				print ("Action: " + item[0])
				print ("Time: " + item[1] + "\n")
				
	return ("\nDone.")

def clearschedules(): #Removes all scheduled items
	cur.execute("DELETE FROM SCHEDULES")
	sql.commit()
	return ("Done.")


def holidaycheck(title):
	title=title.lower().strip()
	cur.execute("SELECT * FROM Holidays WHERE name LIKE \"" + title + "\"")
	hcheck = cur.fetchone()
	if not hcheck:
		return ("Error: " + title + " does not exist as a holiday.")
	return title

def checkholidays(holiday): #Returns custom holidays
	try:
		command = "SELECT * FROM Holidays"
		cur.execute(command)	
	except sqlite3.OperationalError:
		cur.execute("CREATE TABLE IF NOT EXISTS Holidays(name TEXT, items TEXT)")
		sql.commit()
	cur.execute(command)
	if not cur.fetchall():
		return ("Error: No Holidays are currently saved.")
	else:
		if holiday == "none":
			command = "SELECT * FROM Holidays"
		else:
			command = "SELECT * FROM Holidays WHERE name LIKE \"" + holiday + "\""
		cur.execute(command)
		test = cur.fetchall()
		if not test:
			return ("Error: " + holiday + " not found in Holidays Table. Check and try again.")
		for thing in test:
			name = thing[0]
			titles = thing[1]
			titles = titles.split(";")
			if ("none" in holiday):
				print (name)
			else:
				print (name + ":")
				for ttl in titles:
					if ttl == "":
						pass
					else:
						ttl = ttl.replace("movie.","the movie ")
						print (ttl)
				print ("---")
	return ("\nDone.")

def removeholiday(holiday): #Delete custom holiday
	print ("Warning: This will remove the " + holiday + " and all associations. Are you sure you want to proceed?")
	validate = str(raw_input("Yes or No:"))
	if "yes" not in validate.lower():
		return ("Error: You must type yes to remove the holiday.") 
	name = holiday.lower()
	cur.execute("SELECT FROM Holidays WHERE name LIKE \"" + name + "\"")
	if not cur.fetchone():
		return ("Error: " + holiday + " not found to remove.")
	cur.execute("DELETE FROM Holidays WHERE name LIKE \"" + name + "\"")
	sql.commit()
	return ("Successfully removed " + holiday + ".")
def removefromholiday(holiday, title): #Removes a holiday designation from a title
	holiday = holiday.lower()
        if ":" not in title:
                if ("Quit." in title):
                        return ("User Quit. No action taken.")
                elif ("Error" in title):
                        return title
        else:
                title = title.split(":")
                ssn = title[1].strip()
                epn = title[2].strip()
                title = title[0].strip()
		title = titlecheck(title.strip())
		shows = plex.library.section('TV Shows')
		the_show = shows.get(title).episodes()
		for ep in the_show:
			if ((ep.seasonNumber == ssn) and (ep.index == epn)):
				tcheck = ep.title
		try:
			tcheck
		except NameError:
			return ("Error: " + title + " not found to add.")
                title = title + ":" + ssn + ":" + ep
        cur.execute("SELECT * FROM Holidays WHERE name LIKE \"" + holiday.strip() + "\"")
        hcheck = cur.fetchone()
	name = hcheck[0]
	items = hcheck[1]
	if title in items:
		items = items.replace(";;;",";")
		items = items.replace(";;",";")
		items = items.replace(title.strip()+";","")
		cur.execute("DELETE FROM Holidays WHERE name LIKE \"" + name + "\"")
		sql.commit()
		cur.execute("INSERT INTO Holidays VALUES(?,?)",(name,items))
		sql.commit()
		return (title + " has been unassociated with the " + name + " holiday.")
	else:
		return (title + " not found associated with the " + name + " holiday.")
		

def addholiday(holiday, title): 
	holiday = holiday.lower()
	if ":" not in title:
		title = titlecheck(title.strip())
		if ("Quit." in title):
			return ("User Quit. No action taken.")
		elif ("Error" in title):
			return title
	else:
		title = title.split(":")
		ssn = title[1].strip()
		epn = title[2].strip()
		title = title[0].strip()
		title = titlecheck(title.strip())
		shows = plex.library.section('TV Shows')
		the_show = shows.get(title).episodes()
		for ep in the_show:
			if((ep.seasonNumber == ssn) and (ep.index == epn)):
				tcheck = ep.title
		try:
			tcheck
		except NameError:
			return ("Error: " + title + " not found to add.")
		title = title + ":" + ssn + ":" + epn
	cur.execute("SELECT * FROM Holidays WHERE name LIKE \"" + holiday.strip() + "\"")
	hcheck = cur.fetchone()
	if not hcheck:
		name = holiday.strip()
		items = title + ";"
	else:
		name = hcheck[0]
		items = hcheck[1]
		if title in items:
			return ("Error: " + title + " is already associated with the following holiday: " + holiday + ".")
		items = items + title + ";"
	cur.execute("DELETE FROM Holidays WHERE name LIKE \"" + holiday + "\"")
	sql.commit()
	cur.execute("INSERT INTO Holidays VALUES(?,?)",(holiday,items))
	sql.commit()
	return (title + " has been associated with the " + holiday + " holiday.")

def addholiauto(holiday,title):
	cur.execute("SELECT * FROM Holidays WHERE name LIKE \"" + holiday.strip() + "\"")
	hcheck = cur.fetchone()
	if not hcheck:
			name = holiday.strip()
			items = title + ";"
	else:
			name = hcheck[0]
			items = hcheck[1]
			if title in items:
					return ("Error: " + title + " is already associated with the following holiday: " + holiday + ".")
			items = items + title + ";"
	cur.execute("DELETE FROM Holidays WHERE name LIKE \"" + holiday + "\"")
	sql.commit()
	cur.execute("INSERT INTO Holidays VALUES(?,?)",(holiday,items))
	sql.commit()
	return (title + " has been associated with the " + holiday + " holiday.")
	
	
def checkmode(option):
	option = option.lower()
	if "show" in option:
		command = "SELECT State FROM States WHERE Option LIKE \"ENABLEFAVORITESMODESHOW\""
		cur.execute(command)
		if not cur.fetchall():
			cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODESHOW","Off"))
			sql.commit()
	elif "movie" in option:
		command = "SELECT State FROM States WHERE Option LIKE \"ENABLEFAVORITESMODEMOVIE\""
		cur.execute(command)
		if not cur.fetchall():
                        cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODEMOVIE","Off"))
                        sql.commit()
	cur.execute(command)
	say = cur.fetchone()[0]
	return (say)

def addapproved(title):
	checkpw = checkkidspw()
	if ("Error:" in checkpw):
		return checkpw
	title = titlecheck(title)
	command = "SELECT State FROM States WHERE Option LIKE \"APPROVEDLIST\""
        cur.execute(command)
	if not cur.fetchone():
		writeme = title + ";"
		cur.execute("DELETE FROM States WHERE Option LIKE \"APPROVEDLIST\"")
		sql.commit()
		cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDLIST",writeme.strip()))
		sql.commit()
		
	else:
		cur.execute(command)
		writeme = cur.fetchone()[0]
		check = writeme.split(";")
		chks = []
		for item in check:
			chks.append(item)
		if (title not in chks):
			writeme = writeme + title + ";"
			cur.execute("DELETE FROM States WHERE Option LIKE \"APPROVEDLIST\"")
			sql.commit()
			cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDLIST",writeme.strip()))
			sql.commit()
		else:
			return (title + " is already in the approved list.")
	return (title + " has been added to the approved list.")

def removeapproved(title):
	title = titlecheck(title)
        command = "SELECT State FROM States WHERE Option LIKE \"APPROVEDLIST\""
        cur.execute(command)
        if not cur.fetchone():
		return ("No approvied list to modify.")
	cur.execute(command)
	writeme = cur.fetchone()[0]
	check = writeme.split(";")
	chks = []
	for item in check:
		chks.append(item)
	if title in chks:
		repl = title.strip() + ";"
		writeme = writeme.replace(repl,"")
		cur.execute("DELETE FROM States WHERE Option LIKE \"APPROVEDLIST\"")
		sql.commit()
		cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDLIST",writeme.strip()))
		sql.commit()
		#chks.remove(title.strip())
		return (title + " has been removed from the approved list.")
	else:
		return (title + " not found in approved list to remove.")	
def addrejected(title):
        title = titlecheck(title)
        command = "SELECT State FROM States WHERE Option LIKE \"REJECTEDLIST\""
        cur.execute(command)
        if not cur.fetchone():
                writeme = title + ";"
                cur.execute("DELETE FROM States WHERE Option LIKE \"REJECTEDLIST\"")
                sql.commit()
                cur.execute("INSERT INTO States VALUES (?,?)",("REJECTEDLIST",writeme.strip()))
                sql.commit()

        else:
                cur.execute(command)
                writeme = cur.fetchone()[0]
                check = writeme.split(";")
                chks = []
                for item in check:
                        chks.append(item)
                if (title not in chks):
                        writeme = writeme + title + ";"
                        cur.execute("DELETE FROM States WHERE Option LIKE \"REJECTEDLIST\"")
                        sql.commit()
                        cur.execute("INSERT INTO States VALUES (?,?)",("REJECTEDLIST",writeme.strip()))
                        sql.commit()
                else:
                        return (title + " is already in the rejected list.")
        return (title + " has been added to the rejected list.")

def showrejected():
	command = "SELECT State FROM States WHERE Option LIKE \"REJECTEDLIST\""
        cur.execute(command)
        if not cur.fetchone():
		print ("The Rejected List is currently empty.")
	else:
		cur.execute(command)
		rlist = cur.fetchone()[0]
		rlist = rlist.split(";")
		print ("The following items are in the Rejected List:\n")
		for item in rlist:
			item = item.replace("movie.","the movie ")
			if item == "":
				pass
			else:
				print (item)

def showapproved():
	command = "SELECT State FROM States WHERE Option LIKE \"APPROVEDLIST\""
        cur.execute(command)
        if not cur.fetchone():
                print ("The Approved List is currently empty.")
	else:
		cur.execute(command)
		rlist = cur.fetchone()[0]
		rlist = rlist.split(";")
		print ("The following items are in the Approved List:\n")
		for item in rlist:
			item = item.replace("movie.","the movie ")
			if item == "":
				pass
			else:
				print (item)

def addapprovedrating(rating):
	checkpw = checkkidspw()
	if ("Error:" in checkpw):
		return checkpw
	command = "SELECT State FROM States WHERE Option LIKE \"APPROVEDRATINGS\""
        cur.execute(command)
        if not cur.fetchone():
                allowed = ['TV-Y','TV-Y7','TV-G','G','PG']
                for item in allowed:
                        try:
                                xallowed = xallowed + ";" + item
                        except NameError:
                                xallowed = item

                cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDRATINGS",xallowed))
                sql.commit()
		del xallowed
        cur.execute(command)
        allowed = cur.fetchone()[0]
	allowed = allowed.split(";")
	if rating in allowed:
		return ("Error: " + rating + " is already in the allowed list.")
	for item in allowed:
		try:
			if item == "":
				pass
			else:
				xallowed = xallowed + ";" + item
		except NameError:
			xallowed = item
	xallowed = xallowed + ";" + rating
	cur.execute("DELETE FROM States WHERE Option LIKE \"APPROVEDRATINGS\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDRATINGS",xallowed))
	sql.commit()
	return (rating + " has been added to the approved ratings list.")

def removeapprovedrating(rating):
	rating = rating.strip()
	command = "SELECT State FROM States WHERE Option LIKE \"APPROVEDRATINGS\""
        cur.execute(command)
        if not cur.fetchone():
                allowed = ['TV-Y','TV-Y7','TV-G','G', 'PG']
                for item in allowed:
                        try:
                                xallowed = xallowed + ";" + item
                        except NameError:
                                xallowed = item

                cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDRATINGS",xallowed))
                sql.commit()
		del xallowed
        cur.execute(command)
        allowed = cur.fetchone()[0]
        yallowed = allowed.split(";")
        if rating not in yallowed:
                return ("Error: " + rating + " is not in the allowed list.")
	allowed = allowed.replace(rating,"")
	allowed = allowed.replace(";;",";")
	allowed = allowed.strip()
	allowed = allowed.split(";")
	for item in allowed:
                try:
			if item == "":
				pass
			else:
				xallowed = xallowed + ";" + item
                except NameError:
                        xallowed = item
        cur.execute("DELETE FROM States WHERE Option LIKE \"APPROVEDRATINGS\"")
        sql.commit()
        cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDRATINGS",xallowed))
        sql.commit()
	return (rating + " has been removed from the approved ratings list.")
	


def approvedratings():
	command = "SELECT State FROM States WHERE Option LIKE \"APPROVEDRATINGS\""
        cur.execute(command)
	if not cur.fetchone():
                allowed = ['TV-Y','TV-Y7','TV-G','G', 'PG']
                for item in allowed:
                        try:
                                xallowed = xallowed + ";" + item
                        except NameError:
                                xallowed = item

                cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDRATINGS",xallowed))
                sql.commit()
	cur.execute(command)
	allowed = cur.fetchone()[0]
	allowed = allowed.split(";")
	print ("The following ratings are currently allowed in kids mode:\n")
	for item in allowed:
		print (item)
	return ("\nDone.")

def kidscheck(option, title):
	command = "SELECT State FROM States WHERE Option LIKE \"APPROVEDLIST\""
	command2 = "SELECT State FROM States WHERE Option LIKE \"REJECTEDLIST\""
	command3 = "SELECT State FROM States WHERE Option LIKE \"APPROVEDRATINGS\""
	cur.execute(command)
	approved = []
	rejected = []
	try:
		alist = cur.fetchone()[0]
	except Exception:
		alist = ""
	cur.execute(command2)
	try:
		rlist = cur.fetchone()[0]
	except Exception:
		rlist = ""
	alist = alist.split(";")
	for item in alist:
		approved.append(item)
	rlist = rlist.split(";")
	for item in rlist:
		rejected.append(item)
	if title in approved:
		return ("pass")
	if title in rejected:
		return ("fail")
	cur.execute(command3)
	if not cur.fetchone():
		allowed = ['TV-Y','TV-Y7','TV-G','G', 'PG']
		for item in allowed:
			try:
				xallowed = xallowed + ";" + item
			except NameError:
				xallowed = item
			
		cur.execute("INSERT INTO States VALUES (?,?)",("APPROVEDRATINGS",xallowed))
		sql.commit()
	cur.execute(command3)
	allowed = cur.fetchone()[0]
	allowed = allowed.split(";")
	option = option.lower()
	title = title.lower()
	if option == "show":
		command = "SELECT Rating FROM TVshowlist WHERE TShow LIKE \"" + title + "\""
	elif option == "movie":
		title = title.replace("movie.","")
		command = "SELECT Rating FROM Movies WHERE Movie LIKE \"" + title + "\""
	cur.execute(command)
	found = cur.fetchone()[0]
	if found in allowed:
		return ("pass")
	else:
		return ("fail")
def setkidspassword(option):
	checkpw = getkidspw()
	checkme = getpass.getpass('Current Password: ')
	if checkpw.strip() != checkme.strip():
		return ("Error: Password Missmatch. No action taken.")
	option = option.strip()
	command = "DELETE FROM States WHERE Option LIKE \"KIDSPW\""
	cur.execute(command)
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("KIDSPW",option))
	sql.commit()
	return ("The KIDSPW has been set.")

def getkidspw():
	command = "SELECT State FROM States WHERE Option LIKE \"KIDSPW\""
	cur.execute(command)
	if not cur.fetchone():
		password = "supersneakey"
		cur.execute("INSERT INTO States VALUES (?,?)",("KIDSPW",password))
		sql.commit()
	cur.execute(command)
	pw = cur.fetchone()[0]
	return (pw)

def checkkidspw():
	pw = getkidspw()
	pw2 = str(input('Kids Password: '))
	if pw != pw2:
		return ("Error: Invalid Password.")
	return pw	

def enablekidsmode():
	cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODESHOW\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODESHOW","Kids"))
	sql.commit()
	cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODEMOVIE\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODEMOVIE","Kids"))
	sql.commit()

        return ("Favories mode has been turned Kids.")

def enableblockrandom(option):
	check = ["on","off"]
        option = option.lower()
	if option not in check:
                return ("Error: you must specify \"on\" or \"off\" to use this command.")
	cur.execute("DELETE FROM States WHERE Option LIKE \"BLOCKRANDOM\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("BLOCKRANDOM",option.strip()))
	sql.commit()
	return ("BLOCKRANDOM has been set to " + option.strip() + ".")

def enablecustomrandom(option):
        check = ["on","off"]
        option = option.lower()
        if option not in check:
                return ("Error: you must specify \"on\" or \"off\" to use this command.")
        cur.execute("DELETE FROM States WHERE Option LIKE \"CUSTOMRANDOM\"")
        sql.commit()
        cur.execute("INSERT INTO States VALUES (?,?)",("CUSTOMRANDOM",option.strip()))
        sql.commit()
        return ("CUSTOMRANDOM has been set to " + option.strip() + ".")

def checkblockrandom():
	command = "SELECT State from States WHERE Option LIKE \"CUSTOMRANDOM\""
	cur.execute(command)
	if not cur.fetchone():
		cur.execute("INSERT INTO States VALUES (?,?)",("CUSTOMRANDOM","off"))
		sql.commit()
	cur.execute(command)
	option = cur.fetchone()[0]
	return option

def checkcustomrandom():
	command = "SELECT State from States WHERE Option LIKE \"CUSTOMRANDOM\""
        cur.execute(command)
        if not cur.fetchone():
                cur.execute("INSERT INTO States VALUES (?,?)",("CUSTOMRANDOM","off"))
                sql.commit()
        cur.execute(command)
        option = cur.fetchone()[0]
        return option
	

def disablekidsmode():
	kcheck = checkmode("movie")
	if "Kids" in kcheck:
		checkpw = checkkidspw()
		if ("Error:" in checkpw):
			return checkpw
		cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODESHOW\"")
		sql.commit()
		cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODESHOW","Off"))
		sql.commit()
		cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODEMOVIE\"")
		sql.commit()
		cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODEMOVIE","Off"))
		sql.commit()

		return ("Favories mode has been turned Off.")
	else:
		return ("Not in Kids mode. Unable to disable.")

def enablefavoritesmode(mode): #Turns on Favorites mode
	mode = mode.lower()
	if "show" in option:
		cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODESHOW\"")
		sql.commit()
		cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODESHOW","On"))
		sql.commit()
	elif ("movie" in option):
		cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODEMOVIE\"")
                sql.commit()
                cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODEMOVIE","On"))
                sql.commit()
	else:
		return ("Error: You must specify either \"show\" or \"movie\" to use this command.")

	return ("Favories mode " + mode + " has been turned On.")

def disablefavoritesmode(mode): #Turns off Favorites mode
	mode = mode.lower()
        if "show" in option:
                cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODESHOW\"")
                sql.commit()
                cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODESHOW","Off"))
                sql.commit()
        elif ("movie" in option):
                cur.execute("DELETE FROM States WHERE Option LIKE \"ENABLEFAVORITESMODEMOVIE\"")
                sql.commit()
                cur.execute("INSERT INTO States VALUES (?,?)",("ENABLEFAVORITESMODEMOVIE","Off"))
                sql.commit()
        else:
                return ("Error: You must specify either \"show\" or \"movie\" to use this command.")

        return ("Favories mode " + mode + " has been turned Off.")

def disablecommercials(): #Disables commercials from playing before a title starts
        cur.execute("DELETE FROM States WHERE Option LIKE \"COMMERCIALMODE\"")
        sql.commit()
        cur.execute("INSERT INTO States VALUES (?,?)",("COMMERCIALMODE","Off"))
        sql.commit()
	return ("Commercial Mode has been disabled.")

def enablecommercials(): #Allow commercials to play before a title starts, default 2
	cur.execute("DELETE FROM States WHERE Option LIKE \"COMMERCIALMODE\"")
        sql.commit()
        cur.execute("INSERT INTO States VALUES (?,?)",("COMMERCIALMODE","On"))
        sql.commit()
        return ("Commercial Mode has been enabled.")

def listclients(): #Display a list of available clients
	daclients = []
	for client in plex.clients():
		daclients.append(client.title)
	print ("The Following Clients are available.")
	counter = 1
	for client in daclients:
		print (str(counter) + "- " + client.strip() + "\n")
		counter = counter + 1

def changeclient(): #Change the client that playback is allocated to
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

def setmusicclient(): #Sets the client to be used for music
	plexlogin()
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
                cur.execute('DELETE FROM settings WHERE item LIKE \'PLEXMUSICCLIENT\'')
                sql.commit()
                cur.execute('INSERT INTO settings VALUES(?,?)',('PLEXMUSICCLIENT',client))
                sql.commit()
                cur.execute("SELECT * FROM settings WHERE item LIKE \'PLEXMUSICCLIENT\'")
                test = cur.fetchone()
                return ("Music Client successfully set to: " + client.strip())
        except Exception:
                return ("Error. Unable to update client. Please try again.")

def stopplay(): #Stops video playback
	client = plex.client(PLEXCLIENT)
	client.stop('video')

def stopmusic(): #Stops music playback
	plexlogin()
        PLEXMUSICCLIENT = musiccheck()
        client = plex.client(PLEXMUSICCLIENT)
	client.stop('music')


def hitok(): #Clicks the OK button in case a dialog box needs to be dismissed
	client = plex.client(PLEXCLIENT)
	client.select()

def pauseplay(): #Pauses playback
	client = plex.client(PLEXCLIENT)
	client.pause('video')

def pausemusic(): #Pauses music playback
	plexlogin()
        PLEXMUSICCLIENT = musiccheck()
        client = plex.client(PLEXMUSICCLIENT)
	client.pause('music')

def whereat(): #Outputs the playback position of the current title
	client = plex.client(PLEXCLIENT)
	for mediatype in client.timeline():
		if int(mediatype.get('time')) != 0:
			check = mediatype.get('time')
			check2 = mediatype.get('duration')
			check = int(check)/60000
			check2 = int(check2)/60000
			say = ("We are at minute " + str(check) + " out of " + str(check2) + ".")
	try:
		say
	except NameError:
		say = "Nothing is currently playing."
	return (say)

def swhere(num):
	nowp = nowplaying()
	if (("Now playing: " in nowp) and ("Episode: " not in nowp)):
		nowp = nowp.split("Now playing: ")
		nowp = nowp[1].strip()
		type = "movie"
	elif (("Now Playing: " in nowp) and ("Episode: " in nowp)):
		nowp = nowp.split("Now Playing: ")
		nowp = nowp[1].strip()
                nowp = nowp.split("Episode: ")
                show = nowp[0].strip()
                nowp = nowp[1].strip()
                type = "show"
	else:
		nowp = nowp.split("TV Show: ")
		nowp = nowp[1].strip()
		nowp = nowp.split("Episode: ")
		show = nowp[0].strip()
		nowp = nowp[1].strip()
		type = "show"
	if type == "show":
		whrat = whereat()
		whrat = whrat.split(" minute ")
		whrat = whrat[1]
		whrat = whrat.split(" out of ")
		whrat = whrat[0].strip()
		whrat = int(whrat)*60000
	else:
		client = plex.client(PLEXCLIENT)
		for mediatype in client.timeline():
			if int(mediatype.get('time')) != 0:
				check = mediatype.get('time')
				check = int(check)
		whrat = check
	say = int(whrat) + (int(num)*1000)
	return say	

def skipahead(val):
	if val == "none":
		client = plex.client(PLEXCLIENT)
		client.stepForward('video')
		return ("Skip Ahead Complete.")
	else:
		try:
			if ("m" in val.lower()):
				val = val.lower()
				val = val.replace("m","")
				val = int(val) * 60
			elif ("s" in val.lower()):
				val = val.lower()
				val = val.replace("s","")
				val = int(val)
			else:
				val = int(val)
			val = int(val)
			val = swhere(val)
			client = plex.client(PLEXCLIENT)
			client.seekTo(val)
			return ("Skip Ahead Complete.")
		except Exception:
			return ("Error: Skip failed.")

def skipback(val):
	if val == "none":
		client = plex.client(PLEXCLIENT)
		client.stepBack('video')
		return ("Skip Back Complete.")
	else:
                try:
                        if ("m" in val.lower()):
                                val = val.lower()
                                val = val.replace("m","")
                                val = int(val) * -60
                        elif ("s" in val.lower()):
                                val = val.lower()
                                val = val.replace("s","")
                                val = int(val)*-1
                        else:
                                val = int(val)*-1
                        val = int(val)
                        val = swhere(val)
                        client = plex.client(PLEXCLIENT)
                        client.seekTo(val)
                        return ("Skip Back Complete.")
                except Exception:
                        return ("Error: Skip failed.")

def listwildcard(): #Displays name of the current Wild Card show
	cur.execute("SELECT setting FROM settings WHERE item LIKE \"WILDCARD\"")
	wildcard = cur.fetchone()
	wildcard = wildcard[0]

	return wildcard

def changewildcard(show): #Change the wildcard show
	show = show.replace("'","''")
	if "none" in show:
		currentw = listwildcard()
		print ("The Current Wild Card is: " + currentw + ".\n")
		print ("What do you want to replace it with?")
		newwild = str(input('Show: '))
	else:
		newwild = show
	'''
	command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"" + newwild + "\""
	cur.execute(command)
	if not cur.fetchall():
		return ("Error. " + str(newwild) + " Not found in Library to set as wildcard.")
	else:
	'''
	#NEW STUFF HERE - TESTING -
	newwild = titlecheck(newwild)
	if ("ERROR:" in newwild):
		return newwild
	else:
		#END NEW STUFF	
		cur.execute("DELETE FROM settings WHERE item LIKE \"WILDCARD\"")
		sql.commit()
		cur.execute("INSERT INTO settings VALUES(?,?)", ('WILDCARD', newwild))
		sql.commit()
		return (newwild + " has been set as the new Wildcard show.")

def getblockpackagelist():
	command = 'SELECT Name FROM Blocks ORDER BY Name ASC'
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

def helpme(stuff):
	command = "SELECT * FROM help WHERE name LIKE \"" + stuff + "\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: " + stuff + " not found in the help table.")
	cur.execute(command)
	stuff = cur.fetchone()
	name = stuff[0]
	desc = stuff[1]
	exp = stuff[2]
	say = "Command: " + name + "\nDescription: " + desc + "\nUsage Example: " + exp.strip()
	return say

def updatehelp(): #Updates the help file
	cls()
	try:
		cur.execute("DELETE FROM help")
		sql.commit()
		print ("help contents deleted.")
	except sqlite3.OperationalError:
		cur.execute("CREATE TABLE IF NOT EXISTS help(name TEXT, summary TEXT,example TEXT)")
		sql.commit()
		print ("help table built.")

	hfile = homedir + "help"
	#os.system("rm -rf " + hfile)
	try:
		os.remove(hfile)
	except Exception:
		pass
	url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/help"
	newfile = http.request('GET', url, preload_content=False)
	newfile = homedir + "\n" + str(newfile.data)
	with open(hfile, "w") as file:
		file.write(newfile)
	file.close()
	#cmd = "wget -O \"" + hfile + "\" \"https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/help\""
	#os.system(cmd)
	print ("Help File Acquired. Updating DB Now.")
	with open (hfile, "r") as file:
		stuff = file.readlines()
	file.close()
	xnum = int(len(stuff))-1
	for line in stuff:
		try:
			line = line.split(",")
			cur.execute("SELECT * FROM help WHERE name LIKE \"" + line[0] + "\"")
			if not cur.fetchone():
				cur.execute("INSERT INTO help VALUES (?,?,?)",(line[0],line[1],line[2]))
				sql.commit()
		except Exception:
			pass
		progress(xnum)
	clearprogress()
	os.system("rm -rf " + hfile)
	print ("\nHelp file removed now that DB populated.\n")

def getautoupdate():
	command = "SELECT State FROM States WHERE Option LIKE \"AUTOUPDATE\""
	cur.execute(command)
	if not cur.fetchone():
	#if not cur.fetchall():
		cur.execute("INSERT INTO States VALUES (?,?)",("AUTOUPDATE","OFF"))
		sql.commit()
	cur.execute(command)
	val = cur.fetchone()[0]
	cur.execute(command)
	ccheck = cur.fetchall()
	if len(ccheck) > 1:
		cur.execute("DELETE FROM States WHERE Option LIKE \"AUTOUPDATE\"")
		sql.commit()
		printmode()
		if PRINTMODE == "ON":
			print ("FOUND Multiple Autoupdate entries. Deleted and set to off. If you are using this feature you will need to re-enable it.")
	return val

def setautoupdate(val): #Turns autoupdate on. When the updatechecker is un, it will automatically update if a new version was found
	if (val.lower() == "on"):
		val = "ON"
	elif (val.lower() == "off"):
		val = "OFF"
	else:
		return ("ERROR: You must specify \"YES\" or \"NO\" to use this action.")
	cur.execute("DELETE FROM States WHERE Option LIKE \"AUTOUPDATE\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("AUTOUPDATE",val))
	sql.commit()
	return ("Auto Update Status has been set to: " + val)

def updatechecker(): #Checks for new version and if autoupdate is on, it will update to the newest version
	curver = versioncheck()
	print ("System Version: " + curver)
	getme = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/system.py"
	response = http.urlopen('GET', getme, preload_content=False).read()
	response = str(response)
	postver = response.split("version = \"")
	postver = postver[1]
	postver = postver.split("\"")
	postver = postver[0]
	print ("Posted System Version: " + postver)
	command = "SELECT State FROM States WHERE Option LIKE \"AUTOUPDATE\""
	cur.execute(command)
	if not cur.fetchone():
		cur.execute("INSERT INTO States VALUES (?,?)",("AUTOUPDATE","OFF"))
		sql.commit()
		print ("No Automatic Update setting found. Setting to: OFF")
	cur.execute(command)
	upstate = cur.fetchone()[0]
	if ("OFF" not in upstate):
		if curver.strip() != postver.strip():
			print ("Executing Update Script Now.")
			ufile = homedir + "tbn_updater.py"
			try:
				os.remove(ufile)
			except Exception:
				pass
			cmd = "wget -O \"" + ufile + "\" \"https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/tbn_updater.py\""
			os.system(cmd)
			print ("Successfully acquired update script.")
			cmd = "python " + ufile
			print ("Running Update Now.")
			os.system(cmd)
		else:
			print ("No action necessary.")
	else:
		print ("No Update Action Taken.")
	

def generateblock(name):
	if (name == "none"):
		bname = input("Block Name: ")
	else:
		bname = name
	nshow = input("Number of Shows to get?: ")
	try:
		nshow = int(nshow)
	except Exception:
		return ("Error: You must specify a number here.")
	nmve = input ("Number of Movies?: ")
	try:
		nmve = int(nmve)
	except Exception:
		return ("Error: You must specify a number here.")
	smax = nshow
	mmax = nmve
	if smax < 0:
		smax = 0
	if mmax < 0:
		mmax = 0
	scnt = 1
	mcnt = 1
	ttl = smax + mmax

	tcnt = 0
	
	while tcnt < ttl:
		rnt = randint(0,1)
		if rnt == 0:
			if scnt <= smax:
				addme = suggesttvblockuse("none")
				scnt = scnt + 1
			else:
				rnt = 1
		if rnt == 1:
			if mcnt <= mmax:
				addme = suggestmovieblockuse("none")
				addme = "movie." + addme
				mcnt = mcnt + 1
			else:
				addme = suggesttvblockuse("none")
				scnt = scnt + 1
		if tcnt == 0:
			addblock(bname,addme)
		else:
			addtoblock(bname,addme)
		tcnt = tcnt + 1
	say = explainblock(bname)
	print ("\nThe " + bname + " block has been generated.\n\n" + say)
	

	return ("done")


def explainblock(block): #Displays content of specified block
	blist = getblockpackagelist()
	for item in blist:
		check = item
		if block == check:
			command = "SELECT Items FROM Blocks WHERE Name LIKE \"" + block + "\""
			cur.execute(command)
			stuff = cur.fetchall()[0]
			stuff = stuff[0]
			stuff = stuff.split(';')

			for things in stuff:
				things = things.rstrip()
				if "random_movie" in things.lower():
					things = things.replace("Random_movie.", "A random ")
					things = things.replace("random_movie.", "A random ")
					things = things + " movie"
					things = things.replace(";","")
				elif "random_tv" in things.lower():
					things = things.replace("Random_tv.", "A Random ")
					things = things.replace("random_tv.", "A Random ")
					things = things + " TV Show."
					things = things.replace(";","")
				try:
					tns = tns + things + "\n"
				except NameError:
					tns = things + "\n"
				tns = tns.replace("movie.", "the movie ")
			say = "The " + block + " plays the following:\n" + tns
			say = say.replace("''","'")
			command = 'SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + block + '\''
                        cur.execute(command)
                        binfo = cur.fetchone()
                        bname = binfo[0]
                        bitems = binfo[1]
                        bcount = binfo[2]
			bitems = bitems.split(';')
			bitems = bitems[int(bcount)]
			sayme = ""
			if ("random_movie." in bitems):
				bitems = bitems.split("_movie.")
				bitems = bitems[1].strip()
				sayme = "Next Random: Movie. Type: " + bitems + ".\n"
			elif ("random_tv." in bitems):
				bitems = bitems.split("_tv.")
                                bitems = bitems[1].strip()
                                sayme = "Next Random: Show. Type: " + bitems + ".\n"
			say = say + sayme
			return say		

def findinblock(findme):
	cmd = "SELECT Name FROM Blocks WHERE Items LIKE \"%" + findme + "%\""
	cur.execute(cmd)
	if not cur.fetchone():
		return ("No Items found containing: " + findme + ".\n")
	else:
		cur.execute(cmd)
	found = cur.fetchall()
	print (findme + " was found in the following blocks:\n")
	for blk in found:
		blk = blk[0]
		say = explainblock(blk)
		print (say)
		del say
	return ("Done.")

def addblock(name, title): #Creates a new block of programming
	command1 = "SELECT Movie FROM Movies"
	command2 = "SELECT TShow FROM TVshowlist"
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
		title = checkcustomtables(title)
		title = title.lower()
		if type(title) is tuple:
			title = title[0]
		if (("custom." not in title) and ("random_" not in title)):
			title = titlecheck(title)
			if ("ERROR" in title):
				return title
			xname = title
			#print (title)
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
			xname = title
			blname = str(name)
			adtitle = "movie." + str(xname) + ";"
			blcount = 0
			cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (blname, adtitle, blcount))
			sql.commit()
			blname = blname.replace("movie.", "The Movie ")
			say = (adtitle.rstrip() + " has been added to the " + blname + " .")
			return (say)
		elif ("custom." in title):
			title = title.replace("custom.","")
			for item in blist:
                                #check = item.replace(".txt","").rstrip()
                                check = str(item)
                                if name == check:
                                        return ("Error. That block already exists. Pick a new name or use 'addtoblock' to update an existing block.")
			blname = str(name)
			adtitle = str(title) + ";"
			blcount = 0
			cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (blname, adtitle, blcount))
                        sql.commit()
			say = (title.rstrip() + " has been added to the " + blname + " block.")
                        return (say)
		elif ("random_movie." in title.lower()):
			rgenre = title.split("movie.")
			try:
				rgenre = rgenre[1]
			except IndexError:
				Return ("Error. No genre provided.")
			
			cur.execute("SELECT * FROM Movies WHERE Genre LIKE \"%" + rgenre + "%\"")
			if not cur.fetchone():
				return ("Sorry " + str(rgenre.strip()) + " not found as an available genre.")
			else:
				adtitle = title.strip() + ";"
				blcount = 0
				blname = str(name)
				cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (blname, adtitle, int(blcount)))
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
				cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + bname + "\"")
				sql.commit()
				cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, adtitle, blcount))
				sql.commit()
				xname = "Random TV " + rgenre.strip() + " has been added to the block.\n"
				return (xname)
			
				
		else:
			for item in tvcheck:
				if (title.lower() == item.lower().rstrip()):
					xname = item
					mycheck = "True"
			'''
			try:
				mycheck
			except Exception:
				mycheck = "False"
			if "True" in mycheck:
			'''
			blname = str(name).strip()
			adtitle = str(xname).strip() + ";"
			#adtitle = adtitle.replace("'","''")
			blcount = 0
			cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (blname, adtitle, int(blcount)))
			sql.commit()
			blname = blname.replace("movie.", "The Movie ")
			say = (xname.rstrip() + " has been added to the " + blname + ".")
			'''
			else:
				print (xname +" not found in library. Did you mean: \n")
				for item in tvcheck:
					if (xname.lower() in item.lower().rstrip()):
						print (item)	
				say = "Done."
			'''
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
			cur.execute("SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \"" + name + "\"")
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
				#xname = xname.replace("'","''")
				xname = titlecheck(xname.strip())
				if ("Quit." in xname):
					return ("User Quit. No action taken.")
				blname = str(name)
				adtitle = bitems+str(xname)+";"
				blcount = 0
				cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + bname + "\"")
				sql.commit()
				cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, adtitle, bcount))
				sql.commit()
				xname = xname.replace("movie.","The movie ")
				print (xname.rstrip() + " has been added to the block.")
			elif choice == 2:
				xname = str(input('TV Show Name:'))
				xname = xname.replace("'","''")
				for item in tvcheck:
					if (xname.lower() == item.lower().rstrip()):
						xname = item.strip()
						mycheck = "True"
				if ("listshows" in xname):
					mycheck = "True"
				try:
					mycheck
				except Exception:
					mycheck = "False"
				if "True" in mycheck:
					if "listshows" in xname:
						try:
							genre = xname.split("listshows ")
							genre = genre[1].strip()
							xname = listshows(genre)
						except Exception:
							xname = availableshows()
						xname = worklist(xname)
						if (xname == "done"):
							return ("User Quit. No further action taken.")
						elif ("Error:" in xname):
							return xname
						
					blname = str(name)
					#xname = xname.replace("'","''")
					adtitle = bitems+str(xname)+";"
					blcount = 0
					cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + bname + "\"")
					sql.commit()
					cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, adtitle, bcount))
					sql.commit()
					xname = xname.replace("movie.","The Movie ")

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
								cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, adtitle, blcount))
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
								cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, adtitle, blcount))
								sql.commit()
								xname = "Random TV " + rgenre.strip() + " has been added to the block.\n"
								rcheck = "true"
							rcheck = "true"
						else:
							print ("Error. You must choose one of the available options.")
					except Exception:
						print ("Error. You must choose one of the available options.")


			elif choice == 4:
				break
			else:
				print ("Error. You must select either 1- Movie OR 2- TV Show OR 3- Random Item OR 4- Quit.")
			
		say = ("block."+name+ " has been created.")
		return (say)

def addtoblock(blockname, name): #Add a title to an existing block
	blist = getblockpackagelist()
	name = name.replace("''","'")
	if (blockname == "none"):
		print ("Blockname not present. Proceeding to querry mode.\n")
		blockname = str(raw_input('Input Block Name: '))
	if (name == "none"):
		print ("Title to add not present. Proceeding to querry mode.\n")
		name = str(raw_input('Title to add: '))
	if (blockname == "select"):
		print ("Block select mode enabled. Generating list\n")
		blockname = worklist(blist)
		if (("Error:" in blockname) or (blockname == "done")):
			return blockname
	if (name == "select"):
		print ("Title select mode enabled.\n")
		mchoice = int(raw_input('1- TV Show or 2- Movie? '))
		if mchoice == 1:
			name = availableshows()
		elif mchoice ==2:
			name = listmovies("none")
		else:
			return ("Error. Invalid Selection. No action taken.")
		name = worklist(name)
		if (("Error:" in name) or (name == "done")):
			return name

	for item in blist:
		check = item.rstrip()
		if blockname == check:
			acheck = "True"
	try:
		acheck
	except Exception:
		acheck = "False"
	name = checkprecomm(name)
	name = checkcustomtables(name)
	if type(name) is tuple:
		name = name[0]
	name = name.lower()
	if (("random_movie." not in name) and ("random_tv." not in name) and ("custom." not in name) and ("playcommercial" not in name) and ("preroll" not in name)):
		name = titlecheck(name.strip())
		if ("Quit." in name):
			return ("User Quit. No action Taken.")
		elif ("ERROR:" in name):
			return name
	#name = name.replace('movie.movie.','movie.')
	if (('movie.' in name) and ('random_movie.' not in name)):
		pass
	elif ("custom." in name):
		name = name.replace("custom.","")
	elif ("random_movie." in name):
		gcheck = name.split("_movie.")
		gcheck = gcheck[1].strip()
		gcheck = moviegenrechecker(gcheck)
		if ("Error" in gcheck):
			return ("Error. No action taken.")
	elif ("random_tv." in name):
		gcheck = name.split("_tv.")
		gcheck = gcheck[1].strip()
		gcheck = tvgenrechecker(gcheck)
		if ("Error" in gcheck):
			return ("Error. No action taken.")
	elif ("playcommercial" in name):
		#name = "playcommercial"
		name = name.strip()
		if "playcommercial." in name:
			check = name.split("playcommercial.")
			check = check[1].strip()
			cur.execute("SELECT name FROM commercials WHERE name LIKE \"" + check + "\"")
			if not cur.fetchone():
				return ("Error: " + name + " not found as an available commercial.")
	elif ("preroll" in name):
		name = name.strip() 
		if "preroll." in name:
			check = name.split("preroll.")
			check = check[1].strip()
			command = "SELECT name FROM prerolls WHERE name LIKE \"" + check + "\""
			cur.execute(command)
			if not cur.fetchone():
				return ("Error: " + name + " not found as an available preroll.")
		
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
		if ((("movie." in name) or ("CUSTOM." in name)) and ("random_movie." not in name)):
			blname = str(bname)
			adtitle = bitems + str(name) + ";"
			blcount = 0
			command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (blname, adtitle, blcount))
			sql.commit()
			name = name.replace("movie.", "The Movie ")
			say = (name.rstrip() + " has been added to the " + blname + " block.")
			say = say.replace("''","'")
			return (say)

		else:
			xname = name
			blname = str(bname).strip()
			adtitle = bitems + str(xname).strip() + ";"
			blcount = 0
			command = 'DELETE FROM Blocks WHERE Name LIKE \'' + blname + '\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (blname, adtitle, int(blcount)))
			sql.commit()
			xname = xname.replace("movie.", "The Movie ")
			say = (xname.rstrip() + " has been added to the " + blname + " block.")
			say = say.replace("''","'")
			return (say)
		return ("Done.")

def removefromblock(blockname, name): #Remove a title from the specified block
	if (("preroll" in name) or ("playcommercial" in name)):
		pass
	else:
		#name = titlecheck(name)
		pass
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
				if name.lower() == item.lower():
					name = item
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


def replaceinblock(block, nitem, oitem): #Replace on title in a block with a different title
	oitem = oitem.lower()
	nitem = nitem.lower()
	command = "SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \"" + block + "\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: " + block + " not found. Check and try again.")
	cur.execute(command)
	binfo = cur.fetchone()
	bname = binfo[0]
	bitems = binfo[1].lower()
	bcount = binfo[2]
	bxitems = bitems.split(';')
	
	if oitem not in bxitems:
		return ("Error: " + oitem + " not in " + block + " to replace.")
	if (("playcommercial" not in nitem) and ("preroll" not in nitem)):
		nitem = titlecheck(nitem)
	if "Quit" in nitem:
		return ("User Quit. No action taken.")
	elif ("ERROR: " in nitem):
		return (nitem)
	nitem = nitem + ";"
	bitems = bitems.replace(oitem, nitem)
	bitems = bitems.replace(";;",";")
	cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + block + "\"")
	sql.commit()
	cur.execute("INSERT INTO Blocks VALUES(?,?,?)",(block, bitems, bcount))
	sql.commit()
	nitem = nitem.replace(";","")
	nitem = nitem.replace("movie.","the movie ")
	oitem = oitem.replace("movie.","the movie ")
	say = oitem + " has been replaced by " + nitem + " in the " + block + " block."
	return (say)

def reorderblock(block):
	command = 'SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \'' + block + '\''
	cur.execute(command)
	if not cur.fetchone():
		print ("Error. " + block + " not found as an available block.")
	cur.execute(command)
	binfo = cur.fetchone()
	bname = binfo[0]
	bitems = binfo[1]
	bcount = binfo[2]
	bxitems = bitems.split(';')
	lmax = int(len(bxitems)) - 2 
	lmin = 0
	newlist = []
	while lmin <= lmax:
		cchecker = "false"
		while cchecker == "false":
			nmin = 1 
			print ("Select Item " + str(lmin + 1) + ": ")
			for item in bxitems:
				if item == "":
					pass
				#elif (item in newlist):
					#pass
				else:
					print (str(nmin) + ": " + item)
					nmin = nmin + 1
			choice = input('New Item ' + str(lmin + 1) + ' ')
			try:
				if choice.lower() == "quit":
					return ("User quit. No action taken.")	
				choice = int(choice) - 1
				choice = bxitems[choice].strip()
				bxitems.remove(choice)
				newlist.append(choice)
				lmin = lmin + 1
				cchecker = "true"
			except Exception:
				cls()
				print ("Error: You must choose one of the available options to proceed or type quit.")
	for item in newlist:
		try:
			nlist = nlist + item + ";"
		except Exception:
			nlist = item + ";"
	bcount = 0
	cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + block + "\"")
	sql.commit()
	cur.execute("INSERT INTO Blocks VALUES (?,?,?)", (block, nlist, int(bcount)))
	sql.commit()
	say = "The " + block + " block has been reordered."
	return (say)

def playblockpackage(play):
	oblock = play
	list = getblockpackagelist()
	for item in list:
		item = item.replace(".txt", "")
		if (item.lower() in play.lower()):
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
				#print ("Playmode has been set to normal.")
			command = 'DELETE FROM Blocks WHERE Name LIKE \'' + bname + '\''
			cur.execute(command)
			sql.commit()
			cur.execute('INSERT INTO Blocks VALUES(?,?,?)', (bname, bitems, int(bcount)))
			sql.commit()
			play = play.lower()
			play = checkcustomtables(play)
			if type(play) is tuple:
				show = play
				table = show[1].strip()
				show = show[0]
				show = show.replace("CUSTOM.","")
				say = playcustom(show, table)
				skipthat()
				return (say)
				
			if "random_movie." in play:
				play = idtonightsmovie()
				play = play.rstrip()
				cur.execute('DELETE FROM States WHERE Option LIKE \'TONIGHTSMOVIE\'')
				sql.commit()
			elif "random_tv." in play:
				xtype = play
                                xtype = xtype.replace(";","")
                                command = 'SELECT State FROM States WHERE Option LIKE \'TONIGHTSSHOW\''
                                cur.execute(command)
                                if not cur.fetchone():
                                        xtype = xtype.split("random_tv.")
                                        xtype = xtype[1]
                                        xtype = xtype.replace(";","")
                                        play = suggesttv(xtype)
                                        play = play.split("does the TV Show ")
                                        play = play[1]
                                        play = play.split(" sound, ")
                                        play = play[0]
                                else:
                                        cur.execute(command)
                                        play = cur.fetchone()[0]
                                play = play.rstrip()
                                cur.execute('DELETE FROM States WHERE Option LIKE \'TONIGHTSSHOW\'')
                                sql.commit()
			elif ("playcommercial" in play):
				commercial = play
				play = whatupnext()
				play = play.replace("Up next we have The Movie ","movie.")
                                if "The TV Show " in play:
                                        play = play.split("The TV Show ")
                                        play = play[1]
                                        play = play.split(" Season ")
                                        play = play[0]
				skipthat()
				if commercial == "playcommercial":
					commercial = "none"
				else:
					commercial = commercial.split("playcommercial.")
					commercial = commercial[1].strip()
				playcommercial(commercial)
				while "The commercial: " in play:
                                        play = play.replace("The commercial: ", "playcommercial.")
                                        commercial = play
                                        play = whatupnext()
                                        play = play.replace("Up next we have The Movie ","movie.")
                                        if "The TV Show " in play:
                                                play = play.split("The TV Show ")
                                                play = play[1]
                                                play = play.split(" Season ")
                                                play = play[0]
                                        skipthat()
                                        if commercial == "playcommercial":
                                                commercial = "none"
                                        else:
                                                commercial = commercial.split("playcommercial.")
                                                commercial = commercial[1].strip()
                                        playcommercial(commercial)
			elif ("preroll." in play):
				preroll = play
				play = whatupnext()
				play = play.replace("Up next we have The Movie ","movie.")
				if "The TV Show " in play:
					play = play.split("The TV Show ")
					play = play[1]
					play = play.split(" Season ")
					play = play[0]
				elif ("Up next we have " in play):
					play = play.split("Up next we have ")
					play = play[1]
					play = play.split(", ")
					play = play[0].strip()
				skipthat()
				if preroll == "preroll":
					preroll = "none"
				else:
					preroll = preroll.split("preroll.")
					preroll = preroll[1].strip()
				playpreroll(preroll)
				while "The commercial: " in play:
					play = play.replace("The commercial: ", "playcommercial.")
					commercial = play
					play = whatupnext()
					play = play.replace("Up next we have The Movie ","movie.")
					print (play)
					if "The TV Show " in play:
						play = play.split("The TV Show ")
						play = play[1]
						play = play.split(" Season ")
						play = play[0]
					skipthat()
					if commercial == "playcommercial":
						commercial = "none"
					else:
						commercial = commercial.split("playcommercial.")
						commercial = commercial[1].strip()
					playcommercial(commercial)	
			if int(bcount) == 0:
				setplaymode("normal")
				print ("Playmode has been set to normal.")
			play = play.replace("Tonights movie has been set to ","")
			play = titlecheck(play).strip()
			if ("ERROR" in play):
				return play
			rcheck = resumestatus()
			if ("on" in rcheck.lower()):
				say = playwhereleftoff(play,"none")
			else:
				say = playshow(play)
			#playshow(play)	
			return play

def availableshows():
	command = 'SELECT TShow FROM TVshowlist ORDER BY TShow ASC'
	cur.execute(command)
	tshows = cur.fetchall()
	theshows = []
	for shows in tshows:
		theshows.append(shows[0])
	return (theshows)

def wlistcolumns(thearray):
	if int(len(thearray) ==0):
		return ("Error: No Results Found.")
	max = int(len(thearray))
	count = 0
	maxc =30 
	if maxc > (int(len(thearray))):
		maxc = int(len(thearray))
	startarray = thearray
	if int(len(thearray)) > maxc:
		thearray = thearray[0:maxc]	
	exitc = ""
	try:
		while "quit" not in exitc:
			say = ""
			maxsp = 30 
			for item in thearray:
				if item == "":
					pass
				else:
					item = item.strip()
					if int(len(item))-1 > 27:
						item = item[0:25] + "..."
					if ((count >=9) and (count <=99)):
						addme = (maxsp - int(len(item)))
						tab = " "
					elif ((count >=99) and (count <=999)):
						addme = (maxsp - int(len(item)+1))
						tab = ""
					else:
						addme = (maxsp - (int(len(item))-1))
						tab = " "
					item = str(count+1) + ": " + item + (addme*" ")
					if count >= max:
						pass
					elif((count+1)%3 == 0):
						say = say + item + "\n"
					else:
						say = say + item + tab
					count = count + 1
			starter = "The Following Items Were Found:\n\n"
			ender = "\n\nEnter a number to return that item, type \"desc x,\" where x is a number above, \"letter x,\" where x is a letter to jump to that letter, or type \"quit\" to quit.\n"
			say = starter + say + ender
			cls()
			print say
			choice = (raw_input('Choice '))
			if (isanint(choice) is True):
				int (choice)
				choice = int(choice) - 1
				say = startarray[choice]
				exitc = "quit"
			else:
				echeck = ['quit','exit','no']
				if choice.lower() in echeck:
					exitc = "quit"
					return choice	
				elif ("yes" in choice.lower()):
					if maxc == int(len(startarray))-1:
						return ("Done.")
					maxc = maxc + 30
					if maxc > int(len(startarray)):
						maxc = int(len(startarray))
					thearray = startarray[count:maxc]
			
				elif ("letter" in choice.lower()):
					find = choice.lower().split("letter ")
					find = find[1][:1].strip()
					print ("Starting at the letter " + find + ".\n")
					lcount = 0
					lcheck = "go"
					try:
						while "stop" not in lcheck:
							lmcheck = startarray[lcount][:1].lower()
							if find.lower() in lmcheck:
								lcheck = "stop"
							lcount = lcount + 1
						print lcount
						count = lcount -1
						maxc = count + 30
						if maxc > int(len(startarray)):
							maxc = int(len(startarray))
						thearray = startarray[count:maxc]
					except Exception:
						Error = "No items found containing " + find + ".\n"
	
				elif ("desc " in choice.lower()):
					getme = choice.lower().split('desc ')
					getme = getme[1].strip()
					getme = int(getme)
					tcheck = startarray[getme-1]
					media = titlecheck(tcheck)
					print media
					exitd = 'go'
					if "movie." in media:
						media = media.replace("movie.","")
						sayme = moviedetails(media)
					else:
						sayme = showdetails(media)
					print (sayme + "\nReturn to previous menu?")
					while 'yes' not in exitd:
						exitd = str(raw_input("yes?"))
					if count > 29:
						count = count - 30
						maxc = count + 30
					else:
						count = 0
					if maxc > int(len(startarray)):
						maxc = int(len(startarray))
					thearray = startarray[count:maxc]
	
				elif ("setupnext" in choice.lower()):
					media = choice.lower().split("setupnext ")
					media = media[1].strip()
					if (isanint(media) is True):
						media = startarray[int(media)-1]
					setupnext(media)
					media = media.replace("movie.","The Movie ")
					print (media + " will play next from the queue.")
					exitc = "quit"
					return ("Done.")
	
				elif ("queueadd" in choice.lower()):
					media = choice.lower().split("queueadd ")
					media = media[1].strip()
					if (isanint(media) is True):
						media = startarray[int(media)-1]
					queueadd(media)
					print (media + " has been added to the queue.")
					exitc = "quit"
					return ("Done.")
				else:
					print ("Invalid Selection, please try again.")
					if count > 29:
						count = count - 30
						maxc = count + 30
					else:
						count = 0
					if maxc > int(len(startarray)):
						maxc = int(len(startarray))
					thearray = startarray[count:maxc]
	 
		return say
	except KeyboardInterrupt:
		return ("\n\nQuitting. No action taken.")

def worklist(thearray):
	if int(len(thearray) == 0):
		return ("Error: No results found.")
	movies = thearray
	mcount = 1
	mvcount = 0
	mmin = 0
	mmax = 9
	mpmin = 1
	if mmax >= len(movies):
		mmax = int(len(movies))-1
	exitc = ""
	try:
		while "quit" not in exitc:
			cls()
			try:
				print ("Error: " + Error + "\nThe Following Items Were Found:\n")
				del Error
			except NameError:
				print ("The Following Items Were Found:\n")
			while mmin <= mmax:
				print (str(mmin+1) + ": " + movies[mmin])
				mmin = mmin + 1
			print ("\nShowing Items " + str(mpmin) + " out of " + str(mmax+1)+ " Total Found: " + str(len(movies)))
			print ("\nSelect an item to return the corresponding item.\nTo see a description of an item enter \'desc number\', where number is the corresponding number.\nTo jump to a letter enter \'letter a\', where a is the desired letter.\nEnter \'Yes\' to go to the next page, and \'No\' to exit.\n")
			getme = input('Choice:')
			if (("yes" in getme.lower()) and ("letter" not in getme.lower())):
				mvcount = mvcount + 10
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
			elif (("no" in getme.lower()) and ("letter" not in getme.lower())):
				exitc = "quit"
				return ("done")	
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
	
				
			elif ("desc " in getme.lower()):
				getme = getme.lower().split('desc ')
				getme = getme[1].strip()
				getme = int(getme)
				tcheck = movies[getme-1]
				media = titlecheck(tcheck)
				exitd = 'go'
				if "movie." in media:
					media = media.replace("movie.","")
					sayme = moviedetails(media)
				else:
					sayme = showdetails(media)
				print (sayme)
				exitc = "quit"
				return "Done."
			elif (isanint(getme) is True):
				getme = int(getme)
				name = movies[getme-1]
				exitc = "quit"
				return (str(name))

			elif ("setupnext" in getme.lower()):
				media = getme.lower().split("setupnext ")
				media = media[1].strip()
				if (isanint(media) is True):
					media = movies[int(media)-1]
				setupnext(media)
				media = media.replace("movie.","The Movie ")
				print (media + " will play next from the queue.")
				exitc = "quit"
				return ("Done.")
			elif ("queueadd" in getme.lower()):
				media = getme.lower().split("queueadd ")
				media = media[1].strip()
				if (isanint(media) is True):
					media = movies[int(media)-1]
				queueadd(media)
				print (media + " has been added to the queue.")
				exitc = "quit"
				return ("Done.")
			elif (getme.lower() == "reroll"):
				return ("reroll")
			else:
				Error = "Invalid Selection. Please Try Again."
				mmin = mmin - 10
	except KeyboardInterrupt:
		print ("\nQuitting.\n")
		exitc = "quit."
		return ("Done.")


def isanint(checkme):
	try:
		int(checkme)
		return True
	except ValueError:
		return False


def availableblocks(): #Displays available programming blocks
	blocklist = getblockpackagelist()
	for item in blocklist: 
		try:
			blist = blist + item + "\n"
		except NameError:
			blist = item + "\n"
	return blist

def moviegenrefixer():
	command = "Select Movie from Movies"
	cur.execute(command)
	mlist = cur.fetchall()
	for item in mlist:
		item = item[0].strip()
		command = "SELECT * FROM Movies WHERE Movie LIKE \"" + item + "\""
		cur.execute(command)
		found = cur.fetchone()
		genre = found[4].strip()
		if (("  " in genre) or (";" in genre)):
			cur.execute("DELETE FROM Movies WHERE Movie LIKE \"" + item + "\"")
			sql.commit()
			movie = found[0]
			summary = found[1]
			rating = found[2]
			tagline = found[3]
			genre = found[4]
			genre = genre.replace("  "," ")
			genre = genre.replace(";","")
			director = found[5]
			actors = found[6]
			cur.execute('INSERT INTO Movies VALUES(?,?,?,?,?,?,?)', (movie, summary, rating, tagline, genre, director, actors))
			sql.commit()
		

	print ("Movie Genres Fixed.")


def findmovie(movie):
	movie = movie.strip()
	echeck = ['error','no','quit']
	if ("genre." in movie.lower()):
		genre = movie.split("genre.")
		genre = genre[1]
		command = "SELECT Movie FROM Movies WHERE Genre LIKE \"%" + genre + "%\" ORDER BY Movie ASC"
		cur.execute(command)
		tlist = cur.fetchall()
		try:
			mlist = []
			for item in tlist:
				if item not in mlist:
					mlist.append(item[0])
			if ((len(mlist)>10) and ("-l" not in sys.argv)):
				say = wlistcolumns(mlist)
			else:
				worklist(mlist)
		except Exception:
			return ("Error: No movies in the " + genre + " genre have been found.")
		
	elif ("rating." in movie.lower()):
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
			if ((len(mlist)>10) and ("-l" not in sys.argv)):
                                say = wlistcolumns(mlist)
				for item in echeck:
					if say == item:
						return say
				setupnext(say)
                        else:
				worklist(mlist)
	elif ('actor.' in movie.lower()):
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
			if ((len(mlist)>10) and ("-l" not in sys.argv)):
				say = wlistcolumns(mlist)
                                for item in echeck:
                                        if say == item:
                                                return say
                                setupnext(say)
                        else:
				worklist(mlist)
	else:
		command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'%' + movie + '%\''
		cur.execute(command)
		xep = cur.fetchall()
		mlist = []
		if xep != []:
			for item in xep:
				item = item[0].strip()
				if item not in mlist:
					mlist.append(item)
			if ((len(mlist)>10) and ("-l" not in sys.argv)):
				say = wlistcolumns(mlist)
                                for item in echeck:
                                        if say == item:
                                                return say
                                setupnext(say)
                        else:
				worklist(mlist)
		else:
			say = "No results found for " + movie + ". Did you mean:\n"

			if xep == []:
				del xep
				movie = movie.split(' ')
				for title in movie:
					print ("Found containing " + title + "\n")
					command = 'SELECT Movie FROM Movies WHERE Movie LIKE \'%' + title + '%\''
					cur.execute(command)
					xep = cur.fetchall()
					if xep != []:
						for item in xep:
							print (item[0])
						print ("\n")
						say = ""
					else:
						say = ("No items found containing " + title)



			return (say)

def listepisodes(show): #Displays all of the episodes titles of a specified show
	plexlogin()
	show = titlecheck(show)
	command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"" + show + "\""
	cur.execute(command)
	if not cur.fetchall():
		return ("The Show " + show + " not found.")
	else:
		shows = plex.library.section('TV Shows')
		the_show = shows.get(show).episodes()
		max = int(len(the_show))-1
		if max > 10:
			mmax = 10
		else:
			mmax = max
		count = 1

		getme = ""
		while "quit" not in getme.lower():
			cls()
			print ("Showing Items " + str(count) + " - " + str(mmax) + " out of " + str(max+1) + "\n")
			while (count + 1) <= mmax+1:
				print (str(count) + ": " + the_show[count-1].title)
				count = count + 1
			print ("\nSelect a number or type yes to go on. Type \"quit\" to exit.\n")
			getme = input("Choice: " )
			if getme == "yes":
				mmax = mmax + 10
				if mmax > max:
					mmax = max+1
			else:
				try:
					getme = int(getme)
					title = str(the_show[getme-1].title)
					print ("Episode Title: " + title)
					print ("Season Number: " + str(the_show[getme-1].seasonNumber))
					print ("Episode Number: " + str(the_show[getme-1].index))
					print ("Overall Number: " + str(getme))
					say = the_show[getme-1].summary
					print (say + "\n")
					getme = "quit"
				except Exception:
					pass
	return ("Done.")				


def findshow(show):
	echeck = ['quit','error','no']
	if ("genre." in show.lower()):
		genre = show.split("genre.")
		genre = genre[1].strip().lower()
		command = "SELECT TShow from TVshowlist WHERE Genre LIKE \"%" + genre + "%\""
	elif ("rating." in show.lower()):
		rating = show.split("rating.")
		rating = rating[1].strip()
		command = "SELECT TShow FROM TVshowlist WHERE Rating LIKE \"" + rating + "\""
	elif ("duration." in show):
		duration = show.split("duration.")
		duration = int(duration[1].strip())
		command = "SELECT TShow FROM TVshowlist WHERE Duration LIKE \"" + str(duration) + "\""
	else:
		command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"%" + show + "%\""
        cur.execute(command)
        xep = cur.fetchall()
	foundme = []
        try:
                for item in xep:
                       foundme.append(item[0])
		foundme = sorted(foundme)
		if ((len(foundme) >10) and ("-l" not in sys.argv)):
			say = wlistcolumns(foundme)
			for item in echeck:
				if say.lower() == item:
					return say
			setupnext (say)	
		else:
			worklist(foundme)
		say = ("Done.")
        except Exception:
                say = "No results found. Please try again."
        return (say)

def epdetails(show, season, episode):
	plexlogin()
	test = show
	Ssn = season
	Epnum = episode
	shows = plex.library.section("TV Shows")
	theshow = shows.get(show).episodes()
	for ep in theshow:
		if ((int(ep.seasonNumber) == int(Ssn)) and (int(ep.index) == int(Epnum))):
			epname = ep.title
			summary = ep.summary
			showplay = "Episode Name: " + epname + "\nThe Plot Summary is: " + summary
			return showplay
	return ("Error: Show \"" + show + "\" Season: " + season + " Episode: " + episode + " not found.")

def moviedetails(movie):
	movie = titlecheck(movie)
	movie = movie.replace("movie.","")
	if (("ERROR:" in movie) or (movie == "done")):
		return movie
	plexlogin()
	movie = plex.library.section('Movies').get(movie)
	mvname = movie.title
	mvrating = movie.contentRating
	astarring = movie.roles
	for item in astarring:
		try:
			starring = starring + ", " + item.tag
		except NameError:
			starring = item.tag
	adirector = movie.directors
	for item in adirector:
		try:
			director = director + ", " + item.tag
		except NameError:
			director = item.tag
	agenres = movie.genres
	for item in agenres:
		try:
			genres = genres + ", " + item.tag
		except NameError:
			genres = item.tag
	tagline = movie.tagline
	summary = movie.summary
	leftoff = whereleftoff(mvname)
	showplay = "Movie: " + mvname + "\nRated: " + str(mvrating) + "\nStarring: " + starring + " \nDirected By: " + director + "\nGenres: " + genres + "\nTagline: " + tagline + "\nSummary: " + summary + "\n\nResume from minute option: " + str(leftoff) + "."
	return showplay

def moviedbcheck(movie):
	scheck = getsectiontitle(movie)
	if scheck == "Movies":
		movie = movie.replace("movie.","")
		movie = movie.strip()
		command = "SELECT * FROM Movies WHERE Movie LIKE \"" + movie + "\""
		cur.execute(command)
		if not cur.fetchone():
			plexlogin()
			movie = plex.library.section(scheck).get(movie)
			mvname = movie.title
			mvrating = movie.contentRating
			astarring = movie.roles
			for item in astarring:
				try:
					starring = starring + ", " + item.tag
				except NameError:
					starring = item.tag
			adirector = movie.directors
			for item in adirector:
				try:
					director = director + ", " + item.tag
				except NameError:
					director = item.tag
			agenres = movie.genres
			for item in agenres:
				try:
					genres = genres + ", " + item.tag
				except NameError:
					genres = item.tag
			tagline = movie.tagline
			summary = movie.summary
			cur.execute("INSERT INTO Movies VALUES (?,?,?,?,?,?,?)",(mvname,summary,mvrating,tagline,genres,director,starring))
			sql.commit()
			print ("Successfully added " + mvname + " to the movies table.")
	elif scheck == "Commercials":
		movie = movie.replace("playcommercial.","")
		cur.execute("CREATE TABLE IF NOT EXISTS commercials(name TEXT, duration INT)")
		sql.commit()
		command = "SELECT * FROM commercials WHERE Name LIKE \"" + movie + "\""
		cur.execute(command)
		if not cur.fetchone():
			plexlogin()
			movie = plex.library.section(scheck).get(movie)
                        mvname = movie.title
			duration = int(movie.duration)/60000
			cur.execute("INSERT INTO commercials VALUES (?,?)",(mvname,duration))
			sql.commit()
			print ("Successfully added " + mvname + " to the commercials table.")
	elif scheck == "Prerolls":
                movie = movie.replace("preroll.","")
                cur.execute("CREATE TABLE IF NOT EXISTS prerolls(name TEXT, duration INT)")
                sql.commit()
                command = "SELECT * FROM prerolls WHERE Name LIKE \"" + movie + "\""
                cur.execute(command)
                if not cur.fetchone():
                        plexlogin()
                        movie = plex.library.section(scheck).get(movie)
                        mvname = movie.title
                        duration = int(movie.duration)/60000
                        cur.execute("INSERT INTO prerolls VALUES (?,?)",(mvname,duration))
                        sql.commit()
                        print ("Successfully added " + mvname + " to the prerolls table.")
	elif scheck == "show":
		pass
	else:
		tbl = "CUSTOM_" + scheck
		tbl = tbl.replace(" ","_")
		movie = movie.replace("CUSTOM.","")
		#cur.execute("DROP TABLE " + tbl)
		#sql.commit()
		command = "CREATE TABLE IF NOT EXISTS " + tbl + "(name TEXT, duration INT, type TEXT)"
		cur.execute(command)
		sql.commit()
		command = "SELECT * FROM " + tbl + " WHERE Name LIKE \"" + movie + "\""
		cur.execute(command)
		if not cur.fetchone():
                        plexlogin()
                        movie = plex.library.section(scheck).get(movie)
                        mvname = movie.title
                        duration = int(movie.duration)/60000
                        cur.execute("INSERT INTO " + tbl + " VALUES (?,?,?)",(mvname,duration, scheck))
                        sql.commit()
                        print ("Successfully added " + mvname + " to the " + tbl + " table.")
		
		

def epsleft(show):
	show = titlecheck(show)
	if "ERROR" in show:
		return show
	plexlogin()
	fchk = ""
	cshow = show.strip()
	cshow = cshow.replace("movie.","")
	clib = plex.library.sections()
	for video in plex.search(cshow):
		if "stop" not in fchk:
			xshow = video
			if ((xshow.type == "show") and ("movie." not in show) and (xshow.title.lower() == cshow.lower())):
				dbtvcheck(video)
				#getsection(xshow.title)
				SECTION = video.librarySectionID
				xsec = plex.library.sections()
				for lib in xsec:
					if lib.key == SECTION:
						SECTION = lib.title
						schecker = "found"
						show = video.title
						if ("All episodes" in show):
							show = cshow
						fchk = "stop"
	if ("found" in schecker):
		try:
			command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + show + "\""
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
		
		thecount = thecount - 1
		#SECTION = getsection(show)
		shows = plex.library.section(SECTION)
		theshow = shows.get(show).episodes()
		maxs = int(len(theshow))-1
		epleft = maxs - thecount
		return (str(epleft))

def totaleps(show):
	show = titlecheck(show)
        if "ERROR" in show:
                return show
        plexlogin()
        fchk = ""
        cshow = show.strip()
        cshow = cshow.replace("movie.","")
        clib = plex.library.sections()
        for video in plex.search(cshow):
                if "stop" not in fchk:
                        xshow = video
                        if ((xshow.type == "show") and ("movie." not in show) and (xshow.title.lower() == cshow.lower())):
                                dbtvcheck(video)
                                #getsection(xshow.title)
                                SECTION = video.librarySectionID
                                xsec = plex.library.sections()
                                for lib in xsec:
                                        if lib.key == SECTION:
                                                SECTION = lib.title
                                                schecker = "found"
                                                show = video.title
                                                if ("All episodes" in show):
                                                        show = cshow
                                                fchk = "stop"
        if ("found" in schecker):
                shows = plex.library.section(SECTION)
                theshow = shows.get(show).episodes()
		epleft = int(len(theshow))-1
                return (str(epleft))
	


		

def showdetails(show):
	global xlib 
	show = show.replace("'","''")
	command = "SELECT * FROM TVshowlist WHERE TShow LIKE \"" + show + "\""
	cur.execute(command)
	if not cur.fetchone():
		#return ("Error: " + show + " not found. Check title and try again.")
		show = titlecheck(show)
		if (("Error" in show) or (show == "done")):
			return show
		plexlogin()
		nshow = plex.library.section(xlib).get(show)
		name = nshow.title
		summary = nshow.summary
		genres = nshow.genres
		if not genres:
			genres = "Update TBN-Plex DB to get this data."
		rating = nshow.contentRating
		duration = str(int(nshow.duration)/60000)
		#total = str(nshow.leafCount)
		total = totaleps(show)
		whrat = epsleft(show)
		total = total + "\nEpisodes left to watch: " + whrat
		sayme = "For the show: " + name + "\nSummary: " + summary + "\nGenre: " + genres + "\nRating: " + rating + "\nDuration: " + str(duration) + " minutes\nNumber of Episodes: " + str(total)
                return (sayme)
		
		
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
		#total = stuff[5]
		total = totaleps(show)
                whrat = epsleft(show)
                total = total + "\nEpisodes left to watch: " + whrat
		sayme = "For the show: " + name + "\nSummary: " + summary + "\nGenre: " + genres + "\nRating: " + rating + "\nDuration: " + str(duration) + " minutes\nNumber of Episodes: " + str(total)
		return (sayme)

def moviewithtline(tline):
	tline = tline.replace("'","''")
	command = "SELECT Movie, Tagline FROM Movies WHERE Tagline LIKE \"%" + tline.strip() + "%\""
	cur.execute(command)
	if not cur.fetchone():
		return ("No Movies Found with Tagline Like: " + tline)
	cur.execute(command)
	found = cur.fetchall()
	fxd = []
	for fnd in found:	
		tl = fnd[1]
		tl = tl.replace("''","'")
		ttl = fnd[0]
		ttl = ttl.replace("''","'")
		fnd = ttl.strip() + "\n" + tl
		fxd.append(fnd)
	for itm in fxd:
		print (itm + "\n")
	return "\nDone."

def movietagline(movie):
	global xlib
	command = "SELECT Tagline FROM Movies WHERE Movie LIKE \"" + movie + "\""
	cur.execute(command)
	if not cur.fetchone():
		movie = titlecheck(movie)
		if (("Error:" in movie) or (movie == "done")):
			return movie
		movie = movie.replace("movie.","")
		mve = plex.library.section(xlib).get(movie)
		tag = mve.tagline
		if not tag:
			return ("The Move " + movie + " has no tagline.")
		else:
			return tag
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
	sck = randint(0,1)
	if sck == 0:
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
	command = "SELECT Rating FROM Movies WHERE Movie LIKE \"" + movie + "\""
        cur.execute(command)
        if not cur.fetchone():
                return ("Error: " + movie + " not found in DB. Please try again.")
        else:
		try:
			cur.execute(command)
			found = cur.fetchone()[0]
			if "none" in found:
				#return ("The Movie " + movie + " has no rating.")
				return ("No Rating.")
			else:
				#return ("The Movie " + movie + " has a " + found + " rating.")
				return (found)
		except Exception:
			return "The Movie " + movie + " has no rating specified." 

def moviesummary(movie):
	movie = titlecheck(movie)
	movie = movie.replace("movie.","")
	if ("Quit." in movie):
		return ("User Quit. No action taken.")
	elif ("Error:" in movie):
		return (movie)
        command = "SELECT Summary FROM Movies WHERE Movie LIKE \"" + movie + "\""
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
                                #return ("The Movie " + movie + " 's summary is: " + found)
				return found
                except Exception:
                        return "The Movie " + movie + " has no summary in the database."



def setnextep(show, season, episode): #Set the next episode to play in a TV series
	plexlogin()
	show = titlecheck(show)
	if ("Quit." in show):
		return ("User quit. No action taken.")
	elif ("Error:" in show):
		return (show)
	test = show
	Ssn = season
	Epnum = episode
	shows = plex.library.section('TV Shows')
	the_show = shows.get(show).episodes()
	count = 1
	for ep in the_show:
		if((int(ep.seasonNumber) == int(Ssn)) and (int(ep.index) == int(Epnum))):
			xshow = ep.title
			epn = count
			break
		count = count + 1
	try:
		epn
	except NameError:
		return ("Error: Not found.")
	command = "DELETE FROM TVCounts WHERE Show LIKE \"" + show + "\""
	cur.execute(command)
	sql.commit()
	cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, epn))
	sql.commit()
	say = "The Next episode of " + show + " has been set to - " + xshow 
	say = say.rstrip()
	return say

def playspshow(show, season, episode): #Plays a specific episode of a TV show instead of the next in order
	global PLEXCLIENT
	plexlogin()
	test = show
	Ssn = season
	Epnum = episode
	shows = plex.library.section('TV Shows')
	the_show = shows.get(show).episodes()
	for iep in the_show:
		if ((int(iep.seasonNumber) == int(Ssn)) and (int(iep.index) == int(Epnum))):
			ep = str(iep.title)
	the_show = shows.get(show)
	epx = the_show.get(ep)
	client = plex.client(PLEXCLIENT)
	client.playMedia(epx)
	nowplaywrite("TV Show: " + show + " Episode: " + ep)
	CALLMETHIS = gethonorific()
	showsay = 'Playing ' + ep + ' From the show ' + show + ' Now, ' + str(CALLMETHIS)

	return showsay

def movielink(movie):
	plexlogin()
	mve = plex.library.section('Movies').get(movie)
	print mve.getStreamURL(videoResolution='800x600')

def replacestatus(show):
	try:
                command = "SELECT * FROM replaceinblock WHERE name LIKE \"" + show.strip() + "\""
                cur.execute(command)
        except sqlite3.OperationalError:
                cur.execute("CREATE TABLE IF NOT EXISTS replaceinblock(name TEXT, item TEXT, block TEXT, played TEXT)")
                sql.commit()
                return ("replaceinblock table successfully created.")
	cur.execute(command)
	stuff = cur.fetchone()
	if not stuff:
		return ("Show " + show + " is not designated to be replaced in a block.")
	name = stuff[0]
	item = stuff[1]
	item = item.replace(";",", ")
	block = stuff[2]
	played = stuff[3]
	say = "Show to replace: " + name.strip() + "\nReplaced with : " + item.strip() + "\nBlock affected: " + block.strip() + "\nPlaystatus: " + played.strip()
	return say
	

def replacecheck(show):
	theshow = show
	command = "SELECT State FROM States WHERE Option LIKE \"REPLACEWILDCARD\""
	cur.execute(command)
	if not cur.fetchone():
		pass
	else:
		cur.execute(command)
		news = cur.fetchone()[0]
		wcs = listwildcard()
		#print (wcs)
		if wcs.lower() == show.lower():
			#print ("WC FOUND.")
			cur.execute("DELETE FROM States WHERE Option LIKE \"REPLACEWILDCARD\"")
			sql.commit()
			changewildcard(news)
			#return ("done")
	try:
		command = "SELECT item, block, played FROM replaceinblock WHERE name LIKE \"" + show.strip() + "\""
		cur.execute(command)
	except sqlite3.OperationalError:
		cur.execute("CREATE TABLE IF NOT EXISTS replaceinblock(name TEXT, item TEXT, block TEXT, played TEXT)")
		sql.commit()
		print ("replaceinblock table successfully created.")
	cur.execute(command)	
	show = cur.fetchone()
	if not show:
		return ("no")
	block = show[1]
	played = show[2]
	show = show[0]
	olist = show
	cshow = show.split(";")
	nshow = cshow[0]
	if (int(len(cshow))-1 == 0):
		cur.execute("DELETE FROM replaceinblock WHERE name LIKE \"" + theshow + "\"")
		sql.commit()
		newlist = olist.replace(nshow+";","")
		replaceinblock(block,nshow,theshow)
	else:
		newlist = olist.replace(nshow+";","")
		replaceinblock(block,nshow,theshow)
		if ("yes" in played):
			cur.execute("DELETE FROM replaceinblock WHERE name LIKE \"" + theshow + "\"")
			sql.commit()
			cur.execute("INSERT INTO replaceinblock VALUES (?,?,?,?)",(nshow,newlist,block,played))
			sql.commit()
		else:
			cur.execute("DELETE FROM replaceinblock WHERE name LIKE \"" + theshow + "\"")
                        sql.commit()
			show = show.replace("CUSTOM.","")
			cur.execute("INSERT INTO replaceinblock VALUES (?,?,?,?)",(theshow,olist,block,"yes"))
                        sql.commit()
	say = "done"	
	return say

def replacewildcard(name):
	show = titlecheck(name)
	if ("ERROR:" in show):
		return show
	cur.execute("DELETE FROM States WHERE Option LIKE \"REPLACEWILDCARD\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("REPLACEWILDCARD",show))
	sql.commit()
	return ("The next wild card show will be: " + show )
	

def replaceshowinblock(show, nshow, block, playflag):
	tshow = show
	rcheck = replacestatus(show)
	command = "SELECT name FROM Blocks WHERE Name LIKE \"" + block + "\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: " + block + " not found. Check and try again.")
	show = titlecheck(show)
	nshow = titlecheck(nshow)
	#rcheck = replacecheck(show)
	if ("not designated to be replaced" in rcheck):
		cur.execute("INSERT INTO replaceinblock VALUES (?,?,?,?)",(show.strip(),nshow.strip(),block.strip(),playflag.strip()))
                sql.commit()
		return (show + " will be replaced by " + nshow + " in the " + block + " block.")
	else:
		command = "SELECT * FROM replaceinblock WHERE name LIKE \"" + show.strip() + "\""
		cur.execute(command)
		stuff = cur.fetchall()[0]
		name = stuff[0]
		item = stuff[1]
		item = item + ";" + nshow.strip()
		block = stuff[2]
		playstatus = stuff[3]
		cur.execute("DELETE FROM replaceinblock WHERE name LIKE \"" + tshow + "\"")
		sql.commit()
		cur.execute("INSERT INTO replaceinblock VALUES (?,?,?,?)",(name,item,block,playstatus))
		sql.commit()
		return (nshow + " has been associated with " + block + " and " + name + " for replacement purposes.")
		

def playholiday(holiday):
	try:
		cur.execute("SELECT State FROM States WHERE Option LIKE \"NEXTHOLIDAY\"")
		show = cur.fetchone()[0]
		cur.execute("DELETE FROM States WHERE Option LIKE \"NEXTHOLIDAY\"")
		sql.commit()
		if "movie." in show:
			playshow(show)
			return ("Playing " + show + " for the holiday " + holiday + " now.")
		else:
			title = show
			title = title.split(":")
			ssn = title[1].strip()
			ep = title[2].strip()
			title = title[0].strip()
			playspshow(title, ssn, ep)
			return "Playing " + title + " for the holiday " + holiday + " now."
	except Exception:
		holiday = holiday.replace("holiday.","")
		cur.execute("SELECT items FROM Holidays WHERE name LIKE \"" + holiday.strip() + "\"")
		titles = cur.fetchone()[0]
		titles = titles.split(";")
		ttls = []
		for item in titles:
			if item != "":
				ttls.append(item)
		min = 0
		max = int(len(ttls)) - 1
		pcnt = randint(min,max)
		plexlogin()
		if "movie." in ttls[pcnt]:
			playshow(ttls[pcnt])
			return "Playing " + ttls[pcnt] + " for the holiday " + holiday + " now."
		else:
			title = ttls[pcnt]
			title = title.split(":")
			ssn = title[1].strip()
			ep = title[2].strip()
			title = title[0].strip()
			playspshow(title, ssn, ep)
			return "Playing " + title + " for the holiday " + holiday + " now."

def getgenres(show, section):
        global TVGET
	TVGET = section.strip()
        if not cur.fetchone():
                cur.execute("SELECT setting FROM settings WHERE item LIKE \"PLEXSERVERIP\"")
                wlink = cur.fetchone()[0]
                cur.execute("SELECT setting FROM settings WHERE item LIKE \"PLEXSERVERPORT\"")
                wip = cur.fetchone()[0]
                slink = "http://" + wlink + ":" + wip + "/library/sections/"
                response = http.urlopen('GET', slink, preload_content=False).read()
                response = str(response)
                response = response.split("Directory allowSync=")
                for item in response:
                        try:
                                name = item
                                section = item
                                name = name.split("title=\"")
                                name = name[1]
                                name = name.split("\"")
                                name = name[0]
				if name.lower() == TVGET.lower():
					section = section.split("key=\"")
					section = section[1]
					section = section.split("\"")
					section = section[0]

					link = "http://" + wlink + ":" + wip + "/library/sections/" + section + "/all/"
					TVGENREFIX = link
                        except IndexError:
                                pass
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
                if (title.lower().strip() == show.lower().strip()):
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

def deleteshow(show):
	command = "DELETE FROM TVshowlist WHERE TShow LIKE \"" + show + "\""
	cur.execute(command)
	sql.commit()
	return ("Done.")

def playshow(show): #Plays the next episode of a specified TV show
	#SECTION = "TV Shows"
	oshow = show
	if (("block." not in show) and ("custom." not in show) and ("marathon." not in show) and ("minithon." not in show) and ("holiday." not in show)):
		show = titlecheck(show)
		show = checkcustomtables(show)
	if type(show) is tuple:
		show = show[0].lower()
	if "custom." in show:
		show = show.replace("custom.","")
		show = checkcustomtables(show)
		table = show[1].strip()
		show = show[0]
		show = show.replace("CUSTOM.","")
		plexlogin()
		say = playcustom(show, table)
		return say
	else:
		show = oshow
	global PLEXCLIENT
	global pcmd
	kcheckshow = checkmode("show")
	kcheckmovie = checkmode("movie")
	show = show.replace("''","'")

	sayshow = show
	sayshow = sayshow.replace("movie.","The Movie ")
	sayshow = sayshow.replace("preroll.","The Preroll: " )
	sayshow = sayshow.replace("CUSTOM.","")
	sayshow = sayshow.replace("playcommercial.","The Commercial: ")
	if ("ERROR:" in sayshow):
		return sayshow
	printmode()
	if (PRINTMODE == "ON"):
		print ("Trying to start: " + sayshow + "\n")
	try:
		plexlogin()
		fchk = ""
		cshow = show.strip()
		cshow = cshow.replace("movie.","")
		clib = plex.library.sections()
		for video in plex.search(cshow):
			if "stop" not in fchk:
				xshow = video
				if ((xshow.type == "show") and ("movie." not in oshow) and (xshow.title.lower() == cshow.lower())):
					dbtvcheck(video)
					#getsection(xshow.title)
					SECTION = video.librarySectionID
					xsec = plex.library.sections()
					for lib in xsec:
						if lib.key == SECTION:
							if video.type == "episode":
								#markme
								SECTION = lib.title
                                                                schecker = "found"
                                                                show = video.title
								show = cshow
							else:
								SECTION = lib.title
								schecker = "found"
								show = video.title
								if ("All episodes" in show):
									show = cshow
								fchk = "stop"
				elif ((xshow.type.lower() == "movie") and (xshow.title.lower() == cshow.lower()) and ("stop" not in fchk)):
					moviedbcheck(video.title)
					SECTION = video.librarySectionID
					xsec = plex.library.sections()
					show = video.title
					for lib in xsec:
						if lib.key == SECTION:
							SECTION = lib.title
							#schecker = "found"
					if ("movie." not in show):
						show = "movie." + show.strip()	
					mck = "found"
		try:
			schecker
		except Exception:
			schecker = "lost"
	except TypeError:
		schecker = "lost"
	#else:
		#SECTION = "TV Shows"
		#schecker = "found"

	try:
		schecker
	except NameError:
		schecker = "lost"
	try:
		mck
	except NameError:
		mck = "nogo"
	#print (show)
		
	if ("found" in schecker):
		if ("Kids" in kcheckshow):
			kcheck = kidscheck("show",show)
			if "fail" in kcheck.lower():
				print ("Kids mode fail:" + show)
				try:
					if ("playme" not in pcmd):
						skipthat()
				except Exception:
					skipthat()
				return ("Kids mode is currently active. Unable to start " + show + ". It has been skipped.")
		try:
			command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + show + "\""
			cur.execute(command)
			thecount = cur.fetchone()
			thecount = thecount[0]
		except Exception:
			printmode()
			if PRINTMODE == "ON":
				print ("Item not found in DB. Adding")
			thecount = 1 
			cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecount))
			sql.commit()

		if thecount == 0:
			thecount = 1
		
		thecount = thecount - 1
		#SECTION = getsection(show)
		shows = plex.library.section(SECTION)
		theshow = shows.get(show).episodes()
		xshow = theshow[thecount].title
		if (int(thecount)+1 > int(len(theshow))-1):
			rcheck = replacecheck(show.lower())	
			thecountx = 1
		else:
			thecountx = thecount + 2
		command = "DELETE FROM TVCounts WHERE Show LIKE \"" + show + "\""
		cur.execute(command)
		cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, thecountx))
		sql.commit()	
		thecount = str(thecount)
	
		shows = plex.library.section(SECTION)
		show = show.replace("''","'")
		xshow = xshow.replace("''","'")
		the_show = shows.get(show)
		ep = the_show.get(xshow)
		client = plex.client(PLEXCLIENT)
		client.playMedia(ep)
		nowplaywrite("TV Show: " + show + " Episode: " + xshow)
		CALLMETHIS = gethonorific()
		showsay = 'Playing ' + xshow + ' From the show ' + show + ' Now, ' + CALLMETHIS 
		
		return showsay
	elif ("minithon." in show):
		show = show.replace("minithon.","")
		show = titlecheck(show)
		if ("Quit." in show):
			return show
		elif ("Error: " in show):
			return show
		command = "SELECT State FROM States WHERE Option LIKE \"MINITHONCNT\""
		cur.execute(command)
		if not cur.fetchone():
			MINITHONCNT = 1
		else:
			cur.execute(command)
			MINIITHONCNT = int(cur.fetchone()[0])
			cur.execute("DELETE FROM States WHERE Option LIKE \"MINITHONCNT\"")
			sql.commit()
		MINITHONCNT = MINITHONCNT + 1
		command = "SELECT State FROM States WHERE Option LIKE \"MINITHONMAX\""
		cur.execute(command)
		if not cur.fetchone():
			MINITHONMAX = 3
		else:
			cur.execute(command)
			MINITHONMAX = cur.fetchone()[0]
			MINITHONMAX = int(MINITHONMAX)
		if MINITHONCNT <= MINITHONMAX:
			cur.execute("INSERT INTO States VALUES (?,?)",("MINITHONCNT",str(MINITHONCNT)))
			sql.commit()
		else:
			setplaymode("normal")
			print ("Mini-marathon has been played out. Returning to normal mode.")
		say = playshow(show)
		
	
		return (say)	
	elif ("movie." in show):
		if ("Kids" in kcheckmovie):
                        kcheck = kidscheck("movie",show)
                        if "fail" in kcheck.lower():
				print ("Kids show fail: " + show)
                                #skipthat()
                                return ("Kids mode is currently active. Unable to start " + show + ". It has been skipped.")
		show = show.replace("movie.", "")
		command = "SELECT Movie FROM Movies WHERE Movie like\"" + show + "\""
		cur.execute(command)
		if not cur.fetchone():
			if "nogo" in mck:
				return ("Error: " + show + " not found to launch.")
			else:
				mvs = show
		else:
			cur.execute(command)
			mvs = cur.fetchone()[0]
		if mvs.lower() == show.lower():
			show = mvs
			show = show.rstrip()
			show = show.replace("''","'")
			movie = plex.library.section(SECTION).get(show)
			client = plex.client(PLEXCLIENT)
			client.playMedia(movie)
			#playfile(show)
			showplay = show
			nowplaywrite("Movie: " + showplay)
			
			CALLMETHIS = gethonorific()
			return ("Playing the movie " + show + " now, " + CALLMETHIS + ".") 
		return ("Error. " + show + " Not found!")
	elif ("block." in show):
		say = playblockpackage(show)
		show = show.replace("_", " ")
		return ("Starting " + say)
	elif ("holiday." in show):
		say = playholiday(show)
		return (say)
	else:
		
		return ("Media not found to launch. Check the title and try again.")

def musicstartnext():
	plexlogin()
        PLEXMUSICCLIENT = musiccheck()
        client = plex.client(PLEXMUSICCLIENT)
	client.skipNext('music')

def musiccheck():
	command = "SELECT setting FROM settings WHERE item LIKE \"PLEXMUSICCLIENT\""
        cur.execute(command)
        if not cur.fetchone():
                print ("No Music Client is specified. Client for music playback: ")
                setmusicclient()
        cur.execute(command)
        PLEXMUSICCLIENT = cur.fetchone()[0]
	return (PLEXMUSICCLIENT)

def playmusic(artist, show):
	plexlogin()
	PLEXMUSICCLIENT = musiccheck()
	client = plex.client(PLEXMUSICCLIENT)
	songs = plex.library.section("Music").get(artist)
	if ("none" not in show):
		title = songs.get(show)
	else:
		title = plex.library.section("Music").get(artist)
	client.playMedia(title)

def playplaylist(playlist):
	playlist = playlist.lower()
	plexlogin()
	PLEXMUSICCLIENT = musiccheck()
	client = plex.client(PLEXMUSICCLIENT)
	for plist in plex.playlists():
		if playlist == str(plist.title).lower():
			playlist = plist.title
			title = plex.playlist(playlist)
			client.playMedia(title)
			return ("Now playing: " + playlist)
	return ("Error: " + playlist + " not found to play.")

def blocktoplist(block):
	command = "SELECT Items FROM Blocks WHERE Name LIKE \"" + block + "\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: Block not found.")
	cur.execute(command)
	list = cur.fetchone()[0]
	cur.execute("SELECT Count FROM Blocks WHERE Name LIKE \"" + block + "\"")
	count = cur.fetchone()[0]
	count = int(count)
	list = list.split(";")
	queue = []
	ccnt = 0
	rset = "no"
	for item in list:
		if ((item == "") or (ccnt < count)):
			pass
		elif (("random_" in item) and (rset == "yes")):
			pass
		else:
			if ('random_movie.' in item):
				item = idtonightsmovie()
				if ("movie." not in item):
					item = "movie." + item
				rset = "yes"
			elif ("random_tv." in item):
				item = idtonightsshow()
				rset = "yes"
			queue.append(item)
		ccnt = ccnt + 1
	if len(queue) > 0:
                try:
                        removeplaylist("TBNqueue")
                except Exception:
                        pass
        addme = queue[0]
        addvideoplaylist("TBNqueue",addme)
        if len(queue) > 1:
                cnt = 0
                for item in queue:
                        if cnt == 0:
                                pass
                        else:
                                modifyvideoplaylist("TBNqueue",item, "add")
                        cnt = cnt + 1
        return ("Done")

def addplaylist(title, artist, song):
	plexlogin()
        songs = plex.library.section("Music").get(artist)
        if ("none" not in show):
                item = songs.get(song)
        else:
                item = plex.library.section("Music").get(artist)
	plex.createPlaylist(title,item)
	return ("Done")
	return (item + " not found to add to playlist.")

def addvideoplaylist(title, item):
	plexlogin()
	item = item.lower()
	if "movie." in item:
		item = item.replace("movie.","")
		movie = plex.library.section("Movies").get(item)
		plex.createPlaylist(title,movie)
	elif ("custom." in item):
                item = item.replace("custom.","")
                stuff = checkcustomtables(item)
                table = stuff[1].strip()
                item = stuff[0]
                item = item.replace("CUSTOM.","")
                if ("''" in item):
                        item = item.replace("''","'")
                item = plex.library.section(table).get(item)
		plex.createPlaylist(title,item)
	elif ("preroll" in item):
                if item == "preroll":
                        cur.execute("SELECT * FROM commercials WHERE name LIKE \"" + commercial + "\"")
                        found = cur.fetchall()
                        max = int(len(found)) - 1
                        min = 0
                        pcnt = randint(min,max)
                        playme = found[pcnt]
                        item = playme[0]
                else:
                        item = item.replace("preroll.","")
                table = "Prerolls"
                item = plex.library.section(table).get(item)
		plex.createPlaylist(title,item)
        elif ("playcommercial" in item):
                if item == "playcommercial":
                        cur.execute("SELECT * FROM commercials WHERE name LIKE \"" + commercial + "\"")
                        found = cur.fetchall()
                        max = int(len(found)) - 1
                        min = 0
                        pcnt = randint(min,max)
                        playme = found[pcnt]
                        item = playme[0]
                else:
                        item = item.replace("playcommercial.","")
                table = "Commercials"
                item = plex.library.section(table).get(item)
		plex.createPlaylist(title,item)
	else:
		show = item
		try:
                        command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + show + "\""
                        cur.execute(command)
                        thecount = cur.fetchone()
                        thecount = thecount[0]
                except Exception:
			if PRINTMODE == "ON":
				print ("Item not found in DB. Adding")
                        thecount = 1
                        cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecount))
                        sql.commit()

                if thecount == 0:
                        thecount = 1
		shows = plex.library.section('TV Shows')
		show = show.replace("''","'")
		the_show = shows.get(show).episodes()
		xshow = the_show[thecount-1]

                the_show = shows.get(show)
                ep = the_show.get(xshow)
		plex.createPlaylist(title,ep)

def modifyvideoplaylist(playlist, item, action):
	playlist = plex.playlist(playlist)
	item = item.lower()
	if "movie." in item:
                item = item.replace("movie.","")
                movie = plex.library.section("Movies").get(item)
		if action == "add":
			playlist.addItems(movie)
		else:
			playlist.removeItem(movie)
	elif ("custom." in item):
		item = item.replace("custom.","")
		stuff = checkcustomtables(item)
		table = stuff[1].strip()
		item = stuff[0]
		item = item.replace("CUSTOM.","")
		if ("''" in item):
			item = item.replace("''","'")
		item = plex.library.section(table).get(item)
		if (action == "add"):
			playlist.addItems(item)
		else:
			playlist.removeItem(item)
	elif ("preroll" in item):
		if item == "preroll":
			cur.execute("SELECT name FROM prerolls")
			found = cur.fetchall()
			max = int(len(found)) - 1
			min = 0
			pcnt = randint(min,max)
			playme = found[pcnt]
			item = playme[0]
		else:
			item = item.replace("preroll.","")
		table = "Prerolls"
		item = plex.library.section(table).get(item)
		if action == "add":
			playlist.addItems(item)
		else:
			playlist.removeItem(item)
	elif ("playcommercial" in item):
		if item == "playcommercial":
			cur.execute("SELECT name FROM commercials")
			found = cur.fetchall()
			max = int(len(found)) - 1
			min = 0
			pcnt = randint(min,max)
			playme = found[pcnt]
			item = playme[0]
		else:
			item = item.replace("playcommercial.","")
                table = "Commercials"
                item = plex.library.section(table).get(item)
		if action == "add":
			playlist.addItems(item)
		else:
			playlist.removeitem(item)
        else:
                show = item
                try:
                        command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + show + "\""
                        cur.execute(command)
                        thecount = cur.fetchone()
                        thecount = thecount[0]
                except Exception:
			if PRINTMODE == "ON":
				print ("Item not found in DB. Adding")
                        thecount = 1
                        cur.execute('INSERT INTO TVCounts VALUES(?,?)', (show, thecount))
                        sql.commit()

                if thecount == 0:
                        thecount = 1
		shows = plex.library.section('TV Shows')
                show = show.replace("''","'")
                the_show = shows.get(show).episodes()
                xshow = the_show[thecount-1]
                show = show.replace("''","'")
                xshow = xshow.replace("''","'")
                the_show = shows.get(show)
                ep = the_show.get(xshow)
		if action == "add":
			playlist.addItems(ep)
		else:
			playlist.removeItem(ep)

def removeplaylist(plist):
	plexlogin()
	title = plex.playlist(plist)
	title.delete()

def addtoplaylist(title, artist, song):
	plexlogin()
        songs = plex.library.section("Music").get(artist)
        if ("none" not in show):
                item = songs.get(song)
        else:
                item = plex.library.section("Music").get(artist)
	title = plex.playlist(title)
	title.addItems(item)
        return ("Done")

def queuetoplaylist():
	plexlogin()
	command = "SELECT State FROM States WHERE Option LIKE \"queue\""
	cur.execute(command)
	xqueue = cur.fetchone()[0]
	xqueue = xqueue.split(";")
	queue = []
	for item in xqueue:
		if item != "":
			queue.append(item)
	if len(queue) > 0:
		try:
			removeplaylist("TBNqueue")
		except Exception:
			pass
	addme = queue[0]
	addvideoplaylist("TBNqueue",addme)
	
	if len(queue) > 1:
		cnt = 0
		for item in queue:
			if cnt == 0:
				pass
			else:
				modifyvideoplaylist("TBNqueue",item, "add")
			cnt = cnt + 1
		
	return ("Done")
	

def listplaylistitems(plist):
	plexlogin()
	thelist = plex.playlist(plist)
	stuff = thelist.items()
	songs = []
	for things in stuff:
		songs.append(things.title)
	wlistcolumns(songs)

def getartists():
	plexlogin()
	items = plex.library.section("Music")
	atists = items.searchArtists()
	artists = []
	for item in atists:
		item = item.title
		if item not in artists:
			artists.append(item)
	return artists

def getalbums(artist):
	plexlogin()
	item = plex.library.section("Music").get(artist)
	albums = []
	albms = item.albums()
	for thing in albms:
		thing = thing.title
		albums.append(thing)
	return albums	

def getsongs(artist, album):
	plexlogin()
	item = plex.library.section("Music").get(artist)
	albm = item.albums()
	for thing in albm:
		if thing.title.lower() == album.lower():
			songs = thing.tracks()
	sngs = []
	for itm in songs:
		itm = itm.title
		sngs.append(itm)
	return sngs

def getplexplaylists():
	plexlogin()
	playlsts = []
	for plist in plex.playlists():
		playlsts.append(plist.title)
	return playlsts

def progressfunct(num):
	count = 0
	while count < num:
		time.sleep(1)
		count = count + 1
		sys.stdout.write("\r" + str(count) + " out of " + str(num))
		sys.stdout.flush()

def commercialcheck():
	command = "SELECT * FROM States WHERE Option LIKE \"COMMERCIALMODE\""
	cur.execute(command)
        if not cur.fetchall():
		print ("Commercial Mode not set. Setting to Off")
		cur.execute("DELETE FROM States WHERE Option LIKE \"COMMERCIALMODE\"")
		sql.commit()
                cur.execute("INSERT INTO States VALUES (?,?)",("COMMERCIALMODE","Off"))
                sql.commit()
        cur.execute(command)
        check = cur.fetchone()[1]
	return check

def setcommercialbreakcount(number): #Sets the number of commercials to play when the commercialbreak command is issued
	cur.execute("SELECT * FROM commercials")
	if not cur.fetchall():
		return ("Error: not enough commercials in the commercials table to use that setting.")
	else:
		cur.execute("SELECT * FROM commercials")
		found = cur.fetchall()
		if ((int(len(found))-1) < int(number)):
			return ("Error: not enough commercials in the commercials table to use that setting.")
	command = "DELETE FROM States WHERE OPTION LIKE \"COMMERCIALBREAK\""
	cur.execute(command)
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("COMMERCIALBREAK",int(number)))
	sql.commit()
	return ("COMMERCIALBREAKCOUNT has been set to: " + str(number))

def commercialbreak(): #forces a commercial break to stop the current program and play commercials
	cur.execute("SELECT State FROM States WHERE Option LIKE \"COMMERCIALBREAK\"")
	if not cur.fetchone():
		print ("No commercial break settings found. Settings to 2.")
		cur.execute("INSERT INTO States VALUES(?,?)",("COMMERCIALBREAK","2"))
		sql.commit()
	cur.execute("SELECT State FROM States WHERE Option LIKE \"COMMERCIALBREAK\"")
	COMMERCIALBREAK = cur.fetchone()[0]
	playme = []
	ccnt = 1
	while ccnt <= int(COMMERCIALBREAK):
		playc = getcommercial()
		if playc not in playme:
			playme.append(playc)
			ccnt = ccnt + 1
			#print ("Adding " + playc + " to commercial queue.")
	nowp = nowplaying()
	if (("Now playing: " in nowp) and ("Episode: " not in nowp)):
		nowp = nowp.split("Now playing: ")
		nowp = nowp[1].strip()
		type = "movie"
	elif (("Now Playing: " in nowp) and ("Episode: " in nowp)):
		nowp = nowp.split("Now Playing: ")
		nowp = nowp[1].strip()
                nowp = nowp.split("Episode: ")
                show = nowp[0].strip()
                nowp = nowp[1].strip()
                type = "show"
	else:
		nowp = nowp.split("TV Show: ")
		nowp = nowp[1].strip()
		nowp = nowp.split("Episode: ")
		show = nowp[0].strip()
		nowp = nowp[1].strip()
		type = "show"
	if type == "show":
		whrat = whereat()
		whrat = whrat.split(" minute ")
		whrat = whrat[1]
		whrat = whrat.split(" out of ")
		whrat = whrat[0].strip()
		whrat = int(whrat)*60000
	openme = homedir + 'playstatestatus.txt'
	with open(openme, "r") as file:
		checkme = file.read()
	file.close()
	if "On" in checkme:
		playcheckstop()
	pcnt = 1
	while pcnt <= int(COMMERCIALBREAK):
		cur.execute("SELECT duration FROM commercials WHERE name LIKE \"" + playme[pcnt-1] + "\"")
		duration = cur.fetchone()
		duration = duration[0]
		try:
			ppc
		except Exception:
			ppc = "no"
		if ("yes" not in ppc):
			#print (playme[pcnt-1])
			playcommercial(playme[pcnt-1])
		pcnt = pcnt + 1
		if int(duration) >= 60:
			if (ppc == "no"):
				pcnt = pcnt + 1
				ppc = "yes"
		else:
			ppc = "no"
	if type == "show":
		plexlogin()
		whrat = int(whrat)
		shows = plex.library.section('TV Shows')
		the_shows = shows.get(show)
		ep = the_shows.get(nowp)
		client = plex.client(PLEXCLIENT)
		client.playMedia(ep, offset=whrat)
	else:
		playwhereleftoff(nowp, "none")
	if "On" in checkme:
		time.sleep(SLEEPTIME)
		playcheckstart()

def getcommercial():
	cur.execute("SELECT * FROM commercials")
	found = cur.fetchall()
        max = int(len(found)) - 1
        min = 0
        pcnt = randint(min,max)
        playme = found[pcnt]
        show = playme[0]
	return show

def playcommercial(commercial): #Play a commerical
	global plex
	global client
	global PLEXCLIENT
	plexlogin()
	if commercial == "none":
		cur.execute("SELECT * FROM commercials")
	else:
		cur.execute("SELECT * FROM commercials WHERE name LIKE \"" + commercial + "\"")
	found = cur.fetchall()
	if not found:
		return ("Failed to start: " + commercial + ". Check this item and its entry in your plex library.\n")
	if commercial == "none":
		max = int(len(found)) - 1
		min = 0
		pcnt = randint(min,max)
		playme = found[pcnt]
		show = playme[0]
		duration = playme[1]
		duration = int(duration) + 1
	else:
		playme = found[0]
		show = playme[0]
		duration = playme[1]
		duration = int(duration) + 1
	commercial = plex.library.section('Commercials').get(show)
	client = plex.client(PLEXCLIENT)
	try:
		nowplaywrite(str(show))
		client.playMedia(commercial)
		if ("Fail" in externalcheck()):
			time.sleep(duration)
		else:
			try:
				progressfunct(duration)
			except KeyboardInterrupt:
				print ("\rCancelling Commercial.\n")
		return ("Done.")
	except Exception:
		return ("Failed to start: " + show + ". Check this item and its entry in your plex library.\n")

def playcustom(show, table):
	plexlogin()
	if ("''" in show):
		show = show.replace("''","'")
	commercial = plex.library.section(table).get(show)
        client = plex.client(PLEXCLIENT)
        client.playMedia(commercial)
	return ("Now Playing : " + show)

def playpreroll(preroll):
	global plex
        global client
        global PLEXCLIENT
        plexlogin()
	if preroll == "none":
		cur.execute("SELECT * FROM prerolls")
	else:
		cur.execute("SELECT * FROM prerolls WHERE name LIKE \"" + preroll + "\"")
        fnd = cur.fetchall()
        max = int(len(fnd)) - 1
        min = 0
        pcnt = randint(min,max)
        plyme = fnd[pcnt]
        shw = plyme[0]
        durn = plyme[1]
        durn = int(durn) + 1
        commercial = plex.library.section('Prerolls').get(shw)
        client = plex.client(PLEXCLIENT)
        client.playMedia(commercial)
	if ("Fail" in externalcheck()):
		time.sleep(durn)
	else:
		try:
			progressfunct(durn)
		except KeyboardInterrupt:
			print ("\nCancelling Preroll.\n")

def listprerolls():
	echeck = ['quit','error','no']
	cur.execute("SELECT name FROM prerolls")
	list = cur.fetchall()
	prelist = []
	for item in list:
		item = item[0].strip()
		if item not in prelist:
			prelist.append(item)	
	if ((len(prelist) >10) and ("-l" not in sys.argv)):
		say = wlistcolumns(prelist)
		for item in echeck:
			if say.lower() == item:
				return say
	else:
		worklist(prelist)

def listcommercials():
	echeck = ['quit','error','no']
	cur.execute("SELECT name FROM commercials")
	list = cur.fetchall()
	prelist = []
	for item in list:
		item = item[0].strip()
		if item not in prelist:
			prelist.append(item)
	if ((len(prelist) >10) and ("-l" not in str(sys.argv))):
                say = wlistcolumns(prelist)
                for item in echeck:
                        if say.lower() == item:
                                return say
        else:
		say = worklist(prelist)
	if ((say == "done") or ("Done." in say)):
		pass
	else:
		playcommercial(say)

def whereleftoff(item):
	global plex
	if "movie." in item:
		plexlogin()
		item = item.replace("movie.","")
		command = "SELECT Movie FROM Movies WHERE Movie LIKE \"" + item.strip() + "\""
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
			command = "SELECT Count FROM Blocks WHERE Name LIKE \"" + thing + "\""
			cur.execute(command)
			foundc = cur.fetchone()[0]
			if not foundc:
				return ("Block not found. Try again.")
			else:
				command = "SELECT Items FROM Blocks WHERE Name Like \"" + thing + "\""
				cur.execute(command)
				items = cur.fetchone()[0]
				items = items.split(';')
				found = items[foundc]
				return ("Up next is item " + str(foundc + 1) + ":\n" + found)
		return (0)

def getshowleftoff(show, episode):
	show = show.strip()
	xshow = episode.strip()
	global PLEXCLIENT
	plexlogin()
	shows = plex.library.section('TV Shows')
	the_show = shows.get(show)
	#showplay = the_show.rstrip()
	ep = the_show.get(xshow)
	return (ep.viewOffset)
	

def playwhereleftoff(show, nvalue):
	global PLEXCLIENT
	plexlogin()
	show = show.replace(";;","'")
	show = titlecheck(show)
	if nvalue == "none":
		nvalue = 0
	else:
		nvalue = int(nvalue) * 1000
	leftoff = int(whereleftoff(show)) * 60000
	leftoff = leftoff + nvalue
	command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"" + show + "\""
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
			command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + show + "\""
			cur.execute(command)
			thecount = cur.fetchone()
			thecount = thecount[0]
		except Exception:
			if PRINTMODE == "ON":
				print ("Item not found in DB. Adding")
			thecount = 1 
			cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, thecount))
			sql.commit()
			if PRINTMODE == "ON":
				print ("added")

		if thecount == 0:
			thecount = 1
		
		shows = plex.library.section('TV Shows')
		the_show = shows.get(show).episodes()
		xshow = the_show[thecount-1].title
		if int(len(the_show))-1 >= thecount +1:
			thexcount = 1
			rcheck = replacecheck(show)
		else:
			thexcount = thecount + 1

		command = "DELETE FROM TVCounts WHERE Show LIKE \"" + show + "\""
		cur.execute(command)
		cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, thexcount))
		sql.commit()
		shows = plex.library.section('TV Shows')
		the_show = shows.get(show)
		#showplay = the_show.rstrip()
		ep = the_show.get(xshow)
		leftoff = ep.viewOffset + nvalue
		client = plex.client(PLEXCLIENT)
		client.playMedia(ep, offset=leftoff)
		nowplaywrite("TV Show: " + show + " Episode: " + xshow)
		CALLMETHIS = gethonorific()
		showsay = 'Playing ' + xshow + ' From the show ' + show + ' Now, ' + CALLMETHIS 
		return showsay
	elif ("movie." in show):
		show = show.replace("movie.", "")
		command = "SELECT Movie FROM Movies WHERE Movie like\"" + show + "\""
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
				CALLMETHIS = gethonorific()
				return ("Playing the movie " + show + " now, " + CALLMETHIS + ".") 
		return ("Error. " + show + " Not found!")
	elif ("block." in show):
		say = playblockpackage(show)
		show = show.replace("_", " ")
		return ("Starting " + say)
	else:
		return ("Media not found to launch. Check the title and try again.")


def queueadd(addme):
        title = addme
	if type(title) is tuple:
		title = title[0]
	title = title.replace("custom.","")
	title = checkcustomtables(title)
        if type(title) is tuple:
                title = title[0]
	xtype = "queue"
	if ("block." in title):
		title = title.replace("block.","")
		name = verifyblock(title)
		name = "block." + name
		
	elif ("CUSTOM." not in title):
		if (("numb3rs" not in title.lower()) and ("se7en" not in title.lower())):
			title = titlecheck(title).strip()
			title = title.replace("'","")
			name = title
			if ("ERROR:" in name):
				return name
			#xname = xname.replace('movie.','')
			if ("addrand" in addme):
				say = queuefill()
			elif ("Quit." in addme):
				say = "User quit. No action taken."
				return (say)
	else:
		name = title

	if ("User Quit" in name):
		return (name)
	elif ("Error:" in name):
		return (name)

	if ("movie." in name):
		xname = name + ";"
		command = "SELECT State FROM States WHERE Option LIKE \"" + xtype + "\""
		cur.execute(command)
		queue = cur.fetchone()
		queue = queue[0]
		if not queue:
			queue = xname
		else:
			queue = queue + xname
		command = "DELETE FROM States WHERE Option LIKE \"" + xtype + "\""
		cur.execute(command)
		sql.commit()
		cur.execute("INSERT INTO States VALUES(?,?)", (xtype, queue))
		sql.commit()	
		xname = xname.replace("movie.","")
		xname = xname.replace(";","")
		say = xname.strip()
		return say	
		
	else:
		xname = name
		xname = xname + ";"
		command = "SELECT State FROM States WHERE Option LIKE \"" + xtype + "\""
		cur.execute(command)
		queue = cur.fetchone()
		queue = queue[0]
		if not queue:
			queue = xname
		else:
			queue = queue + xname
		command = "DELETE FROM States WHERE Option LIKE \"" + xtype + "\""
		cur.execute(command)
		cur.execute("INSERT INTO States VALUES(?,?)", (xtype, queue))
		sql.commit()
		xname = xname.replace(";","")

		if ("CUSTOM." in xname):
			say = ("The TV Show " + xname.rstrip() + " has been added to the queue.")
		else:
			xname = xname.replace("CUSTOM.","")
			say = (xname)
		return say

def nowplaywrite(showplay):
	cur.execute("DELETE FROM States WHERE Option LIKE \"Nowplaying\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",('Nowplaying',showplay))
	sql.commit()

def nowpdb():
	cur.execute("SELECT State FROM States WHERE Option LIKE \"Nowplaying\"")
	nowp = cur.fetchone()[0]
	return nowp

def nowplaying():
	global plex
	plexlogin()
	psess = plex.sessions()
	for sess in psess:
		#sess.myPlexUsername 
		if (sess.player.title == PLEXCLIENT):
			if "episode" in sess.type:
				say = "Now Playing: " + sess.grandparentTitle.strip() + "\nEpisode: " + sess.title.strip()
			else:
				say = "Now playing: " + sess.title
		else:
			#print (vars(sess))
			if ("nowplaying" in sys.argv):
				print (sess.username + " is playing " + sess.title + " on " + sess.player.title)
			else:
				pass
	try:
		say
	except NameError:
		say = "Nothing is currently playing on " + PLEXCLIENT + "."
	return (say)

def queueget():
	name = "queue"
	command = "SELECT State FROM States WHERE Option LIKE \"" + name + "\""
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]

	
	if (queue == ""):
		queue = queuefill()

	queue = queue.replace(";", ", and then ")
	queue = queue.replace("movie.", "The Movie ")
	queue = queue.replace(' has been added to the queue.',', and then ')

	CALLMETHIS = gethonorific()
	queue = "Up next we have: " + queue + "Agent Smith will find content to watch, " + CALLMETHIS + "."
	
	return queue;

def queuefix():
	command = "DELETE FROM States WHERE Option LIKE \"queue\""
	cur.execute(command)
	sql.commit()
	queue = listwildcard() + ";"
	cur.execute("INSERT INTO States VALUES(?,?)",('queue',queue))
	sql.commit()
	
	return ("The Queue has been rebuilt.")

def queuefill():
	playme = randint(1,9)
	if ("-m" in sys.argv):
		playme = 6
	elif ("-t" in sys.argv):
		playme = 7
	#print (playme)
	#random TV show
	showmode = checkmode("show")
	moviemode = checkmode("movie")
	if playme == 8:
		try:
			block = getrandomblock()
			if "Error:" not in block:
				if ("on" in checkblockrandom()):
					say = setplaymode(block)
					playme = randint(1,7)
				else:
					playme = randint(1,7)
		except Exception:
			playme = randint(1,7)
	if playme == 9:
		if ("on" not in checkcustomrandom()):
			playme = randint(1,7)
		else:
			command = "SELECT name FROM sqlite_master WHERE type='table'"
			cur.execute(command)
			if not cur.fetchone():
				playme = randint(1,7)
			else:
				cur.execute(command)
				clist = cur.fetchall()
				cxlist = []
				for item in clist:
					item = item[0]
					if "CUSTOM_" in item:
						cxlist.append(item)
				min = 0
				max = int(len(cxlist))-1
				pme = randint(min,max)
				ctable = cxlist[pme]
				ctable = ctable.replace("CUSTOM_","")
				tlist = getcustomtable(ctable)
				min = 0
				max = int(len(tlist))-1
				pme = randint(min,max)
				addme = tlist[pme]
				addme = "custom." + addme
			
	if ((playme == 1) or (playme ==5) or (playme == 7)):
		if ((playme == 1) and (showmode == "Off")):
			command = "SELECT TShow FROM TVshowlist"
			cur.execute(command)
			if ((not cur.fetchall()) or (len(cur.fetchall())<25)):
				plexlogin()
				SECTION = "TV Shows"
				tlist = plex.library.section(SECTION).search("")
				tvlist = []
				for item in tlist:
					if item.title not in tvlist:
						tvlist.append(item.title)	
			else:
				cur.execute(command)
				tvlist = cur.fetchall()
				
		elif (showmode == "Kids"):
			print ("Finding a kid friendly show now.")
			command = "SELECT TShow FROM TVshowlist WHERE Rating IN (\"TV-Y\",\"TV-Y7\", \"TV-G\")"
			cur.execute(command)
			if not cur.fetchall():
                                        plexlogin()
                                        SECTION = "TV Shows"
					GEN = ['TV-Y','TV-Y7','TV-G']
                                        tlist = plex.library.section(SECTION).search(None,contentRating=GEN)
					#print tlist
					tvlist = []
					for item in tlist:
						if item.title not in tvlist:
							tvlist.append(item.title)

			else:
				cur.execute(command)
				tvlist = cur.fetchall()

		else:
			command = "SELECT TShow FROM TVshowlist WHERE Genre LIKE \'%Favorite%\'"
			cur.execute(command)
			lcheck = cur.fetchall()
			if (int(len(lcheck)) <25):
				command = "SELECT TShow FROM TVshowlist"
				cur.execute(command)
				if not cur.fetchall():
					plexlogin()
					SECTION = "TV Shows"
					tlist = plex.library.section(SECTION).search("")
					tvlist = []
					for item in tlist:
						if item.title not in tvlist:
							tvlist.append(item.title)
					
				else:
					cur.execute(command)
					tvlist = cur.fetchall()
			else:
				cur.execute(command)
				tvlist = cur.fetchall()
		if type(tvlist) is tuple:
			tlist = []
			for item in tvlist:
				if item[0] not in tlist:
					tlist.append(item[0])
			tvlist = tlist
		sck = randint(0,1)
		if sck == 0:
			shuffle(tvlist)
		max = int(len(tvlist))-1
		min = 0
		playc = randint(min,max)
		addme = tvlist[playc]
	#random Movie
	if ((playme == 2) or (playme ==4) or (playme == 6)):
		mvlist = []
		if (moviemode == "Kids"):
                        print ("Finding a kid friendly movie now.")
                        command = "SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\", \"PG\")"
                        cur.execute(command)
                        if not cur.fetchall():
                                        plexlogin()
                                        SECTION = "Movies"
                                        GEN = ['G','TV-PG']
                                        tlist = plex.library.section(SECTION).search(None,contentRating=GEN)
                                        for item in tlist:
                                                if item.title not in mvlist:
                                                        mvlist.append(item.title)

                        else:
                                cur.execute(command)
                                mlist = cur.fetchall()
                                for item in mlist:
                                        if item[0] not in mvlist:
                                                mvlist.append(item[0])
		
		elif ((playme == 4) and (moviemode == "Off")):
			command = "SELECT Movie FROM Movies"
			cur.execute(command)
			if ((not cur.fetchall()) or (len(cur.fetchall())<25)):
				plexlogin()
				SECTION = "Movies"
				tlist = plex.library.section(SECTION).search("")
				for item in tlist:
					if item.title not in mvlist:
						mvlist.append(item.title)

			else:
				cur.execute(command)
				mlist = cur.fetchall()
				for item in mlist:
					if item[0] not in mvlist:
						mvlist.append(item[0])
	
		else:
			command = "SELECT Movie FROM Movies WHERE Genre LIKE \"%favorite%\""
			try:
				cur.execute(command)
				lcheck = cur.fetchall()
				if (int(len(lcheck))<25):
					command = "SELECT Movie FROM Movies"
				cur.execute(command)
				if not cur.fetchall():
					plexlogin()
					SECTION = "Movies"
					tlist = plex.library.section(SECTION).search("")
					for item in tlist:
						if item.title not in mvlist:
							mvlist.append(item.title)       
				else:
					cur.execute(command)
					mlist = cur.fetchall()
					for item in mlist:
						if item[0] not in mvlist:
							mvlist.append(item[0])
			except Exception:
				plexlogin()
				SECTION = "Movies"
				tlist = plex.library.section(SECTION).search("")
				for item in tlist:
					if item.title not in mvlist:
						mvlist.append(item.title)
		sck = randint(0,1)
                if sck == 0:
			shuffle(mvlist)
		max = int(len(mvlist))-1
		min = 0
		playc = randint(min,max)
		play = mvlist[playc]
		addme = "movie." + play
	if (playme == 3):
		if (showmode == "Kids"):
			print ("Wildcard kids mode- Finding a kid friendly movie now.")
                        command = "SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\", \"PG\")"
                        cur.execute(command)
			addme = cur.fetchall()
			found = randint(0,int(len(addme)))
			addme = addme[found][0]
		else:
			#print ("Using Wild Card Show.")
			cur.execute("SELECT setting FROM settings WHERE item LIKE \"WILDCARD\"")
			addme = cur.fetchone()
			addme = addme[0]
	try:
		return queueadd(addme)
	except UnboundLocalError:
		print ("FAILURE DETECTED:\nOption Tried: " + str(playme) + "\nRETRYING!")
		return queuefill()

def queueremove(item):
	name = "queue"
	command = "SELECT State FROM States WHERE Option LIKE \"" + name + "\""
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]
	queue = queue.replace(';;',';')
	oqueue = queue.lower()
	queue = queue.split(';')
	if (("movie."+item in queue) and (item not in queue)):
		item = "movie." + item
	if (item == "None"):
		removeme = queue[0]
	else:
		if "custom" in item:
			item = item.replace("custom.","")
			removeme = checkcustomtables(item)
			if type(removeme) is tuple:
				removeme = removeme[0]
			else:
				return ("Error: " + item + " not found to remove.")
			
		else:
			removeme = titlecheck(item)
	removeme = removeme + ";"
	removeme = removeme.lower()
	if (removeme in oqueue):
		newqueue = oqueue.replace(removeme, "", 1)
		newqueue = newqueue.replace("movie.';","")
		newqueue = newqueue.lstrip()
		cur.execute("DELETE FROM States WHERE Option LIKE \"Queue\"")
		sql.commit()
		cur.execute("INSERT INTO States VALUES(?,?)", (name, newqueue))
		sql.commit()
		upnext()
		


def queueremovenofill():
	name = "queue"
	command = "SELECT State FROM States WHERE Option LIKE \"" + name + "\""
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]
	oqueue = queue
	queue = queue.split(';')
	removeme = queue[0]
	removeme = removeme + ";"
	newqueue = oqueue.replace(removeme, "")
	newqueue=newqueue.lstrip()
	cur.execute("DELETE FROM States WHERE Option LIKE \"Queue\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES(?,?)", (name, newqueue))
	sql.commit()
	

def upnext():
	command = "SELECT State FROM States WHERE Option LIKE \"Playmode\""
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
	elif "holiday." in playmode:
		playme = playmode
	elif "block" in playmode:
		playme = playmode
	elif "marathon." in playmode:
		show = playmode.split("marathon.")
		show = show[1]
		playme = show
	elif ("custom." in playmode):
		show = getcustomtitle(playmode)
		playme = show
	elif ("minithon." in playmode):
		playme = playmode
	elif ("commercialmode" in playmode):
		playme = playmode

	return playme

def seriesskipback(show):
	command = "SELECT Number from TVCounts WHERE Show LIKE \"" + show + "\""
	cur.execute(command)
	if not cur.fetchone():
		command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"" + show + "\""
		cur.execute(command)
		if not cur.fetchone():
			return ("Error. " + show + " not found.")
		else:
			cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, 1))
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
			cur.execute("DELETE FROM TVCounts WHERE show LIKE \"" + show + "\"")
			sql.commit()
			cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, nowat))
                        sql.commit()
			sayme = nextep(show)
			return (sayme)

def seriesskipahead(show):
	plexlogin()
        command = "SELECT Number from TVCounts WHERE Show LIKE \'" + show + "\'"
        cur.execute(command)
        if not cur.fetchone():
                command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"" + show + "\""
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error. " + show + " not found.")
                else:
                        cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, 1))
                        sql.commit()
                        return ("Show " + show + " has been set to the first episode in the series.")
        else:
                cur.execute(command)
                nowat = cur.fetchone()
                nowat = nowat[0]
		shows = plex.library.section('TV Shows')
		the_show = shows.get(show).episodes()
		max = len(the_show) - 1
                if nowat == max:
                        return ("Show " + show + " is already at the last episode. Unable to skip ahead.")
                else:
                        nowat = int(nowat) + 1
                        cur.execute("DELETE FROM TVCounts WHERE show LIKE \"" + show + "\"")
                        sql.commit()
                        cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, nowat))
                        sql.commit()
                        sayme = nextep(show)
                        return (sayme)
	

def verifyblock(block):
	command = "SELECT Name FROM Blocks WHERE Name LIKE \"" + block + "\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: Block " + block + " not found. Check and try again.")
	cur.execute(command)
	block = cur.fetchone()[0]
	return (block)

def showminithonmax():
	command = "SELECT State FROM States WHERE Option LIKE \"MINITHONMAX\""
	cur.execute(command)
	if not cur.fetchone():
		MINITHONMAX = 3
		cur.execute("INSERT INTO States VALUES (?,?)", ("MINITHONMAX",str(MINITHONMAX)))
		sql.commit()
	else:
		cur.execute(command)
		MINITHONMAX = cur.fetchone()[0]
	MINITHONMAX = str(MINITHONMAX)
		
	return ("The Current Mini-Marathon Maximum is: " + MINITHONMAX + ".")

def setminithonmax(number):
	try:
		MINITHONMAX = int(number)
	except Exception:
		return ("Error: " + number + " is not a valid option here.")
	cur.execute("DELETE FROM States WHERE Option LIKE \"MINITHONMAX\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)", ("MINITHONMAX",str(MINITHONMAX)))
	sql.commit()
	return ("The Mini-Marathon Maximum has been set to: " + str(number) + ".")

def playmode():
	command = "SELECT State FROM States WHERE Option LIKE \"Playmode\""
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

def availplaymodes():
	say = """
""" + bcolors.WARNING + """The following modes are supported:""" + bcolors.ENDC + """
1- normal(""" + bcolors.OKGREEN + """normal""" + bcolors.ENDC + """) - Plays content from your TBN-Plex queue.
2- Block(""" + bcolors.OKGREEN + """block.blocknamehere""" + bcolors.ENDC + """) - Plays a user created block of content.
3- Marathon(""" + bcolors.OKGREEN + """marathon.shownamehere""" + bcolors.ENDC + """) - Plays a specific show continuously until you return us to normal mode.
4- Mini-Marathon(""" + bcolors.OKGREEN + """minithon.shownamehere""" + bcolors.ENDC + """) - Plays a show x number of times before reverting to normal mode. 
5- Binge(""" + bcolors.OKGREEN + """binge.shownamehere""" + bcolors.ENDC + """) - Plays a specific show continususly until you return us to normal mode.

You can change the current playmode by using "setplaymode" and one of the options above. 
ex- setplaymode block.crime_drama_block
ex2- setplaymode normal
	"""
	return (say)

def getrandomblock():
	list = getblockpackagelist()
	max = int(len(list))-1
	pblay = randint(0,max)
	block = list[pblay]
	return block

def getcustomtitle(mode):
	mode = mode.lower().strip()
	mode = mode.replace("custom.","CUSTOM_")
	command = "SELECT name FROM " + mode 
	cur.execute(command)
	xlist = cur.fetchall()
	min = 0
	max = int(len(xlist))-1
	playme = randint(min,max)
	playme = xlist[playme][0]
	return playme

def setplaymode(mode):
	cmode = playmode()
	if mode != cmode:
		cur.execute("DELETE FROM States WHERE Option LIKE \"TONIGHTSMOVIE\"")
		sql.commit()
		cur.execute("DELETE FROM States WHERE Option LIKE \"TONIGHTSSHOW\"")
                sql.commit()
		cur.execute("DELETE FROM States WHERE Option LIKE \"MINITHONCNT\"")
                sql.commit()
	checks = ['normal','block.','marathon.','binge.', 'minithon.', 'holiday.', 'custom.', 'commercialmode']
	setcheck = "fail"
	for item in checks:
		if item in mode:
			setcheck = "pass"
	if ("collection." in mode):
		mode = mode.replace("collection.","")
		cmd = "SELECT * FROM Collections WHERE name LIKE \"" + mode + "\""
		cur.execute(cmd)
		if not cur.fetchone():
			return ("Error: " + mode + " not found as an available Collection.")
		sys.argv.append("-b")
		cur.execute(cmd)
		mve = cur.fetchone()
		mve = mve[1]
		mve = mve.split(";")
		mve = mve[0]
		getcollection(mve)
		say = setplaymode("smartblock")
		return say
		
		

	if ("holiday." in mode):
		hcheck = mode.replace("holiday.","")
		hcheck = hcheck.strip()
		hxcheck = holidaycheck(hcheck)
		if "Error" in hxcheck:
			return hxcheck
	if ("getrandomblock" in mode):
		try:
			mode = getrandomblock()
		except Exception:
			return ("Error: random block get failed.")

	if ("custom." in mode.lower()):
		mode = mode.lower()
		command = "SELECT name FROM sqlite_master WHERE type='table'"
		cur.execute(command)
		list = cur.fetchall()
		mode = mode.replace("custom.","CUSTOM_")
		testme = ""
		for item in list:
			item = item[0]
			if mode.lower() in item.lower():
				mode = mode.replace("CUSTOM_","custom.")
				#return (mode.strip())
				testme = "found"
		if "found" not in testme:
			mode = mode.replace("CUSTOM_","")
			return ("Error: " + mode + " not found as an available custom mode.")
	if "pass" not in setcheck:
		command = "SELECT Name FROM Blocks WHERE Name LIKE \"" + mode + "\""
		cur.execute(command)
		if not cur.fetchone():
			return ("Error: " + mode + " is not an available playmode. Please try again.")
		else:
			cur.execute(command)
			mode = cur.fetchone()[0]
			mode = "block." + mode
	mode = mode.replace("block_","block.")
	command = "DELETE FROM States WHERE Option LIKE \"Playmode\""
	cur.execute(command)
	name = 'Playmode'
	queue = mode	
	cur.execute("INSERT INTO States VALUES(?,?)", (name, queue))
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
		command = "DELETE FROM Blocks WHERE Name LIKE \"" + bname + "\""
		cur.execute(command)
		sql.commit()
		block = "movie."+movie1 + ";movie." + movie2 + ";movie." + movie3 + ";"
		blcount = 0
		cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, block, blcount))
		sql.commit()
		say = movie1 + ", and then " + movie2 + ", and finally " + movie3
		mode = "Random " + xmode + " movie block. This one will play: " + say
	if "block." in mode:
		queuetpl = qtpl()
		if ("on" in queuetpl.lower()):
			show = mode 
                        show = show.replace("block.","")
                        blocktoplist(show)
		cmode = mode.replace("block.","")
		try:
			idtonightsmovie()
		except Exception:
			idtonightsshow()

		say1 = explainblock(cmode)
		#print (say1)
	elif ("normal" in mode):
                queuetpl = qtpl()
                if ("on" in queuetpl.lower()):
			queuetoplaylist()
	return "Playmode has been set to "+ mode

def getblockpackage(play):
	list = getblockpackagelist()
	play = play.replace("block.","")
	for item in list:
		if (item in play):
			command = "SELECT Items, Count FROM Blocks WHERE Name LIKE \"" + play + "\""
			cur.execute(command)
			stuff = cur.fetchone()
			plays = stuff[0]
			plays = plays.split(";")
			name = play
			count = stuff[1]
			play = plays[count]
			play = play.rstrip()
	return play

def setupnext(title):
	otitle = title.strip()
	if ("block." in title):
		block = title.replace("block.","")
		block = verifyblock(block)
		say = setplaymode(block)
		return (say)
	elif ("minithon." in title):
		say = setplaymode(title)
		return say
	elif ("marathin." in title):
		say = setplaymode(title)
		return say
	title = checkcustomtables(title)
	if type(title) is tuple:
		title = title[0]
	if ("CUSTOM." not in title):
		if (("numb3rs" not in title.lower()) and ("se7en" not in title.lower())):
			title = titlecheck(title).strip()
			if ("ERROR:" in title):
				return title
	if "''" in title:
                pass
        else:
                title = title.replace("'","''")
	if "User Quit." in title:
		return (title)
	elif ("Error: " in title):
		return (title)


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
	if genre.lower() in genres.lower():
		return("Error: " + genre + " is already associated with the show " + show)
	genres = genres + " " + genre
	command = 'DELETE FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
	cur.execute(command)
	sql.commit()
	cur.execute('INSERT INTO TVshowlist VALUES(?,?,?,?,?,?)',(TShow, summary, genres, rating, int(duration), int(totalnum)))
	sql.commit()
	return (genre + " has been associated with " + show)

def removegenreshow(show,genre):
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
		genres = genres.replace(genre,"")
		genres = genres.strip()
	else:
                return("Error: " + genre + " is already associated with the show " + show)
        command = 'DELETE FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
        cur.execute(command)
        sql.commit()
        cur.execute('INSERT INTO TVshowlist VALUES(?,?,?,?,?,?)',(TShow, summary, genres, rating, int(duration), int(totalnum)))
        sql.commit()
        return (genre + " has been unassociated with " + show)

def addgenremovie(movie, genre):
	command = 'SELECT * FROM Movies WHERE Movie LIKE \'' + movie + '\''
	cur.execute(command)
	if not cur.fetchone():
		say = didyoumeanmovie(movie)
		if (("Error:" in say) or (say == "done") or (say == "Quit")):
			return (say)
		say = say.replace("movie.","")
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
	if genre.lower() in genres.lower():
		return("Error: " + genre + " is already associated with the movie " + movie)
	genres = genres.strip() + " " + genre 
	command = 'DELETE FROM Movies WHERE Movie LIKE \'' + movie + '\''
	cur.execute(command)
	sql.commit()
	cur.execute('INSERT INTO Movies VALUES(?,?,?,?,?,?,?)',(title, summary, rating, tagline, genres, director, actor))
	sql.commit()
	return (genre + " successfully associated with the movie " + movie ) 	

def removegenremovie(movie, genre):
	command = 'SELECT * FROM Movies WHERE Movie LIKE \'' + movie + '\''
        cur.execute(command)
        if not cur.fetchone():
                say = didyoumeanmovie(movie)
                if (("Error:" in say) or (say == "done") or (say == "Quit")):
                        return (say)
                say = say.replace("movie.","")
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
        if genre.lower() in genres.lower():
		genres = genres.replace(genre,"")
	else:
                return("Error: " + genre + " is not associated with the movie " + movie)
        command = 'DELETE FROM Movies WHERE Movie LIKE \'' + movie + '\''
        cur.execute(command)
        sql.commit()
        cur.execute('INSERT INTO Movies VALUES(?,?,?,?,?,?,?)',(title, summary, rating, tagline, genres, director, actor))
        sql.commit()
        return (genre + " successfully unassociated with the movie " + movie )


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
	if sys.stdin.isatty():
		return ("Pass")
	else:
		return ("Fail")

def gencheck(tshow):
	plexlogin()
	for video in plex.search(tshow):
		#if video.type == "show":
			'''
			SECTION = video.librarySectionID
			xsec = plex.library.sections()
			show = video.title
			for lib in xsec:
				if lib.key == SECTION:
					SECTION = lib.title
			shows = plex.library.section(SECTION)
			theshow = shows.get(show)
			print theshow.type
			print theshow.title
			print theshow.summary
			print theshow.roles
			print theshow.genres
			print ("\n")
			print (vars(theshow))
			'''
			print (video.type)
			print (video.title)
			print (video.summary)
			print (video.roles)
			print (video.genres)
			print ("\n")
			print (vars(video))
			print ("\n--------------------\n")
	return ("Done.")

def dbtvcheck(video):
	plexlogin()
	libs = plex.library.sections()
	for lib in libs:
		if ((lib.key == video.librarySectionID) and (video.type == "show")):
			SECTION = lib.title
	try:
		xshow = video
		show = video.title
		command = "SELECT * FROM TVshowlist WHERE TShow LIKE \"" + show + "\""
		cur.execute(command)
		if not cur.fetchone():
			name = str(show)
			summary = xshow.summary
			summary = str(summary.encode('ascii','ignore')).strip()
			rating = str(xshow.contentRating)
			rating = rating.replace("__NA__","NA")
			duration = int(xshow.duration)/60000
			agenre = xshow.genres
			try:
				agenre = str(agenre)
				if agenre == "__NA__":
					agenre = ""
					agenre = getgenres(name, SECTION)
			except IndexError:
				agenre = getgenres(name, SECTION)

			bgenre = ""

			for item in agenre:
				if ((item == " ") or(item == "")):
					pass
				elif (item not in bgenre):
					try:
						bgenre = bgenre + " " + item.strip()
					except NameError:
						bgenre = item.strip()
			bgenre = bgenre.strip()
			totalnum = int(xshow.leafCount)
			cur.execute("SELECT * FROM TVshowlist WHERE TShow LIKE\"" + name + "\"")
			if not cur.fetchone():
				cur.execute("INSERT INTO TVshowlist VALUES (?,?,?,?,?,?)",(name,summary,bgenre,rating,duration,totalnum))
				sql.commit()
				if PRINTMODE == "ON":
					print ("\nFound and Successfully added " + name + " to the TVshowlist table.\n")
	except NameError:
		pass

def getsection(title):
	plexlogin()
	otitle = title
        oshow = title
        cshow = title
        cshow = title.replace("movie.","")
        #for video in plex.search(cshow):
        ssec = plex.library.sections()
        for lib in ssec:
                for video in lib.search(cshow):
                        xshow = video
                        if ((xshow.type == "show") and ("movie." not in oshow) and (xshow.title.lower() == oshow.lower())):
				show = video.title
				xsec = plex.library.sections()
				for lib in xsec:
					if lib.key == video.librarySectionID:
						say = lib.type
                                #return xshow.title
                        elif ((xshow.type.lower() == "movie") and (xshow.title.lower() == cshow.lower())):
                                try:
                                        say
                                except Exception:
                                        xsec = plex.library.sections()
                                        for lib in xsec:
                                                if lib.key == video.librarySectionID:
							say = lib.type
        try:
                return say
        except NameError:
                return ("ERROR: " + oshow + " NOT FOUND.\n")

def getsectiontitle(title):
	plexlogin()
        oshow = title
        cshow = title
        cshow = title.replace("movie.","")
        #for video in plex.search(cshow):
        ssec = plex.library.sections()
        for lib in ssec:
                for video in lib.search(cshow):
                        xshow = video
                        if ((xshow.type == "show") and ("movie." not in oshow) and (xshow.title.lower() == oshow.lower())):
                                show = video.title
                                xsec = plex.library.sections()
                                for lib in xsec:
                                        if lib.key == video.librarySectionID:
                                                say = lib.type
                                #return xshow.title
                        elif ((xshow.type.lower() == "movie") and (xshow.title.lower() == cshow.lower())):
                                try:
                                        say
                                except Exception:
                                        xsec = plex.library.sections()
                                        for lib in xsec:
                                                if lib.key == video.librarySectionID:
                                                        say = lib.title
	return say

def spellchecker(title):
	try:
		d = enchant.Dict("en_US")
	except ImportError:
		print ("Enchant Library Not Found. Spell Checking Failed.")
		return title
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
	return newt

def addcustomtitle(ntitle, otitle):
	ctitle = ntitle
	ctitle = customtitlecheck(ctitle)
	if ctitle.lower() == otitle.lower():
		return ("ERROR: " + ntitle + " already maps to: " + otitle + "\n")
	otitle = titlecheck(otitle)
	if ("ERROR:" in otitle):
		return otitle
	otitle = otitle.replace("movie.","")
	ntitle = ntitle.strip().lower()
	otitle = otitle.strip().lower()
	cur.execute("INSERT INTO CUSTOMTITLES VALUES (?,?)",(otitle, ntitle))
	sql.commit()
	return ("Successfully associated " + ntitle + " with: " + otitle + ".\n")

def removecustomtitle(ctitle):
	customtitlecheck(ctitle)
	cur.execute("DELETE FROM CUSTOMTITLES WHERE ctitle LIKE \"" + ctitle.strip() + "\"")
	sql.commit()
	return ("Removed associations for: " + ctitle + ".\n")	

def customtitlecheck(title):
	title = title.lower()
	command = "SELECT * FROM CUSTOMTITLES WHERE ctitle LIKE \"" + title + "\""
	try:
		cur.execute(command)
	except sqlite3.OperationalError:
		cur.execute("CREATE TABLE IF NOT EXISTS CUSTOMTITLES(otitle TEXT, ctitle TEXT)")
		sql.commit()
		print ("Sucessfully Added Needed CUSTOMTITLES Table.")
	cur.execute(command)
	if not cur.fetchone():
		#print ("No Custom Title Found.")
		return title
	else:
		cur.execute(command)
		title = cur.fetchone()[0]
		return title
		


def titlecheck(title):
	global xlib
	global ttlchk
	global tccnt
	title = customtitlecheck(title)
	try:
		tccnt
	except Exception:
		tccnt = 1
	if "yes" not in ttlchk:
		plexlogin()
		otitle = title
		oshow = title
		cshow = title
		cshow = title.replace("movie.","")
		#for video in plex.search(cshow):
		ssec = plex.library.sections()
		for lib in ssec:
			for video in lib.search(cshow):
				xshow = video
				if ((xshow.type == "show") and ("movie." not in oshow) and (xshow.title.lower() == oshow.lower())):
					say = xshow.title
					xlib = lib.title
					#return xshow.title
				elif ((xshow.type.lower() == "movie") and (xshow.title.lower() == cshow.lower())):
					try:
						say
					except Exception:
						say = xshow.title
						xsec = plex.library.sections()
						for lib in xsec:
							if lib.key == video.librarySectionID:
								if lib.title == "Movies":
									say = "movie." + say
								xlib = lib.title
		try:
			ttlchk = "yes"
			return say
		except NameError:
			try:
				print (say)
				del say
			except NameError:
				pass
			otitle = title
			if tccnt == 2:
				title = specialfixer(title)
				tccnt = 3
			elif tccnt == 1:
				title = spellchecker(title).lower().strip()
				tccnt = 0
			elif tccnt == 0:
				atitle = title
				atitle = atitle.split(" ")
				if atitle[0].lower == "the":
					atitle.pop[0]
				else:
					atitle.insert(0,"the")
				for item in atitle:
					try:
						ntitle = ntitle + item + " "
					except NameError:
						ntitle = item + " "
				ntitle = ntitle.strip()
				title = ntitle
				del atitle
				del ntitle
				tccnt = 2
			if tccnt <3:
				ttlchk = "no"
				#print ("Title Not Found. Trying: " + title + "\n")
				oxtitle = title
				title = titlecheck(title)
				if ("ERROR:" not in title):
					return title
				if ("ERROR:" in title):
					title = oxtitle
			return ("ERROR: " + oshow + " NOT FOUND.\n")
	else:
		return title

def specialfixer(title):
	removeme = ["'",":","!",",","-"]
	for itm in removeme:
		title = title.replace(itm,"")
	return (title)

def didyoumeanboth(title):
	#title = titlecheck(title).strip()
	movie = title
	movie = movie.replace("'","''")
	movie = movie.replace("movie.","")
	passcheck = ['the', 'and', 'a', 'to', 'of', 'for', 'an', 'on', 'with', '&', 'from', ' ', '']
	found = []
	#darker
	tshow = movie
	show = movie
	checks = []
	if (" " in show):
		show = show.split(' ')
		for item in show:
			if ((item.lower() not in passcheck) and (int(len(item)) > 3) and (item not in checks)):
				checks.append(item)
	else:
		try:
			checks.append(show)
		except Exception:
			pass
	for item in checks:
		command = "SELECT Movie FROM Movies WHERE Movie LIKE \"%" + item + "%\" ORDER BY Movie ASC"
		cur.execute(command)
		if cur.fetchall():
			cur.execute(command)
			foundme = cur.fetchall()
			for items in foundme:
				mchk = "movie." + items[0].strip().lower()
				if mchk not in found:
					found.append(mchk)
	del checks
	show = title
	tshow = show
        checks = []
        show = show.split(' ')
        for item in show:
                if item.lower() not in passcheck:
                        checks.append(item)
        for item in checks:
                command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"%" + item + "%\" ORDER BY TShow ASC"
                cur.execute(command)
		if not cur.fetchall():
			pass
		else:
                        cur.execute(command)
                        foundme = cur.fetchall()
                        for items in foundme:
                                if items[0].strip() not in found:
                                        found.append(items[0].strip())
        if not found:
                return ("Error: " + tshow + ", nor anything close was found in your library.")
	if "Fail" in externalcheck():
		return (found[0])
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
	if ("Error:" in show):
		return ("Error.")
	passcheck = ['the', 'and', 'a', 'to', 'of', 'for', 'an', 'on', 'with', '&', 'from', ' ', '']
	tshow = show
	checks = []
	found = []
	show = show.split(' ')
	for item in show:
		if item.lower() not in passcheck:
			checks.append(item)
	print (tshow + " not found. Did you mean on of the following, perhaps:\n")
	for item in checks:
		command = "SELECT TShow FROM TVshowlist WHERE TShow LIKE \"%" + item + "%\""
		cur.execute(command)
		if cur.fetchall():
			cur.execute(command)
			foundme = cur.fetchall()
			for items in foundme:
				if items[0].strip() not in found:
					found.append(items[0].strip())
	if not found:
		return ("Error: " + tshow + ", nor anything close was found in your library.")
	if ("Fail" in externalcheck()):
		return (found[0])
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
	passcheck = ['the', 'and', 'a', 'to', 'of', 'for', 'an', 'on', 'with', '&', 'from', ' ', '']
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
                command = "SELECT Movie FROM Movies WHERE Movie LIKE \"%" + item + "%\""
                cur.execute(command)
                if cur.fetchall():
                        cur.execute(command)
                        foundme = cur.fetchall()
                        for items in foundme:
				mchk = "movie." + items[0].strip().lower()
                                if mchk not in found:
                                        found.append(mchk)
        if not found:
                return ("Error: " + tshow + ", nor anything close was found in your library.")
	elif ("Fail" in externalcheck()):
		return found[0]
        choicecount = 1
        max = int(len(found))
        for item in found:
		item = item.replace("movie.","")
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
		command = "SELECT State FROM States WHERE Option LIKE \"" + name + "\""
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

def aftercommpreroll():
	command = "SELECT State FROM States WHERE Option LIKE \"Playmode\""
        cur.execute(command)
        playmode = cur.fetchone()
        playmode = playmode[0].replace("block.","")
	command = "SELECT Items, Count FROM Blocks WHERE Name LIKE \"" + playmode + "\""
	cur.execute(command)
	try:
		stuff = cur.fetchone()
		plays = stuff[0]
		plays = plays.split(";")
		count = int(stuff[1]) + 1
		play = plays[count]
		play = play.rstrip()
	except Exception:
		play = "Nothing."
	return play
	

def whatupnext():
	plexlogin()
	command = "SELECT State FROM States WHERE Option LIKE \"Playmode\""
	cur.execute(command)
	playmode = cur.fetchone()
	playmode = playmode[0]

	if (("normal" in playmode) or ("binge." in playmode) or ("-q" in sys.argv)):
		queue = openqueue()
		if queue == " ":
			updatehelp()
                        cls()
			if PRINTMODE == ON:
				print ("Successfully updated help file.")
				print ("First run situation detected. Taking approprate action.\n")
			queuefix()
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
		elif (("custom." in playme) or ("CUSTOM." in playme)):
			playme = playme.lower()
			say = playme.replace("custom.","")
			return (say)
		else:

			playme = playme.strip()
			playme = playme.rstrip()
			try:
				command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + playme + "\""
				cur.execute(command)
				thecount = cur.fetchone()
				thecount = thecount[0]
			except Exception:
				thecount = 1
				cur.execute("INSERT INTO TVCounts VALUES(?,?)", (playme, thecount))
				sql.commit()
			if thecount ==0:
				thecount = 1
			epnum = int(thecount)-1
			shows = plex.library.section("TV Shows")
			the_show = shows.get(playme).episodes()
			#ep = str(the_show[epnum].title)
			ep = the_show[epnum].title
			ssn = str(the_show[epnum].seasonNumber)
			xep = str(the_show[epnum].index)
			playme = "The TV Show " + playme +" Season " + ssn + " Episode " + xep + ", " + ep
			playme = playme.rstrip()

		upnext = "Up next we have " + playme
	elif ("holiday." in playmode):
		say = playmode.replace("holiday.","")
		holiday = playmode.split("holiday.")
		holiday = holiday[1].strip()
		#say = "Up next a random " + say + " holiday program will play."
		#print say
		try:
			command = "SELECT State FROM States WHERE Option LIKE \"NEXTHOLIDAY\""
			cur.execute(command)
			show = cur.fetchone()[0]
			if "movie." in show:
				show = show.replace("movie.","The Movie ")
				say = "The next item is " + show + " for the holiday " + holiday + "."
			else:
				title = show
				title = title.split(":")
				ssn = title[1].strip()
				ep = title[2].strip()
				title = title[0].strip()
				say = "The next item is " + title + " for the holiday " + holiday + "."
		except Exception:
			holiday = playmode.replace("holiday.","")
			cur.execute("SELECT items FROM Holidays WHERE name LIKE \"" + holiday.strip() + "\"")
			titles = cur.fetchone()[0]
			titles = titles.split(";")
			ttls = []
			for item in titles:
				if item != "":
					ttls.append(item)
			min = 0
			max = int(len(ttls)) - 1
			pcnt = randint(min,max)
			plexlogin()
			addme = ttls[pcnt]
			cur.execute("INSERT INTO States VALUES (?,?)",("NEXTHOLIDAY",addme))
			sql.commit()
			show = addme
			if "movie." in show:
                                show = show.replace("movie.","The Movie ")
                                say = "The next item is " + show + " for the holiday " + holiday + "."
                        else:
                                title = show
                                title = title.split(":")
                                ssn = title[1].strip()
                                ep = title[2].strip()
                                title = title[0].strip()
                                say = "The next item is " + title + " for the holiday " + holiday + "."

		return (say)
	elif (("custom." in playmode) or ("CUSTOM." in playmode)):
		say = playmode.replace("custom.","")
		say = "Up next is a random " + say + " program."
		return (say)
	elif ("block." in playmode):
		block = getblockpackage(playmode)
		block = block.lower()
		block = checkcustomtables(block)
		if type(block) is tuple:
			block = block[0]
		if ("random_movie." in block):
			upnext = idtonightsmovie()
			if upnext == " ":
				findnewmovie()
				upnext = idtonightsmovie()
		elif ("random_tv." in block):
			upnext = idtonightsshow()
			if upnext == " ":
				findnewshow()
				upnext = idtonightsshow()
		elif ("CUSTOM." in block):
			block = block.replace("CUSTOM.","")
			block = checkcustomtables(block)
			table = block[1].strip()
			show = block[0]
			show = show.replace("CUSTOM.","")
			upnext = show
		elif ("playcommercial" in block):
			upnext = block
			upnext = upnext.replace("playcommercial.","The commercial: ")
			if ("The commercial: " not in upnext):
				upnext = "A random Commercial"
		elif ("preroll" in block):
			upnext = block
			upnext = upnext.replace("preroll.","The preroll: ")
			if ("The preroll: " not in upnext):
				upnext = "A random preroll"
		else:
			bcheck = block
			bcheck = bcheck.replace("movie.","")
			SECTION = getsection(bcheck)
			if ("movie." in block):
				episode = block.split("movie.")
				episode = episode[1].rstrip()
				episode = "The Movie " + episode
			else:
				if "show" in SECTION:
					episode = nextep(block)
					block = playmode.replace("block.","")
				else:
					episode = block
			#upnext = upnext.replace("''","'")
			upnext = "Up next we have " + episode
			upnext = upnext.replace("For the show ", "")
			upnext = upnext.replace("Up next is ", "")
			upnext = upnext.replace(" we have the", ",")
	elif (("playcommercial" in playmode) or ("commercialmode" in playmode)):
		upnext = playmode 
		upnext = upnext.replace("playcommercial.","The commercial: ")
		if ("The commercial: " not in upnext):
			upnext = "A random Commercial"
	elif ("preroll" in playmode):
		upnext = playmode 
		upnext = upnext.replace("preroll.","The preroll: ")
		if ("The preroll: " not in upnext):
			upnext = "A random preroll"
	elif ("marathon." in playmode):
		show = playmode.split("marathon.")
		show = show[1]
		episode = nextep(show)
		episode = episode.rstrip()
		upnext = "Up next we have " + episode
		upnext = upnext.replace("For the show ", "")
		upnext = upnext.replace(" we have the", ",")
	elif ("minithon." in playmode):
		command = ("SELECT State FROM States WHERE Option LIKE \"MINITHONCNT\"")
		cur.execute(command)
		if not cur.fetchone():
			ccount = 0
		else:
			cur.execute(command)
			ccount = cur.fetchone()[0]
		command = ("SELECT State FROM States WHERE Option LIKE \"MINITHONMAX\"")
                cur.execute(command)
                if not cur.fetchone():
                        mcount = 0
                else:
                        cur.execute(command)
                        mcount = cur.fetchone()[0]
		sleft = int(mcount) - int(ccount)
		sleft = ". There are " + str(sleft) + " episodes left in the Mini-Marathon."
		show = playmode.split("minithon.")
		show = show[1]
		episode = nextep(show)
		episode = episode.rstrip()
		upnext = "\nWe are in mini-marathon mode, watching " + show
                upnext = episode + upnext + sleft
                upnext = upnext.replace("For the show ", "")
                upnext = upnext.replace(" we have the", ",")


	return upnext

def getmovie(genre):
	cur.execute("SELECT Movie FROM Movies WHERE Genre LIKE \"%" + genre + "%\"")
	found = cur.fetchall()
	tnum = randint(0,int(len(found)-1))
	found = found[tnum]
	found = found[0]
	return (found)

def getshow(genre):
	cur.execute("SELECT TShow FROM TVshowlist WHERE Genre LIKE \"%" + genre + "%\"")
	found = cur.fetchall()
        tnum = randint(0,int(len(found)-1))
        found = found[tnum]
        found = found[0]
        return (found)

def idtonightsshow():
	mode = playmode()
	if "block." in mode:
		mode = mode.split("block.")
                mode = mode[1].strip()
                cur.execute("SELECT State FROM States WHERE Option LIKE \"TONIGHTSSHOW\"")
                if ((not cur.fetchone()) or (cur.fetchone() == "")):
                        command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                        cur.execute(command)
                        found = cur.fetchone()[0]
                        command = "SELECT Count FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                        cur.execute(command)
                        bcount = cur.fetchone()[0]
                        bcount = int(bcount)
                        found = found.split(";")
			thing = found[bcount].lower()
			if "random_tv." in thing:
				item = thing.split("_tv.")
				item = item[1]
				say = getshow(item)
				say = settonightsshow(say)
				return (say)
		else:
			cur.execute("SELECT State FROM States WHERE Option LIKE \"TONIGHTSSHOW\"")
                        state = cur.fetchone()[0]
                        if state == "":
                                command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                                cur.execute(command)
                                found = cur.fetchone()[0]
                                command = "SELECT Count FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                                cur.execute(command)
                                bcount = cur.fetchone()[0]
                                bcount = int(bcount)-1
                                found = found.split(";")
                                for thing in found:	
					thing = thing.lower()
                                        if "random_tv." in thing:
                                                item = thing.split("_tv.")
                                                item = item[1]
                                                say = getshow(item)
                                                say = settonightsshow(say)
                                                return (say)
			command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                        cur.execute(command)
                        found = cur.fetchone()[0]
                        command = "SELECT Count FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                        cur.execute(command)
                        bcount = cur.fetchone()[0]
                        bcount = int(bcount)-1
                        cur.execute("SELECT State FROM States WHERE Option LIKE \"TONIGHTSSHOW\"")
                        found = cur.fetchone()
                        found = found[0]
                        if ((not found) or (found == "")):
                                command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                                cur.execute(command)
                                found = cur.fetchone()[0]
                                found = found.split(";")
                                ccnt = 0
                                for items in found:
                                        items = items.lower()
                                        if (("random_tv." in items) and (ccnt <= bcount)):
                                                genre = items.split("tv.")
                                                genre = genre[1].strip()
                                                found = suggesttv(genre)
                                                found = found.split("the TV Show ")
                                                found = found[1]
                                                found = found.split(" sound, ")
                                                found = found[0].strip()
                                                found = settonightsshow(found)
                                        ccnt = ccnt + 1
        else:
                found = "Not in block playback mode. No movie is scheduled tonight."
        return (found)

def idtonightsmovie():
	mode = playmode()
	if "block." in mode:
		mode = mode.split("block.")
		mode = mode[1].strip()
		cur.execute("SELECT State FROM States WHERE Option LIKE \"TONIGHTSMOVIE\"")
		if ((not cur.fetchone()) or (cur.fetchone() == "")):
			command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
			cur.execute(command)
			found = cur.fetchone()[0]
			command = "SELECT Count FROM Blocks WHERE Name LIKE \'" + mode + "\'"
			cur.execute(command)
			bcount = cur.fetchone()[0]
			bcount = int(bcount)-1	
			found = found.split(";")
			for thing in found:
				thing = thing.lower()
				if "random_movie." in thing:
					item = thing.split("_movie.")
					item = item[1]
					say = suggestmovieblockuse(item)
					#say = getmovie(item)
					say = settonightsmovie(say)
					return (say)
		else:
			cur.execute("SELECT State FROM States WHERE Option LIKE \"TONIGHTSMOVIE\"")
			state = cur.fetchone()[0]
			if state == "":
				command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
				cur.execute(command)
				found = cur.fetchone()[0]
				command = "SELECT Count FROM Blocks WHERE Name LIKE \'" + mode + "\'"
				cur.execute(command)
				bcount = cur.fetchone()[0]
				bcount = int(bcount)-1
				found = found.split(";")
				for thing in found:
					thing = thing.lower()
					if "random_movie." in thing:
						item = thing.split("_movie.")
						item = item[1]
						#say = getmovie(item)
						say = suggestmovieblockuse(item)
						say = settonightsmovie(say)
						return (say)
			command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                        cur.execute(command)
                        found = cur.fetchone()[0]
                        command = "SELECT Count FROM Blocks WHERE Name LIKE \'" + mode + "\'"
                        cur.execute(command)
                        bcount = cur.fetchone()[0]
                        bcount = int(bcount)-1
			cur.execute("SELECT State FROM States WHERE Option LIKE \"TONIGHTSMOVIE\"")
			found = cur.fetchone()
			found = found[0]
			if ((not found) or (found == "")):
				command = "SELECT Items FROM Blocks WHERE Name LIKE \'" + mode + "\'"
				cur.execute(command)
				found = cur.fetchone()[0]
				found = found.split(";")
				ccnt = 0
				for items in found:
					items = items.lower()
					if (("random_movie." in items) and (ccnt <= bcount)):
						genre = items.split("movie.")
						genre = genre[1].strip()
						found = suggestmovieblockuse(genre)
						'''
						found = found.split("the movie: ")
						found = found[1]
						found = found.split("sound, ")
						found = found[0].strip()
						'''
						found = settonightsmovie(found)
					ccnt = ccnt + 1
	else:
		found = "Not in block playback mode. No movie is scheduled tonight."
	return (found)
		
		

def settonightsmovie(movie):
	#movie = movie.replace("movie.","")
	movie = titlecheck(movie)
	if ("ERROR" in movie):
		return movie
	movie = titlecheck(movie)
	cur.execute("DELETE FROM States WHERE Option LIKE \"TONIGHTSMOVIE\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES(?,?)",('TONIGHTSMOVIE',movie))
	sql.commit()
	movie = movie.replace('movie.','The Movie ')
	return (movie)

def settonightsshow(show):
	show = titlecheck(show)
	if ("ERROR" in show):
		return show
	show = titlecheck(show)
	cur.execute("DELETE FROM States WHERE Option LIKE \"TONIGHTSSHOW\"")
        sql.commit()
        cur.execute("INSERT INTO States VALUES(?,?)",('TONIGHTSSHOW', show))
        sql.commit()
	return ("Tonights show has been set to " + show)

def restartshow(show):
	show = titlecheck(show)
	if ("ERROR" in show):
		return show
	show = show.strip()
	sayme = "Restart " + show + "- Yes or No?"
	checkme = input(sayme)
	if (checkme.lower() == "yes"):
		command = "DELETE FROM TVCounts WHERE Show LIKE \"" + show + "\""
		cur.execute(command)
		sql.commit()
		say = show + " will start from the beginning of the series."
	else:
		say = "Error: Invalid response. No action taken."
	return say

def nextep(show):
	plexlogin()
	if ("Quit." in show):
		return ("User quit. No action taken.")
	try:
		command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + show + "\""
		cur.execute(command)
		thecount = cur.fetchall()
		thecount = thecount[0]
	except Exception:
		thecount = 1
		cur.execute("INSERT INTO TVCounts VALUES(?,?)", (show, thecount))
		sql.commit()

	if thecount == 0:
		thecount = 1
	try:
		epnum = thecount[0]
	except Exception:
		epnum = thecount
	epnum = epnum-1
	#epnum = str(epnum)
	shows = plex.library.section('TV Shows')
	theshow = shows.get(show).episodes()
	episode = theshow[epnum].title
	try:
		episode = str(episode)
	except Exception:
		episode = episode.encode("utf8")
		epidose = str(episode)
	ssn = str(theshow[epnum].seasonNumber)
	xep = str(theshow[epnum].index)
	episode = episode.replace("''","'")
	try:
		episode = str(episode)
	except Exception:
		episode = episode.decode("utf8")
		episode = str(episode)
	try:
		episode = "For the show " + str(show) + ", Up next is Season " + ssn + ", Episode " + xep + ", " + str(episode)
	except Exception:
		pass
	episode = episode.rstrip()
	return episode


def removeblock(block):
	say = availableblocks()
	if "none" in block:
		print("Block Package to Remove?")
		print (say + "\n\n")
		block = str(input('Block: '))
	if block in say:
		print ("Removing and recreating the " + block + " block now.")
	else:
		return ("Error, block not found to remove. Please try check and try again.")
	bname = block.strip()
	command = "DELETE FROM Blocks WHERE Name LIKE \"" + bname + "\""
	cur.execute(command)
	sql.commit()
	return ("Block " + block + " has been successfully removed.")

def jumpinblock(num):
	pm = playmode()
	if ("block." in pm):
		#print ("Good")
		pass
	else:
		return ("Error: Not in block package mode.")
	block = pm.replace("block.","")
	try:
		num = int(num)
	except Exception:
		return ("Error: Location in block must be a number value. IE: 1.")
	if num < 0:
		print ("Negative number input has been autocorrected.\n")
		num = num * (-1)
	if num > 0:
		num = int(num)-1
	command = "SELECT Items, Count FROM Blocks WHERE Name LIKE \"" + block + "\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Error: Block " + block + " not found.")
	else:
		cur.execute(command)
		stuff = cur.fetchone()
	things = stuff[0]
	blk = things
	bcnt = stuff[1]
	things = things.split(";")
	bmax = int(len(things))-1
	if num+1 > bmax:
		return ("Error: Jumpto location is greater than number of items in block. Unable to comply.")
	cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + block + "\"")
	sql.commit()
	cur.execute("INSERT INTO Blocks VALUES (?,?,?)",(block,str(blk.strip()),int(num)))
	sql.commit()
	return ("Done.")	

def skipthat():
	mode = playmode()
	try:
		option = str(sys.argv[2])
		if "normal" in option:
			print ("Skip Enabled")
	except Exception:
		option = ""
	if (("normal" in mode) or ("normal" in option) or ("-q" in sys.argv)):
		command = "SELECT State FROM States WHERE Option LIKE \"Queue\""
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
	elif ("minithon." in mode):
		max = showminithonmax()
		max = max.split("is: ")
		max = max[1].strip()
		max = max.replace(".","")
		command = "SELECT State FROM States WHERE Option LIKE \"MINITHONCNT\""
		cur.execute(command)
		if not cur.fetchone():
			ccount = 0
		else:
			cur.execute(command)
			ccount = cur.fetchone()[0]
		ccount = int(ccount) + 1
		ccount = str(ccount)
		cur.execute("DELETE FROM States WHERE Option LIKE \"MINITHONCNT\"")
		sql.commit()
		if int(ccount) <= int(max):
			cur.execute("INSERT INTO States VALUES (?,?)",("MINITHONCNT",ccount))
			sql.commit()
			return ("We have increased the Mini-Marathon count.")
		else:
			say = setplaymode("normal")
			return (say)
	elif ("binge." in mode):

		return ("We are in binge mode. Change playmodes to use this option or add 'normal' to your command to skip what is up next in the queue.")
	elif ("holiday." in mode):
		cur.execute("DELETE FROM States WHERE Option LIKE \"NEXTHOLIDAY\"")
		sql.commit()
		say = whatupnext()
		return (say)
	else:
		play = upnext()
		list = getblockpackagelist()
		for item in list:
			item = item.replace(".txt", "")
			if (item in play):
				check = whatupnext()
				xitem = item
				yitem = item + ".txt"
				xitem = xitem.replace('.txt','')
				command = "SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \"" + xitem + "\""
				cur.execute(command)
				binfo = cur.fetchone()
				bname = binfo[0]
				bitems = binfo[1]
				bcount = binfo[2]
				bxitems = bitems.split(';')
				max_count = len(bxitems)
				play = bxitems[bcount]
				rcheck = bxitems[bcount]
				if "random_movie." in rcheck.lower():
                                        deletetonightsmovie()
                                elif "random_tv." in rcheck.lower():
                                        deletetonightsshow()
				bcount = bcount + 1
				if int(bcount) == (int(max_count)-1):
					bcount = 0
					setplaymode("normal")
					print ("Playmode has been set to normal.")
				command = "DELETE FROM Blocks WHERE Name LIKE \"" + bname + "\""
				cur.execute(command)
				sql.commit()
				cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, bitems, int(bcount)))
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
	command = "DELETE FROM States WHERE Option LIKE \"TONIGHTSMOVIE\""
	cur.execute(command)
	sql.commit()
	say = idtonightsmovie()
	return(say)

def findnewshow():
	command = "DELETE FROM States WHERE Option LIKE \"TONIGHTSSHOW\""
        cur.execute(command)
        sql.commit()
        say = idtonightsshow()
        return(say)

def deletetonightsmovie():
	command = "DELETE FROM States WHERE Option LIKE \"TONIGHTSMOVIE\""
        cur.execute(command)
        sql.commit()

def deletetonightsshow():
	command = "DELETE FROM States WHERE Option LIKE \"TONIGHTSSHOW\""
        cur.execute(command)
        sql.commit()


def openqueue():
	name = "queue"
	command = "SELECT State FROM States WHERE Option LIKE \"" + name + "\""
	cur.execute(command)
	queue = cur.fetchone()
	queue = queue[0]
	if not queue:
		queue = queuefill()
	return queue

def restartblock(block):
	if block == "none":
		block = playmode()
		block = block.replace("block.","")
	try:	
		command = "SELECT Name, Items, Count FROM Blocks WHERE Name LIKE \"" + block + "\""
		cur.execute(command)
		binfo = cur.fetchone()
		bname = binfo[0]
		bitems = binfo[1]
		bcount = "0"
	except TypeError:
		return ("Block not found to restart.")
	else:
		command = "DELETE FROM Blocks WHERE Name LIKE \"" + bname + "\""
		cur.execute(command)
		sql.commit()
		cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (bname, bitems, int(bcount)))
		sql.commit()

	return ("Done")
def tvgenrechecker(genre):
	if "none" not in genre:
                command = "SELECT TShow from TVshowlist WHERE Genre LIKE \"%" + genre + "%\""
                cur.execute(command)
                if not cur.fetchone():
                        print ("Error. No movies were found associtated with the " + genre + " genre.")
			thegenres = availgenretv()
			genre = worklist(thegenres)
		return (genre)

def moviegenrechecker(genre):
	if "none" not in genre:
                command = "SELECT Movie from Movies WHERE Genre LIKE \"%" + genre + "%\""
                cur.execute(command)
                if not cur.fetchone():
                        print ("Error. No movies were found associtated with the " + genre + " genre.")
			thegenres = availgenremovie()
			genre = worklist(thegenres)
	return (genre)

def randommovieblock(genre):
	if "none" not in genre:
		command = "SELECT Movie from Movies WHERE Genre LIKE \"%" + genre + "%\""
		cur.execute(command)
		if not cur.fetchone():
			return "Error. No movies were found associtated with the " + genre + " genre."
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
	cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + mode1 + "\"")
	sql.commit()
	cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (mode1, addme, "0"))
	sql.commit()
	cur.execute("DELETE FROM States WHERE Option LIKE \"Playmode\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES(?,?)", ('Playmode', mode))
	sql.commit()
	return (say)

def randomtvblock(genre):
	if "none" not in genre:
		command = "SELECT TShow FROM TVshowlist WHERE Genre LIKE \"%" + genre + "%\""
                cur.execute(command)
                if not cur.fetchone():
                        return "Error. No shows were found associtated with the " + genre + " genre. Use availtvgenres to see the list of available TV genres."
	show1 = suggesttvblockuse(genre)
	show2 = suggesttvblockuse(genre)
	if show2 == show1:
		show2 = suggesttvblockuse(genre)
	show3 = suggesttvblockuse(genre)
	if ((show2 == show3) or (show1 == show3)):
		show3 = suggesttvblockuse(genre)
	say = "I have generated the following " + genre + " show block: \n" + show1 + "\n" + show2 + "\n" + show3
	mode1 = "randomshowblock"
	mode = "block.randomshowblock"
	addme = show1 + ";" + show2 + ";" + show3 + ";"
	cur.execute("DELETE FROM Blocks WHERE Name LIKE \"" + mode1 + "\"")
        sql.commit()
        cur.execute("INSERT INTO Blocks VALUES(?,?,?)", (mode1, addme, "0"))
        sql.commit()
        cur.execute("DELETE FROM States WHERE Option LIKE \"Playmode\"")
        sql.commit()
        cur.execute("INSERT INTO States VALUES(?,?)", ('Playmode', mode))
        sql.commit()
        return (say)
	cur

def getnewblock():
	try:
		genre = str(sys.argv[2])
	except IndexError:
		genre = "none"
	check = playmode()
	if "block." not in check:
		return ("Sorry, but this command only works if randommovieblock or randomshowblock is active.")
	if "block.randommovieblock" in check:
		say = randommovieblock(genre)
	elif ("block.randomshowblock" in check):
		say = randomtvblock(genre)
	else:
		say = "Error. No action taken."
	return say

def randomshowblock(genre):
	command = "SELECT TShow FROM TVshowlist WHERE Genre LIKE \"%" + genre + "%\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Error. " + genre + " not found as an availble TV show genre. Use availtvgenres to see the available show genres.")

def moviechoice(option):
	found = []
	option = option.lower()
	if (("genre." in option)):
		noption = option.replace("genre.","")
		while (int(len(found)) <3):
			fnd = suggestmovieblockuse(noption)
			if "Error:" in fnd:
				return fnd
			elif fnd not in found:
				found.append(fnd)
	elif (("rating." in option) or ("actor." in option)):
		while (int(len(found))<3):
			fnd = suggestmovieblockuse(option)
			if "Error:" in fnd:
				return fnd
			elif fnd not in found:
				found.append(fnd)
	else:
		return ("Error: You must specify a \"genre.\" or a \"rating.\" or a \"actor.\" to use this command.")
			
	say = worklist(found)
	if (say == "done"):
		return ("User Quit. No Action Taken.")
	elif ("Error:" in say):
		return (say)
	elif (say == "reroll"):
		say = moviechoice(option)
		return (say)
	if ("setupnext" not in say):
		if ("movie." not in say):
			say = "movie." + say
		say = setupnext(say)
	return say

def tvchoice(option):
	found = []
	option = option.lower()
	if ("genre." in option):
		noption = option.replace("genre.","")
		while (int(len(found)) <3):
			fnd = suggesttvblockuse(noption)
			if "Error:" in fnd:
				return fnd
			elif fnd not in found:
				found.append(fnd)
	elif (("rating." in option) or ("duration." in option)):
		while (int(len(found)) <3):
			fnd = suggesttvblockuse(option)
			if "Error:" in fnd:
				return fnd
			elif fnd not in found:
				found.append(fnd)
	else:
		return ("Error: You must specify  a \"genre.\" or a \"rating.\" or a \"duration.\" to use this command")
	say = worklist(found)
        if (say == "done"):
                return ("User Quit. No Action Taken.")
        elif (say == "reroll"):
                say = tvchoice(option)
                return (say)
	elif ("Error:" in say):
		return say
        say = setupnext(say)
        return say

def suggestcustom(table):
	table = "CUSTOM_" + table
	command = "SELECT name FROM "+ table
	cur.execute(command)
	stuff = []
	if not cur.fetchall():
		return ("Error: " + table + " not found.")
	else:
		cur.execute(command)
		found = cur.fetchall()
		for item in found:
			stuff.append(item[0])
	min = 0
	max = int(len(stuff))-1
	plc = randint(min,max)
	playme = stuff[plc]
	addme = "custom." + playme
	command = "DELETE from States WHERE Option LIKE \"Pending\""
	cur.execute(command)
	sql.commit()
	cur.execute("INSERT INTO States VALUES(?,?)", ('Pending',addme))
	sql.commit()
	return playme

def suggestsomething():
	getme = randint(0,1)
	if getme == 0:
		found = suggestmovie("none")
	else:
		found = suggesttv("none")
	return (found)

def suggestmovieblockuse(genre):
	check = checkmode("movie")
	#command = "SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\")"
	if (genre == "none"):
		if ("Kids" in check):
			cur.execute("SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\")")
		else:
			cur.execute('SELECT Movie FROM Movies')
		playfiles = cur.fetchall()
		min = 0
		max = int(len(playfiles)-1)
		playc = randint(min,max)
		play = playfiles[playc][0]
		play = play.rstrip()
	elif ("rating." in genre):
		genre = genre.replace("rating.","").strip().upper()
		if ("Kids" in check):
			command = "SELECT Movie FROM Movies WHERE Rating LIKE \"" + genre + "\" AND Rating NOT IN (\"R\",\"none\", \"PG-13\")"
		else:
			command = "SELECT Movie FROM Movies WHERE Rating LIKE \"" + genre + "\""
		cur.execute(command)
		if not cur.fetchone():
			return ("Error: "  + genre + " not found as an available rating.")
		cur.execute(command)
                playfiles = cur.fetchall()
                min = 0
                max = int(len(playfiles)-1)
                playc = randint(min,max)
                play = playfiles[playc][0]
                play = play.rstrip()
	elif ("actor." in genre):
                genre = genre.replace("actor.","").strip()
		if ("Kids" in check):
			command = "SELECT Movie FROM Movies WHERE Actors LIKE \"%" + genre + "%\" AND Rating NOT IN (\"R\",\"none\", \"PG-13\")"
		else:
			command = "SELECT Movie FROM Movies WHERE Actors LIKE \"%" + genre + "%\""
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: "  + genre + " not found as an available Actor.")
                cur.execute(command)
                playfiles = cur.fetchall()
                min = 0
                max = int(len(playfiles)-1)
                playc = randint(min,max)
                play = playfiles[playc][0]
                play = play.rstrip()
	else:
		genre = genre.rstrip()
		if ("Kids" in check):
			command = "SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\") AND Genre LIKE \"%" + genre + "%\""
			cur.execute(command)
		elif (genre == "none"):
			cur.execute("SELECT Movie FROM Movies")
		else:
			cur.execute("SELECT Movie FROM Movies WHERE Genre LIKE \"%" + genre + "%\"")
		found = cur.fetchall()
		min = 0
		max = int(len(found))
		playc = randint(min,max)
		play = found[playc]
		play = play[0]
	return play

def suggesttvblockuse(genre):
	if (genre == "none"):
		cur.execute('SELECT TShow from TVshowlist')
		playfiles = cur.fetchall()
		min = 0
		max = int(len(playfiles)-1)
		playc = randint(min,max)
		play = playfiles[playc][0]
		play = play.strip()
	elif ("rating." in genre):
                genre = genre.replace("rating.","").strip().upper()
                command = "SELECT TShow FROM TVshowlist WHERE Rating LIKE \"" + genre + "\""
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: "  + genre + " not found as an available rating.")
                cur.execute(command)
                playfiles = cur.fetchall()
                min = 0
                max = int(len(playfiles)-1)
                playc = randint(min,max)
                play = playfiles[playc][0]
                play = play.rstrip()
	elif ("duration." in genre):
                genre = genre.replace("duration.","").strip().upper()
                command = "SELECT TShow FROM TVshowlist WHERE Duration LIKE \"" + genre + "\""
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: "  + genre + " not found as an available duration.")
                cur.execute(command)
                playfiles = cur.fetchall()
                min = 0
                max = int(len(playfiles)-1)
                playc = randint(min,max)
                play = playfiles[playc][0]
                play = play.rstrip()
	else:
		genre = genre.rstrip()
		cur.execute("SELECT TShow FROM TVshowlist WHERE Genre LIKE \"%" + genre + "%\"")
		found = cur.fetchall()
		min = 0
		max = int(len(found)-1)
		playc = randint(min,max)
		play = found[playc][0]
	return play


def suggestmovie(genre):
	#favcheck = checkmode("movie")
	favcheck = "off"
	if (genre == "none") or (genre == "all"):
		if ("On" in favcheck):
			command = "SELECT Movie from Movies WHERE Genre LIKE \"%favorite%\""
		elif ("Kids" in favcheck):
			command = "SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\")"
		else:
			command = "SELECT Movie FROM Movies"
		cur.execute(command)
		mvlist = cur.fetchall()
		min = 0
		max = int(len(mvlist)-1)
		playc = randint(min,max)
		play = mvlist[playc]
		play = play[0].rstrip()
		for mvs in mvlist:
			if mvs[0].lower() == play.lower():
				play = mvs[0]	
		addme = "movie." + play

		command = "DELETE from States WHERE Option LIKE \"Pending\""
		cur.execute(command)
		sql.commit()
		cur.execute("INSERT INTO States VALUES(?,?)", ('Pending',addme))
		sql.commit()
		
	elif ("rating." in genre):
                rating = genre.split("rating.")
                rating = rating[1].strip()
		if ("On" in favcheck):
                        command = "SELECT Movie from Movies WHERE Genre LIKE \"%favorite%\" AND Rating LIKE \"" + rating + "\""
		elif ("Kids" in favcheck):
                        command = "SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\") AND Rating LIKE \"" + rating + "\""
		else:
			command = "SELECT Movie FROM Movies WHERE Rating LIKE \"" + rating + "\""
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: No Movies found with a " + rating + " rating.")
                else:
                        mlist = cur.fetchall()
                        min = 0
                        max = int(len(mlist)-1)
                        mcount = randint(min,max)
                        play = mlist[mcount][0]
                        addme = "movie." + play
			command = "DELETE from States WHERE Option LIKE \"Pending\""
			cur.execute(command)
			sql.commit()
			cur.execute("INSERT INTO States VALUES(?,?)", ('Pending',addme))
			sql.commit()
	elif ("actor." in genre):
		rating = genre.split("actor.")
                rating = rating[1].strip()
		if ("On" in favcheck):
                        command = "SELECT Movie from Movies WHERE Genre LIKE \"%favorite%\" AND Actors LIKE \"%" + rating + "%\""
                elif ("Kids" in favcheck):
                        command = "SELECT Movie FROM Movies WHERE Rating NOT IN (\"R\",\"none\", \"PG-13\") AND Actors LIKE \"%" + rating + "%\""
                else:
			command = "SELECT Movie FROM Movies WHERE Actors LIKE \"%" + rating + "%\""
                cur.execute(command)
                if not cur.fetchone():
                        return ("Error: No Movies found starring " + rating + ".")
                else:
			cur.execute(command)
                        mlist = cur.fetchall()
                        min = 0
                        max = int(len(mlist)-1)
                        mcount = randint(min,max)
                        play = mlist[mcount][0]
                        addme = "movie." + play
			command = "DELETE from States WHERE Option LIKE \"Pending\""
                        cur.execute(command)
                        sql.commit()
                        cur.execute("INSERT INTO States VALUES(?,?)", ('Pending',addme))
                        sql.commit()

	else:
		genre = genre.rstrip()
		cur.execute("SELECT Movie FROM Movies WHERE Genre LIKE \"%" + genre + "%\"")
		found = cur.fetchall()
		min = 0
		max = int(len(found))
		playc = randint(min,max)
		play = found[playc]
		play = play[0].rstrip()
		addme = "movie." + play
		command = "DELETE from States WHERE Option LIKE \"Pending\""
		cur.execute(command)
		sql.commit()
		cur.execute("INSERT INTO States VALUES(?,?)", ('Pending',addme))
		sql.commit()

	CALLMETHIS = gethonorific()
	return "How does the movie: " + play + " sound, " + CALLMETHIS + "?"

def suggesttv(genre):
	if (genre == "none"):
		favcheck = checkmode("show")
                if ("On" in favcheck):
                        command = "SELECT TShow from TVshowlist WHERE Genre LIKE \"%favorite%\""
		elif ("Kids" in favcheck):
			command = "SELECT TShow FROM TVshowlist WHERE Rating IN (\"TV-Y\",\"TV-Y7\", \"TV-PG\", \"TV-G\")"
                else:
                        command = "SELECT TShow FROM TVshowlist"
		cur.execute(command)
		playfiles = cur.fetchall()
		if int(len(playfiles)-1) <= 24:
			cur.execute("SELECT TShow FROM TVshowlist")
			playfiles = cur.fetchall()
		min = 0
		max = int(len(playfiles))-1
		playc = randint(min,max)
		play = playfiles[playc]
		play = play[0].rstrip()
		addme = play
	elif("rating." in genre):
		rating = genre.split("rating.")
		rating = rating[1].strip()
		command = "SELECT TShow FROM TVshowlist WHERE Rating LIKE \"" + rating + "\""
		cur.execute(command)
		if not cur.fetchall():
			return("Error: Rating " + rating + " not found in library. Check and try again.")
		else:
			cur.execute(command)
			foundt = cur.fetchall()
                        max = len(foundt)
                        max = int(max) - 1
                        pcnt = randint(0, max)
                        play = foundt[pcnt][0]
	elif("duration." in genre):
                rating = genre.split("duration.")
                rating = rating[1].strip()
                command = "SELECT TShow FROM TVshowlist WHERE Duration LIKE \"" + rating + "\""
                cur.execute(command)
                if not cur.fetchall():
                        return("Error: Duration length " + rating + " not found in library. Check and try again.")
                else:
                        cur.execute(command)
                        foundt = cur.fetchall()
                        max = len(foundt)
                        max = int(max) - 1
                        pcnt = randint(0, max)
                        play = foundt[pcnt][0]
	else:
		command = "SELECT TShow FROM TVshowlist WHERE Genre LIKE \"%" + genre + "%\""
		cur.execute(command)
		if not cur.fetchall():
			return("Error. Genre: " + genre + " not found. Please try again.")
		else:
			cur.execute(command)
			foundt = cur.fetchall()
			max = len(foundt)
			max = int(max) - 1
			pcnt = randint(0, max)
			play = foundt[pcnt][0]
	play = play.rstrip()
	command = "DELETE FROM States WHERE Option LIKE \"Pending\""
	cur.execute(command)
	sql.commit()
	cur.execute("INSERT INTO States VALUES(?,?)", ('Pending',play))
	sql.commit()

	CALLMETHIS = gethonorific()
	return "How does the TV Show " + play + " sound, " + CALLMETHIS + "?"

def listshows(genre):
	command = 'SELECT TShow from TVshowlist WHERE Genre LIKE \'%' + genre + ';%\' ORDER BY TShow ASC'
	cur.execute(command)
	if not cur.fetchall():
		return("Error: " + " No shows were found in the " + genre + " genre.")
	cur.execute(command)
	play = cur.fetchall()
	shows = []
	for item in play:
		shows.append(item[0].strip())
	shows = sorted(shows)

	return (shows)

def listmovies(genre):
	if genre == "none":
		cur.execute("SELECT Movie FROM Movies ORDER BY Movie ASC")
	else:
		cur.execute("SELECT Movie FROM Movies WHERE Genre LIKE \"%" + genre + "%\" ORDER BY Movie ASC")
	thelist = cur.fetchall()
	movies = []
	for movie in thelist:
		movies.append(movie[0])

	return (movies)
		
def whatispending():
	command = "SELECT State FROM States WHERE Option LIKE \"Pending\""
	cur.execute(command)
	if not cur.fetchone():
		return ("Nothing is pending.")
	else:
		cur.execute(command)
		pending = cur.fetchone()
		pending = pending.replace("movie.","The Movie ")
		pending = pending.replace("custom.","")
		return (pending + " is currently in the pending queue.")
	
def getpending():
	command = "SELECT State FROM States WHERE Option LIKE \"Pending\""
        cur.execute(command)
        if not cur.fetchone():
                return ("Nothing is pending.")
        else:
                cur.execute(command)
                pending = cur.fetchone()[0]
		return (pending)

def playpending():
	item = getpending()
	if (item == "Nothing is pending."):
		return ("Error: Nothing is Pending Queue to Play.")
	else:
		cur.execute("DELETE FROM States WHERE Option LIKE \"Pending\"")
                sql.commit()
		say = playshow(item)
		return (say)

def addsuggestion():
	command = "SELECT State FROM States WHERE Option LIKE \"Pending\""
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
		command = "DELETE FROM States WHERE Option LIKE \"Pending\""
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
	setwebhookstatus("OFF")

def playcheckstatus():
	cmd = "python " + homedir + "playstatus.py"
	stuff = subprocess.check_output(cmd, shell=True)
	return (stuff)

def webhookscheck():
	cmd = "python " + homedir + "webhookstatus.py"
	try:
		stuff = subprocess.check_output(cmd, shell=True)
	except Exception:
		stuff = "webhookstatus.py not installed or has an error. Manual check necessary."
        return (stuff)

def webhookstatus():
	cmd = "python " + homedir + "webhookstatus.py"
        stuff = subprocess.check_output(cmd, shell=True)
	cmd = "SELECT State FROM States WHERE Option LIKE \"WEBHOOKSTATUS\""
	cur.execute(cmd)
	if not cur.fetchone():
		cur.execute("INSERT INTO States VALUES (?,?)",("WEBHOOKSTATUS","OFF"))
		sql.commit()
	cur.execute(cmd)
	wstatus = cur.fetchone()[0]
	wstatus =  (stuff + "\nWebhook checking is: " + wstatus + ".")
	return wstatus

def setwebhookstatus(value):
	value = value.lower().strip()
	if ((value == "on") or (value == "off") or (value == "sleep")):
		pass
	else:
		return ("ERROR: You must use \"ON\" or \"OFF\" to use this command.")
	if value == "on":
		value = "ON"
		playcheckstop()
	elif value == "off":
		value = "OFF"
	elif value == "sleep":
		value = "SLEEP"
	cur.execute("DELETE FROM States WHERE Option LIKE \"WEBHOOKSTATUS\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES (?,?)",("WEBHOOKSTATUS",value))
	sql.commit()
	return ("WEBHOOKSTATUS has been set to: " + value + ".")
	
	

def checkpstatus():
	openme = homedir + 'playstatestatus.txt'
        with open(openme, "r") as file:
                checkme = file.read()
        file.close()
        if "On" in checkme:
                playcheckstop()
		return ("On")
	else:
		return ("Off")

def resumestatus():
	command = "SELECT State FROM States WHERE Option LIKE \"RESUMESTATUS\""
	cur.execute(command)
	if not cur.fetchone():
		print ("No resume status. Setting to off.")
		say = setresumestatus("Off")
	else:
		cur.execute(command)
		say = cur.fetchone()[0]
	return say

def setresumestatus(option):
	option = option.lower()
	if (("on" not in option) and ("off" not in option)):
		return ("Error: You must specify 'On' or 'Off' to use this command")
	cur.execute("DELETE FROM States WHERE Option LIKE \"RESUMESTATUS\"")
	sql.commit()
	option = option.strip()
	cur.execute("INSERT INTO States VALUES (?,?)",("RESUMESTATUS",option))
	sql.commit()
	say = option
	return say

def setqueuetoplex(option):
	option = option.lower()
	if (("on" not in option) and ("off" not in option)):
		return ("Error: You must specify 'On' or 'Off' to use this command")
	cur.execute("DELETE FROM States WHERE Option LIKE \"QUEUETOPLAYLIST\"")
        sql.commit()
        option = option.strip()
        cur.execute("INSERT INTO States VALUES (?,?)",("QUEUETOPLAYLIST",option))
        sql.commit()
        say = option
        return say

def getqueuetoplaylist():
	command = "SELECT State FROM States WHERE Option LIKE \"QUEUETOPLAYLIST\""
        cur.execute(command)
        if not cur.fetchone():
                print ("No queuetoplaylist status. Setting to off.")
                say = setqueuetoplex("Off")
        else:
                cur.execute(command)
                say = cur.fetchone()[0]
        return say

def startnextprogram():
	pstatus = checkpstatus()
	plexlogin()
	commcheck = commercialcheck()
	if "On" in commcheck:
		playcommercial("none")
	show = upnext().lower()
	command = "SELECT State FROM States WHERE Option LIKE \"Playmode\""
	cur.execute(command)
	pmode = cur.fetchone()[0]
	if (("normal" in pmode) or ("binge." in pmode) or ("minithon." in pmode) or ("custom." in pmode) or ("holiday." in show)):
		rcheck = resumestatus()
		if ("on" in rcheck.lower()):
			say = playwhereleftoff(show, "none")
		else:
			say = playshow(show)
	if ("block." in show):
		say = playshow(show)
	if (("block." or "binge.") not in show):
		skipthat()
	if ("commercialmode" in show):
		playcommercial('none')
		say = "Done."
	say = say + "\n"
	if "On" in pstatus:
		time.sleep(SLEEPTIME)
		playcheckstart()
	queuetpl = qtpl()
	if ("on" in queuetpl.lower()):
		if "normal" in pmode:
			queuetoplaylist()
		elif ("block." in show):
			show = show.replace("block.","")
			blocktoplist(show)

def qtpl():
	command = "SELECT State FROM States WHERE Option LIKE \"QUEUETOPLAYLIST\""
        cur.execute(command)
        if not cur.fetchone():
                cur.execute("INSERT INTO States VALUES (?,?)",("QUEUETOPLAYLIST","Off"))
                sql.commit()
        cur.execute(command)
        queuetpl = cur.fetchone()[0]
	return queuetpl

def progress(num):
        num = int(num)
        global pcount
        try:
                        pcount
        except NameError:
                        pcount =0
        perc = round((float(pcount) / float(num)) * 100, 1)
        sys.stdout.write("\r" + str(perc) + "%")
        sys.stdout.flush()
        pcount = pcount + 1

def clearprogress():
        global pcount
        pcount = 0

def backuptvcounts():
	wfile = homedir + "tvcounts"
	with open(wfile,"w+") as file:
		file.write("")
	file.close()
	command = "SELECT * FROM TVCounts"
	cur.execute(command)
	if not cur.fetchall():
		return ("Error: No TV Counts Found to Backup.")
	cur.execute(command)
	tl = cur.fetchall()
	xnum = int(len(tl)-1)
	for itm in tl:
		if ((itm[0] == "") or ("Error:" in itm[0]) or ("movie." in itm[0])):
			cur.execute("DELETE FROM TVCounts WHERE Show LIKE \"" + itm[0] + "\"")
			sql.commit()
		else:
			wme = str(itm[0]) + ":::" + str(itm[1])
			wme = wme.strip()
			wme = wme + "\n"
			with open(wfile, "a") as file:
				file.write(wme)
			file.close()
			del wme
		progress(xnum)
	clearprogress()
	del xnum
	return ("\nTV Counts have been backed up to: \"" + wfile + "\".")

def restoretvcounts():
	wfile = homedir + "tvcounts"
	try:
		with open(wfile,"r") as file:
			tcs = file.readlines()
		file.close()
	except IOError:
		return ("Error: file \"tvcounts\" not found in \"" + homedir + "\". Make sure the tvcounts file exists in the correct location and try again.")
	print ("\nDo you want to overwrite existing entries if any exit?\n")
	cchk = input('Yes or No?: ')
	if "yes" in cchk.lower():
		cck = "yes"
	else:
		cck = "no"
	xnum = int(len(tcs)-1)
	for itm in tcs:
		itm = itm.split(":::")
		name = itm[0].strip()
		try:
			num = int(itm[1].strip())
		except ValueError:
			print num
		command = ("SELECT * FROM TVCounts WHERE Show LIKE \"" + name + "\"")
		cur.execute(command)
		if not cur.fetchone():
			cur.execute("INSERT INTO TVCounts VALUES (?,?)",(name,num))
			sql.commit()
		else:
			if (cck == "yes"):
				cur.execute("DELETE FROM TVCounts WHERE Show LIKE \"" + name + "\"")
				sql.commit()
				cur.execute("INSERT INTO TVCounts VALUES (?,?)",(name,num))
				sql.commit()
		progress(xnum)
        clearprogress()
        del xnum

	return ("\nTV Counts have been restored.\n")
			
	
def backuptvdb():
        try:
                cur.execute("DELETE FROM backshowlist")
                sql.commit()
        except Exception:
                cur.execute('CREATE TABLE IF NOT EXISTS backshowlist(TShow TEXT, Summary TEXT, Genre TEXT, Rating TEXT, Duration INT, Totalnum INT)')
                sql.commit()
	cur.execute("INSERT INTO backshowlist SELECT * FROM TVshowlist")
	sql.commit()
	print ("Shows tables has been successfully backed up.")

def restoretvdb():
        cur.execute("DELETE FROM TVshowlist")
        sql.commit()
        cur.execute("INSERT INTO TVshowlist SELECT * FROM backshowlist")
        sql.commit()
        print ("TV Shows Tables restored.")

def backupmoviedb():
	try:
                cur.execute("DELETE FROM backupmovies")
                sql.commit()
        except Exception:
                cur.execute('CREATE TABLE IF NOT EXISTS backupmovies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
                sql.commit()
        cur.execute("INSERT INTO backupmovies SELECT * FROM Movies")
        sql.commit()
        print ("Movies table has been successfully backed up.")

def restoremoviedb():
	cur.execute("DELETE FROM Movies")
        sql.commit()
        cur.execute("INSERT INTO Movies SELECT * FROM backupmovies")
        sql.commit()
	print ("Movies Tables successfully restored.")

def statuscheck():
	pmode = playmode()
	print ("Playmode: " +pmode)
	if "block." in pmode:
		pmode = pmode.replace("block.","")
		block = explainblock(pmode)
		print ("\n\n" + block + "\n")
	else:
		say = whatupnext()
		say = say.replace("''","'")
		print (say)
	pstatus = playcheckstatus()
	print ("\n" + pstatus +"\n")
	wstatus = webhookstatus()
	print (wstatus + "\n")
	resstatus = resumestatus()
	print ("Resume Feature Option is: " + resstatus)
	
	randstatus = checkblockrandom()
	print ("Random Block Option is: " + randstatus)
	custstatus = checkcustomrandom()
	print ("Custom Table Queue Option is: " + custstatus)
	favm = checkmode("movie")
	favtv = checkmode("show")
	print ("Favorites Mode Movies is: " + favm)
	print ("Favorites Mode Shows is : " + favtv)
	ccheck = commercialcheck()
	print ("Commercial Injection is: " + ccheck)
	queuetpl = qtpl()
	print ("Queue To Playlist is: " + queuetpl)
	autou = getautoupdate()
	print ("Automatic Update Status is: " + autou)
	wc = listwildcard()
	print ("The Current Wild Card Show is: " + wc)
	cur.execute("SELECT State FROM States WHERE Option LIKE \"REPLACEWILDCARD\"")
	if not cur.fetchone():
		pass
	else:
		cur.execute("SELECT State FROM States WHERE Option LIKE \"REPLACEWILDCARD\"")
		newwc = cur.fetchone()[0]
		xsay = "The Next Wild Card Show is: " + newwc + "."
		print (xsay)
	printmode()
	print ("PRINTMODE is currently: " + PRINTMODE)
	CALLMETHIS = gethonorific()
	print ("I call thee: " + CALLMETHIS)

def smartplist(thetext):
	print ("\nWarning: This action may take a few minutes depending on the size of your library.\n")
	plist = []
	plname = "TBNSmartPlayList"
	pcnt = 0
	plexlogin()
	try:
		dlist = plex.playlist(plname)
		dlist.delete()
	except Exception:
		pass
	ssec = plex.library.sections()
	try:
		for lib in ssec:
			if lib.type == "artist":
				pass
			elif (lib.type == "movie"):
				print ("Scanning " + lib.title + " now.")
				for video in lib.search(""):
					if thetext.lower() in video.summary.lower():
						if "-p" not in sys.argv:
							plist.append(video.title)
						else:
							movie = plex.library.section(lib.title).get(video.title)
							plist.append(movie)
				if (("-p" in sys.argv) and (len(plist)>0)):
					if pcnt == 0:
						plex.createPlaylist(plname,plist)
					else:
						playlist = plex.playlist(plname)
						playlist.addItems(plist)
					pcnt = pcnt + 1
								
			else:
				print ("Scanning " + lib.title + " now.")
				for video in lib.search(""):
					sname = video.title
					eps = video.episodes()
					for ep in eps:
						if thetext.lower() in ep.summary.lower():
							if "-p" not in sys.argv:
								addme = sname.strip() + ":" + str(ep.seasonNumber) + ":" + str(ep.index)
								addme = str(addme)
								plist.append(addme)
								del addme
							else:
								shows = plex.library.section(lib.title)
								movie = shows.get(video.title).get(ep.title)
								plist.append(movie)
				if (("-p" in sys.argv) and (len(plist)>0)):
					if pcnt == 0:
						plex.createPlaylist(plname,plist)
					else:
						playlist = plex.playlist(plname)
						playlist.addItems(plist)
					pcnt = pcnt + 1
		if len(plist) >0:
			if ("-p" not in sys.argv):
				print ("Scan Finished. Creating Holiday mode smartplaylist now.")
				try:
					cur.execute("DELETE FROM Holidays WHERE name LIKE \"smartplist\"")
					sql.commit()
				except sqlite3.OperationalError:
					cur.execute("CREATE TABLE IF NOT EXISTS Holidays(name TEXT, items TEXT)")
					sql.commit()
				for item in plist:
					#print ("Adding: " + item)
					say = addholiauto("smartplist",item)
				checkholidays("smartplist")
			return ("\nDone.")
		else:
			return ("Error: No items found to generate smartplaylist.")
	except KeyboardInterrupt:
		return ("\nUser Cancelled.")

def getlikemovie(xmovie):
	#print ("Finding Similar Movies.")
	global ttlchk
	found = []
	import tmdbsimple as tmdb
        tmdb.API_KEY = "ff44b56e7ea4641918abc6cf46d19a1c"
        search = tmdb.Search()
        response = search.movie(query=xmovie)
	for s in search.results:
		if s['title'].lower() == xmovie.lower():
			mid = s['id']
			movie = tmdb.Movies(mid)
			response = movie.similar_movies()
			response = response['results']
			for item in response:
				if item['title'] not in found:
					found.append(item['title'])
	if len(found) > 0:
		cfound = []
		ccnt = 0
		max = int(len(found))-1
		if ("-f" in sys.argv):
			pcnt = randint(0,max)
			playme = found[pcnt]
			return playme
		print ("Successfully Acquired Like Movies. Comparing to your library now. WARNING: This may take a moment.")
		while ccnt <= max:
			itm = found[ccnt]
			try:
				itm = titlecheck(itm)
			except Exception:
				print (itm)
				itm = "ERROR"
			ttlchk = "no"
			if (("ERROR" not in itm) and (itm not in cfound)):
				cfound.append(itm)
			ccnt = ccnt + 1
		if len(cfound) > 0:
			if ("-b" in sys.argv):
				bcnt = 0
				max = int(len(cfound))-1
				while bcnt <= max:
					print cfound[bcnt]
					if bcnt == 0:
						removeblock("smartblock")
						addblock("smartblock",cfound[bcnt])
					else:
						addtoblock("smartblock",cfound[bcnt])
					bcnt = bcnt + 1
					ttlchk = "no"
				print ("\nSuccessfully Created smartblock with the results.\n")
			print ("The following similar movies were located in your library:\n")
			for ite in cfound:
				ite = ite.replace("movie.","The Movie ")
				print ite
		else:
			print ("No similar items found in your library. Here are the similar movies found that are not in your library:\n")
			for thy in found:
				thy = thy.replace("movie.","The Movie ")
				print thy
		return ("\nDone.")
	else:
		return ("Error: Nothing similar found to: " + xmovie + ".")

def getcollection(xmovie):
	xmovie = titlecheck(xmovie)
	if ("ERROR: " in xmovie):
		return xmovie
	xmovie = xmovie.replace("movie.","")
	global ttlchk
	collection = []
	collectionx = []
	try:
		import tmdbsimple as tmdb
	except Exception:
		print ("Error: tmdb library not found. Install and try again. \"pip install tmdbsimple\"")
		return ("ERROR: tmdb library not found.")
	tmdb.API_KEY = "ff44b56e7ea4641918abc6cf46d19a1c"
	search = tmdb.Search()
	response = search.movie(query=xmovie)
	sset = "no"
	for s in search.results:
		if ((s['title'] in xmovie) and (sset == "no")):
			try:
				mid = s['id']
				movie = tmdb.Movies(mid)
				response = movie.info()
				cid = response['belongs_to_collection']
				#print cid['id']
				sset = "yes"
			except Exception:
				#print ("fail")
				pass

	try:
		movie = tmdb.Movies(mid)
	except IndexError:
		return ("Error:" + xmovie + " not found. Please try again.")
	response = movie.info()
	cid = response['belongs_to_collection']
	if not cid:
                return ("Error: " + xmovie + " is not associated with a collection.")
	cid = cid['id']
	coll = tmdb.Collections(cid)
	colld = coll.info()
	for item in colld['parts']:
		writeme = item['original_title'] + "," + item['release_date']
		collection.append(writeme)
		collectionx.append(item['original_title'])
	if ("-p" in sys.argv):
		ocoll = collection
		collection = []
		ccnt = 0
		for item in ocoll:
			item = item.split(",")
			date = item[1].strip()
			title = item[0]
			date = date.split("-")
			date = date[0]
			if ccnt == 0:
				ylidy = title.strip() + ","
			else:
				cdate = ocoll[ccnt-1]
				cdate = cdate.split(",")
				cdate = cdate[1].strip()
				cdate = cdate.split("-")
				cdate = cdate[0].strip()
				#print date
				#print cdate
				if cdate > date:
					ylidy = title.strip() + "," + ylidy
				else:
					ylidy = ylidy + "," + title.strip()
			ccnt = ccnt + 1
		#print ylidy
		collection = ylidy.split(",")
		#print collection
		collectionplist(collection)
		print ("Successfully added the following to the TBNSmartPlist:\n")
	if ("-b" in sys.argv):
		#newstuff
		ocoll = collection
                collection = []
                ccnt = 0
		dates = []
                for item in ocoll:
                        item = item.split(",")
                        date = item[1].strip()
			date = date.split("-")
			date = date[0]
			if date not in dates:
				dates.append(date)
		collection = []
		dcnt = 0
		dates.sort()
		for itm in dates:
			for item in ocoll:
				if itm in item:
					addme = item.split(",")
					addme = addme[0]
					addme = "movie."+addme
					collection.append(addme)
                #print ylidy
		collectionx = collection
		#endnewstuff
		max = int(len(collectionx))-1
		ccnt = 0
		while ccnt <= max:
			if ccnt == 0:
				removeblock("smartblock")
				addblock("smartblock",collectionx[ccnt])
			else:
				addtoblock("smartblock",collectionx[ccnt])
			ccnt = ccnt + 1
			ttlchk = "no"
		if ("getcollection" in show):
			print ("Successfully created a smartblock with the following:")
	return collectionx

def collectiontitlecheck(title):
	global ttlchk
	if "yes" not in ttlchk:
		plexlogin()
		otitle = title
		oshow = title
		try:
			cshow = str(title)
		except Exception:
			cshow = title
		cshow = title.replace("movie.","")
		#for video in plex.search(cshow):
		ssec = plex.library.sections()
		for lib in ssec:
			try:
				for video in lib.search(cshow):
					xshow = video
					if ((xshow.type.lower() == "movie") and (xshow.title.lower() == cshow.lower())):
							say = xshow
			except Exception:
				return ("Error: " + title + " not found.")
		try:
			return say
		except Exception:
			return ("Error: " + title + " not found.")

def collectionplist(array):
	collection = array
	plist = []
	for item in collection:
		ttl = collectiontitlecheck(item)
		try:
			if ("Error" in ttl):
				pass
		except Exception:
			plist.append(ttl)
	plname = "TBNSmartPlayList"
	pcnt = 0
	plexlogin()
	try:
		dlist = plex.playlist(plname)
		dlist.delete()
	except Exception:
		pass
	if (("-p" in sys.argv) and (len(plist)>0)):
		plex.createPlaylist(plname,plist)

def collectiondetails(xname):
	command = "SELECT * FROM Collections WHERE name LIKE \"" + xname + "\""
	cur.execute(command)
	if not cur.fetchone():
		return("Error: " + xname + " not found as a Collection in your Collection table.")
	cur.execute(command)
	found = cur.fetchone()
	ttls = found[1]
	ttls = ttls.split(";")
	for item in ttls:
		if item == "":
			pass
		else:
			print (item)
	return ("\nDone.")

def listcollections(cname):
	if cname == "none":
		command = "SELECT name FROM Collections"
	else:
		command = "SELECT name FROM Collections WHERE name LIKE \"%" + cname + "%\""
	cur.execute(command)
	if not cur.fetchall():
		return ("Error: No Collections found. Run \"getallcollections\" to find Collections in your library.")
	cur.execute(command)
	clist = cur.fetchall()
	cxlist = []
	for item in clist:
		cxlist.append(item[0])
	if ((len(cxlist) <30) or ("-l" in sys.argv)):
		worklist(cxlist)
	else:
		wlistcolumns(cxlist)
	return ("\nDone.")

def getcollections():
	import tmdbsimple as tmdb
	tmdb.API_KEY = "ff44b56e7ea4641918abc6cf46d19a1c"
	search = tmdb.Search()
	print ("WARNING: This action will take a while to process. It is recommended you run this during the off hours.")
	colcmd = "SELECT * FROM Collections"
	try:
		cur.execute(colcmd)
	except sqlite3.OperationalError:
		cur.execute("CREATE TABLE IF NOT EXISTS Collections(name TEXT, items TEXT)")
		sql.commit()
		if PRINTMODE == "ON":
			print ("Successfully added Collections table.")

	cur.execute("DELETE FROM Collections")
	sql.commit()
	cur.execute("SELECT Movie FROM Movies")
	mlist = cur.fetchall()
	mvlist = []
	for item in mlist:
		if item[0] not in mvlist:
			mvlist.append(item[0])

	colcount = 0
	print (len(mvlist))
	for item in mvlist:
		collection = []
		collectionx = []
		#print item
		thettl = item
		fcheck = "no"
		try:
			response = search.movie(query=item)
			sset = "no"
			for s in search.results:
				if ((s['title'] == item) and (sset == "no")):
					try:
						mid = s['id']
						movie = tmdb.Movies(mid)
						response = movie.info()
						cid = response['belongs_to_collection']
						#print cid['id']
						sset = "yes"
					except Exception:
						#print ("fail")
						pass

			try:
				movie = tmdb.Movies(mid)
			except Exception:
				fcheck = "yes"
			if fcheck == "no":
				response = movie.info()
				cid = response['belongs_to_collection']
				if not cid:
					pass
				else:
					cid = cid['id']
					coll = tmdb.Collections(cid)
					colld = coll.info()
					for item in colld['parts']:
						writeme = item['original_title'] + "," + item['release_date']
						collection.append(writeme)
						collectionx.append(item['original_title'])
					ocoll = collection
					collection = []
					ccnt = 0
					for item in ocoll:
						item = item.split(",")
						date = item[1].strip()
						title = item[0]
						date = date.split("-")
						date = date[0]
						if ccnt == 0:
							ylidy = title.strip() + ","
						else:
							cdate = ocoll[ccnt-1]
							cdate = cdate.split(",")
							cdate = cdate[1].strip()
							cdate = cdate.split("-")
							cdate = cdate[0].strip()
							#print date
							#print cdate
							if cdate > date:
								ylidy = title.strip() + "," + ylidy
							else:
								ylidy = ylidy + "," + title.strip()
						ccnt = ccnt + 1
					#print ylidy
					collection = ylidy.split(",")
					colname = colld['name']
					for item in collection:
						if item == "":
							pass
						else:
							try:
								newcol = newcol + ";" + item.strip()
							except NameError:
								newcol = item.strip()
					if ";" not in newcol:
						newcol = newcol + ";"
					cur.execute("SELECT * FROM Collections WHERE name LIKE \"" + colname + "\"")
					if not cur.fetchone():
						cur.execute("INSERT INTO Collections VALUES (?,?)",(colname, newcol))
						sql.commit()
						print ("Found Collection in your library: " + colld['name'])
					del newcol
			del collection
			del collectionx
					#print collection
		except Exception:
			#print ("Error, skipping " + thettl + ".")
			pass
	return ("\nDone.")

def wait(number):
	try:
		counter = 0
		if ("Pass" in externalcheck()):
			while counter <= number:
				progress(number)
				counter = counter + 1
				time.sleep(1)
			clearprogress()
		else:
			time.sleep(number)
	except KeyboardInterrupt:
		pass

def timechecker(thing):
	thing = thing.lower()
	thing = thing.replace("now + ","now+")
	if ("now+" in thing):
		import datetime
		thing = thing.replace("now+","")
		if ("m" in thing):
		
                        thing = thing.replace("m","")
                        thing = int(thing)
                        now = datetime.datetime.now()
                        thing = str(now + datetime.timedelta(minutes = thing))
		elif ("h" in thing):
			thing = thing.replace("h","")
			thing = int(thing)
			now = datetime.datetime.now()
			thing = str(now + datetime.timedelta(hours = thing))

		thing = thing.split(" ")
		thing = thing[1]
		thing = thing.split(":")
		hr = thing[0]
		min = thing[1]
		thing = hr + ":" + min
		
	if (" am" in thing):
		thing = thing.replace(" am"," AM")
	if (" pm" in thing):
		thing = thing.replace(" pm"," PM")
	cck = thing
	cck = thing.split(":")
	cck = thing[0]
	if ((cck > 0) and ("am" not in thing.lower()) and ("pm" not in thing.lower())):
		#print ("Given 24hr time. Converting...")
		from datetime import datetime
		d = datetime.strptime(thing, "%H:%M")
		thedate = d.strftime("%-I:%M %p")
	else:
		thedate = thing
	return thedate

def availableactions(actn):
	if actn == "none":
		command = "SELECT * FROM help ORDER BY name ASC"
	else:
		command = "SELECT * FROM help WHERE name LIKE \"%" + actn + "%\""
	cur.execute(command)
	found = cur.fetchall()
	actns = []
	for item in found:
		actns.append(item[0])
	return actns

def trivia(movie):
	movie = titlecheck(movie)
        if ("ERROR: " in movie):
                return movie
        movie = movie.replace("movie.","")
	try:
		import imdb
	except Exception:
		return ("Error: You must install the imdbpy library to use this action.")
	i = imdb.IMDb()
	movie = movie.strip()
	mvlst = i.search_movie(movie)
	mve = mvlst[0]
	i.update(mve)
	i.update(mve, 'trivia')
	try:
		tlist = mve['trivia']
	except Exception:
		return ("No trivia options available for this option.")
	min = 0
	max = len(mve['trivia'])
	rand = randint(min,max)
	return (tlist[rand])

def whodirected(xmovie):
	try:
                import imdb
        except Exception:
                return ("Error: You must install the imdbpy library to use this action.")
	i = imdb.IMDb()
	movie = xmovie.strip()
	mvlist = i.search_movie(movie)
        mve = mvlist[0]
	if ((mve.data['kind'] == "tv series") and ("-s" not in sys.argv)):
                        mve = mvlist[1]
        i.update(mve)
	nme = mve.data['director']
	direct = nme[0]
	return direct

def whoplayed(ctr, xmovie):
	try:
                import imdb
        except Exception:
                return ("Error: You must install the imdbpy library to use this action.")
        i = imdb.IMDb()
        movie = xmovie.strip()
	try:
		mvlist = i.search_movie(movie)
		mve = mvlist[0]
		if ((mve.data['kind'] == "tv series") and ("-s" not in sys.argv)):
			mve = mvlist[1]
	except Exception:
		return ("ERROR: " + xmovie + " not found.")
			
        i.update(mve)
	#print (mve.data['kind'])
	nme = mve.data['cast']
	for actr in nme:
		if str(actr.currentRole).lower() == str(ctr).lower():
			direct = actr
	try:
		direct
	except Exception:
		for actr in nme:
			#print str(actr.currentRole)
			if str(ctr).lower() in str(actr.currentRole).lower():
				direct = actr
	try:
		direct
	except Exception:
		if " " not in ctr:
			pass
		else:
			print ("Failed with given name. Trying a hail marry.")
			excludeme = ['a','the','of','for','at']
			ctst = ctr.split(" ")
			for itm in ctst:
				if itm in excludeme:
					pass
				else:
					for actr in nme:
						if str(itm).lower() in str(actr.currentRole).lower():
							direct = actr
				
	try:
		direct
	except Exception:
		direct = "ERROR: " + ctr + " Not Found in " + xmovie + "."

        return direct

def goofs(movie):
	try:
               import imdb
        except Exception:
               return ("Error: You must install the imdbpy library to use this action.")
        i = imdb.IMDb()
        movie = movie.strip()
        mvlst = i.search_movie(movie)
        mve = mvlst[0]
	i.update(mve)
        i.update(mve, 'all')
        min = 0
        max = len(mve['quotes'])
        rand = randint(min,max)
        return (mve['quotes'][rand])

def faqs(movie):
	movie = titlecheck(movie)
        if ("ERROR: " in movie):
                return movie
        movie = movie.replace("movie.","")
	try:
               import imdb
        except Exception:
               return ("Error: You must install the imdbpy library to use this action.")
        i = imdb.IMDb()
        movie = movie.strip()
        mvlst = i.search_movie(movie)
        mve = mvlst[0]
        i.update(mve)
        i.update(mve, ['faqs'])
        min = 0
        max = len(mve['faqs'])
        rand = randint(min,max)
        return (mve['faqs'][rand])

def triviagame():
	mve = suggestmovieblockuse("none")
	randc = randint(0,7)
	#randc = 7
	if randc == 5:
		pass
	else:
		try:
			cur.execute("DELETE FROM States WHERE Option LIKE \"THEANSWER\"")
			sql.commit()
		except Exception:
			pass
		THEANSWER = mve.strip()
		mve = mve.replace("movie.","The Movie ")
		cur.execute("INSERT INTO States VALUES (?,?)",("THEANSWER",THEANSWER))
		sql.commit()
	if randc == 0:
		say = trivia(mve)
		say = "Guess the movie based on this random fact:\n" + say
	elif randc == 1:
		say = whodirected(mve)
		say2 = movierating(mve)
                say = "This movie was directed by: " + str(say) + " and rated: " + say2 + "."
	elif randc == 2:
		plexlogin()
		mve = mve.replace("movie.","")
		for video in plex.search(mve):
			if video.type == "movie":
				#print (video.roles)
				starring = []
				scnt = 0
				if len(video.roles)<2:
					smax = int(len(video.roles))-1
				else:
					smax = 2
				while scnt <= smax:
					starring.append(video.roles[scnt].tag)
					scnt = scnt + 1
				for itm in starring:
					try:
						xstar = xstar + itm + "\n"
					except NameError:
						xstar = itm + "\n"
				say = "This movie starred:\n" + xstar
	elif randc == 3:
		say = movietagline(mve)
		if say == "__NA__":
			print ("No Tagline, trying again.")
			say = triviagame()
		say = "This Movies Tagline is:\n" + say
	elif randc == 4:
		import imdb
		i = imdb.IMDb()
		mvlist = i.search_movie(mve)
		mve = mvlist[0]
		if ((mve.data['kind'] == 'tv series') and ("-s" not in sys.argv)):
			mve = mvlist[1]
		i.update(mve)
		nme = mve.data['cast']
		acnt = randint(0,2)
		actr = nme[acnt]
		cname = actr.currentRole
		say = str(actr) + " played " + str(cname) + " in one of the main roles."
	elif randc == 5:
		import imdb
                i = imdb.IMDb()
                mvlist = i.search_movie(mve)
                mve = mvlist[0]
                if ((mve.data['kind'] == 'tv series') and ("-s" not in sys.argv)):
                        mve = mvlist[1]
                i.update(mve)
                nme = mve.data['cast']
                acnt = randint(0,2)
                actr = nme[acnt]
                cname = actr.currentRole
		THEANSWER = "ACTOR." + str(actr).strip()
		try:
			cur.execute("DELETE FROM States WHERE Option LIKE \"THEANSWER\"")
			sql.commit()
		except Exception:
			pass
		cur.execute("INSERT INTO States VALUES (?,?)",("THEANSWER",THEANSWER))
		sql.commit()
		say = "Who played " + str(cname) + " in the movie : " + str(mve) + "."
	elif randc == 6:
		mve = mve.replace("movie.","")
		say = moviesummary(mve)
		if ("has no summary" in say):
			say = triviagame()
		else:
			say = "This movie has the following summary:\n" + say
	elif randc == 7:
                import imdb
                i = imdb.IMDb()
                mvlist = i.search_movie(mve)
                mve = mvlist[0]
                if ((mve.data['kind'] == 'tv series') and ("-s" not in sys.argv)):
                        mve = mvlist[1]
                i.update(mve)
                nme = mve.data['cast']
                acnt = randint(0,2)
                actr = nme[acnt]
                cname = actr.currentRole
                THEANSWER = "ACTOR." + str(cname).strip()
                try:
                        cur.execute("DELETE FROM States WHERE Option LIKE \"THEANSWER\"")
                        sql.commit()
                except Exception:
                        pass
                cur.execute("INSERT INTO States VALUES (?,?)",("THEANSWER",THEANSWER))
                sql.commit()
                say = "Who did " + str(actr) + " play in the movie : " + str(mve) + "."
		


	try:
		cur.execute("DELETE FROM States WHERE Option LIKE \"THEQUESTION\"")
		sql.commit()
	except Exception:
		pass
	cur.execute("INSERT INTO States VALUES (?,?)",("THEQUESTION",say))
	sql.commit()
	return (say)

def triviahint():
	mve = triviaanswer()
	if mve == "NOANSWER":
		return ("Wait for next round.")
	elif ("ACTOR." in mve):
		return ("There are no hints for this question.")
	LASTO = lasttriviaoption()
	randc = randint(0,4)
	#randc = 4
	while str(randc) == str(LASTO):
		randc = randint(0,4)
	setlasttriviaoption(randc)
	if randc == 0:
		say = trivia(mve)
                say = "This movie has the following random fact:\n" + say
        elif randc == 1:
                say = whodirected(mve)
                say = "This movie was directed by:\n" + str(say)
        elif randc == 2:
                plexlogin()
                mve = mve.replace("movie.","")
                for video in plex.search(mve):
                        if video.type == "movie":
                                #print (video.roles)
                                starring = []
                                scnt = 0
                                if len(video.roles)<2:
                                        smax = int(len(video.roles))-1
                                else:
                                        smax = 2
                                while scnt <= smax:
                                        starring.append(video.roles[scnt].tag)
                                        scnt = scnt + 1
                                for itm in starring:
                                        try:
                                                xstar = xstar + itm + "\n"
                                        except NameError:
                                                xstar = itm + "\n"
                                say = "This movie starred:\n" + xstar
        elif randc == 3:
                say = movietagline(mve)
                if say == "__NA__":
                        print ("No Tagline, trying again.")
                        say = triviahint()
		else:
			say = "This Movies Tagline is:\n" + say
	elif randc == 4:
                import imdb
                i = imdb.IMDb()
                mvlist = i.search_movie(mve)
                mve = mvlist[0]
                if ((mve.data['kind'] == 'tv series') and ("-s" not in sys.argv)):
                        mve = mvlist[1]
                i.update(mve)
                nme = mve.data['cast']
                acnt = randint(0,2)
                actr = nme[acnt]
                cname = actr.currentRole
                say = str(actr) + " played " + str(cname) + " in one of the main roles."
	return (say)

def setlasttriviaoption(num):
	try:
		cur.execute("DELETE FROM States WHERE Option LIKE \"LASTTRIVIAOPTION\"")
		sql.commit()
	except Exception:
		pass
	cur.execute("INSERT INTO States VALUES (?,?)", ("LASTTRIVIAOPTION",str(num)))
	sql.commit()

def lasttriviaoption():
	cmd = "SELECT State FROM States WHERE Option LIKE \"LASTTRIVIAOPTION\""
	cur.execute(cmd)
	if not cur.fetchone():
		return ("None")
	cur.execute(cmd)
	LASTO = cur.fetchone()[0]
	return LASTO
		

def triviaanswer():
	try:
		cur.execute("SELECT State FROM States WHERE Option LIKE \"THEANSWER\"")
		THEANSWER = cur.fetchone()[0]
		return THEANSWER
	except TypeError:
		return ("No recent trivia questions asked.")

def triviaclearanswer():
	try:
		cur.execute("DELETE FROM States WHERE Option LIKE \"THEANSWER\"")
		sql.commit()
		cur.execute("DELETE FROM States WHERE Option LIKE \"THEQUESTION\"")
		sql.commit()
	except Exception:
		pass
	addme = "NOANSWERS"
	qaddme = "NOQUESTION"
	cur.execute ("INSERT INTO States VALUES (?,?)",("THEANSWER",addme))
	sql.commit()
	cur.execute ("INSERT INTO States VALUES (?,?)",("THEQUESTION",qaddme))
        sql.commit()
	return ("Done.")

def triviaquestion():
	try:
		cur.execute("SELECT State FROM States WHERE Option LIKE \"THEQUESTION\"")
		if not cur.fetchone():
			THEQUESTION = "No Recent Trivia Questions."
		else:
			cur.execute("SELECT State FROM States WHERE Option LIKE \"THEQUESTION\"")
			THEQUESTION = cur.fetchone()[0]
			if THEQUESTION == "NOQUESTION":
				THEQUESTION = "No Recent Trivia Questions. Wait for next round."
	except Exception:
		THEQUESTION = "No Recent Trivia Questions."
	return THEQUESTION

def deletefromtable(table,title):
	badtables = ['blocks','schedules','states','tvcounts','help','replaceinblock','settings','customtitles','collections','holidays','musicalbums','musicartists']
	if table.lower() in badtables:
		return ("Error: Invalid Table Selected. Please Try again.")
	if ("custom_" in table.lower()):
		OPTION = "name"
	elif ("movie" in table.lower()):
		OPTION = "Movie"
	elif (("commercials" in table.lower()) or ("prerolls" in table.lower())):
		OPTION = "name"
	elif ("shows" in table.lower()):
		OPTION = "TShow"
	cmd = "DELETE FROM " + table.strip() + " WHERE " + OPTION.strip() + " LIKE \"" + title.strip() + "\""
	try:
		chcmd = "SELECT * FROM " + table.strip() + " WHERE " + OPTION.strip() + " LIKE \"" + title.strip() + "\""
		cur.execute(chcmd)
		if not cur.fetchone():
			return ("ERROR: Title " + title + " not found in " + table + " to remove.")
		cmd = str(cmd)
		cur.execute(cmd)
		sql.commit()
		return ("Successfully Deleted: " + title + " from " + table)
	except IndexError:
		return ("Error: Command failed\n" + cmd)

def setprintmode(option):
	option = option.lower().strip()
	if (option == "on"):
		option = "ON"
	elif (option == "off"):
		option = "OFF"
	else:
		return ("ERROR: PRINTMODE can only be set to \"ON\" or \"OFF\"")
	cur.execute("DELETE FROM States WHERE Option LIKE \"PRINTMODE\"")
	sql.commit()
	cur.execute("INSERT INTO States VALUES(?,?)",("PRINTMODE",option))
	sql.commit()
	return ("PRINTMODE has been set to: " + option + ".")

def printmode():
	global PRINTMODE
	cmd = "SELECT State FROM States WHERE Option LIKE \"PRINTMODE\""
	cur.execute(cmd)
	if not cur.fetchone():
		cur.execute("INSERT INTO States VALUES (?,?)",("PRINTMODE","ON"))
		sql.commit()
	else:
		cur.execute(cmd)
		pstate = cur.fetchone()[0]
		PRINTMODE = pstate

def versioncheck():
	version = "4.01"
	return version
	

#commandsgohere
printmode()
try:	
	if (("-h" in sys.argv) or ("-l" in sys.argv)):
		if ("-h" in sys.argv):
			show = argprocessor("-h")
		else:
			show = argprocessor("-l")
	else:
		
		show = str(sys.argv[1])
	show = show.replace("+"," ")
	if ("-h" in sys.argv):
                for argv in sys.argv:
                        if ((argv == "-h") or ("system.py" in argv)):
                                pass
                        else:
				try:
					say = helpme(argv)
				except sqlite3.OperationalError:
					updatehelp()
					cls()
					if PRINTMODE == "ON":
						print ("Successfully Updated Help Files.")
					say = helpme(argv)
                try:
                        say
                except NameError:
                        say = "Sorry, but that entry was not found in the help table. Run \"updatehelp\" and try again if you have not updated recently."
	elif ("deletefromtable" in show):
		try:
			tbl = str(sys.argv[2])
			ttl = str(sys.argv[3])
			say = deletefromtable(tbl,ttl)
		except IndexError:
			say = "Error: You must supply both a table name and a title from that table to use this command."
	elif ("getprintmode" in show):
		say = PRINTMODE
	elif("setprintmode" in show):
		try:
			option = str(sys.argv[2])
			say = setprintmode(option)
		except IndexError:
			say = "ERROR: You must specify \"ON\" or \"OFF\" to use this command."
	elif ("triviagame" in show):
		say = triviagame()
	elif ("triviaanswer" in show):
		say = triviaanswer()
		say = say.replace("ACTOR.","")
	elif ("triviaclearanswer" in show):
		say = triviaclearanswer()
	elif ("triviaquestion" in show):
		say = triviaquestion()
	elif ("triviahint" in show):
		say = triviahint()
	elif ("playpending" in show):
		say = playpending()
	elif ("gencheck" in show):
		show = sys.argv[2]
		say = gencheck(show)
	elif ("sethonorific" in show):
		try:
			myname = sys.argv[2]
		except Exception:
			myname = "none"
		say = sethonorific(myname)
	elif ("gethonorific" in show):
		say = gethonorific()
		say = "I call thee: " + say
	elif (show == "trivia"):
		try:
			movie = sys.argv[2]
			say = trivia(movie)
		except IndexError:
			say = "Error: You must enter a movie to use this action."
	elif ("faqs" in show):
                try:
                        movie = sys.argv[2]
                        say = faqs(movie)
                except IndexError:
                        say = "Error: You must enter a movie to use this action."
	elif ("whodirected" in show):
                try:
                        movie = sys.argv[2]
                        say = whodirected(movie)
                except IndexError:
                        say = "Error: You must enter a movie to use this action."
	elif ("whoplayed" in show):
                try:
			char = sys.argv[2]
                        movie = sys.argv[3]
                        say = whoplayed(char, movie)
                except IndexError:
                        say = "Error: You must enter a movie to use this action."
	elif ("moviewithtline" in show):
		try:
			tline = sys.argv[2]
			say = moviewithtline(tline)
		except IndexError:
			say = "Error: You must supply a Tagline to use this command."
	elif ("setsleeptime" in show):
		try:
			num = str(sys.argv[2])
			say = setsleeptime(num)
		except IndexError:
			say = "ERROR: You must specify a Intiger to use this command."
	elif ("listcollections" in show):
		try:
			cname = str(sys.argv[2])
		except IndexError:
			cname = "none"
		say = listcollections(cname)
	elif ("schedchecker" in show):
		for item in sys.argv:
			try:
				say = say + " " + item
			except NameError:
				say = item
		say = schedchecker(say)
	elif ("collectiondetails" in show):
		col = sys.argv[2]
		say = collectiondetails(col)
	elif ("getallcollections" in show):
		say = getcollections()
	elif ("getcollection" in show):
		movie = str(sys.argv[2])
		sme = getcollection(movie)
		if (("Error" in sme) or ("ERROR" in sme)):
			say = sme
		else:
			try:
				for item in sme:
					print item
			except Exception:
				pass
			say = "\nDone."
	elif ("getlikemovie" in show):
		movie = str(sys.argv[2])
		say = getlikemovie(movie)
	elif ("smartplist" in show):
		thetext = sys.argv[2]
		say = smartplist(thetext)
	elif ("swhere" in show):
		num = sys.argv[2]
		say = swhere(num)
	elif ("timechecker" in show):
		ttime = sys.argv[2]
		say = timechecker(ttime)
	elif ("wait" in show):
		try:
			num = int(sys.argv[2])
			wait(num)
			say = "" 
		except NameError:
			say = "Error: You must supply an intiger to use this action."
	elif ("addschedule" in show):
		try:
			action = str(sys.argv[2])
			time = str(sys.argv[3])
			time = timechecker(time)
			day = str(sys.argv[4])
			say = addschedule(action, time, day)
		except IndexError:
			say = "Error: You must suppily an \"action,\" \"time,\" and \"day\" to use this command."
	elif ("removeschedule" in show):
		try:
			time = sys.argv[2]
			day = sys.argv[3]
			say = removeschedule(time,day)
		except IndexError:
			say = "Error: You must provde a time and a day/date to use this command."
	elif ("viewschedules" in show):
		say = viewschedules()
	elif ("clearschedule" in show):
		say = clearschedules()
	elif ("deleteshow" in show):
		show = sys.argv[2]
		say = deleteshow(show)
	elif ("backuptvcounts" in show):
		say = backuptvcounts()
	elif ("restoretvcounts" in show):
		say = restoretvcounts()
	elif ("backuptvdb" in show):
		backuptvdb()
		say = "Done."
	elif ("removetvdb" in show):
		removetvdb()
		say = "Done."
	elif ("restoretvdb" in show):
		restoretvdb()
		say = "Done."
	elif ("backupmoviedb" in show):
                backupmoviedb()
                say = "Done."
        elif ("removemoviedb" in show):
                removemoviedb()
                say = "Done."
        elif ("restoremoviedb" in show):
                restoremoviedb()
                say = "Done."
	elif ("updatehelp" in show):
		updatehelp()
		say = "Done."
	elif ("updatechecker" in show):
		updatechecker()
		say = "\nDone."
	elif ("setautoupdate" in show):
		val = sys.argv[2]
		say = setautoupdate(val)
	elif ("getautoupdate" in show):
		say = getautoupdate()
	elif ("playmusic" in show):
		try:
			artist = str(sys.argv[2])
			try:
				song = sys.argv[3]
			except IndexError:
				song = "none"
			playmusic(artist,song)
			say = "done"
		except Exception:
			say = "Error: You must supply a artist and optionally a song to proceed."
	elif ("musicstartnext" in show):
		musicstartnext()
		say = "Done"
	elif ("setmusicclient" in show):
		setmusicclient()
		say = "done"
	elif ("listplaylistitems" in show):
		try:
			plist = str(sys.argv[2])
			listplaylistitems(plist)
			say = "done"
		except IndexError:
			say = "Error: You must specify a playlist to use this command."
	elif ("playplaylist" in show):
		try:
			playlist = str(sys.argv[2])
			say = playplaylist(playlist)
		except IndexError:
			say = "Error: You must specify a playlist to use this command."
	elif ("getartists" in show):
		say = getartists()
		say = wlistcolumns(say)
	elif ("getalbums" in show):
		try:
			artist = str(sys.argv[2])
			say = getalbums(artist)
			if "Error" not in say:
				worklist(say)
				say = "Done"

		except IndexError:
			say = "Error: You must specify an artist to use this command."
	elif ("getsongs" in show):
		try:
			artist = str(sys.argv[2])
			album = str(sys.argv[3])
			say = getsongs(artist, album)
			say = wlistcolumns(say)
		except IndexError:
			say = "Error: you must supply an album to use this command."
	elif ("availableactions" in show):
		try:
			if sys.argv[2] == "-l":
				actn = "none"
			else:
				actn = sys.argv[2]
		except IndexError:
			actn = "none"
		say = availableactions(actn)
		if ("-l" not in sys.argv):
			say = wlistcolumns(say)
		else:
			say = worklist(say)
	elif ("getcustomtitle" in show):
		title = str(sys.argv[2])
		say = getcustomtitle(title)
	elif ("checkcustomtable" in show):
		item = str(sys.argv[2])
		say = checkcustomtables(item)
	elif ("getcustomtable" in show):
		table = str(sys.argv[2])
		say = getcustomtable(table)
		if ("Error:" in say):
			pass
		elif ((int(len(say)) <= 10) or ("-l" in sys.argv)):
			say = worklist(say)
		else:
			say = wlistcolumns(say)
	elif ("listcustomtables" in show):
		stuff = listcustomtables()
		if ((int(len(stuff)) <=10) and ("-l" not in sys.argv)):
			say = worklist(stuff)
		else:
			say = wlistcolumns(stuff)
	elif ("statuscheck" in show):
		statuscheck()
		say = "Done."
	elif ("replacecheck" in show):
		item = sys.argv[2]
		say = replacecheck(item)
	elif ("replacestatus" in show):
		try:
			show = str(sys.argv[2])
			say = replacestatus(show)
		except IndexError:
			say = "Error: You must specify a show to use this command."
	elif ("replaceshowinblock" in show):
		try:
			show = str(sys.argv[2])
			nshow = str(sys.argv[3])
			block = str(sys.argv[4])
			playflag = str(sys.argv[5])
			say = replaceshowinblock(show, nshow, block, playflag)
		except IndexError:
			say = "You must provide a show, new show, block, and playflag(yes/no) to use this command."
	elif ("jumpinblock" in show):
		try:
			xnum = sys.argv[2]
			say = jumpinblock(xnum)
			say2 = whatupnext()
			say = say + "\n" + say2
		except IndexError:
			say = "Error: You must specify where in the block to jump."
			
	elif (("resumestatus" in show) and ("set" not in show)):
		say = resumestatus()
		say = "Resume Status is: " + say + "."
	elif ("setresumestatus" in show):
		option = str(sys.argv[2])
		say = setresumestatus(option)
		if "Error" not in say:
			say = "Resume Status has been set to: " + say + "."
	elif (("queuetoplexstatus" in show) and ("set" not in show)):
                say = getqueuetoplaylist()
                say = "Queuetoplaylist Status is: " + say + "."
        elif ("setqueuetoplex" in show):
                option = str(sys.argv[2])
                say = setqueuetoplex(option)
                if "Error" not in say:
                        say = "Queuetoplaylist Status has been set to: " + say + "."
	elif (("titlecheck" in show) and ("customtitlecheck" not in show)):
		show = str(sys.argv[2])
		show = titlecheck(show)
		sect = getsection(show)
		say = show + ", Section: " + sect
	elif ("customtitlecheck" in show):
		show = sys.argv[2]
		say = customtitlecheck(show)

	elif ("addcustomtitle" in show):
		try:
			ntitle = str(sys.argv[2])
			otitle = str(sys.argv[3])
			say = addcustomtitle(ntitle,otitle)
		except IndexError:
			say = "ERROR: You must provide both a new title and an original title to use this action."
	elif ("removecustomtitle" in show):
		try:
			ctitle = str(sys.argv[2])
			say = removecustomtitle(ctitle)
		except IndexError:
			say = "Error: You must supply a custom title to use this action."
	elif ("checkholidays" in show):
		try:
			holiday = str(sys.argv[2])
		except IndexError:
			holiday = "none"
		say = checkholidays(holiday)
	elif ("addholiday" in show):
		try:
			holiday = str(sys.argv[2])
			title = str(sys.argv[3])
			say = addholiday(holiday,title)
		except IndexError:
			say = "Error: You must supply both a holiday and a title to use this command"
	elif ("removeholiday" in show):
		try:
			holiday = str(sys.argv[2])
			say = removeholiday(holiday)
		except IndexError:
			say = "Error: You must provide a holiday to use this command."
	elif ("removefromholiday" in show):
                try:
                        holiday = str(sys.argv[2])
                        title = str(sys.argv[3])
                        say = removefromholiday(holiday,title)
                except IndexError:
                        say = "Error: You must supply both a holiday and a title to use this command"
	elif ("playholiday" in show):
		try:
			holiday = str(sys.argv[2])
			say = playholiday(holiday)
		except IndexError:
			say = "Error: You must specify a holiday to use this command."
	elif ("movielink" in show):
		movie = str(sys.argv[2])
		movielink(movie)
		say = "Done"
	elif ("changeplexpw" in show):
		try:
			password = str(sys.argv[2])
			say = changeplexpw(password)
		except IndexError:
			password = getpass.getpass("Password: ")
			say = changeplexpw(password)
	elif ("changeplexip" in show):
		changeplexip()
		say = "Done."
	elif ("moviegenrefixer" in show):
		moviegenrefixer()
		say = "Done."
	elif ("approvedratings" in show):
		say = approvedratings()
	elif ("addapprovedrating" in show):
		try:
			rating = str(sys.argv[2])
			say = addapprovedrating(rating)
		except IndexError:
			say = "Error: You must provide a rating to use this command."
	elif ("removeapprovedrating" in show):
                try:
                        rating = str(sys.argv[2])
                        say = removeapprovedrating(rating)
                except IndexError:
                        say = "Error: You must provide a rating to use this command."
	elif ("setkidspassword" in show):
		try:
			pw = str(sys.argv[2])
			say = setkidspassword(pw)
		except Exception:
			pw = getpass.getpass("New Password: ")
			say = setkidspassword(pw)
	elif ("restartshow" in show):
		try:
			show = str(sys.argv[2])
			say = restartshow(show)
		except IndexError:
			say = "Error: You must provide a show name to use this command."
	elif ("moviechoice" in show):
		try:
			option = str(sys.argv[2])
			say = moviechoice(option)
		except IndexError:
			#say = "Error. You must include an genre. rating. or actor. to use this command."
			option = "genre.none"
			say = moviechoice(option)
	elif ("tvchoice" in show):
		try:
                        option = str(sys.argv[2])
                        say = tvchoice(option)
                except IndexError:
                        say = "Error. You must include an genre. rating. or duration. to use this command."
	elif ("enablekidsmode" in show):
		say = enablekidsmode()
	elif ("disablekidsmode" in show):
		say = disablekidsmode()
	elif ("checkblockrandom" in show):
		say = checkblockrandom()
		say = "BLOCKRANDOM is " + say + "."
	elif ("setblockrandom" in show):
		try:
			option = str(sys.argv[2])
			say = enableblockrandom(option)
		except IndexError:
			say = "Error: You must specify either \"on\" or \"off\" to use this command."
	elif ("setcustomrandom" in show):
                try:
                        option = str(sys.argv[2])
                        say = enablecustomrandom(option)
                except IndexError:
                        say = "Error: You must specify either \"on\" or \"off\" to use this command."
	elif ("enablecommercials" in show):
		say = enablecommercials()
	elif ("disablecommercials" in show):
		say = disablecommercials()
	elif ("playcommercial" in show):
		try:
			comm = str(sys.argv[2])
		except IndexError:
			comm = "none"
		say = playcommercial(comm)
	elif (("commercialbreak" in show) and ("setcommercialbreakcount" not in show)):
		commercialbreak()
		say = "Done."
	elif ("setcommercialbreakcount" in show):
		try:
			number = int(sys.argv[2])
			say = setcommercialbreakcount(number)
		except Exception:
			say = "Error: You must provide a number to use this command."
			
	elif ("playpreroll" in show):
		try:
			comm = str(sys.argv[2])
			comm = comm.replace("preroll.","")
		except IndexError:
			comm = "none"
		playpreroll(comm)
		say = "done"
	elif ("listprerolls" in show):
		listprerolls()
		say = "Done."
	elif ("listcommercials" in show):
		listcommercials()
		say = "Done."
	elif ("commercialcheck" in show):
		say = commercialcheck()
		say = "Commercials are currently: " + say + "."
	elif ("listplexplaylists" in show):
		say = getplexplaylists()
		say = worklist(say)
	elif ("addplaylist" in show):
		try:
			title = str(sys.argv[2])
			artist = str(sys.argv[3])
			item = str(sys.argv[4])
			say = addplaylist(title, artist, item)
		except IndexError:
			say = "Error: you must specify a title, artist, and an item to use this command."
	elif ("addtoplaylist" in show):
                try:
                        title = str(sys.argv[2])
                        artist = str(sys.argv[3])
                        item = str(sys.argv[4])
                        say = addtoplaylist(title, artist, item)
                except IndexError:
                        say = "Error: you must specify a title, artist, and an item to use this command."
	elif ("blocktoplist" in show):
		block = str(sys.argv[2])
		say = blocktoplist(block)
	elif ("queuetoplaylist" in show):
			say = queuetoplaylist()
	elif ("addapproved" in show):
		try:
			title = str(sys.argv[2])
			say = addapproved(title)
		except IndexError:
			say = "Error: You must specify a title to use this command"
	elif ("removeapproved" in show):
		try:
			title = str(sys.argv[2])
			say = removeapproved(title)
		except IndexError:
			say = "Error: You must specify a title to use this command."
	elif ("addrejected" in show):
		try:
                        title = str(sys.argv[2])
                        say = addrejected(title)
                except IndexError:
                        say = "Error: You must specify a title to use this command"
	elif ("showrejected" in show):
		showrejected()
		say = "Done."
	elif ("showapproved" in show):
		showapproved()
		say = "Done."
	elif ("enablefavoritesmode" in show):
		try:
			option = str(sys.argv[2])
			say = enablefavoritesmode(option)
		except IndexError:
			say = "Error: You must supply add either 'shows' or 'movies' to use this command."
	elif ("disablefavoritesmode" in show):
		try:
                        option = str(sys.argv[2])
                        say = disablefavoritesmode(option)
                except IndexError:
                        say = "Error: You must supply add either 'shows' or 'movies' to use this command."
	elif ("checkfavoritesmode" in show):
		try:
                        option = str(sys.argv[2])
			option = option.replace("shows","show")
			option = option.replace("movies","movie")
                        say = checkmode(option)
			if ("Error" in say):
				say = "Error: You must supply add either 'shows' or 'movies' to use this command."
			else:
				say = "Favorites " + show + " mode is currently: " + say
                except IndexError:
                        say = "Error: You must supply add either 'shows' or 'movies' to use this command."
	elif ("addfavoritemovie" in show):
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
		except IndexError:
			say = "Error: Both a Movie and a Show are required to use this command."
	elif ("removegenremovie" in show):
		try:
			movie = str(sys.argv[2])
			genre = str(sys.argv[3])
			say = removegenremovie(movie, genre)
		except IndexError:
			say = "Error: Both a Movie and a Show are required to use this command."
			
	elif ("queueadd" in show):
		addme = str(sys.argv[2])
		say = queueadd(addme)
		say = say + " has been added to the queue."
		#saythat(say)
	elif ("whereat" in show):
		plexlogin()
		if PRINTMODE == "ON":
			nowp = nowplaying()
			say = whereat()
			say = "For " + nowp + "- " + say 
		else:
			say = whereat()
	elif ("listwildcard" in show):
		say = listwildcard()
		say = "The Current Wild Card Show is: " + say
		cur.execute("SELECT State FROM States WHERE Option LIKE \"REPLACEWILDCARD\"")
		if not cur.fetchone():
			pass
		else:
			cur.execute("SELECT State FROM States WHERE Option LIKE \"REPLACEWILDCARD\"")
			newwc = cur.fetchone()[0]
			say = say + "\nThe Next Wild Card Show is: " + newwc + "."
	elif ("changewildcard" in show):
		try:
			show = str(sys.argv[2])
		except Exception:
			show = "none"
		say = changewildcard(show)
	elif ("replacewildcard" in show):
		try:
			show = str(sys.argv[2])
			say = replacewildcard(show)
		except Exception:
			say = "Error: You must specify a show name to use this command."
	elif ("idtonightsmovie" in show):
		say = idtonightsmovie()
		say = say.replace("movie.", "The Movie ")
		say = "Tonights feature is " + say 
	elif ("idtonightsshow" in show):
		say = idtonightsshow()
		say = "Tonights show is " + say
	elif ("settonightsmovie" in show):
		try:
			movie = str(sys.argv[2])
			say = settonightsmovie(movie)
		except IndexError:
			say = "Error: You must provide a movie to use this command."
	elif ("findnewmovie" in show):
		say = findnewmovie()
	elif ("getnewblock" in show):
		say = getnewblock()
	elif ("randommovieblock" in show):
		try:
			genre = str(sys.argv[2])
		except IndexError:
			genre = "none"
		say = randommovieblock(genre)
	elif ("randomtvblock" in show):
		try:
			genre = str(sys.argv[2])
		except IndexError:
			genre = "none"
		say = randomtvblock(genre)
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
		#say = "Playback has been stopped. A new program will start unless you have already stopped playstatus.py"
		say = "Playback has been stopped."
	elif ("pauseplay" in show):
		plexlogin()
		pauseplay()
		say = "Playback has been paused."
	elif ("stopmusic" in show):
		stopmusic()
		say = "Music has been stopped."
	elif ("pausemusic" in show):
		pausemusic()
		say = "Music has been paused/resumed."
	elif ("hitok" in show):
		plexlogin()
		hitok()
		say = "done"
	elif (("skipahead" in show) and ("series" not in show)):
		plexlogin()
		try:
			val = sys.argv[2]
		except IndexError:
			val = "none"
		say = skipahead(val)
	elif (("skipback" in show) and ("series" not in show)):
		plexlogin()
		try:
			val = sys.argv[2]
			say = skipback(val)
		except IndexError:
			say = skipback("none")
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
		CALLMETHIS = gethonorific()
		say = "Playback State Checking will stop, and the system will sleep when the current program ends. Be well, " + CALLMETHIS + "."
	elif ("getwebhookstatus" in show):
		say = webhookstatus()
	elif ("setwebhookstatus" in show):
		try:
			value = str(sys.argv[2])
			say = setwebhookstatus(value)
		except IndexError:
			say = "Error: You must specify \"On\" or \"Off\" to use this command."
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
		queue = queue[0].lower()
		if item == "None":
			say = upnext()
			queueremove('None')
			say = say + " has been removed from the queue."
		else:
			if item.lower() in queue:
				item = item.lower()
				queueremove(item)
				say = item + " has been removed from the queue."
			else:
				say = item + " not found in queue to remove."
	elif ("whatupnext" in show):
		say = whatupnext()
		say = say.replace("movie.","The Movie ")
		if (("The commercial" in say) or ("The preroll" in say)):
			say2 = aftercommpreroll()
			say2 = say2.replace("movie.","The movie ")
			say = say + "\nFollowed by " + say2
		say = say.replace("playcommercial.","The commercial ")
		say = say.replace("preroll.","The preroll ")
		say = say.replace("''","'")
		#say = "Upnext we have " + say
	elif ("aftercommpreroll" in show):
		say = aftercommpreroll()
	elif ("whatsafterthat" in show):
		say = whatsafterthat()
	elif ("startnextprogram" in show):
		try:
			startnextprogram()
		except Exception:
			print ("Failed to start last program. Trying again next pass.")
		say = "done."
	elif ("skipthat" in show):
		say = skipthat()
		say = say.replace("movie.","The Movie ")
		try:
			if "No queue to skip." in say:
				say = queuefill()
		except TypeError:
			say = skipthat()
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
	elif ("suggestcustom" in show):
                try:
                        genre = str(sys.argv[2])
			say = suggestcustom(genre)
                except IndexError:
			say = "Error: You must enter a custom table name to use this command."
	elif ("suggesttv" in show):
		try:
			genre = str(sys.argv[2])
		except IndexError:
			genre = "none"
		say = suggesttv(genre)
		#saythat(say)
	elif ("suggestsomething" in show):
		say = suggestsomething()
	elif ("suggestblock" in show):
		try:
			say = getrandomblock()
			say1 = explainblock(say)
			say = "How does the " + say + " block sound, sir?"
			print (say1)
		except Exception:
			say = "Error: Block get failed."
	elif (("findinblock" in show) or ("searchblock" in show)):
		try:
			findme = str(sys.argv[2])
			say = findinblock(findme)
		except IndexError:
			say = "Error: You must specify an item to use this command."
	elif ("listshows" in show):
		try:
			genre = str(sys.argv[2])
			say = listshows(genre)
			if ((len(say)<30) or ("-l" in sys.argv)):
				worklist(say)
				say = "Done"
			else:
				say = wlistcolumns(say)
		except IndexError:
			show = availableshows()
			if ((len(show)<30) or ("-l" in sys.argv)):
				worklist(show)
				say = "Done"
			else:
				say = wlistcolumns(show)
	elif ("listepisodes" in show):
		try:
			show = str(sys.argv[2])
			say = listepisodes(show)
		except IndexError:
			say = "Specificy a show to use this command."
	elif ("listmovies" in show):
		try:
			genre = str(sys.argv[2])
			if genre == "-l":
				genre = "none"
		except IndexError:
			genre = "none"
			
		say = listmovies(genre)
		if ((len(say)<30) or ("-l" in str(sys.argv))):
			worklist(say)
			say = "Done"
		else:
			say = wlistcolumns(say)

	elif ("addsuggestion" in show):
		say = addsuggestion()
		#saythat(say)
	elif ("whatispending" in show):
		say = whatispending()
		#saythat(say)
	elif ("availableblocks" in show):
		try:
			say = availableblocks()
			say = say.split("\n")
			if ("-l" not in sys.argv):
				say = wlistcolumns(say)
			else:
				say = worklist(say)
		except NameError:
			say = "You must first create a block to use this command. Use 'addblock' for more information."

	elif ("restartblock" in show):
		try:
			block = str(sys.argv[2])
		except Exception:
			block = "none"
		say = restartblock(block)
	elif ("explainblock" in show):
		try:
			block = str(sys.argv[2])
			say = explainblock(block)
		except Exception:
			block = playmode()
			if ("block." in block):
				block = block.replace("block.","")
				#wmark
				command = "SELECT Items, Count FROM Blocks WHERE Name LIKE \"" + block + "\""
                                cur.execute(command)
                                found = cur.fetchone()
                                items = found[0]
                                count = found[1]
                                items = items.split(';')
                                item = items[int(count)]
				say = explainblock(block)
				try:
					mve = idtonightsmovie()
					mve = mve.replace("movie.","The movie ")
					mve = "The next random movie is: " + mve + "\n"
				except Exception:
					mve = ""
				try:
					tve = idtonightsshow()
					tve = "The next random show is: " + tve + "\n"
				except Exception:
					tve = ""
				wve = whatupnext()
				wve = wve.replace("movie.","")
				wve = wve.replace("''","'")
				item = item.lower()
				item = item.replace("''","'")
				item = item.replace("movie.","the movie ")
				if ("random_tv." in item):
					item = item.replace("random_tv.", "A random ")
					item = item + " show"
				elif ("random_movie." in item):
					item = item.replace("random_movie.", "A random ") 
					item = item + " movie"
				if "The movie" not in wve:
					wve = "Item " + str(count+1) + ", " + item + " is next.\n"
				# + wve
				say = say + mve + tve + "\n" + wve
			else:
				say = "Error: No block specified."
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
	elif ("generateblock" in show):
		try:
			bname = str(sys.argv[2])
		except IndexError:
			bname = "none"
		say = generateblock(bname)
	elif ("removeblock" in show):
		try:
			block = str(sys.argv[2])
		except Exception:
			block = "none"
		say = removeblock(block)
		
	elif ("addtoblock" in show):
		try:
			block = str(sys.argv[2])
		except Exception:
			block = "none"
		try:
			item = str(sys.argv[3])
		except Exception:
			item = "none"
		say = addtoblock(block, item)
	elif ("replaceinblock" in show):
		try:
			block = str(sys.argv[2])
			nitem = str(sys.argv[3])
			oitem = str(sys.argv[4])
			say = replaceinblock(block, nitem, oitem)
		except IndexError:
			say = "Error. You must supply a block, new item, and old item to use this command."
	elif ("reorderblock" in show):
		try:
			block = str(sys.argv[2])
			say = reorderblock(block)
		except Exception:
			say = "Error. You must supply a block to use this command."

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
		CALLMETHIS = gethonorific()
		say = CALLMETHIS + ", the last feature has ended, starting " + say
		
	elif ("blockplay" in show):
		plexlogin()
		play = str(sys.argv[2])
		say = playblockpackage(play)
	elif ("nextep" in show)and ("setnextep" not in show):
		show = str(sys.argv[2])
		show = titlecheck(show)
		if ("ERROR:" in show):
			say = show
		else:
			say = nextep(show)

	elif ("getplaymode" in show):
		say = playmode()
		if ("block." in say):
			say = say.replace("block.","")
			say = "We are in block package mode. The active block is: " + say + "."
		elif ("marathon." in say):
			say = say.replace("marathon.","")
			say = "We are in marathon mode watching " + say + "."
		elif ("binge." in say):
			say = say.replace("binge.","")
			say = "We are in binge playmode watching " + say + "."
		elif ("minithon." in say):
			say = say.replace("minithon.","")
			say = "We are in Mini-Marathon mode watching " + say + "."
		else:
			say = "We are in " + say + " playmode."
	elif ("setplaymode" in show):
		try:
			mode = str(sys.argv[2])
		except Exception:
			mode = show.split("setplaymode ")
			mode = mode[1]
		try:
			say = setplaymode(mode)
			say = say.replace("minithon.","Mini-Marathon: ")
			say = say.replace("block.", "Block Package Mode: ")
			say = say.replace("binge.", "Binge Mode: ")
			say = say.replace("marathon.", "Marathon Mode: ")
		except Exception:
			setplaymode(mode)
			say = whatupnext()
			say = say.replace("is active.", "is now active.")
	elif ("availplaymodes" in show):
		cls()
		say = availplaymodes()
	elif ("setminithonmax" in show):
		try:
			number = str(sys.argv[2])
			say = setminithonmax(number)
		except Exception:
			say = "Error: You must supply a number to use this command."
	elif ("showminithonmax" in show):
		say = showminithonmax()

	elif ("epdetails" in show):
		plexlogin()
		shows = plex.library.section('TV Shows')
		try:
			show = str(sys.argv[2])
			the_show = shows.get(show).episodes()
			try:
				season = str(sys.argv[3])
				episode = str(sys.argv[4])
				say = epdetails(show, season, episode)
			except IndexError:
				command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + show + "\""
				cur.execute(command)
				if not cur.fetchone():
					say = epdetails(show, 1, 1)
				else:
					cur.execute(command)
					Tnum = cur.fetchone()[0]
					Tnum = int(Tnum)
					plexlogin()
					summary = the_show[Tnum-1].summary
					presay = nextep(show)
					say = presay + "\n" + summary
				if len(say) > 350:
					say = say[:350] + " ..."
		except IndexError:
			say2 = "Assuming you ment the next up show or movie.\n"
			unext = upnext()
			try:
				del command
			except NameError:
				pass
			if ("block." in unext):
				block = unext.split('block.')[1].strip()
				command = "SELECT Items, Count FROM Blocks WHERE Name LIKE \"" + block + "\""
				cur.execute(command)
				found = cur.fetchone()
				items = found[0]
				count = found[1]
				items = items.split(';')
				item = items[int(count)]
				if ("random_movie" in item):
					command = "SELECT State FROM States WHERE Option LIKE \"TONIGHTSMOVIE\""
					cur.execute(command)
					mve = cur.fetchone()[0]
					mve = mve.replace("movie.","")
					command = "SELECT Summary FROM Movies WHERE Movie LIKE \"" + mve.strip() + "\""
				elif ("random_tv" in item):
					command = "SELECT State FROM States WHERE Option LIKE \"TONIGHTSSHOW\"" 
				elif ("movie." in item):
					item = item.replace("movie.","")
					command = "SELECT Summary FROM Movies WHERE Movie LIKE \"" + item.strip() + "\""
				else:
					the_show = shows.get(item).episodes()
					command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + item + "\""
					cur.execute(command)
					if not cur.fetchone():
						summary = the_show[0].summary
					else:
						cur.execute(command)
						Tnum = cur.fetchone()[0]
						Tnum = int(Tnum)
						summary = the_show[Tnum-1].summary
			elif ("movie." in unext):
				command = "SELECT Summary FROM Movies WHERE Movie LIKE \"" + unext.split('movie.')[1].strip() + "\""
			else:
				the_show = shows.get(unext).episodes()
				command = "SELECT Number FROM TVCounts WHERE Show LIKE \"" + unext + "\""
				cur.execute(command)
				if not cur.fetchone():
					summary = the_show[0].summary
				else:
					cur.execute(command)
					Tnum = cur.fetchone()[0]
					Tnum = int(Tnum)
					summary = the_show[Tnum-1].summary
				del command
			try:
				cur.execute(command)
				say3 = cur.fetchone()[0] + " ..."
			except Exception:
				say3 = summary
			wsay = whatupnext()
			wsay = wsay.replace("movie.","The Movie ")
			if len(say3) > 350:
				say3 = say3[:350] + " ..."
			say = say2 + "\n" + wsay + "\n" + say3
	elif ("moviedetails" in show):
		movie = str(sys.argv[2])
		say = moviedetails(movie)
	elif ("showdetails" in show):
		show = str(sys.argv[2])
		say = showdetails(show)
	elif ("epsleft" in show):
		try:
			show = str(sys.argv[2])
			say = epsleft(show)
		except IndexError:
			say = "ERROR: You must specify a show to use this command."
	elif ("findmovie" in show):
		movie = str(sys.argv[2])
		findmovie(movie)
		say = "Done"
	elif ("findshow" in show):
		show = str(sys.argv[2])
		show = show.replace("'","''")
		say = findshow(show)
		say = "Done"
	elif ("setnextep" in show):
		show = str(sys.argv[2])
		season = str(sys.argv[3])
		episode = str(sys.argv[4])
		say = setnextep(show, season, episode)

	elif "nowplaying" in show:
		say = nowplaying()
	elif "nowpdb" in show:
		say = nowpdb()

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
		kcheck = checkmode("movie")
		if "Kids" not in kcheck:
			try:
				openme = homedir + 'playstatestatus.txt'
				with open(openme, "r") as file:
					checkme = file.read()
				file.close()
				if "On" in checkme:
					playcheckstop()
				item = str(sys.argv[2])
				say = playwhereleftoff(item,"none")
				time.sleep(SLEEPTIME)
				if "On" in checkme:
					playcheckstart()
			except IndexError:
				say = "Error. You must specify a movie or show to use this command."
		else:
			say = "Error: Unable to use resumeplay while in kids mode."

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
	elif (("mutemusic" in show) and ("unmute" not in show)):
                mutemusic()
                say = "Audio has been muted."
        elif "unmutemusic" in show:
                unmutemusic()
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
	elif ("versioncheck" in show):
		say = versioncheck()
	else:
		#def playme
		SLEEPTIME = 5
		pcmd = "playme"
		plexlogin()
		show = checkcustomtables(show)
		#if ("CUSTOM." in show):
		if type(show) is tuple:
			table = show[1].strip()
			show = show[0]
			show = show.replace("CUSTOM.","")
			say = playcustom(show, table)
		else:
			if show == "playspshow":
				pass
			else:
				oshow = show
				show = show.replace("''","'")
				show = titlecheck(show)
				if "Error:" in show:
					show = oshow
			pstatus = checkpstatus()
			try:
				title = str(sys.argv[2])
				season = str(sys.argv[3])
				episode = str(sys.argv[4])
				say = playspshow(title, season, episode)
			
			except IndexError:
				rcheck = resumestatus()
				if "on" in rcheck.lower():
					say = playwhereleftoff(show,"none")
				else:
					
					say = playshow(show)
			if "On" in pstatus:
				time.sleep(SLEEPTIME)
				playcheckstart()
	try:
		say = str(say)
		say = say.replace("''","'")
	except AttributeError:
		say = "Done"
	print (say)
except IndexError:
	show = "We're Sorry, but either that command wasn't recognized, or no input was received. Please try again."  
