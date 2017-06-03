

import os
import sys
import getpass

user = getpass.getuser()

newdir = homedir
getfiles = newdir + "aliases"
badfix = newdir + "bad_aliases"

try:
	with open (badfix, "r") as file:
		removeme = file.readlines()
	file.close()
except Exception:
	cmd = "wget -O \"" + badfix + "\" \"https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/bad_aliases\""
        os.system(cmd)
	print ("Bad Aliases File Acquired.")
	with open (badfix, "r") as file:
                removeme = file.readlines()
        file.close()

with open(getfiles, "r") as file:
	thelines = file.readlines()
file.close

workingdir = "/home/" + user + "/.bashrc"

print ("Checking for bad entries.")

with open(workingdir, "r") as file:
	oldfile = file.readlines()
file.close()

for line in oldfile:
	if line in removeme:
		print ("Bad Entry Found: " + line + " -- Removing.\n")
		pass
	else:
		try:
			newfile = newfile + line
		except Exception:
			newfile = line

try:
	newfile
	command = "sudo cp " + workingdir + " /home/" + user + "/backup_bashrc"
	os.system(command)
	print("Successfully backed up bash file... just in case..")
	with open (workingdir, "w") as file:
		file.write(newfile)
	file.close()
	print ("Bad Entries have been purged. Moving on.")
except Exception:
	print ("No Bad Entries Found. No fix actions taken. Moving on.")

with open (workingdir, "r" )as file:
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
		print ("added: " + tline)

print ("Aliases successfully added. Adding play status files now.\n")
