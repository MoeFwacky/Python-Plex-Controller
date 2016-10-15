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
global pcount

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
	getsections()
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
	getsections()
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

def progress(num):
	num = int(num)
	global pcount
	try:
		pcount
	except NameError:
		pcount = 0
	pcount = pcount + 1
	perc = round((float(pcount) / float(num)) * 100, 1)
	sys.stdout.write("\r" + str(perc) + "%")
	sys.stdout.flush()

def clearprogress():
	global pcount
	pcount = 0

def getsections():
	cur.execute("SELECT setting FROM settings WHERE item LIKE \"SERVERIP\"")
	wlink = cur.fetchone()[0]
	cur.execute("SELECT setting FROM settings WHERE item LIKE \"SERVERPORT\"")
	wip = cur.fetchone()[0]
	slink = "http://" + wlink + ":" + wip + "/library/sections/"
	response = http.urlopen('GET', slink, preload_content=False).read()
        response = str(response)
	response = response.split("Directory allowSync=")
	print ("The Following Sections are available off your server.")
	for item in response:
		name = item
		section = item
		try:
			name = name.split("title=\"")
			name = name[1]
			name = name.split("\"")
			name = name[0]

			section = section.split("key=\"")
			section = section[1]
			section = section.split("\"")
			section = section[0]

			link = "http://" + wlink + ":" + wip + "/library/" + section + "/all/"
			print ("Name: " + name + "\nSection: " + section + "\nLink: " + link)
		except IndexError:
			pass
def getshows():	
	print ("Getting TVshowlist now.")
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	shows = response.split('<Directory ratingKey=')
	counter = 1
	xnum = int(len(shows))-1

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
		title = title.replace("&#39;","'")
		
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
		except IndexError:
			genre2 = "none"
		try:
			genre3 = genres[3]
			genre3 = genre3.split('" />')
			genre3 = genre3[0]
		except IndexError:
			genre3 = "none"
		genre = genre.split('" />')
		
		genre = genre[0] + ";" + genre2 + ";" + genre3 + ";"
		genre = genre.replace('none;','')
		
			
			
		studio = studio.split("studio=\"")
		try:
			studio = studio[1]
			studio = studio.split("\"")
			studio = studio[0]
		except IndexError:
			studio = "None"
		TShow = TShow.replace("'","''")
		summary = summary.replace("&#39;","'")
		summary = summary.replace("'","''")
		summary = str(summary.decode('ascii','ignore')).strip()
		cur.execute("SELECT * FROM TVshowlist WHERE TShow LIKE \"" + TShow + "\"")
		try:
			if not cur.fetchone():
				cur.execute("INSERT INTO TVshowlist VALUES(?, ?, ?, ?, ?, ?)", (TShow, summary, genre, rating, int(duration), int(totalnum)))
				sql.commit()
				#marker
				progress(xnum)
		except IndexError: 
			print ("\nError adding " + TShow)
			with open(PROBLEMS, 'a') as file:
				file.write(TShow + "\n")
			file.close()
				
		
		counter = counter + 1

	clearprogress()	
	print ("\n\nTV Show List Generated.")


def fixTVfiles():

	if "Windows" in ostype:
		PLdir = homedir + "Genre\\TV\\"
	else:
		PLdir = homedir + "/Genre/TV/"

	from os import listdir
	from os.path import isfile, join
	
	showlist = [f for f in listdir(PLdir) if isfile(join(PLdir, f))]
	say = showlist
	for item in say:
		WorkingDir = PLdir + item
		with open(WorkingDir, 'r') as file:
			startfile = file.read()
		file.close()
		startfile = startfile.rstrip()
		with open(WorkingDir, 'w') as file:
			file.write(startfile)
		file.close()

	print ("Part 1 done. Moving on.")
	if "Windows" in ostype:
		PLdir = homedir + "\\Studio\\"
	else:
		PLdir = homedir + "/Studio/" 

	showlist = [f for f in listdir(PLdir) if isfile(join(PLdir, f))]
	say = showlist
	for item in say:
		WorkingDir = PLdir + item
		with open(WorkingDir, 'r') as file:
			startfile = file.read()
		file.close()
		startfile = startfile.rstrip()
		with open(WorkingDir, 'w') as file:
			file.write(startfile)
		file.close()
	print ("\nTV Files Cleaned")

