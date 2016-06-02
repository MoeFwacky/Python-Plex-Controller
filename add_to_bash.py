import os
import sys
import getpass

user = str(sys.argv[1])

addme = """

#Plex system.py aliases

alias whatupnext='python /home/pi/hasystem/system.py whatupnext'
alias startnextprogram='python /home/pi/hasystem/system.py startnextprogram'
alias queueshow='python /home/pi/hasystem/system.py queueshow'
alias suggestmovie='python /home/pi/hasystem/system.py suggestmovie'
alias moviedetails='python /home/pi/hasystem/system.py moviedetails'
alias idtonightsmovie='python /home/pi/hasystem/system.py idtonightsmovie'
alias findmovie='python /home/pi/hasystem/system.py findmovie'
alias findshow='python /home/pi/hasystem/system.py findshow'
alias suggesttv='python /home/pi/hasystem/system.py suggesttv'
alias addsuggestion='python /home/pi/hasystem/system.py addsuggestion'
alias skipthat='python /home/pi/hasystem/system.py skipthat'
alias whatispending='python /home/pi/hasystem/system.py whatispending'
alias playme='python /home/pi/hasystem/system.py'
alias nowplaying='python /home/pi/hasystem/system.py nowplaying'
alias nextep='python /home/pi/hasystem/system.py nextep'
alias queueadd='python /home/pi/hasystem/system.py queueadd'
alias idplaymode='python /home/pi/hasystem/system.py getplaymode'
alias getplaymode='python /home/pi/hasystem/system.py getplaymode'
alias setplaymode='python /home/pi/hasystem/system.py setplaymode'
alias availableblocks='python /home/pi/hasystem/system.py availableblocks'
alias explainblock='python /home/pi/hasystem/system.py explainblock'
alias epdetails='python /home/pi/hasystem/system.py epdetails'
alias setnextep='python /home/pi/hasystem/system.py setnextep'
alias stopplayback='python /home/pi/hasystem/system.py stopplayback'
alias pauseplayback='python /home/pi/hasystem/system.py pauseplayback'
alias addblock='python /home/pi/hasystem/system.py addblock'
alias addtoblock='python /home/pi/hasystem/system.py addtoblock'
alias removefromblock='python /home/pi/hasystem/system.py removefromblock'
alias removeblock='python /home/pi/hasystem/system.py removeblock'
alias setupnext='python /home/pi/hasystem/system.py setupnext'
alias playcheckstatus='python /home/pi/hasystem/playstatus.py'
alias playcheckstart='python /home/pi/hasystem/system.py playcheckstart'
alias playcheckstop='python /home/pi/hasystem/system.py playcheckstop'
alias playchecksleep='python /home/pi/hasystem/system.py playchecksleep'
alias whereat='python /home/pi/hasystem/system.py whereat'
alias findsomethingelse='python /home/pi/hasystem/system.py findsomethingelse'
alias findnewmovie='python /home/pi/hasystem/system.py findnewmovie'
alias addfavoritemovie='python /home/pi/hasystem/system.py addfavoritemovie'
alias listclients='python /home/pi/hasystem/system.py listclients'
alias changeclient='python /home/pi/hasystem/system.py changeclient'
alias listwildcard='python /home/pi/hasystem/system.py listwildcard'
alias changewildcard='python /home/pi/hasystem/system.py changewildcard'
"""

newdir = "/home/" + user + "/"
addme = addme.replace("/home/pi/", newdir)


workingdir = "/home/" + user + "/.bashrc"

with open(workingdir, "r") as file:
	checkme = file.read()
file.close()

if addme in checkme:
	print ("Necessary aliases already in bash. Adding play status files now.")
else:

	with open(workingdir, "a") as file:
		file.write(addme)
	file.close()

	print ("Aliases successfully added. Adding play status files now.\n")
