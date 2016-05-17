import os
import time
import urllib3
import getpass
import sqlite3

user = getpass.getuser()

maindir = "/home/" + user + "/hasystem/"

MYDB = maindir + "myplex.db"
sql = sqlite3.connect(MYDB)
cur = sql.cursor()

command = "SELECT setting FROM settings WHERE item LIKE \'ClientIP\'"
cur.execute(command)
clientip = cur.fetchone()
clientip = clientip[0]


playstate = maindir + "playstate.txt"
playstatestatus = maindir + "playstatestatus.txt"
pstate1 = maindir + "pstate.txt"
perror = maindir + "perror.txt"

def pstate():

	with open(playstate, "w") as file:
		file.write("")
	file.close()

	command = "sshpass -p 'rasplex' ssh -o StrictHostKeyChecking=no root@" + clientip + "tail -n 15 /storage/.plexht/temp/plexhometheater.log >> " + playstate

	check = "DEBUG: CPlexTimelineManager::ReportProgress updating subscribers: (playing)"
	check1 = "CPlexTimelineManager::ReportProgress updating subscribers: (paused)"
	check3 = "CPlexRemoteSubscriber::shouldRemove will not remove because elapsed: 10"

	os.system(command)
	#reads mini-log to do the check
	with open(playstate, "r") as file:
		results = file.readlines()
	file.close()
	#log of the state of previous scan
	with open(pstate1, "r") as file:
		pstate = file.read()
	file.close()
	found = ""
	for result in results:

		if "playing" in result:
			writeme = "playing"
			if "playing" not in pstate:
				with open(pstate1, "w") as file:
					file.write(writeme)
				file.close()
				
			ecount = "0"
			with open(perror, "w") as file:
				file.write(ecount)
			file.close()
			found = "yes"

			return ("playing")
		elif "paused" in result:
			writeme = "paused"
			if "paused" not in pstate:
				with open(pstate1, "w") as file:
					file.write(writeme)
				file.close()
			found = "yes"

			return ("paused")
		elif check3 in result:
			found = "no"
		else:
			found = "no"
	#this check is necessary because there are times where paused/play is not detected on a scan. I found that without this, the script was more apt to incorrectly detect a stop event and launch a new program when it shouldn't. Feel free to remove it and test without it. 
	if "no" in found:
		try:
			with open(perror, "r") as file:
				ecount = file.read()
			file.close()
		except Exception:
			ecount = 0

		ecount = int(ecount)
		if ecount == 2:
			with open(playstatestatus, "r") as file:
				plstate = file.read()
			file.close()
			if "On" in plstate:
				scommand = "python /home/" + user + "/hasystem/system.py startnextprogram"
				os.system(scommand)
				with open(perror, "w") as file:
					file.write("0")
				file.close()
				with open(pstate1, "w") as file:
					file.write("stopped")
				file.close()
				return ("Starting Next Program")
			elif "Sleep" in plstate:
				print ("sleeping")
				with open(playstatestatus, "w") as file:
					file.write("Off")
				file.close()
				with open(perror, "w") as file:
                                        file.write("0")
                                file.close()

				#tvofflink = ""
				#http = urllib3.PoolManager()
				#response = http.urlopen('GET', tvofflink, preload_content=False).read()
				return ("System has been put to sleep")
		else:
			ecount = ecount + 1
			ecount = str(ecount)
			with open(perror, "w") as file:
				file.write(ecount)
			file.close()	
			return ("Log Error. Checking Again.")
			
while True:
	with open(playstatestatus, "r") as file:
		plstate = file.read()
	file.close()
	if "Off" not in plstate:

		playstate = pstate()
		#print (playstate)
		#if it is starting a new program, wait to allow the program to start before resuming the playback checks. 
		if "Starting Next Program" in playstate:
			#print (playstate)
			time.sleep(30)
		elif "System has been put to sleep" in playstate:
			print (playstate)
			time.sleep(30)
	time.sleep(5)
	


