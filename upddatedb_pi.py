homedir = 'c:\\users\\rob\\documents\\hasystem\\'
import urllib3
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
test2 = cur.fetchone()
if not cur.fetchone():
	test2 = ""
try:
	test2 = test2[0]
except IndexError:
	test2 = ""
#print (test2)
#print ("1")
if (test2 == ""):
	print ("Looks like you have never run the update DB script. I need some information to proceed.\n Enter the link to your metadata.\n Example: http://192.168.1.134:32400/library/metadata/\n")
	TVPART = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVPART",TVPART.strip()))
	sql.commit()
	print (TVPART + " has been added to the settings table. Moving on.")
else:
	TVPART = test2

command = 'SELECT setting FROM settings WHERE item LIKE \'TVGET\''
cur.execute(command)
test1 = cur.fetchone()
#print (test1)
if not cur.fetchone():
	test1 = ""
try:
	test1 = test1[0]
except IndexError:
	test1 = ""

if ((test1 == "")):
	print ("Enter the link to your TV show tree.\nExample: http://192.168.1.134:32400/library/sections/1/all/ \n")
	TVGET = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("TVGET",TVGET.strip()))
	sql.commit()
	print (TVGET + " has been added to the settings table. Moving on.")
else:
	TVGET = test1

command = 'SELECT setting FROM settings WHERE item LIKE \'MOVIEGET\''
cur.execute(command)
test = cur.fetchone()
if not cur.fetchone():
	test = ""
try:
	test = test[0]
except IndexError:
	test = ""
if ((test == "")):
	print ("Enter the link to your Movie tree.\nExample: http://192.168.1.134:32400/library/sections/2/all/ \n")
	MOVIEGET = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("MOVIEGET",MOVIEGET.strip()))
	sql.commit()
	print (MOVIEGET + " has been added to the settings table. Moving on.")
else:
	MOVIEGET = test

print ("Database update starting...\n")	

cur.execute('CREATE TABLE IF NOT EXISTS shows(TShow TEXT, Episode TEXT, Season INT, Enum INT, Tnum INT, Summary TEXT, Link TEXT)')
sql.commit()
cur.execute('CREATE TABLE IF NOT EXISTS Movies(Movie TEXT, Summary TEXT, Rating TEXT, Tagline TEXT, Genre TEXT, Director TEXT, Actors TEXT)')
sql.commit()


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
	print ("TV Files Cleaned")

def getshow(show):
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	#print (response)
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
	#print (genre)


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
		print ("No Studio Available. Skipping " + TShow)

	show = show.split('" key')
	show = show[0]
	show = show.replace("\"", "")
	show = show.rstrip()
	episode = show

	link = TVPART + show + "/allLeaves"

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
				#print (TShow)
				Episode = str(Episode)
				#print (Episode)
				Season = int(Season)
				#print (str(Season))
				Enum = int(Enum)
				#print (str(Enum))
				Tnum = int(Tnum)
				#print (str(Tnum))
				Summary = str(Summary.encode('ascii','ignore').strip())
				#print (Summary)
				Link = str(Link.strip().encode('ascii','replace'))
				#print (Link)

				if ("'" in TShow):
					TShow = TShow.replace("'","\'")
					print (TShow)
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
	response = http.urlopen('GET', TVGET, preload_content=False).read()
	response = str(response)
	#print (response)
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
		#print (genre)
		
			
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
			print ("No Studio Available. Skipping " + TShow)
			
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
					#print (TShow)
					Episode = str(Episode)
					#print (Episode)
					Season = int(Season)
					#print (str(Season))
					Enum = int(Enum)
					#print (str(Enum))
					Tnum = int(Tnum)
					#print (str(Tnum))
					Summary = str(Summary.encode('ascii','ignore').strip())
					#print (Summary)
					Link = str(Link.strip().encode('ascii','replace'))
					#print (Link)

					if ("'" in TShow):
						TShow = TShow.replace("'","\'")
						print (TShow)
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


def fixmvfiles():

	PLdir = homedir + "movielist.txt"
	
	with open(PLdir, 'r') as file:
		startfile = file.read()
	file.close()
	startfile = startfile.rstrip()
	with open(PLdir, 'w') as file:
		file.write(startfile)
	file.close()
	print ("Movie File Cleaned")
	
#mark

def getmovies():
	response = http.urlopen('GET', MOVIEGET, preload_content=False).read()
	response = str(response)
	#print (response)
	shows = response.split('<Video ratingKey=')
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
			print ("No Rating Available. Skipping " + name)
			rating = "none"
		
		tagline = tagline.split("tagline=\"")
		try:
			tagline = tagline[1]
			tagline = tagline.split("\" ")
			tagline = tagline[0]
		except IndexError:
			print ("No Tagline Available. Skipping " + name)
			tagline = "none"
			
		summary = summary.split("summary=\"")
		try:
			summary = summary[1]
			summary = summary.split("\"")
			summary = summary[0]
		except IndexError:
			print ("No Summary Available. Skipping " + name)
			summary = "none"

		#marker
				
			
		summary = summary.replace('&apos;','\'')
		summary = summary.replace('&amp;','&')
		summary = summary.replace(',', ' ')	
		summary = summary.replace('\'','')
		try:
			summary = summary.decode("ascii", "ignore")
		except Exception:
			pass
		name = name.replace('&apos;','\'')
		name = name.replace('&amp;','&')
		name = name.replace(',', ' ')
		#print (tagline)
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
		#print (name + "  " + summary + "  " + rating + "  " + tagline + "  " + bgenre + "  " + directors + "  " + bactors)
		
		try:
			cur.execute('SELECT * FROM Movies WHERE Movie LIKE \'' + name + '\'')
			if not cur.fetchone():
				cur.execute('INSERT INTO Movies VALUES(?, ?, ?, ?, ?, ?, ?)', (name, summary, rating, tagline, bgenre, directors, bactors))
				sql.commit()
				print ("New movie found and added to the DB.")
		except Exception:
			print ("Error adding " + name)
			with open(PROBLEMS, 'a') as file:
				file.write(name.decode("ascii", "ignore") + " " + bactors + "\n")
			file.close()
		counter = counter + 1

	fixmvfiles()

try:
	if "Windows" not in ostype:
		option = str(sys.argv[1])
	else:
		print ("Notice: For Windows, the update db script may default to 'all' when there is an argument failure.\n")
		option = "all"
	if ("updatetv" in option):
		gettvshows()
	elif ("updatemovies" in option):
		getmovies()
	elif ("all" in option):
		gettvshows()
		getmovies()

except IndexError:
	print ("No option specified. Use 'updatetv' or 'updatemovies' or 'all' to update your db.")		
print ("Done")	
		

