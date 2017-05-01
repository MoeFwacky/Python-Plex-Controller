

import os
import sys
import getpass
import subprocess
import sqlite3
import urllib3
import platform
try:
	urllib3.disable_warnings()
except Exception:
	pass

def worklist(thearray):
	if int(len(thearray) == 0):
		return ("Error: No results found.")
	movies = thearray
	mcount = 1
	mvcount = 0
	mmin = 0
	mmax = 9
	mpmin = 1
	if mmax >= len(movies):
		mmax = int(len(movies))-1
	exitc = ""
	while "quit" not in exitc:
		cls()
		try:
			print ("Error: " + Error + "\nThe Following Items Were Found:\n")
			del Error
		except NameError:
			print ("The Following Items Were Found:\n")
		while mmin <= mmax:
			print (str(mmin+1) + ": " + movies[mmin])
			mmin = mmin + 1
		print ("\nShowing Items " + str(mpmin) + " out of " + str(mmax+1)+ " Total Found: " + str(len(movies)))
		print ("\nSelect an item to return the corresponding item.\nTo see a description of an item enter \'desc number\', where number is the corresponding number.\nTo jump to a letter enter \'letter a\', where a is the desired letter.\nEnter \'Yes\' to go to the next page, and \'No\' to exit.\n")
		getme = input('Choice:')
		if (("yes" in getme.lower()) and ("letter" not in getme.lower())):
			mvcount = mvcount + 10
			mpmin = mmax + 1
			mmax = mmax + 10
			if (mmax > int(len(movies)-1)):
				mcheck = int(mmax) - int(len(movies)-1)
				if ((mcheck > 0) and (mcheck < 10)):
					mmax = mmax-mcheck
				elif mcheck > 10:
					return ("Done.")
			if (mmax == int(len(movies)+9)):
				return ("Done")
		elif (("no" in getme.lower()) and ("letter" not in getme.lower())):
			exitc = "quit"
			return ("done")
		else:
			try:
				return movies[int(getme)-1]
			except Exception:
				Error = "Invalid Selection. Please Try Again."
				mmin = mmin - 10

try:
	import certifi
	http = urllib3.PoolManager(
    	cert_reqs='CERT_NONE', # Force certificate check.
    	ca_certs=certifi.where(),  # Path to the Certifi bundle.
	)
except Exception:
	http = urllib3.PoolManager()
	#print ("Note: You can install the \"certifi\" library to resolve certificate error notices.")

try:
	input = raw_input
except NameError:
	pass

def cls():
   os.system('cls' if os.name=='nt' else 'clear')

ostype = platform.system()

try:
	extraopt = str(sys.argv[1])
except Exception:
	extraopt = "none"

if "Linux" in ostype:

	user = getpass.getuser()

	if ("root" in user):
		print ("Run this command as your non-root user, without sudo. You will be prompted for sudo access where it is necessary in this setup.")
	else:

		newdir = "/home/" + user + "/"
		homedir = "/home/" + user + "/hasystem/"
		writeme = "homedir = \'" + homedir + "\'\n"
		writemehome = writeme

		print ("Hello " + user + ". I am now adding the alias add script now. You may be prompted for sudo.\n")
		
		#updateing add_to_bash.py
		if not os.path.exists(homedir):
			os.makedirs(homedir)
			sayme = "The necessary directory has been created.\n"
		else:
			sayme = "Necsessary Directory Exists. Moving on.\n"

		print (sayme)
		file0 = homedir + "add_to_bash.py"
		try:
			os.remove(file0)
		except Exception:
			pass
		print ("Successfully removed add_to_bash.py. Getting latest file.")
		try:
			url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/add_to_bash.py"
			newfile = http.request('GET', url, preload_content=False)
			newfile = writemehome + str(newfile.data)
			#print newfile
			with open(file0, 'wb') as file:
				file.write(newfile)
			file.close()
			print ("File successfully moved to the necessary directory.")
		except IOError:
			print ("warning add_to_bash.py does not exist. Alias commands will not work.")
		
		#get alias file
		file10 = homedir + "aliases"
		try:
			os.remove(file10)
		except Exception:
			pass
		print ("Successfully removed aliases. Getting latest file.")
		try:
			url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/aliases"
			newfile = http.request('GET', url, preload_content=False)
			#print (newfile)
			with open(file10, 'wb') as file:
				file.write(newfile.data)
			file.close()
			print ("File successfully moved to the necessary directory.")
		except IOError:
				print ("warning aliases does not exist. Alias commands will not work.")
		try:
			command = "sudo python " + file0 + " " + user.strip()
			#print (command)
			os.system(command)
		except Exception:
			print ("Failed to add aliases to Bash. see add_to_bash.py for list of alias it is recommended you add.\n")
			updatecheck = "fail"


		print ("Trying to add a cron entry for the play checking script now.\n")

		#get add_to_cron.py
		file00 = homedir + "add_to_cron.py"
		try:
			os.remove(file00)
		except Exception:
			pass
		print ("Successfully removed add_to_cron.py. Getting latest file.")
		try:
			url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/add_to_cron.py"
			newfile = http.request('GET', url, preload_content=False)
			newfile = writemehome + str(newfile.data)
			with open(file00, 'wb') as file:
				file.write(newfile)
			file.close()
			print ("File successfully moved to the necessary directory.")
		except IOError:
			print ("warning add_to_cron.py does not exist. Cron add will fail.")
		try:
			command = "sudo python " + file00 + " " + user.strip()
			os.system(command)
		except Exception:
			print ("Failed to add cronjob. see add_to_cron.py for recommended job.\n")
			updatecheck = "fail"
	
		try:
			filex1 = homedir + "tbn_schedule.py"
			os.remove(filex1)
			print ("Removed tbn_schedule.py. Updating Now.")
		except Exception:
			pass
		try:
			url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/tbn_schedule.py"
			newfile = http.request('GET', url, preload_content=False)
			newfile = writemehome + str(newfile.data)
			#print newfile
			with open(filex1, 'wb') as file:
				file.write(newfile)
			file.close()
			print ("tbn_schedule.py successfully updated.")
		except IOError:
			print ("warning tbn_schedule.py does not exist. Scheduling will not work.")

		