def getshow(show):
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	shows = response.split('<Directory ratingKey=')
	counter = 1

	workingdir = homedir + "tvshowlist.txt"

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

		try:
			with open(workingdir, 'a') as file:
				file.write(title)
				file.write("\n")
			file.close()
		except FileNotFoundError:
			with open(workingdir, 'w+') as file:
				file.write(title)
				file.write("\n")
			file.close()


		name = title
		TShow = name
		if (("'" in TShow) and ("''" not in TShow)):
			TShow = TShow.replace("'","''")
		title = title + '.txt.'
		title = homedir + title

	genres = genres.split("<Genre tag=\"")
	try:
			genre = genres[1]
	except IndexError:
			genre = "none"
	try:
			genre2 = genres[2]
			genre2 = genre2.split('" />')
			genre2 = genre2[0]
	except IndexError:
			genre2 = "none"
	try:
			genre3 = genres[3]
			genre3 = genre3.split('" />')
			genre3 = genre3[0]
	except IndexError:
			genre3 = "none"
	genre = genre.split('" />')

	genre = genre[0]


	if (genre != "none"):
		if "Windows" in ostype:
			path = homedir + "\\Genre\\TV\\" + str(genre) + ".txt"
		else:
			path = homedir + "Genre/TV/" + str(genre) + ".txt"
		try:
			with open(path, 'a') as file:
				file.write(TShow)
				file.write("\n")
			file.close()
		except FileNotFoundError:
			with open(path, 'w') as file:
				file.write(TShow)
				file.write("\n")
			file.close()
		if "none" != genre2:
			if "Windows" in ostype:
				path = homedir + "\\Genre\\TV\\" + str(genre2) + ".txt"
			else:
				path = homedir + "Genre/TV/" + str(genre2) + ".txt"
			
			try:
				with open(path, 'a') as file:
					file.write(TShow)
					file.write("\n")
				file.close()
			except FileNotFoundError:
				print (genre2 + " created!")
	with open(path, 'w+') as file:
		file.write(TShow)
		file.write("\n")
	file.close()
	if "none" != genre3:
		if "Windows" in ostype:
			path = homedir + "\\Genre\\TV\\" + str(genre3) + ".txt"
		else:
			path = homedir + "Genre/TV/" + str(genre3) + ".txt"
		try:
			with open(path, 'a') as file:
				file.write(TShow)
				file.write("\n")
			file.close()
		except FileNotFoundError:
			print (genre3 + " created!")
			with open(path, 'w+') as file:
				file.write(TShow)
				file.write("\n")
			file.close()

	studio = studio.split("studio=\"")
	try:
		studio = studio[1]
		studio = studio.split("\"")
		studio = studio[0]
		path = homedir + "/Studio/" + str(studio) + ".txt"
		try:
			with open(path, 'a') as file:
				file.write(TShow)
				file.write("\n")
			file.close()
		except FileNotFoundError:
			print ("Studio File Created")
			with open(path, 'w+') as file:
				file.write(TShow)
				file.write("\n")
			file.close()
	except IndexError:
		print (\n"No Studio Available. Skipping " + TShow)

	show = show.split('" key')
	show = show[0]
	show = show.replace("\"", "")
	show = show.rstrip()
	episode = show

	link = TVPART + show + "/allLeaves"

	xresponse = http.urlopen('GET', link, preload_content=False).read()
	xresponse = str(xresponse)

	episodes = xresponse.split('type="episode" title="')
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
		episode = episode.replace("&#39;","'")
		Episode = episode.strip()
		if ("<?xml version=" in episode.strip()):
			Tnum = 0
		else:

			if ("(" in episode):
				xepisode = name + " " + episode
				with open(FIXME, 'a') as file:
					file.write(xepisode)
				file.close()
			if episode != "Original":
				try:
					Tnum = Tnum + 1
				except Exception:
					Tnum = 0
				Season = Season.split('parentIndex="')

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
				Summary = Summary.replace("&#39;","'")
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
				TShow = TShow.replace("&#39;","''")
				Episode = str(Episode)
				Episode = Episode.replace("&#39;","''")
				Season = int(Season)
				Enum = int(Enum)
				Tnum = int(Tnum)
				Summary = str(Summary.encode('ascii','ignore').strip())
				Link = str(Link.strip().encode('ascii','replace'))
				try:
					cur.execute('SELECT * FROM shows WHERE TShow LIKE \'' + TShow + '\' AND Tnum LIKE \'' + str(Tnum) + '\'')
					if not cur.fetchone():
						cur.execute('INSERT INTO shows VALUES(?, ?, ?, ?, ?, ?, ?)', (TShow, Episode, Season, Enum, Tnum, Summary, Link))
						sql.commit()
						print ("New Episode Found: " + TShow + " Episode: " + Episode)
				except Exception:
					print ("Error adding " + TShow)
					with open(PROBLEMS, 'a') as file:
						file.write(TShow + " " + Episode + "\n")
					file.close()



			counter = counter + 1

	fixTVfiles()
	print ("TV entries checked.")



	

