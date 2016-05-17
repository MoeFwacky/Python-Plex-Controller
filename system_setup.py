import os
import sys
import getpass
import subprocess
import sqlite3

user = getpass.getuser()

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
"""

indexfile = """
<?php
$name = $_GET['playme'];
if (isset($name)){
#echo $name;
echo "<center><h3>TVN Plex Web Controller</h3><br>";
$command = 'python /home/""" + user + """/hasystem/system.py "'.$name . '"';

}else{
echo "<center><h3>TheBaconNation.com Home Automation Web Controller</h3><br><h2>Error: </h2><br>";
$command = '/usr/bin/python /home/""" + user + """/hasystem/system.py';
}

$xcommand = escapeshellcmd($command);
$output = shell_exec($xcommand);
echo $output;

?>
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
writeme = "@reboot python /home/" + user + "/pi/hasystem/piplaystate.py &"

with open(workd, "r") as file:
	checkme1 = file.read()
file.close()

if writeme in checkme1:
	print ("Cron entry for piplaystate.py already present. No action taken.")
else:
	try:
		with open(workd, "a") as file:
			file.write(writeme)
		file.close()
		print ("A Cron entry has been added for piplaystate.py\n")
	except Exception:
		print ("\nError adding piplaystate entry to cron. You need to manually add the following to your cron tab: @reboot python /home/" + user + "/hasystem/piplaystate.py &")

if addme in checkme:
	print ("Necessary aliases already in bash. Adding play status files now.")
else:

	with open(workingdir, "a") as file:
		file.write(addme)
	file.close()

	print ("Aliases successfully added. Adding play status files now.\n")

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
        file6 = homedir + "piplaystate.py"
        with open (file6, "r") as file:
                readme = file.read()
        file.close()
        print ("check pass. piplaystate.py exists.")
except IOError:
	try:
		command = "cp -r ./piplaystate.py " + file6
		os.system(command)
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
		command = "cp -r ./playstatus.py " + file7
                os.system(command)
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
		command = "cp -r ./upddatedb_pi.py " + file8
                os.system(command)
                print ("File successfully moved to the necessary directory.")
        except Exception:
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

'''
#webserver action is currently commented out for further testing purposes.

print ("\nDo you want to also run a webserver?\n")
webcheck = str(raw_input('Yes or No: '))
if "y" in webcheck.lower():
	phpcheck = "sudo apt-get -y install php5 libapache2-mod-php5"
	os.system(phpcheck)
	webdir = "/var/www/"
	webindex = webdir + "index.php"
	apcheck = "dpkg --get-selections | grep apache"
	try:
		output = subprocess.check_output(apcheck, shell=True)
	except Exception:
		output = ""
	if "apache2" in output:
		print ("Apache already installed. Updating index.php file now.")
		try:
			with open(webindex, "w") as file:
				file.write(indexfile)
			file.close()
		except Exception:
			try:
				writedir = homedir + "index.php"
				with open(writedir, "w") as file:
					file.write(indexfile)
				file.close()
				command = "sudo cp /home/" + user + "/hasystem/index.php /var/www/html/index.php"
				os.system(command)
				command = "sudo /etc/init.d/apache2 restart"
				os.system(command)
				print ("Successfully updated /var/www/html/index.php.")
			except exception:
				print ("Attempts to update /var/www/html/index.php failed.")

	else:
		command = "sudo apt-get install apache2"
		os.system(command)
		try:
                        with open(webindex, "w") as file:
                                file.write(indexfile)
                        file.close()
                except Exception:
                        print ("Error updating index.php file in /var/www/html/. You will need to manually fix that to take advantage of the web interaction ability.")

'''

if ("pass" in updatecheck):
	print ("Would you like to update your system database now to add the available shows and movies in your library?")
	choice = str(raw_input('Yes or No? '))
	if "y" in choice.lower():
		command = "python " + homedir + "upddatedb_pi.py all"
		os.system(command)
	print ("If you needed that entry for cron it was: @reboot python /home/pi/hasystem/piplaystate.py &")
else:
	print ("The files system_setup.py can add have been added.\n Done!")

