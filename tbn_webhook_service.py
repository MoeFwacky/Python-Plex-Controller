homedir = '/home/pi/hasystem/'

import web
import time
import os
import sqlite3
import getpass
import urllib3

urls = ('/.*', 'hooks')

app = web.application(urls, globals())

DEFAULTDIR = homedir

MYDB = DEFAULTDIR + "myplex.db"
sql = sqlite3.connect(MYDB, check_same_thread=False)
cur = sql.cursor()

http = urllib3.PoolManager()

def getclient(data):
	client = data
	client = client.split("\"Player\":")
	client = client[1]
	client = client.split("},")
	client = client[0]
	client = client.split("title\":\"")
	client = client[1]
	client = client.split("\"")
	client = client[0]
	return (client)

def getaction(data):
	action = data
	action = action.split("event\":\"")
	action = action[1]
	action = action.split("\"")
	action = action[0]
	return action


class hooks:
	def POST(self):
		cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXCLIENT\'')
		PLEXCLIENT = cur.fetchone()
		PLEXCLIENT = PLEXCLIENT[0]

		cur.execute("SELECT State FROM States WHERE Option LIKE \"WEBHOOKSTATUS\"")
		WSTATUS = cur.fetchone()[0]
		data = web.data()
		#print (data)
		client = getclient(data)
		action = getaction(data)
		#print WSTATUS
		if WSTATUS == "ON":
			if (("media.pause" in action) and (PLEXCLIENT == client)):
				#PAUSED ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
				pass
			#elif (("media.resume" in action) and (PLEXCLIENT == client)):
				#RESUME ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
			#	pass
			elif (("media.stop" in action) and (PLEXCLIENT == client)):
				#stopped ACTIONS GO BETWEEN HERE and the time.sleep()...
                                time.sleep(2)
				cmd1 = "python " + homedir + "system.py startnextprogram"
                                os.system(cmd1)
				#WSTATUS = "ON"
				#print ("Stopped")
				#WSTATUS = "Pending"
				#command = "python " + homedir + "system.py startnextprogram"
				#print ("Starting Next Program")
				#os.system(command)
			elif (("media.play" in action) and (PLEXCLIENT == client)):
				#PLAY ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
				pass
		elif WSTATUS == "PENDING":
                        if (("media.pause" in action) and (PLEXCLIENT == client)):
                                #PAUSED ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
                                pass
                        elif (("media.resume" in action) and (PLEXCLIENT == client)):
                                #RESUME ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
                                pass
#			elif (("media.stop" in action) and (PLEXCLIENT == client)):
#                               time.sleep(2)
#                               cmd1 = "python " + homedir + "system.py startnextprogram"
#                               os.system(cmd1)
#				print ("Duplicate Request, Dropping.")
			elif (("media.play" in action) and (PLEXCLIENT == client)):
				#print ("Media Playing, Resetting Status.")
				time.sleep(5)
				WSTATUS = "ON"
				cmd1 = "python " + homedir + "system.py setwebhookstatus on"
				os.system(cmd1)
		elif WSTATUS == "SLEEP":
			if (("media.pause" in action) and (PLEXCLIENT == client)):
				#PAUSED ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
				pass
			elif (("media.resume" in action) and (PLEXCLIENT == client)):
				#RESUME ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
				pass
			elif (("media.stop" in action) and (PLEXCLIENT == client)):
				cmd1 = "python /home/pi/hasystem/system.py setwebhookstatus off"
				os.system(cmd1)
				#stopped ACTIONS GO BETWEEN HERE 
				#pass
			elif (("media.play" in action) and (PLEXCLIENT == client)):
				#PLAY ACTIONS GO BELOW HERE... COMMMENT OUT THE pass TO USE
				pass


		return 'OK'

if __name__ == '__main__':
    app.run()