def gettvshows():	
	print ("Getting TV Show Episodes Now.")
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	shows = response.split('<Directory ratingKey=')
	xnum = int(len(shows))-1
	counter = 1

	workingdir = homedir + "tvshowlist.txt"

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
		
		try:
			with open(workingdir, 'a') as file:
				file.write(title)
				file.write("\n")
			file.close()
		except FileNotFoundError:
			with open(workingdir, 'w+') as file:
				file.write(title)
				file.write("\n")
			file.close()
			
		
		name = title
		TShow = name
		if (("'" in TShow) and ("''" not in TShow)):
			TShow = TShow.replace("'","''")
		title = title + '.txt.'
		title = homedir + title
		
		genres = genres.split("<Genre tag=\"")
		try:
			genre = genres[1]
		except IndexError:
			genre = "none"
		try:
			genre2 = genres[2]
			genre2 = genre2.split('" />')
			genre2 = genre2[0]
		except IndexError:
			genre2 = "none"
		try:
			genre3 = genres[3]
			genre3 = genre3.split('" />')
			genre3 = genre3[0]
		except IndexError:
			genre3 = "none"
		genre = genre.split('" />')
		
		genre = genre[0]
			
		if (genre != "none"):
		
			path = homedir + "Genre/TV/" + str(genre) + ".txt"
			try:
				with open(path, 'a') as file:
					file.write(TShow)
					file.write("\n")
				file.close()
			except FileNotFoundError:
				with open(path, 'w') as file:
					file.write(TShow)
					file.write("\n")
				file.close()
			if "none" != genre2:
				path = homedir + "Genre/TV/" + str(genre2) + ".txt"
				try:
					with open(path, 'a') as file:
						file.write(TShow)
						file.write("\n")
					file.close()
				except FileNotFoundError:
					print (genre2 + " created!")
					with open(path, 'w+') as file:
						file.write(TShow)
						file.write("\n")
					file.close()
			if "none" != genre3:
				path = homedir + "Genre/TV/" + str(genre3) + ".txt"
				try:
					with open(path, 'a') as file:
						file.write(TShow)
						file.write("\n")
					file.close()
				except FileNotFoundError:
					print (genre3 + " created!")
					with open(path, 'w+') as file:
						file.write(TShow)
						file.write("\n")
					file.close()
				
		studio = studio.split("studio=\"")
		try:
			studio = studio[1]
			studio = studio.split("\"")
			studio = studio[0]
			path = homedir + "/Studio/" + str(studio) + ".txt"
			try:
				with open(path, 'a') as file:
					file.write(TShow)
					file.write("\n")
				file.close()
			except FileNotFoundError:
				print ("Studio File Created")
				with open(path, 'w+') as file:
					file.write(TShow)
					file.write("\n")
				file.close()
		except IndexError:
			print ("\nNo Studio Available. Skipping " + TShow)
			
		show = show.split('" key')
		show = show[0]
		show = show.replace("\"", "")
		show = show.rstrip()
		episode = show
		
		link = TVPART + show + "/allLeaves"
		xresponse = http.urlopen('GET', link, preload_content=False).read()
		xresponse = str(xresponse)
		
		episodes = xresponse.split('type="episode" title="')
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
				Tnum = 0
			else:
			
				if ("(" in episode):
					xepisode = name + " " + episode
					with open(FIXME, 'a') as file:
						file.write(xepisode)
					file.close()
				if episode != "Original":
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
					TShow = TShow.replace("&#39;","''")
					Episode = str(Episode)
					Episode = Episode.replace("'","''")
					Episode = Episode.replace("&#39;","''")
					Season = int(Season)
					Enum = int(Enum)
					Tnum = int(Tnum)
					Summary = str(Summary.encode('ascii','ignore').strip())
					Summary = Summary.replace("'","''")
					Summary = Summary.replace("&#39;","''")
					Link = str(Link.strip().encode('ascii','replace'))

					cur.execute("SELECT * FROM shows WHERE TShow LIKE \"" + TShow + "\" AND Tnum LIKE \"" + str(Tnum) + "\"")
					try:
						if not cur.fetchone():
							cur.execute("INSERT INTO shows VALUES(?, ?, ?, ?, ?, ?, ?)", (TShow, Episode, Season, Enum, Tnum, Summary, Link))
							sql.commit()
							#print ("New Episode Found: " + TShow + " Episode: " + Episode)
					except Exception: 
						print ("Error adding " + TShow)
						with open(PROBLEMS, 'a') as file:
							file.write(TShow + " " + Episode + "\n")
						file.close()
					
				
		progress(xnum)	
		counter = counter + 1

	fixTVfiles()
	clearprogress()
	print ("\n\nTV Episode entries checked.")


