import os
import sys
import getpass
import subprocess
import sqlite3
import urllib3
import platform


http = urllib3.PoolManager()

try:
	input = raw_input
except NameError:
	pass


def cls():
   os.system('cls' if os.name=='nt' else 'clear')

ostype = platform.system()

try:
	extraopt = str(sys.argv[1])
except Exception:
	extraopt = "none"

if "Linux" in ostype:

	user = getpass.getuser()

	if ("root" in user):
		print ("Run this command as your non-root user, without sudo. You will be prompted for sudo access where it is necessary in this setup.")
	else:

		addme = """

		#Plex system.py aliases

		alias whatupnext='python /home/pi/hasystem/system.py whatupnext'
		alias whatsafterthat='python /home/pi/hasystem/system.py whatsafterthat'
		alias startnextprogram='python /home/pi/hasystem/system.py startnextprogram'
		alias queueshow='python /home/pi/hasystem/system.py queueshow'
		alias suggestmovie='python /home/pi/hasystem/system.py suggestmovie'
		alias moviedetails='python /home/pi/hasystem/system.py moviedetails'
		alias idtonightsmovie='python /home/pi/hasystem/system.py idtonightsmovie'
		alias findmovie='python /home/pi/hasystem/system.py findmovie'
		alias findshow='python /home/pi/hasystem/system.py findshow'
		alias suggesttv='python /home/pi/hasystem/system.py suggesttv'
		alias addsuggestion='python /home/pi/hasystem/system.py addsuggestion'
		alias skipthat='python /home/pi/hasystem/system.py skipthat'
		alias skipahead='python /home/pi/hasystem/system.py skipahead'
		alias skipback='python /home/pi/hasystem/system.py skipback'
		alias whatispending='python /home/pi/hasystem/system.py whatispending'
		alias playme='python /home/pi/hasystem/system.py'
		alias nowplaying='python /home/pi/hasystem/system.py nowplaying'
		alias nextep='python /home/pi/hasystem/system.py nextep'
		alias queueadd='python /home/pi/hasystem/system.py queueadd'
		alias idplaymode='python /home/pi/hasystem/system.py getplaymode'
		alias getplaymode='python /home/pi/hasystem/system.py getplaymode'
		alias setplaymode='python /home/pi/hasystem/system.py setplaymode'
		alias availableblocks='python /home/pi/hasystem/system.py availableblocks'
		alias explainblock='python /home/pi/hasystem/system.py explainblock'
		alias epdetails='python /home/pi/hasystem/system.py epdetails'
		alias setnextep='python /home/pi/hasystem/system.py setnextep'
		alias stopplayback='python /home/pi/hasystem/system.py stopplayback'
		alias pauseplayback='python /home/pi/hasystem/system.py pauseplayback'
		alias addblock='python /home/pi/hasystem/system.py addblock'
		alias addtoblock='python /home/pi/hasystem/system.py addtoblock'
		alias removefromblock='python /home/pi/hasystem/system.py removefromblock'
		alias removeblock='python /home/pi/hasystem/system.py removeblock'
		alias setupnext='python /home/pi/hasystem/system.py setupnext'
		alias playcheckstatus='python /home/pi/hasystem/playstatus.py'
		alias playcheckstart='python /home/pi/hasystem/system.py playcheckstart'
		alias playcheckstop='python /home/pi/hasystem/system.py playcheckstop'
		alias playchecksleep='python /home/pi/hasystem/system.py playchecksleep'
		alias whereat='python /home/pi/hasystem/system.py whereat'
		alias findsomethingelse='python /home/pi/hasystem/system.py findsomethingelse'
		alias findnewmovie='python /home/pi/hasystem/system.py findnewmovie'
		alias addfavoritemovie='python /home/pi/hasystem/system.py addfavoritemovie'
		alias listclients='python /home/pi/hasystem/system.py listclients'
		alias changeclient='python /home/pi/hasystem/system.py changeclient'
		"""


		newdir = "/home/" + user + "/"
		addme = addme.replace("/home/pi/", newdir)

		homedir = "/home/" + user + "/hasystem/"
		print (homedir)

		print ("Hello " + user + ". I am now adding the alias add script now. You will be prompted for sudo for this.\n")

		if not os.path.exists(homedir):
			os.makedirs(homedir)
			sayme = "The necessary directory has been created."
		else:
			sayme = ""

		print (homedir)
		
		try:
			file0 = homedir + "add_to_bash.py"
			with open (file0, "r") as file:
				readme = file.read()
			file.close()
			print ("check pass.  add_to_bash.py exists.")
		except IOError:
			try:
				url = "https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/add_to_bash.py"
				newfile = http.request('GET', url, preload_content=False)
				print ("...")
				print (newfile)
				print ("go")
				with open(file0, 'wb') as file:
					file.write(newfile)
				file.close()
				print ("on")
				print ("File successfully moved to the necessary directory.")
			except IOError:
				print ("warning add_to_bash.py does not exist. The TBN controller will not work.")
		try:
			print ("test1")
			command = "sudo python " + file0 + " " + user.strip()
			print (command)
			os.system(command)
		except Exception:
			print ("Failed to add aliases to Bash. see add_to_bash.py for list of alias it is recommended you add.\n")
			updatecheck = "fail"


		print ("Done. " + user + " " + sayme + " I am now trying to add a cron entry for the play checking script.")

		try:
			file00 = homedir + "add_to_cron.py"
			with open (file00, "r") as file:
				readme = file.read()
			file.close()
			print ("check pass.  add_to_cron.py exists.")
		except IOError:
			try:
				url = "https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/add_to_cron.py"
				newfile = http.request('GET', url, preload_content=False)
				with open(file00, 'wb') as file:
					file.write(newfile)
				file.close()
				print ("File successfully moved to the necessary directory.")
			except IOError:
				print ("warning add_to_cron.py does not exist. Cron add will fail.")
		try:
			command = "sudo python " + file00 + " " + user.strip()
			os.system(command)
		except Exception:
			print ("Failed to add cronjob. see add_to_cron.py for recommended job.\n")
			updatecheck = "fail"

		

