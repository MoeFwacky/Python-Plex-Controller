import os
import getpass
import time

user = getpass.getuser()
place = "/home/" + user + "/hasystem/playstatus.txt"
place2 = "/home/" + user + "/hasystem/playstatestatus.txt"
with open(place, "w") as file:
	file.write("")
file.close()

command = "ps aux | grep piplaystate.py >> " + place
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
check1 = "python /home/" + user + "/hasystem/piplaystate.py"
if check1 in stuff:
	print ("The Playback script is running")
else:
	print ("The Playback checking script is not running. Trying to restart.")
	command = "python /home/" + user + "/hasystem/piplaystate.py &"
	os.system(command)
	time.sleep(1)
	print ("I have tried to automatically start the script. Rerun playcheckstatus to confirm it is running.")