def fixmvfiles():

	PLdir = homedir + "movielist.txt"
	
	with open(PLdir, 'r') as file:
		startfile = file.read()
	file.close()
	startfile = startfile.rstrip()
	with open(PLdir, 'w') as file:
		file.write(startfile)
	file.close()
	print ("\nMovie File Cleaned. Restoring Genres Now.")
	

def getmovies():
	response = http.urlopen('GET', MOVIEGET, preload_content=False).read()
	response = str(response)
	#print (response)
	shows = response.split('<Video ratingKey=')
	xnum = int(len(shows))-1
	counter = 1
	Moviedir = homedir + "movielist.txt"

	while counter <= int(len(shows)-1):

		show = shows[counter]
		
		genres = show
		studio = show
		director = show
		actors = show
		rating = show
		summary = show
		tagline = show
		
		title = show
		title = title.split('title="')
		title = title[1]
		title = title.split('"')
		title = title[0]
		
		title = title.replace('&apos;','\'')
		title = title.replace('&amp;','&')
		title = title.replace("&#39;","'")
		#title = title.replace('?','')
		#title = title.replace('/',' ')
		
		try:
			with open(Moviedir, 'a') as file:
				file.write(title)
				file.write("\n")
			file.close()
		except FileNotFoundError:
			with open(Moviedir, 'w+') as file:
				file.write(title)
				file.write("\n")
			file.close()
			
		
		name = title
			
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
		
		genre = genre[0]
		bgenre = genre + " " + genre2 + " " + genre3
		#print (genre)
		
		directors = director.split("<Director tag=\"")
		
		try:
			director = directors[1]
		except IndexError:
			director = "none"
		try:
			director2 = directors[2]
			director2 = director2.split('" />')
			director2 = director2[0]
			
		except IndexError:
			director2 = "none"
		try:
			director3 = directors[3]
			director3 = director3.split('" />')
			director3 = director3[0]
			
		except IndexError:
			director3 = "none"
		director = director.split('" />')
		director = director[0]
		directors = director + " " + director2 + " " + director3
		directors = directors.replace("none", "")
		#print (directors)
		
		actorss = actors.split("<Role tag=\"")
		
		try:
			actors = actorss[1]
		except IndexError:
			actors = "none"
		try:
			actors2 = actorss[2]
			actors2 = actors2.split('" />')
			actors2 = actors2[0]
			
		except IndexError:
			actors2 = "none"
		try:
			actors3 = actorss[3]
			actors3 = actors3.split('" />')
			actors3 = actors3[0]
			
		except IndexError:
			actors3 = "none"
		actors = actors.split('" />')
		actors = actors[0]
		bactors = actors + " " + actors2 + " " + actors3
		bactors = bactors.replace("none", "")
		
		rating = rating.split("contentRating=\"")
		try:
			rating = rating[1]
			rating = rating.split("\"")
			rating = rating[0]
		except IndexError:
			#print ("No Rating Available. Skipping " + name)
			rating = "none"
		
		tagline = tagline.split("tagline=\"")
		try:
			tagline = tagline[1]
			tagline = tagline.split("\" ")
			tagline = tagline[0]
		except IndexError:
			#print ("No Tagline Available. Skipping " + name)
			tagline = "none"
			
		summary = summary.split("summary=\"")
		try:
			summary = summary[1]
			summary = summary.split("\"")
			summary = summary[0]
		except IndexError:
			#print ("No Summary Available. Skipping " + name)
			summary = "none"

		#marker
				
			
		summary = summary.replace('&apos;','\'')
		summary = summary.replace('&amp;','&')
		summary = summary.replace("&#39;","'")
		summary = summary.replace(',', ' ')	
		summary = summary.replace('\'','')
		try:
			summary = summary.decode("ascii", "ignore")
		except Exception:
			pass
		name = name.replace('&apos;','\'')
		name = name.replace('&amp;','&')
		name = name.replace(',', ' ')
		name = name.replace("'","''")
		#tagline = tagline.replace('&apos;','\'')
		tagline = tagline.replace('&apos;','')
		tagline = tagline.replace('&amp;','&')
		tagline = tagline.replace(',', ' ')
		tagline = tagline.replace('\'','')
		try:
			tagline = tagline.decode("ascii", "ignore")
		except Exception:
			pass
		#directors = directors.replace('&apos;','\'')
		directors = directors.replace('&apos;','')
		directors = directors.replace('&amp;','&')
		directors = directors.replace(',', ' ')
		directors = directors.replace('\'','')
		try:
			directors = directors.decode("ascii", "ignore")
		except Exception:
			pass
		#bgenre = bgenre.replace('&apos;','\'')
		bgenre = bgenre.replace('&apos;','')
		bgenre = bgenre.replace('&amp;','&')
		bgenre = bgenre.replace(',', ' ')
		bgenre = bgenre.replace("none", "")
		#bactors = bactors.replace('&apos;','\'')
		bactors = bactors.replace('&apos;','')
		bactors = bactors.replace('\'','')
		bactors = bactors.replace('&amp;','&')
		bactors = bactors.replace(',', ' ')
		try:
			bactors = bactors.decode("ascii", "ignore")
		except Exception:
			pass
		
		try:
			cur.execute('SELECT * FROM Movies WHERE Movie LIKE \'' + name + '\'')
			if not cur.fetchone():
				cur.execute('INSERT INTO Movies VALUES(?, ?, ?, ?, ?, ?, ?)', (name, summary, rating, tagline, bgenre, directors, bactors))
				sql.commit()
		except Exception:
			print ("\nError adding " + name)
			with open(PROBLEMS, 'a') as file:
				file.write(name.decode("ascii", "ignore") + " " + bactors + "\n")
			file.close()
		progress(xnum)
		counter = counter + 1
	clearprogress()
	fixmvfiles()

