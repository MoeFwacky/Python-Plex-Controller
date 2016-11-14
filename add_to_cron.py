import sys

user = str(sys.argv[1])

workd = "/etc/crontab"
writeme = "* * * * * * " + user + " python /home/ " + user + "/hasystem/tbn_schedule.py\n@reboot " + user + " python /home/" + user + "/hasystem/piplaystate.py > /dev/null 2>&1 &"

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
		print ("\nError adding piplaystate entry to cron. You need to manually add the following to your cron tab: @reboot " + user + "python /home/" + user + "/hasystem/piplaystate.py >/dev/null 2>&1")

