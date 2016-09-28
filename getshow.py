#homedir = 'full path to location of myplex.db goes here.'
import urllib3
import subprocess
import requests
import time
import os
import sys
import sqlite3
import platform
#top

try:
	input = raw_input
except NameError:
	pass

global favtv
global favmve
global tvgenres
global moviegenres

favtv = []
favmve = []
tvgenres = []
moviegenres = []

MYDB = homedir + "myplex.db"
http = urllib3.PoolManager()

sql = sqlite3.connect(MYDB)
cur = sql.cursor()

FIXME = homedir + "fixme.txt"
PROBLEMS = homedir + "problems.txt"
with open (PROBLEMS, "w") as file:
	file.write('')
file.close()

ostype = platform.system()

cur.execute('CREATE TABLE IF NOT EXISTS settings(item TEXT, setting TEXT)')
sql.commit()

command = 'SELECT setting FROM settings WHERE item LIKE \'TVPART\''
cur.execute(command)
if not cur.fetchone():
	print ("Looks like you have never run the update DB script. I need some information to proceed.\n Enter the link to your metadata.\n Example: http://192.168.1.134:32400/library/metadata/\n")
	TVPART = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVPART",TVPART.strip()))
	sql.commit()
	print (TVPART + " has been added to the settings table. Moving on.")
else:
	cur.execute(command)
	test2 = cur.fetchone()[0]
	TVPART = test2

command = 'SELECT setting FROM settings WHERE item LIKE \'TVGET\''
cur.execute(command)
if not cur.fetchone():
	print ("Enter the link to your TV show tree.\nExample: http://192.168.1.134:32400/library/sections/1/all/ \n")
	TVGET = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVGET",TVGET.strip()))
	sql.commit()
	print (TVGET + " has been added to the settings table. Moving on.")
else:
	cur.execute(command)
	test1 = cur.fetchone()[0]
	TVGET = test1

command = 'SELECT setting FROM settings WHERE item LIKE \'MOVIEGET\''
cur.execute(command)
if not cur.fetchone():
	print ("Enter the link to your Movie tree.\nExample: http://192.168.1.134:32400/library/sections/2/all/ \n")
	MOVIEGET = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("MOVIEGET",MOVIEGET.strip()))
	sql.commit()
	print (MOVIEGET + " has been added to the settings table. Moving on.")
else:
	cur.execute(command)
	test = cur.fetchone()[0]
	MOVIEGET = test

print ("Database update starting...\n")	