def getcommercials():
	cur.execute("CREATE TABLE IF NOT EXISTS commercials(name TEXT, duration INT)")
	sql.commit()
	command = "SELECT setting FROM settings WHERE item LIKE \"COMPART\""
	cur.execute(command)
	if not cur.fetchone():
		getsection()
		print ("You need to supply the link to find your commercials.\nExample: http://192.168.1.134:32400/library/metadata/\n")
		COMPART = str(input('Link:'))
		cur.execute("INSERT INTO settings VALUES(?,?)", ("COMPART",COMPART.strip()))
		sql.commit()
		print (COMPART + " has been added to the settings table. Moving on.")
	else:
		cur.execute(command)
		COMPART = cur.fetchone()[0]

	cur.execute("DELETE FROM commercials")
	sql.commit()
	
	response = http.urlopen('GET', COMPART, preload_content=False).read()
	response = str(response)
	commercials = response.split("<Video ratingKey=")
	counter = 1

	while counter <= int(len(commercials)-1):
		comc = commercials[counter]
		duration = comc

		comc = comc.split("title=\"")
		comc = comc[1]
		comc = comc.split("\"")
		comc = comc[0].strip()

		duration = duration.split("duration=\"")
		duration = duration[1]
		duration = duration.split("\"")
		duration = duration[0].strip()
		duration = int(duration)/1000
		cur.execute("SELECT * FROM commercials WHERE name LIKE \"" + comc + "\"")
		if not cur.fetchone():
			cur.execute("INSERT INTO commercials VALUES (?,?)", (comc, duration))
			sql.commit()
			#print ("New Commercial Found: " + comc)
		counter = counter + 1
	
	print ("Done")

