import os
import sys
import getpass
import subprocess
import sqlite3
import urllib3
import platform

#urllib3.disable_warning()

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
                else:
			try:
				return movies[int(getme)-1]
			except Exception:
				Error = "Invalid Selection. Please Try Again."
				mmin = mmin - 10



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

		newdir = "/home/" + user + "/"
		homedir = "/home/" + user + "/hasystem/"
		writeme = "homedir = \'" + homedir + "\'\n"
		writemehome = writeme

		print ("Hello " + user + ". I am now adding the alias add script now. You will be prompted for sudo for this.\n")

		if not os.path.exists(homedir):
			os.makedirs(homedir)
			sayme = "The necessary directory has been created."
		else:
			sayme = ""

		print (sayme)
				
		try:
			file0 = homedir + "add_to_bash.py"
			with open (file0, "r") as file:
				readme = file.read()
			file.close()
			print ("check pass.  add_to_bash.py exists.")
		except IOError:
			try:
				url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/add_to_bash.py"
				newfile = http.request('GET', url, preload_content=False)
				newfile = writemehome + str(newfile.data)
				print newfile
				with open(file0, 'wb') as file:
					file.write(newfile)
				file.close()
				print ("File successfully moved to the necessary directory.")
			except IOError:
				print ("warning add_to_bash.py does not exist. Alias commands will not work.")
		try:
			filex1 = homedir + "tbn_schedule.py"
			with open (filex1, "r") as file:
				readme = file.read()
			file.close()
			print ("check pass.  tbn_schedule.py exists.")
		except IOError:
			try:
				url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/tbn_schedule.py"
				newfile = http.request('GET', url, preload_content=False)
				newfile = writemehome + str(newfile.data)
				print newfile
				with open(filex1, 'wb') as file:
					file.write(newfile)
				file.close()
				print ("File successfully moved to the necessary directory.")
			except IOError:
				print ("warning tbn_schedule.py does not exist. Scheduling will not work.")
		try:
                        file10 = homedir + "aliases"
                        with open (file10, "r") as file:
                                readme = file.read()
                        file.close()
                        print ("check pass.  aliases exists.")
                except IOError:
                        try:
                                url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/aliases"
                                newfile = http.request('GET', url, preload_content=False)
                                #print (newfile)
                                with open(file10, 'wb') as file:
                                        file.write(newfile.data)
                                file.close()
                                print ("File successfully moved to the necessary directory.")
                        except IOError:
                                print ("warning aliases does not exist. Alias commands will not work.")
		try:
			command = "sudo python " + file0 + " " + user.strip()
			#print (command)
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
				url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/add_to_cron.py"
				newfile = http.request('GET', url, preload_content=False)
				newfile = writemehome + str(newfile.data)
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
	#/Users/username/Desktop/projects/TBN-Plex/
	if "darwin" in ostype:
		homedir = homedir + "hasystem/"
		writeme = homedir + "hassytem/"
	else:
		homedir = homedir + "hasystem\\"
		writeme = "homedir = \'" + homedir + "\\'\n"
	writemehome = writeme
	

	
if not os.path.exists(homedir):
	os.makedirs(homedir)
	print (homedir + " has been successfully created.\n")
else:
	print (homedir + " already exists. Moving on.")
	
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
		url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/system.py"
		newfile = http.request('GET', url, preload_content=False)
		newfile = newfile.data
		#print (newfile)
		with open(file5, 'wb') as file:
			file.write(newfile)
		file.close()
		with open (file5, 'r') as file:
			rewrite = file.read()
		file.close()
		rewrite = writemehome + "\n" + rewrite
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
		url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/piplaystate.py"
		newfile = http.request('GET', url, preload_content=False)
		newfile = newfile.data
		with open(file6, 'wb') as file:
			file.write(newfile)
		file.close()
		with open (file6, 'r') as file:
			rewrite = file.read()
		file.close()
		rewrite = writemehome + "\n" + rewrite
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
		url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/playstatus.py"
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
		url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/upddatedb_pi.py"
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
		
file8a = homedir + "getshow.py"
try:
	with open (file8a, "r") as file:
		readme = file.read()
	file.close()
	print ("check pass. getshow.py exists.")
	updatecheck = "pass"
