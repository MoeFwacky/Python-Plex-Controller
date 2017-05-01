

import os
import getpass
import sqlite3
from time import localtime, strftime
from datetime import date
import calendar
import time

user = getpass.getuser()

DEFAULTDIR = homedir
ACTIONLOG = homedir + "tbn_schedules.log"
try:
	with open (ACTIONLOG, "r") as file:
		log = file.read()
	file.close()
except Exception:
	with open (ACTIONLOG, "w+") as file:
		file.write("File Opened\n")
	file.close()
	print ("Successfully created Log File.")

MYDB = DEFAULTDIR + "myplex.db"
sql = sqlite3.connect(MYDB)
cur = sql.cursor()
dte = date.today()
TODAY = str(calendar.day_name[dte.weekday()]).lower()

WEEKDAYS = ['monday','tuesday','wednesday','thursday','friday']
WEEKENDS = ['saturday','sunday']

thetime = strftime("%-I:%M %p", localtime())
#thetime = "4:46 PM"

if (thetime == "11:59 PM"):
	cur.execute("DELETE FROM SCHEDULES WHERE day LIKE \"today\"")
	sql.commit()

command = "SELECT * FROM SCHEDULES"

cur.execute(command)
if not cur.fetchall():
	pass
else:
	cur.execute(command)
	found = cur.fetchall()
	for item in found:
		if item[1] == thetime:
			actn = []
			print (item[0])
			actions = item[0]
			actions = actions.split(";")
			dcheck = item[2].lower()
			if ("-x" in dcheck):
				cur.execute("DELETE FROM SCHEDULES WHERE time LIKE \"" + thetime + "\" AND action LIKE \"" + str(item[0].strip()) + "\"")
				sql.commit()
				dcheck = dcheck.replace(" -x","")
			if (((dcheck == "weekdays") and (TODAY in WEEKDAYS)) or ((dcheck == "weekends") and (TODAY in WEEKENDS))):
				dcheck = TODAY
			print dcheck
			if ((dcheck == "today") or (dcheck == "everyday") or (dcheck == TODAY)):
				for thing in actions:
					if thing != "":
						actn.append(thing)
				for whatsit in actn:
					if "wait " in whatsit:
						num = whatsit.replace("wait ","")
						num = int(num.strip())
						#print ("sleeping " + str(num) + " seconds.")
						time.sleep(num)
					else:
						action = "python " + DEFAULTDIR + "system.py " + whatsit + ""
						print ("Executing: " + action)
						os.system(action)
			with open (ACTIONLOG, "a") as file:
				file.write(str(item))
			file.close()
				