def getprerolls():
        cur.execute("CREATE TABLE IF NOT EXISTS prerolls(name TEXT, duration INT)")
        sql.commit()
        command = "SELECT setting FROM settings WHERE item LIKE \"PREROLLPART\""
        cur.execute(command)
        if not cur.fetchone():
		getsections()
                print ("You need to supply the link to find your prerolls.\nExample: http://192.168.1.134:32400/library/metadata/\n")
                PREROLLPART = str(input('Link:'))
                cur.execute("INSERT INTO settings VALUES(?,?)", ("PREROLLPART",PREROLLPART.strip()))
                sql.commit()
                print (PREROLLPART + " has been added to the settings table. Moving on.")
        else:
                cur.execute(command)
                PREROLLPART = cur.fetchone()[0]

	cur.execute("DELETE FROM prerolls")
	sql.commit()

        response = http.urlopen('GET', PREROLLPART, preload_content=False).read()
        response = str(response)
        commercials = response.split("<Video ratingKey=")
        counter = 1

        while counter <= int(len(commercials)-1):
                comc = commercials[counter]
                duration = comc

                comc = comc.split("title=\"")
                comc = comc[1]
                comc = comc.split("\"")
                comc = comc[0].strip()

                duration = duration.split("duration=\"")
                duration = duration[1]
                duration = duration.split("\"")
                duration = duration[0].strip()
                duration = int(duration)/1000
                cur.execute("SELECT * FROM prerolls WHERE name LIKE \"" + comc + "\"")
                if not cur.fetchone():
                        cur.execute("INSERT INTO prerolls VALUES (?,?)", (comc, duration))
                        sql.commit()
                        #print ("New preroll Found: " + comc)
                counter = counter + 1

        print ("Done")

def getcustomsection(name):
	sname = "CUSTOM_" + name.lower().strip()
	command = "CREATE TABLE IF NOT EXISTS "+ sname + "(name TEXT, duration INT, type TEXT)"
	cur.execute(command)
        sql.commit()
        command = "SELECT setting FROM settings WHERE item LIKE \"" + sname + "\""
        cur.execute(command)
        if not cur.fetchone():
		getsections()
                print ("You need to supply the link to find your " + name.strip() + " section.\nExample: http://192.168.1.134:32400/library/sections/9/all/\n")
                PREROLLPART = str(input('Link:'))
                cur.execute("INSERT INTO settings VALUES(?,?)", (sname,PREROLLPART.strip()))
                sql.commit()
                print (PREROLLPART + " has been added to the settings table. Moving on.")
        else:
                cur.execute(command)
                PREROLLPART = cur.fetchone()[0]

        cur.execute("DELETE FROM " + sname)
        sql.commit()

        response = http.urlopen('GET', PREROLLPART, preload_content=False).read()
        response = str(response)
	type = response
	type = type.split("librarySectionTitle=\"")
	type = type[1]
	type = type.split("\"")
	type = type[0].strip()
	
        commercials = response.split("<Video ratingKey=")
        counter = 1

        while counter <= int(len(commercials)-1):
                comc = commercials[counter]
                duration = comc

                comc = comc.split("title=\"")
                comc = comc[1]
                comc = comc.split("\"")
                comc = comc[0].strip().strip()
		comc = comc.replace("&#39;","''")
		comc = comc.replace("&amp;","&")

                duration = duration.split("duration=\"")
                duration = duration[1]
                duration = duration.split("\"")
                duration = duration[0].strip()
                duration = int(duration)/1000
		
                cur.execute("SELECT * FROM " + sname + " WHERE name LIKE \"" + comc + "\"")
                if not cur.fetchone():
                        cur.execute("INSERT INTO " + sname + " VALUES (?,?,?)", (comc, duration, type))
                        sql.commit()
                        #print ("New " + sname + " Found: " + comc)
                counter = counter + 1

        print ("Done")

