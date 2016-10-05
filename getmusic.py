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

MYDB = homedir + "myplex.db"
http = urllib3.PoolManager()

sql = sqlite3.connect(MYDB)
cur = sql.cursor()

cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERIP\'')
PLEXSERVERIP = cur.fetchone()
PLEXSERVERIP = PLEXSERVERIP[0]

cur.execute('SELECT setting FROM settings WHERE item LIKE \'PLEXSERVERPORT\'')
PLEXSERVERPORT = cur.fetchone()
PLEXSERVERPORT = PLEXSERVERPORT[0]

ostype = platform.system()

METADATA = "http://" + PLEXSERVERIP + ":" + PLEXSERVERPORT

command = 'SELECT setting FROM settings WHERE item LIKE \'MUSICGET\''
cur.execute(command)
if not cur.fetchone():
	getsections()
	print ("\nEnter the link to your TV show tree.\nExample: http://" + PLEXSERVERIP + ":" + PLEXSERVERPORT + "/library/sections/1/all/ \n")
	MUSICGET = str(input('Link:'))
	cur.execute('INSERT INTO settings VALUES(?, ?)', ("MUSICGET",MUSICGET.strip()))
	sql.commit()
	print (MUSICGET + " has been added to the settings table. Moving on.")
else:
	cur.execute(command)
	test1 = cur.fetchone()[0]
	MUSICGET = test1

cur.execute('CREATE TABLE IF NOT EXISTS MusicArtists(artist TEXT, Summary TEXT, Genre TEXT)')
sql.commit()
cur.execute('CREATE TABLE IF NOT EXISTS MusicAlbums(album TEXT, title TEXT, track INT)')
sql.commit()


def getartists():	
	response = http.urlopen('GET', MUSICGET, preload_content=False).read()
	response = str(response)
	#print (response)
	artists = response.split('<Track ratingKey=')
	counter = 0

	while counter <= int(len(shows)-1):
		artist = artists[counter]
		summary = artist
		genre = artist
		key = artist
		
		artist = artist.split("title=\"")
		artist = artist[1].strip()
		artist = artist.split("\"")
		artist = artist[0]

		try:
			summary = summary.split("summary=\"")
			summary = summary[1]
			summary = summary.split("\"")
			summary = summary[0]
			summary = summary.replace("'","''")
			summary = str(summary.decode('ascii','ignore')).strip()
		except IndexError:
			summary = "Unavailable"
			
		key = key.split("key=\"")
		key = key[1]
		key = key.split("\"")
		key = key[0]
		
		try:
			genre = genre.split("\">")
			genre = genre[1]
			genre = genre.split("tag=\"")
			genres = []
			for item in genre:
				item = item.replace("\"/>").strip()
				genres.append(item)
			gres = ""
			for thing in genres:
				gres = gres + thing + " "
		except IndexError:
			gres = "None"
		
		cur.execute("SELECT * FROM MusicArtists WHERE artist LIKE \"" + artist + "\"")
		try:
			if not cur.fetchone():
				cur.execute("INSERT INTO MusicArtists VALUES(?, ?, ?)", (artist, summary, genre))
				sql.commit()
				META1 = METADATA + key
				resp1 = http.urlopen('GET', META1, preload_content=False).read()
				resp1 = str(resp1)
				albums = albums.split("Directory ratingKey=")
				for album in albums:
					akey = album
					aname = album
					
					aname = aname.split("title=\"")
					aname = aname[1]
					aname = aname.split("\"")
					aname = aname[0]
					
					akey = akey.split("key=\"")
					akey = akey[1]
					akey = akey.split("\"")
					akey = akey[0]
					
					META2 = METADATA + akey
					resp2 = http.urlopen('GET', META2, preload_content=False).read()
					resp2 = str(resp2)
					xtitle = resp2.split("title=\"")
					tnum = 1
					for title in xtitle:
						title = title.split("\"")
						title = title[0]
						cur.execute("SELECT * FROM MusicAlbums WHERE album LIKE \"" + anme + " and WHERE title LIKE \"" + title + "\"")
						if not cur.fetchone():
							cur.execute("INSERT INTO MusicAlbums VALUES (?,?,?)", (aname, title, tnum))
							sql.commit()
						tnum = tnum + 1
								
		except Exception: 
			print ("Error adding " + artist)
			
		counter = counter + 1

	
	print ("Music entries checked.")

getartists()

