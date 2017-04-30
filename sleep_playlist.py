homedir = '/home/pi/hasystem/'

from random import randint
import sys

def plexlogin():
	global plex
	from plexapi.myplex import MyPlexAccount
	from plexapi.server import PlexServer
	
	PLEXSERVERIP = "SERVERIPGOESHERE" #plex server ip goes here. 
	PLEXSERVERPORT = "32400"   #usually 32400, but if yours is different replace.
	baseurl = 'http://' + PLEXSERVERIP + ':' + PLEXSERVERPORT
	#note: May need to add your local network as an network authorized without access to use the local access method.
	try:
		LOGGEDIN
	except Exception:
		try:
			
			plex = PlexServer(baseurl)
		except Exception:
			print ("Local Fail. Trying cloud access.")
			#You will need to add your username, password, servername below if your local access fails.
			PLEXUN = "MYPLEXUN"
			PLEXPW = "MYPLEXPW"
			PLEXSVR = "PLEXSERVERNAME"
			
			user = MyPlexAccount.signin(PLEXUN,PLEXPW)

			plex = user.resource(PLEXSVR).connect()
		
		LOGGEDIN = "YES"


def geteps(cshow, num):
	global plex
	plexlogin()
	ccheck = ""
	TITLE = "TBN_PLEX: SLEEPER"
	for video in plex.search(cshow):
		if video.type == "show":
			xshow = video.episodes()
			xnum = int(len(xshow))-1
			ccheck = "found"
	if "found" not in ccheck:
		return ("Error: " + cshow + " not found in library.")
	try:
		title = plex.playlist(TITLE)
		title.delete()
	except Exception:
		pass
	min = 0
	eps = []
	while (min <= (num-1)):
		epn = randint(0,xnum)
		addme = xshow[epn]
		if ("unwatched" not in sys.argv):
			if addme not in eps:
				eps.append(addme)
				min = min + 1
		else:
			if addme.viewCount >0:
				pass
			else:
				if addme not in eps:
					eps.append(addme)
					min = min + 1
	ccnt = 0
	plex.createPlaylist(TITLE,eps)
	return ("Sleep Playlist: \"TBN_PLEX: SLEEPER\" has been successfully created.")
			
	
try:
	show = str(sys.argv[1])
	num = int(sys.argv[2])
	say = geteps(show,num)
except IndexError:
	say = "Error: You must provide both a show name and a number of episodes to use this command."
print (say)
