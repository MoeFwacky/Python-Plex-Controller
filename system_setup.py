import os
import sys
import getpass
import subprocess
import sqlite3
import urllib2

user = getpass.getuser()

if user == "root":
	print ("Error. This setup should be run this using your normal user account. Where root is needed, you will be prompted.")
else:
	try:
		extraopt = str(sys.argv[1])
	except Exception:
		extraopt = "none"

	addme = """

	#Plex system.py aliases

	alias whatupnext='python /home/pi/hasystem/system.py whatupnext'
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

	if not os.path.exists(homedir):
		os.makedirs(homedir)
		sayme = "The necessary directory has been created."
	else:
		sayme = ""


	print ("Hello " + user + ". " + sayme + " I am now adding the system aliases to the bash.")

	workingdir = "/home/" + user + "/.bashrc"

	with open(workingdir, "r") as file:
		checkme = file.read()
	file.close()

	workd = "/etc/crontab"

	with open(workd, "r") as file:
		checkme1 = file.read()
	file.close()

	writeme = "@reboot python /home/" + user + "/hasystem/piplaystate.py"

	if writeme in checkme1:
		print ("Cron entry for piplaystate.py already present. No action taken.")
	else:
		try:
			file9 = homedir + "add_to_cron.py"
			with open (file9, "r") as file:
				readme = file.read()
			file.close()
			print ("check pass. add_to_cron.py exists.")
		
		except IOError:
			try:
				getme = urllib2.urlopen('https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/add_to_cron.py')
				getme = getme.read()
				newfile = homedir + "add_to_cron.py"
				with open (newfile, 'wb') as file:
					file.write(getme)
				file.close()
				print ("File add_to_cron successfully moved to the necessary directory.")
			except Exception:
				print ("warning add_to_cron.py does not exist. The system will be unable to add the cron entry.")
		try:		
			command = "sudo python " + homedir + "add_to_cron.py " + user
			os.system(command)
		except Exception:
			print ("Failed to update Cron.")
		
	if addme in checkme:
		print ("Necessary aliases already in bash. Adding play status files now.")
	else:
		try:
			file10 = homedir + "add_to_bash.py"
			with open (file10, "r") as file:
				readme = file.read()
			file.close()
			print ("check pass. add_to_bash.py exists.")
		
		except IOError:
			try:
				getme = urllib2.urlopen('https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/add_to_bash.py')
				getme = getme.read()
				newfile = homedir + "add_to_bash.py"
				with open (newfile, 'wb') as file:
					file.write(getme)
				file.close()
				print ("File add_to_bash successfully moved to the necessary directory.")
			except Exception:
				print ("warning add_to_bash.py does not exist. The system will be unable to add the bash entry.")
		try:
			command = "sudo python " + homedir + "add_to_bash.py"
			os.system(command)
			print ("Aliases successfully added. Adding play status files now.\n")
		except Exception:
			print ("Failed to add entries to bash.")

	studio = homedir +"Studio/"
	if not os.path.exists(studio):
		os.makedirs(studio)

	genre = homedir + "Genre/"
	if not os.path.exists(genre):
		os.makedirs(genre)

	genre = genre + "TV/"
	if not os.path.exists(genre):
		os.makedirs(genre)

	try:
		file1 = homedir + "playstate.txt"
		with open (file1, "r") as file:
			readme = file.read()
		file.close()
		print ("playstate text file already exists. Checking pstate file now.")

	except IOError:
		command = "touch " + homedir + "playstate.txt"
		os.system(command)
		print ("playstate text file successfully added.")	
	try:
		file2 = homedir + "pstate.txt"
		with open (file2, "r") as file:
			readme = file.read()
		file.close()
		print ("pstate text file already exists. Checking perror file now.")
	except IOError:
		command = "touch " + homedir + "pstate.txt"
		os.system(command)
		print ("pstate text file successfully added.")

	try:
		file3 = homedir + "perror.txt"
		with open (file3, "r") as file:
			readme = file.read()
		file.close()
		print ("perror text file already exists. Checking playstatestatus file now.")
	except IOError:
		command = "touch " + homedir + "perror.txt"
		os.system(command)
		print ("playstate text file successfully added.")

	try:
		file4 = homedir + "playstatestatus.txt"
		with open (file4, "r") as file:
			readme = file.read()
		file.close()
		print ("playstatestatus text file already exists. Checking script file now.")
	except IOError:
		file4 = homedir + "playstatestatus.txt"
		with open (file4, "w") as file:
			file.write("Off")
		file.close()
		
		print ("playstate text file successfully added.")
			
	try:
		file11 = homedir + "tonights_movie.txt"
		with open (file11, "r") as file:
			readme = file.read()
		file.close()
		print ("tonights_movie.txt text file already exists. Checking script file now.")
	except IOError:
		file11 = homedir + "tonights_movie.txt"
		with open (file11, "w") as file:
			file.write("")
		file.close()
		
		print ("playstate text file successfully added.")

	try:
		file6 = homedir + "piplaystate.py"
		with open (file6, "r") as file:
			readme = file.read()
		file.close()
		print ("check pass. piplaystate.py exists.")
	except IOError:
		try:
			getme = urllib2.urlopen('https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/piplaystate.py')
			getme = getme.read()
			newfile = homedir + "piplaystate.py"
			with open (newfile, 'wb') as file:
				file.write(getme)
			file.close()
			print ("File successfully moved to the necessary directory.")
		except Exception:
			print ("warning piplaystate.py does not exist. The play check status script will not work.")

	try:
		file7 = homedir + "playstatus.py"
		with open (file7, "r") as file:
				readme = file.read()
		file.close()
		print ("check pass. playstatus.py exists.")
	except IOError:
		try:
			getme = urllib2.urlopen('https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/playstatus.py')
			getme = getme.read()
			newfile = homedir + "playstatus.py"
			with open (newfile, 'wb') as file:
				file.write(getme)
			file.close()
			print ("File successfully moved to the necessary directory.")
		except Exception:
			print ("warning playstatus.py does not exist. The play check status script will not work.")

	try:
		file8 = homedir + "upddatedb_pi.py"
		with open (file8, "r") as file:
			readme = file.read()
		file.close()
		print ("check pass. upddatedb_pi.py exists.")
		updatecheck = "pass"
	except IOError:
		try:
			getme = urllib2.urlopen('https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/upddatedb_pi.py')
			getme = getme.read()
			newfile = homedir + "upddatedb_pi.py"
			with open (newfile, 'wb') as file:
				file.write(getme)
			file.close()
			print ("File successfully moved to the necessary directory.")
		except Exception:
			print ("warning updateddb_pi.py does not exist. The system will be unable to build the shows and movie tables in your database.")
			updatecheck = "fail"

	try:
		file12 = homedir + "system.py"
		with open (file12, "r") as file:
			readme = file.read()
		file.close()
		print ("check pass. system.py exists.")
		updatecheck = "pass"
	except IOError:
		try:
			getme = urllib2.urlopen('https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/system.py')
			getme = getme.read()
			newfile = homedir + "system.py"
			with open (newfile, 'wb') as file:
				file.write(getme)
			file.close()
			print ("File successfully moved to the necessary directory.")
		except Exception:
			print ("warning system.py does not exist. The system will be unable to build the shows and movie tables in your database.")
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

	#check to see if client IP is present. Used for play check script.
	cur.execute('SELECT setting FROM settings WHERE item LIKE \'ClientIP\'')
	if not cur.fetchone():
		clientip = str(raw_input('Input Client IP: '))
		cur.execute('INSERT INTO settings VALUES(?,?)', ('ClientIP', clientip.strip()))
		sql.commit()

	#checks for plex user name and PW. Used for Plex API. 
	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXUN\'')
	if not cur.fetchone():
		PLEXUN = str(raw_input('Plex Username: '))
		writeme = str("PLEXUN")
		cur.execute('INSERT INTO settings VALUES(?,?)', (writeme,PLEXUN))
		sql.commit()

	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXPW\'')
	if not cur.fetchone():
		PLEXPW = str(raw_input('Plex Password: '))
		cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXPW',PLEXPW))
		sql.commit()

	#checks for client name and server name. used by Plex API.
	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSVR\'')
	if not cur.fetchone():
		PLEXSVR = str(raw_input('Plex Server Name: '))
		cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXSVR',PLEXSVR))
		sql.commit()

	cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXCLIENT\'')
	if not cur.fetchone():
		PLEXCLIENT = str(raw_input('Plex Client Name: '))
		cur.execute('INSERT INTO settings VALUES(?,?)', ('PLEXCLIENT',PLEXCLIENT))
		sql.commit()

	#get wildcard show name. Used as part of random media picking mechanism.
	cur.execute('SELECT setting FROM settings WHERE item LIKE \'WILDCARD\'')
	if not cur.fetchone():
		WILDCARD = str(raw_input('Wild Card Show: '))
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
	try:
		updatecheck
	except NameError:
		updatecheck = "fail"

	if ("pass" in updatecheck):
		print ("Would you like to update your system database now to add the available shows and movies in your library?")
		choice = str(raw_input('Yes or No? '))
		if "y" in choice.lower():
			command = "python " + homedir + "upddatedb_pi.py all"
			os.system(command)
		print ("If you needed that entry for cron it was: @reboot python /home/pi/hasystem/piplaystate.py &")
	else:
		print ("The files system_setup.py can add have been added.\n Done!")