else:
	print (ostype)
	print ("Unable to add cron or bash entries on a Windows system. I am skipping those steps.")
	hcheck = "negative"
	while ("goon" not in hcheck):
		
		print ("In what directory would you like to place the /hasystem folder and associated files?\nFor Example: 'C:\\home\\user\\documents\\' Note: This location needs to currently exist.")
		homedir = input('Path ')
		homedir = homedir.replace("\\", "\\\\")
		print (homedir)
		if not os.path.exists(homedir):
			cls()
			print ("\nError. That directory does not exist. Please try again.\n")
		else:
			hcheck = "goon"
			
	print ("Pass")
	homedir = homedir + "hasystem\\"
	
writeme = "homedir = \'" + homedir + "\\'\n"
	
if not os.path.exists(homedir):
	os.makedirs(homedir)
	print (homedir + " has been successfully created.\n")
else:
	print (homedir + " already exists. Moving on.")
studio = homedir +"Studio\\"
if not os.path.exists(studio):
	os.makedirs(studio)

genre = homedir + "Genre\\"
if not os.path.exists(genre):
	os.makedirs(genre)

genre = genre + "TV\\"
if not os.path.exists(genre):
	os.makedirs(genre)
	
file1 = homedir + "playstate.txt"
try:
	with open (file1, "r") as file:
		readme = file.read()
	file.close()
	print ("playstate text file already exists. Checking pstate file now.")

except IOError:
	with open (file1, "w") as file:
		file.write("")
	file.close()
	print ("playstate text file successfully added.")
file2 = homedir + "pstate.txt"
try:
	with open (file2, "r") as file:
		readme = file.read()
	file.close()
	print ("pstate text file already exists. Checking perror file now.")
except IOError:
	with open (file2, "w") as file:
		file.write("")
	file.close()
	print ("pstate text file successfully added.")
file3 = homedir + "perror.txt"
try:
	with open (file3, "r") as file:
		readme = file.read()
	file.close()
	print ("perror text file already exists. Checking playstatestatus file now.")
except IOError:
	with open (file3, "w") as file:
		file.write("")
	file.close()
	print ("playstate text file successfully added.")
file4 = homedir + "playstatestatus.txt"
try:
	with open (file4, "r") as file:
		readme = file.read()
	file.close()
	print ("playstatestatus text file already exists. Checking script file now.")
except IOError:
	file4 = homedir + "playstatestatus.txt"
	with open (file4, "w") as file:
		file.write("Off")
	file.close()
	print ("playstatestatus text file successfully added.")
