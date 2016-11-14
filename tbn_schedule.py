import os
import getpass
import sqlite3
from time import localtime, strftime
from datetime import date
import calendar

user = getpass.getuser()

DEFAULTDIR = homedir

MYDB = DEFAULTDIR + "myplex.db"
sql = sqlite3.connect(MYDB)
cur = sql.cursor()
dte = date.today()
TODAY = str(calendar.day_name[dte.weekday()]).lower()

thetime = strftime("%-I:%M %p", localtime())

command = "SELECT * FROM SCHEDULES"

#command = "SELECT * FROM SCHEDULES WHERE time LIKE \"" + str(thetime).strip() + "\""

cur.execute(command)
if not cur.fetchall():
	pass
else:
	cur.execute(command)
	found = cur.fetchall()
	for item in found:
		if item[1] == thetime:
			if (thetime == "11:59 PM"):
				cur.execute("DELETE FROM SCHEDULES WHERE day LIKE \"today\"")
				sql.commit()
			actn = []
			actions = item[0]
			actions = actions.split(";")
			if ((item[2].lower() == "today") or (item[2].lower() == "everyday") or (item[2].lower() == TODAY)):
				if item[2].lower() == "today":
					cur.execute("DELETE FROM SCHEDULES WHERE time LIKE \"" + str(thetime).strip() + "\" AND day LIKE \"today\"")
					sql.commit()
				for thing in actions:
					if thing != "":
						actn.append(thing)
				for whatsit in actn:
					action = "python " + DEFAULTDIR + "system.py \"" + whatsit + "\""
					#print ("Executing: " + action)
					os.system(action)
					


#cur.execute("DELETE FROM SCHEDULES")
#sql.commit()