else:
	print ("Unable to add cron or bash entries on a Windows system. I am skipping those steps.")
	
	hcheck = "negative"
	homedir = os.path.dirname(os.path.abspath(__file__))
	#homedir = homedir + "hasystem\\"
	writeme = "homedir = \'" + homedir + "\\'\n"
	writemehome = writeme
	

	
if not os.path.exists(homedir):
	os.makedirs(homedir)
	print (homedir + " has been successfully created.\n")
else:
	print (homedir + " already exists. Moving on.")
	

file5 = homedir + "system.py"
try:
	os.remove(file5)
	print ("Successfully removed system.py.")
except Exception:
	pass

try:
	url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/system.py"
	newfile = http.request('GET', url, preload_content=False)
	newfile = newfile.data
	#print (newfile)
	with open(file5, 'wb') as file:
		file.write(newfile)
	file.close()
	with open (file5, 'r') as file:
		rewrite = file.read()
	file.close()
	rewrite = writemehome + "\n" + rewrite
	with open(file5, "w") as file:
		file.write(rewrite)
	file.close()
	print ("system.py file successfully updated.")
except FileNotFoundError:
	print ("warning system.py does not exist. The TBN controller will not work.")
file6 = homedir + "piplaystate.py"
try:
	os.remove(file6)
	print ("Removed piplaystate.py. Getting newest version.")
except Exception:
	pass

try:
	url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/piplaystate.py"
	newfile = http.request('GET', url, preload_content=False)
	newfile = newfile.data
	with open(file6, 'wb') as file:
		file.write(newfile)
	file.close()
	with open (file6, 'r') as file:
		rewrite = file.read()
	file.close()
	rewrite = writemehome + "\n" + rewrite
	with open(file6, "w") as file:
		file.write(rewrite)
	file.close()
	print ("piplaystate.py successfully updated.")
except Exception:
	print ("warning piplaystate.py does not exist. The play check status script will not work.")
file7 = homedir + "playstatus.py"
try:
	os.remove(file7)
	print ("Removed playstatus.py. Updating now.")
except Exception:
	pass
	
try:
	url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/playstatus.py"
	newfile = http.request('GET', url, preload_content=False)
	newfile = newfile.data
	with open(file7, 'wb') as file:
		file.write(newfile)
	file.close()
	with open (file7, 'r') as file:
		rewrite = file.read()
	file.close()
	rewrite = writeme + rewrite
	with open(file7, "w") as file:
		file.write(rewrite)
	file.close()
	print ("File successfully moved to the necessary directory.")
except Exception:
	print ("warning playstatus.py does not exist. The play check status script will not work.")
	
file8 = homedir + "upddatedb_pi.py"
try:
	os.remove(file8)
	print ("Removed upddatedb_pi.py. Updating now.")
except Exception:
	pass
	
try:
	url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/upddatedb_pi.py"
	newfile = http.request('GET', url, preload_content=False)
	newfile = newfile.data
	with open(file8, "wb") as file:
		file.write(newfile)
	file.close()
	with open (file8, 'r') as file:
		rewrite = file.read()
	file.close()
	rewrite = writeme + rewrite
	with open(file8, "w") as file:
		file.write(rewrite)
	file.close()
	
	print ("File successfully moved to the necessary directory.")
	updatecheck = "pass"
except FileNotFoundError:
	print ("warning updateddb_pi.py does not exist. The system will be unable to build the shows and movie tables in your database.")
	updatecheck = "fail"
		
file9 = homedir + "tbn_webhook_service.py"
try:
	os.remove(file9)
	print ("Removed tbn_webhook_service. Updating now.")
except Exception:
	pass
	
try:
	url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/tbn_webhook_service.py"
	newfile = http.request('GET', url, preload_content=False)
	newfile = newfile.data
	with open(file9, "wb") as file:
		file.write(newfile)
	file.close()
	with open (file9, 'r') as file:
		rewrite = file.read()
	file.close()
	rewrite = writeme + rewrite
	with open(file9, "w") as file:
		file.write(rewrite)
	file.close()
	
	print ("File successfully moved to the necessary directory.")
	updatecheck = "pass"
except FileNotFoundError:
	print ("warning tbn_webhook_service.py does not exist. The system will be unable to use webhooks to react to playback state.")
	updatecheck = "fail"
	
file10 = homedir + "webhookstatus.py"
try:
	os.remove(file10)
	print ("Removed webhookstatus. Updating now.")
except Exception:
	pass
	
try:
	url = "https://raw.githubusercontent.com/MoeFwacky/Python-Plex-Controller/master/webhookstatus.py"
	newfile = http.request('GET', url, preload_content=False)
	newfile = newfile.data
	with open(file10, "wb") as file:
		file.write(newfile)
	file.close()
	with open (file10, 'r') as file:
		rewrite = file.read()
	file.close()
	rewrite = writeme + rewrite
	with open(file10, "w") as file:
		file.write(rewrite)
	file.close()
	
	print ("File successfully moved to the necessary directory.")
	updatecheck = "pass"
except FileNotFoundError:
	print ("warning webhookstatus.py does not exist. The system will be unable to use webhooks to react to playback state.")
	updatecheck = "fail"	
print ("Update Finished.\n")