def startupactiontv():
	cur.execute("DELETE FROM TVshowlist")
	sql.commit()
	cur.execute("DELETE FROM shows")
	sql.commit()
	print ("TV Tables purged and ready for data.")

def startupactionmovie():
	cur.execute("DELETE FROM Movies")
	sql.commit()
        print ("Movie Tables purged and ready for data.")

def getfavorites():
	global favtv
	global favmve
	cur.execute("SELECT Movie FROM Movies WHERE Genre LIKE \"%favorite%\"")
	mlist = cur.fetchall()
	for mve in mlist:
		mve = mve[0]
		if mve.strip() not in favmve:
			favmve.append(mve)

	cur.execute("SELECT TShow FROM TVshowlist WHERE Genre LIKE \"%favorite%\"")
	tvlist = cur.fetchall()
	for item in tvlist:
		item = item[0]
		if item not in favtv:
			favtv.append(item)

	print ("Favorites Acquired. Moving On.")

def restorefavorites():
	global favtv
        global favmve
	cmdtv = "python ./system.py addfavoriteshow "
	cmdmv = "python ./system.py addfavoritemovie "
	
	for show in favtv:
		command = cmdtv + "\"" + show.strip() + "\""
		os.system(command)
	
	for movie in favmve:
		command = cmdmv + "\"" + movie.strip() + "\""
		os.system(command)

	print ("Favorites Restored.")

def getgenrestv():
	global tvgenres
	command = "SELECT Genre FROM TVshowlist ORDER BY Genre ASC"
        cur.execute(command)
        fgenres = cur.fetchall()
        xshowlist = []
        for genres in fgenres:
                genre = genres[0].split(";")
                for xgen in genre:
                        if xgen not in xshowlist:
                                xshowlist.append(xgen)
	for genre in xshowlist:
		genre = genre.strip()
		command = "SELECT TShow from TVshowlist where Genre LIKE \"%" + genre + "%\""
		cur.execute(command)
		shows = cur.fetchall()
		for show in shows:
			show = show[0]

			try:
				writeme = writeme + "," + show
			except NameError:
				writeme = genre + ":" + show
		tvgenres.append(writeme)
		del writeme
	print ("TV Genres Saved.")

def getgenresmovie():
	global moviegenres
	command = "SELECT Genre FROM Movies ORDER BY Genre ASC"
	cur.execute(command)
	fgenres = cur.fetchall()
	xmovies = []
	for genres in fgenres:
		genre = genres[0].split(" ")
		for xgen in genre:
			if ((xgen not in xmovies) and (xgen != "")):
				xmovies.append(xgen)
	for genre in xmovies:
		if genre == " ":
			pass
		else:
			genre = genre.strip()
			command = "SELECT Movie FROM Movies WHERE Genre LIKE \"%" + genre + "%\""
			cur.execute(command)
			movies = cur.fetchall()
			for movie in movies:
				movie = movie[0]
				try:
					writeme = writeme + "," + movie
				except NameError:
					writeme = genre + ":" + movie
				moviegenres.append(writeme)
				del writeme
	print ("Movie Genres Saved.")
	
