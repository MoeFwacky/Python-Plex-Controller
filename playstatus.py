

import os
import subprocess
import time
place2 = homedir + "playstatestatus.txt"

command = "ps aux | grep piplaystate.py | grep -v grep"
try:
	stuff = subprocess.check_output(command, shell=True)
except subprocess.CalledProcessError:
	stuff = ""

#time.sleep(1)
with open(place2, "r") as file:
	status = file.read()
file.close()

sayme = "Playback checking is: " + status + ".\n"
print (sayme)

if "piplaystate.py" in stuff:
	print ("The Playback script is running")
else:
	print ("The Playback checking script is not running. Trying to restart.")
	command = "python " + homedir + "piplaystate.py >/dev/null &"
	os.system(command)
	time.sleep(1)
	command = "ps aux | grep piplaystate.py | grep -v grep"
	stuff = subprocess.check_output(command, shell=True)
	if "piplaystate.py" in stuff:
		print ("The Playback script is running")
	else:
		print ("Error: Failed to automatically start piplaystate.py.")


