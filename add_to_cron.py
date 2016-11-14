import sys

user = str(sys.argv[1])

workd = "/etc/crontab"
writeme = "@reboot " + user + " python /home/" + user + "/hasystem/piplaystate.py > /dev/null 2>&1 &"
writeme2 = "* * * * * " + user + " python /home/" + user + "/hasystem/tbn_schedule.py"

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
		print ("Failed to add cron entry for piplaystate.py.")
if writeme2 not in checkme1:
	try:
		with open(workd, "a") as file:
			file.write(writeme2)
		file.close()
		print ("A Cron entry has been added for tbn_schedule.py\n")
	except Exception:
		print ("Failed to add cron entry for tbn_schedule.py.")

