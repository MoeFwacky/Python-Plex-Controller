import os
import sys
import getpass

user = str(sys.argv[1])


newdir = "/home/" + user + "/hasystem/"
getfiles = newdir + "aliases"

with open(getfiles, "r") as file:
	thelines = file.readlines()
file.close

workingdir = "/home/" + user + "/.bashrc"

with open(workingdir, "r") as file:
	checkme = file.read()
file.close()

for tline in thelines:
	tline = tline.replace('/home/pi/hasystem/', newdir)
	tcheck = tline.split("=")
	tcheck = tcheck[0]
	#print (tcheck)
	if tcheck not in checkme:
		with open(workingdir, "a") as file:
			file.write(tline)
		file.close()
		print ("added" + tline)
	else:
		#print ("Already exists. Checking next.")
		pass


print ("Aliases successfully added. Adding play status files now.\n")
