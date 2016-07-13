homedir = 'addhomedirhere'

import urllib3
import requests
import time
import os
import sys
import sqlite3

#top
Maindir = homedir
PROBLEMS = Maindir + "problems.txt"
command = "rm -rf " + PROBLEMS
os.system(command)

MYDB = Maindir + "myplex.db"

http = urllib3.PoolManager()

sql = sqlite3.connect(MYDB)
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS settings(item TEXT, setting TEXT)')
sql.commit()

command = 'SELECT setting FROM settings WHERE item LIKE \'TVPART\''
cur.execute(command)
test2 = cur.fetchone()
if ((test2 == "") or (not cur.fetchone())):
	print ("Looks like you have never run the update DB script. I need some information to proceed.\n Enter the link to your metadata.\n Example: http://192.168.1.134:32400/library/metadata/\n")
	TVPART = str(raw_input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVPART",TVPART.strip()))
	sql.commit()
	print (TVPART + " has been added to the settings table. Moving on.")
else:
	TVPART = test2[0]

command = 'SELECT setting FROM settings WHERE item LIKE \'TVGET\''
cur.execute(command)
test1 = cur.fetchone()
print (test1)
if ((not cur.fetchone()) or (test1 == "")):
        print ("Enter the link to your TV show tree.\nExample: http://192.168.1.134:32400/library/sections/1/all \n")
        TVGET = str(raw_input('Link:'))
        cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVGET",TVGET.strip()))
        sql.commit()
        print (TVGET + " has been added to the settings table. Moving on.")
else:
	TVGET = test1[0]

command = 'SELECT setting FROM settings WHERE item LIKE \'MOVIEGET\''
cur.execute(command)
test = cur.fetchone()
if ((not cur.fetchone()) or (test == "")):
        print ("Enter the link to your Movie tree.\nExample: http://192.168.1.134:32400/library/sections/2/all \n")
        MOVIEGET = str(raw_input('Link:'))
        cur.execute('INSERT INTO settings VALUES(?, ?)', ("MOVIEGET",MOVIEGET.strip()))
        sql.commit()
        print (MOVIEGET + " has been added to the settings table. Moving on.")
else:
	MOVIEGET = test[0]

print ("Database update starting...\n")	


def gettvshows():	
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	#print (response)
	shows = response.split('<Directory ratingKey=')
	counter = 1

	workingdir = Maindir + "tvshowlist.txt"

	while counter <= int(len(shows)-1):

		show = shows[counter]
		
		genres = show
		studio = show
		
		
		title = show
		title = title.split('title="')
		title = title[1]
		title = title.split('"')
		title = title[0]
		
		title = title.replace('&apos;','\'')
		title = title.replace('&amp;','&')
		title = title.replace('?','')
		title = title.replace('/',' ')
		
		summary = show
		rating = show
		duration = show
		totalnum = show
		
		summary = show
		summary = summary.split('summary="')
		summary = summary[1]
		summary = summary.split('"')
		summary = summary[0]
		summary = summary.replace('\'','')
		
		rating = show
		try:
			rating = rating.split('contentRating="')
			rating = rating[1]
			rating = rating.split('"')
			rating = rating[0]
		except Exception:
			rating = 'N\A'
		duration = show
		duration = duration.split('duration="')
		duration = duration[1]
		duration = duration.split('"')
		duration = duration[0]
		duration = int(duration)/60000
		
		totalnum = show
		totalnum = totalnum.split(' leafCount="')
		totalnum = totalnum[1]
		totalnum = totalnum.split('"')
		totalnum = totalnum[0]
		
		name = title
		TShow = name
				
		genres = genres.split("<Genre tag=\"")
		try:
			genre = genres[1]
		except IndexError:
			genre = "none"
		try:
			genre2 = genres[2]
			genre2 = genre2.split('" />')
			genre2 = genre2[0]
			#print (genre2)
		except IndexError:
			genre2 = "none"
		try:
			genre3 = genres[3]
			genre3 = genre3.split('" />')
			genre3 = genre3[0]
			#print (genre2)
		except IndexError:
			genre3 = "none"
		genre = genre.split('" />')
		
		genre = genre[0] + ";" + genre2 + ";" + genre3 + ";"
		genre = genre.replace('none;','')
		#print (genre)
		
			
			
		studio = studio.split("studio=\"")
		try:
			studio = studio[1]
			studio = studio.split("\"")
			studio = studio[0]
		except IndexError:
			studio = "None"
		#marker
		TShow = TShow.replace("'","''")
		summary = summary.replace("'","''")
		try:
			cur.execute("SELECT * FROM TVshowlist WHERE TShow LIKE \"" + TShow + "\"")
			if not cur.fetchone():
				cur.execute("INSERT INTO TVshowlist VALUES(?, ?, ?, ?, ?, ?)", (TShow, summary, genre, rating, duration, int(totalnum)))
				sql.commit()
				
		except Exception: 
			print ("Error adding " + TShow)
			try:
				with open(PROBLEMS, 'a') as file:
					file.write(TShow + "\n")
				file.close()
			except Exception:
				TShow = 'ERRORHERE'
				with open(PROBLEMS, 'a') as file:
                                        file.write(TShow + "\n")
                                file.close()
			try:
				with open(PROBLEMS, 'a') as file:
					file.write(summary + "\n")
				file.close()
			except Exception:
				summary = "ERRORHERE"
				with open(PROBLEMS, 'a') as file:
                                        file.write(summary + "\n")
                                file.close()
			try:
                                with open(PROBLEMS, 'a') as file:
                                        file.write(genre + "\n")
                                file.close()
                        except Exception:
                                genre = "ERRORHERE"
                                with open(PROBLEMS, 'a') as file:
                                        file.write(genre + "\n")
                                file.close()
			try:
                                with open(PROBLEMS, 'a') as file:
                                        file.write(rating + "\n")
                                file.close()
                        except Exception:
                                rating = "ERRORHERE"
                                with open(PROBLEMS, 'a') as file:
                                        file.write(rating + "\n")
                                file.close()
			try:
                                with open(PROBLEMS, 'a') as file:
                                        file.write(duration + "\n")
                                file.close()
                        except Exception:
                                duration = "ERRORHERE"
                                with open(PROBLEMS, 'a') as file:
                                        file.write(duration + "\n\n")
                                file.close()
					
				
		
		counter = counter + 1

	
	print ("TV entries checked.")

gettvshows()
		

print ("Done")	
		