file5 = homedir + "system.py"
try:
	with open (file5, "r") as file:
		readme = file.read()
	file.close()
	print ("check pass. system.py exists.")
except IOError:
	try:
		url = "https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/system.py"
		newfile = http.request('GET', url, preload_content=False)
		newfile = newfile.data
		#print (newfile)
		with open(file5, 'wb') as file:
			file.write(newfile)
		file.close()
		with open (file5, 'r') as file:
			rewrite = file.read()
		file.close()
		rewrite = writeme + rewrite
		with open(file5, "w") as file:
			file.write(rewrite)
		file.close()
		print ("File successfully moved to the necessary directory.")
	except FileNotFoundError:
		print ("warning system.py does not exist. The TBN controller will not work.")
file6 = homedir + "piplaystate.py"
try:
	with open (file6, "r") as file:
		readme = file.read()
	file.close()
	print ("check pass. piplaystate.py exists.")
except IOError:
	try:
		url = "https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/piplaystate.py"
		newfile = http.request('GET', url, preload_content=False)
		newfile = newfile.data
		with open(file6, 'wb') as file:
			file.write(newfile)
		file.close()
		with open (file6, 'r') as file:
			rewrite = file.read()
		file.close()
		rewrite = writeme + rewrite
		with open(file6, "w") as file:
			file.write(rewrite)
		file.close()
		print ("File successfully moved to the necessary directory.")
	except Exception:
		print ("warning piplaystate.py does not exist. The play check status script will not work.")
file7 = homedir + "playstatus.py"
try:
	with open (file7, "r") as file:
		readme = file.read()
	file.close()
	print ("check pass. playstatus.py exists.")
except IOError:
	try:
		url = "https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/playstatus.py"
		newfile = http.request('GET', url, preload_content=False)
		newfile = newfile.data
		with open(file7, 'wb') as file:
			file.write(newfile)
		file.close()
		with open (file7, 'r') as file:
			rewrite = file.read()
		file.close()
		rewrite = writeme + rewrite
		with open(file7, "w") as file:
			file.write(rewrite)
		file.close()
		print ("File successfully moved to the necessary directory.")
	except Exception:
		print ("warning playstatus.py does not exist. The play check status script will not work.")
file8 = homedir + "upddatedb_pi.py"
try:
	with open (file8, "r") as file:
		readme = file.read()
	file.close()
	print ("check pass. upddatedb_pi.py exists.")
	updatecheck = "pass"
except IOError:
	try:
		url = "https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/upddatedb_pi.py"
		newfile = http.request('GET', url, preload_content=False)
		newfile = newfile.data
		#print (newfile)
		
		#print (writeme)
		with open(file8, "wb") as file:
			file.write(newfile)
		file.close()
		with open (file8, 'r') as file:
			rewrite = file.read()
		file.close()
		rewrite = writeme + rewrite
		with open(file8, "w") as file:
			file.write(rewrite)
		file.close()
		
		print ("File successfully moved to the necessary directory.")
		updatecheck = "pass"
	except FileNotFoundError:
		print ("warning updateddb_pi.py does not exist. The system will be unable to build the shows and movie tables in your database.")
		updatecheck = "fail"

print ("Checking Database now.\n")

MYDB = homedir + "myplex.db"
sql = sqlite3.connect(MYDB)
cur = sql.cursor()

#generating settings table if it does not already exist.
cur.execute('CREATE TABLE IF NOT EXISTS settings(item TEXT, setting TEXT)')
sql.commit()

#deletes existing settings if the reset flag is present
if "reset" in extraopt:
	cur.execute('DELETE FROM settings')
	sql.commit()
'''
#check to see if client IP is present. Used for play check script.
cur.execute('SELECT setting FROM settings WHERE item LIKE \'ClientIP\'')
if not cur.fetchone():
	clientip = str(input('Input Client IP: '))
	cur.execute('INSERT INTO settings VALUES(?,?)', ('ClientIP', clientip.strip()))
	sql.commit()
'''

#checks for plex user name and PW. Used for Plex API.
print ("You Will need to use Either LOCAL or CLOUD access to have the TBN Controller control your client. It is recommended you use both for fail back purposes, however, if you do not want to or know the information for one, you can use garbage data. Remember, you need to use either LOCAL or CLOUD access for this to work properly. \n\n")
print ("Setting up local access now.\n")

cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXTOKEN\'')
if not cur.fetchone():
	PLEXTOKEN = str(input('Plex Token: '))
	writeme = str("PLEXTOKEN")
	cur.execute('INSERT INTO settings VALUES(?,?)', (writeme,PLEXTOKEN))
	sql.commit()
	
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERIP\'')
if not cur.fetchone():
	PLEXSERVERIP = str(input('Plex Server IP: '))
	writeme = str("PLEXSERVERIP")
	cur.execute('INSERT INTO settings VALUES(?,?)', (writeme,PLEXSERVERIP))
	sql.commit()

cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERPORT\'')
if not cur.fetchone():
	PLEXSERVERPORT = str(input('Plex Server Port: '))
	writeme = str("PLEXSERVERPORT")
	cur.execute('INSERT INTO settings VALUES(?,?)', (writeme,PLEXSERVERPORT))
	sql.commit()
	
print ("\nFinished getting necessary local access information. Getting Plex Cloud information now.\n")
	
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXUN\'')
if not cur.fetchone():
	PLEXUN = str(input('Plex Username: '))
	writeme = str("PLEXUN")
	cur.execute('INSERT INTO settings VALUES(?,?)', (writeme,PLEXUN))
	sql.commit()

cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXPW\'')
if not cur.fetchone():
	PLEXPW = str(input('Plex Password: '))
	cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXPW',PLEXPW))
	sql.commit()

print ("\nFinished getting necessary cloud information. Getting necessary general information now.\n")
#checks for client name and server name. used by Plex API.
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSVR\'')
if not cur.fetchone():
	PLEXSVR = str(input('Plex Server Name: '))
	cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXSVR',PLEXSVR))
	sql.commit()

	
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXCLIENT\'')
if not cur.fetchone():
	print ("Enter Plex Client Name. Note: If you do not know this name, enter garbage data and run 'changeclient' once you have finished running the system_setup script.\n")
	PLEXCLIENT = str(input('Plex Client Name: '))
	cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXCLIENT',PLEXCLIENT))
	sql.commit()

#get wildcard show name. Used as part of random media picking mechanism.
cur.execute('SELECT setting FROM settings WHERE item LIKE \'WILDCARD\'')
if not cur.fetchone():
	print ("Enter your Wild Card Show. This is the show you are working your way through that will play more often than some other ransom TV show or random movie when automated selection is in play.\n")
	WILDCARD = str(input('Wild Card Show: '))
	cur.execute('INSERT INTO settings VALUES(?,?)', ('WILDCARD',WILDCARD))
	sql.commit()
	

cur.execute('CREATE TABLE IF NOT EXISTS States(Option TEXT, State TEXT)')
sql.commit()

cur.execute('DELETE FROM States')
sql.commit()

cur.execute('INSERT INTO States VALUES(?,?)', ('Playmode','normal'))
sql.commit()

cur.execute('INSERT INTO States VALUES(?,?)', ('queue',' '))
sql.commit()

cur.execute('INSERT INTO States VALUES(?,?)', ('Pending', ''))
sql.commit()

cur.execute('INSERT INTO States VALUES(?,?)', ('Nowplaying','Stopped'))
sql.commit()

cur.execute('CREATE TABLE IF NOT EXISTS shows(TShow TEXT, Episode TEXT, Season INT, Enum INT, Tnum INT, Summary TEXT, Link TEXT)')
sql.commit()

cur.execute('CREATE TABLE IF NOT EXISTS Movies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
sql.commit()

cur.execute('CREATE TABLE IF NOT EXISTS TVCounts(Show TEXT, Number INT)')
sql.commit()

cur.execute('CREATE TABLE IF NOT EXISTS Blocks(Name TEXT, items TEXT, Count INT)')
sql.commit()

print ("Necessary File check complete.")

if ("pass" in updatecheck):
	print ("Would you like to update your system database now to add the available shows and movies in your library? This is highly recommended and may take some time depending on the size of your library. If you do not update your library some actions will error.\n")
	choice = str(input('Yes or No? '))
	if "y" in choice.lower():
		if "Windows" not in ostype:
			command = "python " + homedir + "upddatedb_pi.py all"
		else:
			command = homedir + "upddatedb_pi.py all"
		os.system(command)
	print ("If you needed that entry for cron it was: @reboot python /home/pi/hasystem/piplaystate.py &")
else:
	print ("The files system_setup.py can add have been added.\n Done!")            