def restoregenrestv():
	global tvgenres
	xnum = int(len(tvgenres))-1
	for genre in tvgenres:
		genre = genre.split(":")
		shows = genre[1]
		genre = genre[0]
		shows = shows.split(",")
		for show in shows:
			show = show.strip()
			say = addgenreshow(show,genre)
		progress(xnum)
	clearprogress()
	print ("TV Genres Restored.")

def restoregenremovies():
	global moviegenres
	xnum = int(len(moviegenres))-1
	for gre in moviegenres:
		if gre == " ":
			pass
		else:
			gre = gre.split(":")
			shows = gre[1]
			genre = gre[0]
			shows = shows.split(",")
			for show in shows:
				show = show.strip()
				say = addgenremovie(show, genre)
		progress(xnum)
	clearprogress()
        print ("\nMovie Genres Restored.")

def addgenreshow(show, genre):
        command = 'SELECT * FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
        cur.execute(command)
        if not cur.fetchone():
                return ("Error: " + show + " not found. Check title and try again.")
        cur.execute(command)
        stuff = cur.fetchone()
        TShow = stuff[0]
        summary = stuff[1]
        try:
                genres = stuff[2]
        except Exception:
                genres = ""
        rating = stuff[3]
        duration = stuff[4]
        totalnum = stuff[5]
        if genre.lower() in genres.lower():
                return("Error: " + genre + " is already associated with the show " + show)
        genres = genres + " " + genre
        command = 'DELETE FROM TVshowlist WHERE TShow LIKE \'' + show + '\''
        cur.execute(command)
        sql.commit()
        cur.execute('INSERT INTO TVshowlist VALUES(?,?,?,?,?,?)',(TShow, summary, genres, rating, int(duration), int(totalnum)))
        sql.commit()
        return (genre + " has been associated with " + show)

def addgenremovie(movie, genre):
        command = 'SELECT * FROM Movies WHERE Movie LIKE \'' + movie + '\''
        cur.execute(command)
        if not cur.fetchone():
		say = "Error restoring genre " + genre + " to movie " + movie
		return ("Error restoring genre " + genre + " to movie " + movie)
        cur.execute(command)
        stuff = cur.fetchone()
        title = stuff[0]
        summary = stuff[1]
        rating = stuff[2]
        tagline = stuff[3]
        genres = stuff[4]
        director = stuff[5]
        actor = stuff[6]
        if genre.lower() in genres.lower():
                return("Error: " + genre + " is already associated with the movie " + movie)
        genres = genres.strip() + " " + genre
        command = 'DELETE FROM Movies WHERE Movie LIKE \'' + movie + '\''
        cur.execute(command)
        sql.commit()
        cur.execute('INSERT INTO Movies VALUES(?,?,?,?,?,?,?)',(title, summary, rating, tagline, genres, director, actor))
        sql.commit()
        return (genre + " successfully associated with the movie " + movie )
	
try:
	if "Windows" not in ostype:
		option = str(sys.argv[1])
	else:
		print ("Notice: For Windows, the update db script may default to 'all' when there is an argument failure.\n")
		option = "all"
	#getsections()
	if ("updatetv" in option):
		getgenrestv()
		startupactiontv()
		getshows()
		gettvshows()
		#getshows()
		restoregenrestv()
	elif ("updatemovies" in option):
		getgenresmovie()
		startupactionmovie()
		getmovies()
		restoregenremovies()
	elif ("all" in option):
		getgenrestv()
		getgenresmovie()
		startupactiontv()
		startupactionmovie()
		gettvshows()
		getshows()
		getmovies()
		restoregenrestv()
		restoregenremovies()
	elif ("getcommercials" in option):
		getcommercials()
		print ("Commercial Get Finished.")
	elif ("getprerolls" in option):
		getprerolls()
		print ("Preroll Get Finished.")
	elif ("getcustomsection" in option):
		try:
			option = str(sys.argv[2])
			getcustomsection(option)
			print ("Get Custom Done.")
		except IndexError:
			print ("Error: You must supply a section name to use this command.")
	elif ("getsections" in option):
		getsections()

except TypeError:
	print ("No option specified. Use 'updatetv' or 'updatemovies' or 'all' to update your db.")		
print ("Done")
