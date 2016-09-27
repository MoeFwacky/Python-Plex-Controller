import os
import time
place = "/home/pi/hasystem/playstatus.txt"
place2 = "/home/pi/hasystem/playstatestatus.txt"
with open(place, "w") as file:
	file.write("")
file.close()

command = "ps aux | grep piplaystate.py | grep -v grep >> /home/pi/hasystem/playstatus.txt"
os.system(command)

time.sleep(1)

with open(place, "r") as file:
	stuff = file.read()
file.close()
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
	print ("I have tried to automatically start the script. Rerun playcheckstatus to confirm it is running.")