except IOError:
	try:
		url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/getshow.py"
		newfile = http.request('GET', url, preload_content=False)
		newfile = newfile.data
		#print (newfile)
		
		#print (writeme)
		with open(file8a, "wb") as file:
			file.write(newfile)
		file.close()
		with open (file8a, 'r') as file:
			rewrite = file.read()
		file.close()
		rewrite = writeme + rewrite
		with open(file8a, "w") as file:
			file.write(rewrite)
		file.close()
		
		print ("File successfully moved to the necessary directory.")
		updatecheck = "pass"
	except FileNotFoundError:
		print ("warning getshow.py does not exist.")
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

#checks for plex user name and PW. Used for Plex API.
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXUN\'')
if not cur.fetchone():
	PLEXUN = str(input('Plex Username: '))
	writeme = str("PLEXUN")
	cur.execute('INSERT INTO settings VALUES(?,?)', (writeme,PLEXUN))
	sql.commit()
else:
	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXUN\'')
	PLEXUN = cur.fetchone()[0]

cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXPW\'')
if not cur.fetchone():
	pass
else:
	cur.execute('DELETE FROM settings WHERE item LIKE \'PLEXPW\'')
	sql.commit()
	print("Found Old stored password. Scrubbing from DB. You will be prompted for it, when needed, like now.\n")

print ("Your Plex Password is needed to proceed. Note: This password is not stored, and if needed in the future you will be prompted for it.")
PLEXPW = str(getpass.getpass('Plex Password: '))

from plexapi.myplex import MyPlexAccount
user = MyPlexAccount.signin(PLEXUN,PLEXPW)

print("\rSuccessfully Logged In.\n")

resces = user.resources()
servers = []
for item in resces:
	if "Plex Media Server" in item.product:
		servers.append(item.name)
server = worklist(servers)
for item in resces:
        if "Plex Media Server" in item.product:
                servers.append(item.name)
                if item.name == server:
			PLEXSVR = item.name
			PLEXSERVERIP = str(item.connections[0].address)
			PLEXSERVERPORT = str(item.connections[0].port)

baseurl = "http://" + PLEXSERVERIP + ":" + PLEXSERVERPORT
from plexapi.server import PlexServer
plex = PlexServer(baseurl)
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSVR\'')
if not cur.fetchone():
        cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXSVR',PLEXSVR))
        sql.commit()
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERIP\'')
if not cur.fetchone():
        cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXSERVERIP',PLEXSERVERIP))
        sql.commit()
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERPORT\'')
if not cur.fetchone():
        cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXSERVERPORT',PLEXSERVERPORT))
        sql.commit()
cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXCLIENT\'')
if not cur.fetchone():
	daclients = []
        for client in plex.clients():
                daclients.append(client.title)
        print ("Select a Client. The Following Clients are available:")
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
                print ("Client successfully set to: " + client.strip())
        except Exception:
                print ("Error. Unable to update client. Please try again.")

#get wildcard show name. Used as part of random media picking mechanism.
cur.execute('SELECT setting FROM settings WHERE item LIKE \'WILDCARD\'')
if not cur.fetchone():
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

cur.execute('CREATE TABLE IF NOT EXISTS Movies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
sql.commit()

cur.execute('CREATE TABLE IF NOT EXISTS backupmovies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
sql.commit()

cur.execute("CREATE TABLE IF NOT EXISTS TVshowlist(TShow TEXT, Summary TEXT, Genre TEXT, Rating TEXT, Duration INT, Totalnum INT)")
sql.commit()

cur.execute("CREATE TABLE IF NOT EXISTS backshowlist(TShow TEXT, Summary TEXT, Genre TEXT, Rating TEXT, Duration INT, Totalnum INT)")
sql.commit()

cur.execute('CREATE TABLE IF NOT EXISTS TVCounts(Show TEXT, Number INT)')
sql.commit()

cur.execute('CREATE TABLE IF NOT EXISTS Blocks(Name TEXT, items TEXT, Count INT)')
sql.commit()

print ("Necessary File check complete.")

if ("pass" in updatecheck):
	print ("Would you like to update your system database now to add the available shows and movies in your library?")
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
