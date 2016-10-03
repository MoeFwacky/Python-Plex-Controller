homedir = 'c:\\users\\rob\\documents\\hasystem\\'
import time
import os
import sqlite3
import getpass
import platform

ostype = platform.system()
global cur
global sql
global plex

MYDB = homedir + "myplex.db"

def dblogin():
	global cur
	global sql
	

	sql = sqlite3.connect(MYDB)
	cur = sql.cursor()

def plexlogin():
	global plex
	global cur
	global sql
	global client
	from plexapi.myplex import MyPlexAccount
	
	dblogin()
	
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
	
	user = MyPlexAccount.signin(PLEXUN, PLEXPW)
	try:
		from plexapi.server import PlexServer
		baseurl = 'http://192.168.1.134:32400'
		token = 'WJBTq6E9WeYAss6wUtNk'
		plex = PlexServer(baseurl, token)
		#print ("using local access.")
	except Exception:
		print ("Local Fail. Trying cloud access.")
		plex = user.resource(PLEXSVR).connect()
	client = plex.client(PLEXCLIENT)
	

def sessionstatus():
	global plex
	global cur
	global sql
	dblogin()
	plexlogin()
	psess = plex.sessions()
	if not psess:
		return ("Stopped")
	else:
		cur.execute('SELECT State FROM States WHERE Option LIKE \'Nowplaying\'')
		nowp = cur.fetchone()
		nowp = nowp[0]
		if "TV Show:" in nowp:
			nowp = nowp.split("Episode: ")
			nowp = nowp[1]
		elif "Movie:" in nowp:
			nowp = nowp.split("Movie: ")
			nowp = nowp[1]
		for sess in psess:
			sess = sess.title
			#print (sess)
			
			if nowp in sess:
				#print ("Go")
				return ("Playing")
		#print ("Fail")
		return ("Unknown")

def playstatus():
	global cur
	global sql
	global client
	plexlogin()
	pstatus = client.isPlayingMedia()
	sql.close()
	#print (pstatus)

	if pstatus is True:
		return ("Playing")
	else:
		return ("Stopped")
#say = sessionstatus()
#print (say)
while True:
	checkdir = homedir + "playstatestatus.txt"
	with open(checkdir,'r') as file:
		stuff = file.read()
	file.close()
	#print (stuff)
	#try:
	if ("Off" not in stuff):
		print ("Doing a session check.")
		dblogin()
		state = sessionstatus()
		try:
			#print (state)
			if "Unknown" in state:
				print ("Unknown presented. Using playstate method.")
				state = playstatus()
		except Exception:
			print ("Session check failed. Checking Playstate method.")
			state = playstatus()
		if ("Playing" in state):
		
			sql = sqlite3.connect(MYDB)
			cur = sql.cursor()
			#print ("Playing")
			cur.execute("DELETE FROM States WHERE Option LIKE \'Playstate\'")
			sql.commit
			cur.execute("INSERT INTO States VALUES(?,?)",('Playstate','Playing'))
			sql.commit
			sql.close()
		elif ("Sleep" in state):
			sql = sqlite3.connect(MYDB)
			cur = sql.cursor()
			cur.execute("DELETE FROM States WHERE Option LIKE \'Playstate\'")
			sql.commit
			cur.execute("INSERT INTO States VALUES(?,?)",('Playstate','Stopped'))
			sql.commit
			sql.close()
			#command = "python /home/pi/huec.py alllights off"
			#os.system(command)
			command = "python " + homedir + " playcheckstop"
			os.system(command)
			time.sleep(30)
		else:
			sql = sqlite3.connect(MYDB)
			cur = sql.cursor()
			print ("Stopped")
			cur.execute("DELETE FROM States WHERE Option LIKE \'Playstate\'")
			sql.commit
			cur.execute("INSERT INTO States VALUES(?,?)",('Playstate','Stopped'))
			sql.commit
			sql.close()
			command = "python " + homedir + "/system.py startnextprogram"
			os.system(command)
			time.sleep(45)
	#except Exception:
		#print ("Timeout Error. Checking again next pass.")
	time.sleep(10)



