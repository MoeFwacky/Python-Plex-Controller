import time
import os
import sqlite3
import getpass

user = getpass.getuser()

DEFAULTDIR = "/home/" + user + "/hasystem/"

MYDB = DEFAULTDIR + "myplex.db"

def sessionstatus():
	sql = sqlite3.connect(MYDB)
        cur = sql.cursor()
        cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXUN\'')
        PLEXUN = cur.fetchone()
        PLEXUN = str(PLEXUN[0]).strip()

        cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXPW\'')
        PLEXPW = cur.fetchone()
        PLEXPW = str(PLEXPW[0]).strip()

        cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSVR\'')
        PLEXSVR = cur.fetchone()
        PLEXSVR = PLEXSVR[0]

        cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXCLIENT\'')
        PLEXCLIENT = cur.fetchone()
        PLEXCLIENT = PLEXCLIENT[0]

	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERIP\'')
	PLEXSERVERIP = cur.fetchone()
	PLEXSERVERIP = PLEXSERVERIP[0]

	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERPORT\'')
	PLEXSERVERPORT = cur.fetchone()
	PLEXSERVERPORT = PLEXSERVERPORT[0]

	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERTOKEN\'')
	PLEXSERVERTOKEN = cur.fetchone()
	PLEXSERVERTOKEN = PLEXSERVERTOKEN[0]


        from plexapi.myplex import MyPlexAccount
	try:
		from plexapi.server import PlexServer
		baseurl = 'http://' + PLEXSERVERIP + ':' + PLEXSERVERPORT
		token = PLEXSERVERTOKEN
		plex = PlexServer(baseurl, token)
		#print ("using local access.")
	except Exception:
		print ("Local Fail. Trying cloud access.")
		user = MyPlexAccount.signin(PLEXUN, PLEXPW)
		plex = user.resource(PLEXSVR).connect()
        client = plex.client(PLEXCLIENT)	
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
			
			if nowp in sess:
				#print ("Go")
				return ("Playing")
		print ("Fail")
		return ("Unknown")

def playstatus():
	
	sql = sqlite3.connect(MYDB)
	cur = sql.cursor()
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

	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERIP\'')
        PLEXSERVERIP = cur.fetchone()
        PLEXSERVERIP = PLEXSERVERIP[0]

        cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERPORT\'')
        PLEXSERVERPORT = cur.fetchone()
        PLEXSERVERPORT = PLEXSERVERPORT[0]

        cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERTOKEN\'')
        PLEXSERVERTOKEN = cur.fetchone()
        PLEXSERVERTOKEN = PLEXSERVERTOKEN[0]

        from plexapi.myplex import MyPlexAccount
        try:
                from plexapi.server import PlexServer
                baseurl = 'http://' + PLEXSERVERIP + ':' + PLEXSERVERPORT
                token = PLEXSERVERTOKEN
	
                plex = PlexServer(baseurl, token)
        except Exception:
		user = MyPlexAccount.signin(PLEXUN, PLEXPW)
                print ("Local Fail. Trying cloud access.")

		plex = user.resource(PLEXSVR).connect()
	client = plex.client(PLEXCLIENT)

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
	with open('/home/pi/hasystem/playstatestatus.txt','r') as file:
		stuff = file.read()
	file.close()
	try:
		if ("Off" not in stuff):
			try:
				print ("Doing a session check.")
				state = sessionstatus()
				if "Unknown" in state:
					print ("Unknown presented. Using playstate method.")
					state = playstatus()
			except Exception:
				print ("Session check failed. Checking Playstate method.")
				state = playstatus()
			if ("Playing" in state):
			
				sql = sqlite3.connect(MYDB)
				cur = sql.cursor()
				cur.execute("DELETE FROM States WHERE Option LIKE \'Playstate\'")
				sql.commit
				cur.execute("INSERT INTO States VALUES(?,?)",('Playstate','Playing'))
				sql.commit
				sql.close()
			elif ("Sleep" in stuff):
				sql = sqlite3.connect(MYDB)
				cur = sql.cursor()
				cur.execute("DELETE FROM States WHERE Option LIKE \'Playstate\'")
				sql.commit
				cur.execute("INSERT INTO States VALUES(?,?)",('Playstate','Stopped'))
				sql.commit
				sql.close()
				command = "python /home/pi/huec.py alllights off"
				os.system(command)
				command = "python /home/pi/hasystem/system.py playcheckstop"
				os.system(command)
				time.sleep(20)
			else:
				sql = sqlite3.connect(MYDB)
				cur = sql.cursor()
				print ("Stopped")
				cur.execute("DELETE FROM States WHERE Option LIKE \'Playstate\'")
				sql.commit
				cur.execute("INSERT INTO States VALUES(?,?)",('Playstate','Stopped'))
				sql.commit
				sql.close()
				command = "python " + DEFAULTDIR + "/system.py startnextprogram"
				os.system(command)
				time.sleep(20)
	except Exception:
		print ("Timeout Error. Checking again next pass.")
	time.sleep(10)