cur.execute('CREATE TABLE IF NOT EXISTS shows(TShow TEXT, Episode TEXT, Season INT, Enum INT, Tnum INT, Summary TEXT, Link TEXT)')
sql.commit()
cur.execute('CREATE TABLE IF NOT EXISTS Movies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
sql.commit()
cur.execute('CREATE TABLE IF NOT EXISTS TVshowlist(TShow TEXT, Summary TEXT, Genre TEXT, Rating TEXT, Duration INT, Totalnum INT)')
sql.commit()
def getshow(findme):	
	print (findme)
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	#print (response)
	shows = response.split('<Directory ratingKey=')
	counter = 1

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
		#print (title)
		if findme.lower().strip() == title.lower().strip():
			print ("FOUND!!")
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
			TShow = TShow.replace("'","''")
			summary = summary.replace("'","''")
			summary = str(summary.encode('ascii','ignore')).strip()
			cur.execute("SELECT * FROM TVshowlist WHERE TShow LIKE \"" + TShow + "\"")
			try:
				if not cur.fetchone():
					cur.execute("INSERT INTO TVshowlist VALUES(?, ?, ?, ?, ?, ?)", (TShow, summary, genre, rating, int(duration), int(totalnum)))
					sql.commit()
			except Exception: 
				print ("Error adding " + TShow)
				with open(PROBLEMS, 'a') as file:
					file.write(TShow + "\n")
				file.close()
					
			
		counter = counter + 1

	
	print ("TV entries checked.")


def gettvshows(findme):	
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	#print (response)
	shows = response.split('<Directory ratingKey=')
	counter = 1

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
		
		if title.lower().strip() == findme.lower().strip():
		
		
			name = title
			TShow = name
			if (("'" in TShow) and ("''" not in TShow)):
				TShow = TShow.replace("'","''")
				print (TShow)
			
			
			show = show.split('" key')
			show = show[0]
			show = show.replace("\"", "")
			show = show.rstrip()
			episode = show
			
			link = TVPART + show + "/allLeaves"
			print (link)
			xresponse = http.urlopen('GET', link, preload_content=False).read()
			xresponse = str(xresponse)
			
			episodes = xresponse.split('type="episode" title="')
			#print (episodes)
			for episode in episodes:
				Season = episode
				Enum = episode
				Summary = episode
				Link = episode
				episode = episode.split('"')
				episode = episode[0]
				episode = episode + "\n"
				episode = episode.replace('&apos;','\'')
				episode = episode.replace('&amp;','&')
				Episode = episode.strip()
				if ("<?xml version=" in episode.strip()):
					#print ("Pass")
					Tnum = 0
				else:
				
					if ("(" in episode):
						xepisode = name + " " + episode
						with open(FIXME, 'a') as file:
							file.write(xepisode)
						file.close()
					#episode = episode.rstrip()
					#print (episode)
					if episode != "Original":
						#print ("Skipping")
					#else:
					
						#with open(title, "a") as file:
							#file.write(episode)
						#file.close()
					
						try:
							Tnum = Tnum + 1
						except Exception:
							Tnum = 0
						#print (Season)
						Season = Season.split('parentIndex="')
						#print (Season)
						
						Season = Season[1]
						Season = Season.split('"')
						Season = Season[0]
						
						Enum = Enum.split('index="')
						Enum = Enum[1]
						Enum = Enum.split('"')
						Enum = Enum[0]
						
						Summary = Summary.split('summary="')
						Summary = Summary[1]
						Summary = Summary.split('" index')
						Summary = Summary[0]
						Summary = Summary.replace(",", "")
						Summary = Summary.replace('\xe2',"")
						Summary = Summary.replace("&quot","")
						try:
							Summary = Summary.decode("ascii", "ignore")
						except Exception:
							pass
						#Summary = remove_accents(Summary)
						
						
						Link = Link.split('<Part id=')
						Link = Link[1]
						Link = Link.split('key="')
						Link = Link[1]
						Link = Link.split('" duration')
						Link = Link[0]
						
						TShow = str(TShow)
						#TShow = TShow.replace("'","''")
						#print (TShow)
						Episode = str(Episode)
						Episode = Episode.replace("'","''")
						#print (Episode)
						Season = int(Season)
						#print (str(Season))
						Enum = int(Enum)
						#print (str(Enum))
						Tnum = int(Tnum)
						#print (str(Tnum))
						Summary = str(Summary.encode('ascii','ignore').strip())
						Summary = Summary.replace("'","''")
						#print (Summary)
						Link = str(Link.strip().encode('ascii','replace'))
						#print (Link)

						cur.execute("SELECT * FROM shows WHERE TShow LIKE \"" + TShow + "\" AND Tnum LIKE \"" + str(Tnum) + "\"")
						try:
							if not cur.fetchone():
								cur.execute("INSERT INTO shows VALUES(?, ?, ?, ?, ?, ?, ?)", (TShow, Episode, Season, Enum, Tnum, Summary, Link))
								sql.commit()
								print ("New Episode Found: " + TShow + " Episode: " + Episode)
						except Exception: 
							print ("Error adding " + TShow)
							with open(PROBLEMS, 'a') as file:
								file.write(TShow + " " + Episode + "\n")
							file.close()
	
		counter = counter + 1

	print ("TV entries checked.")


try:
	print (str(sys.argv))
	print (str(sys.argv[1]))
	findme = str(sys.argv[1])
	getshow(findme)
	gettvshows(findme)

except IndexError:
	print ("Error: You must specify a show to use this command.")		
print ("Done")
