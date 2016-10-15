import os
import subprocess
import time
place2 = homedir + "playstatestatus.txt"
with open(place, "w") as file:
	file.write("")
file.close()

command = "ps aux | grep piplaystate.py | grep -v grep"
stuff = subprocess.check_output(command, shell=True)

time.sleep(1)
with open(place2, "r") as file:
	status = file.read()
file.close()

sayme = "Playback checking is: " + status + ".\n"
print (sayme)

if "hasystem/piplaystate.py" in stuff:
	print ("The Playback script is running")
else:
	print ("The Playback checking script is not running. Trying to restart.")
	command = "python /home/pi/hasystem/piplaystate.py >/dev/null 2>&1"
	os.system(command)
	time.sleep(1)
	stuff = subprocess.check_output(command, shell=True)
	if "hasystem/piplaystate.py" in stuff:
		print ("The Playback script is running")
	else:
		print ("Error: Failed to automatically start piplaystate.py.")


