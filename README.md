##TheBaconNation Plex Controller##

* [The demo setup video.](https://youtu.be/YMEXIZOcpDM)
* [A link to a demo of the controller in action.](https://youtu.be/HRJbNHRQO6I)
* [How To Create a Block Package.](https://youtu.be/a5lOLjzunMQ)
* [Our Homepage.](http://thebaconnation.com)
* [The Beginnings of a bad web ui.](https://youtu.be/u0ur4koeDFM)
* [How to use replaceshowinblock feature.](https://youtu.be/oMDl-6GRK30)

* [The TBN-Plex Discord Channel.](https://discordapp.com/channels/206249843209797632/206249843209797632)

TheBaconNation Plex Controller Help Document

##Important Note:##
Since server version 1.1.4xxx you will need to add the ip or subnect for your TBN-Plex controller device to the autorized IP list in your Plex Server Settings. Look for "allowed without authorization." If not added you may run into issues updating your TBN-Plex DB.

##Before You Begin:##
The following librarys are needed:
The python plex api. User "pip install plexapi"

The following library is optional:
enchant. You can use "pip install pyenchant" to get it. Spell checking will be turned back on in a future update. When that happens, if you do not have this library you will be warned. 

###How To Install:###
Get the most recent version of the system_setup.py file. Place it in your home directory and run it as your preferred user.
Example:
curl "https://raw.githubusercontent.com/amazingr4b/TBN-Plex/master/system_setup.py" -o "system_setup.py"
python system_setup.py

##Update Note:##
The easiest way to update is remove all files in your HA system directory except your myplex.db file, as well as any other backup files you want to retain. Rerun system_setup.py. If a more recent setup file is available, get that first. 
Note: When running system_setup.py, you may be prompted for your server, client, and wild card show again. 

3 scripts are necessary to use the TBN Plex Controller:
* system.py - this is the main script used by the controller.
* upddatedb_pi.py - this is the script used to update the controllers database. 
* system_setup.py - this script creates the necessary files, database, and prompts the user for the information the controller needs to do its job. 

There is one optional script- piplaystate.py. This script uses the API access to check the playback status of the client you are using at a regular interval. When the mode is "On," when a program stopps the system will automatically launch a new progarm, and continue to do so untill it is in eithr "Off" or "Sleep" mode. You will need to add to code to the sleep mode actions to have this action do more than just stop playchecking at the end of a program.

##Other Script Descriptions:##

* piplaystate.py - Gets the playback state from your client.
* playstatus.py - Runs in the background. When enabled uses piplaystate.py to get the status of your client. 
* getshows.py - Updates DB entries for a single specified show.
* tbn_scedule.py - On linux systems, is run once a minute by cron to trigger scheduled TBN-Plex actions.
* add_to_bash.py - On linux systems, updates bash shortcut entries. Note: Needs to be run as sudo, and username specified as an argument.
* add_to_cron.py - On linux systems, updates entries in etc/crontab


##Supported Operating Systems:##
These scripts should theoretically run on any system capable of running python, however, the system_setup.py script only currently supports Linux and Windows based installs. How to do a manual install will be added as a help doc at a later date. 

#Installing TBN Plex:##
To install the TBN Plex Controller, place the system_setup.py script files in your home directory. The system_setup.py script will make a directory in your home folder, "hasystem/", or prompt your for a directory, depending on your OS, which it will store its necessary files and database in.

Install the TBN Plex Controller by running "python system_setup.py" The system setup script will ask you a few questions to get the data it needs to proceed. Once it is ready it will ask you if you want to update your database. Updating the TBN-Plex database is now optional, but recommended. The automated playback options, suggest, moviechoice, and random_movie/tv, etc options will function much better when the TBN-Plex database is updated. 

NOTE: If you enter an incorrect value during setup, which prevents some element from either getting data or working, you can run "python system_setup.py reset" and it will delete the previously stored data and prompt you for it again.  

Regarding Database Updates:
The upddatedb_pi.py script will update your TBN Plex DB. The TBN Plex Controller uses a separate database so you do not need to worry about corrupting your existing Plex Database. 

You can update your database independent of the system_setup.py script by running "python upddatedb_pi.py movie/shows/custom_shows/prerolls/commercials/custom." Larger libraries will take more time to scan versus smaller libraries.
Notes:
* movie - scans your Movie section
* shows - scans your TV Show section
* custom_shows - scans alternate TV Show sections
* prerolls - scans your prerolls section
* commercials - scans your commercials section
* custom. - scans alternate library types, ie- fights, music_videos, comedy. usage ex- "python upddatedb_py.py custom.fights"

For the times when you only need to get entires for a single show a second update script has been added: getshows.py. Usage is as follows: python getshows.py "Name of show here." This script will check your plex server for the specified show, and any new entries are added to the TBN-Plex DB.
Note: does not update existing entires.
2nd note: Is pretty much obsolete now that the scrip automatically updates add entires when found on the server. 

##After Install Notes:##
It is recommended you run "python system.py updatehelp" to populdate you help table with the most recent help entries. 99% of the commands now support the "-h" argument, which will give a description and useage details for the given command. 

Before you can use the block package commands, or block package playback, you first need to create a block package. You can use the "addblock" modifier to create a block package. 

When you run system_setup.py the playmode is set/reset to normal, and your queue is set to " ". It is recommended you do a "whatupnext" after you run the system_setup.py script. From there your queue should never be empty. The controller is designed so something will always be up next. 


##Available Playmodes:##
* normal - plays items from the queue. Will find content when the queue is exhaused.
* block.blockname - plays through the specified block, onces finished reverts to normal mode.
* marathon.show - plays the specified show until user changes mode.
* holiday.usercreatedholiday - plays items from the user created holiday list.
* commercialmode - plays random items from the tbn-plex commercials table unless user plays something else/changes playmode.
* custom.customsectionname - plays items from a custom.table user added using upddateddb.py custom.insertablenamehere. 

###Available Commands:###
If the system_setup.py script succeeded in adding commands to your bash shell, and after you have restarted it, you should be able to use the following commands without having "python system.py " in front of them. If that failed, or if say you do not use the bash shell, you will need to add "python system.py " in front of the following commands. Similarly, if you want to use this script in concert with something like a webserver or voice control agent, you can use "python system.py actionshere" to use any one of the following commands. 

Note- If the option you are giving contains a space(" ") you will need to put quotes ("" or '') around that option.

2nd Note- Commands that return a list of items, like "findmovie," support the "-l" argument. When not included, if more than 30 items are retuned you get a column list of 30 items with longer titles shortened. When more than 30 items are returned and the "-l" argument is included, you will get the list in 10s, with no titles shortened.

##Command Syntax:##
Command (options, if any, don't use the parenthesis)/ Example Usage / Description

* playme (tvshow/movie) / playme "The Big Bang Theory" OR playme "movie.The Matrix" / plays the next episode from the specified show or the specified movie.
* addfavoritemovie / addfavoritemovie "The Matrix" / adds the specified movie to the favorites list.
* addfavoriteshow / addfavoriteshow "Marvels Daredevil" / adds the specified show to the favorites list.
* addgenreshow / addgenreshow "Good Eats" "Cooking" / adds a custom genre to the specified shows genre list.
* addgenremovie / addgenremovie "Deadpool" "Not Super Hero" / adds a custom genre to the specified movies genre list.
* queueadd / queueadd psych OR queuadd "movie.The Matrix" / adds the specified item to the end of the queue.
* whereat / whereat / Lists where you are at in the current feature. *relies on optional scripts
* idtonightsmovie / idtonightsmovie / if your block package contains a random movie option, this should list that movie.
* idtonightsshow / idtonightsshow / if your block package contains a random show option, this should list that show.
* getnewblock / getnewblock / if you are playing a random movie or show block, this command will generate a new block.
* listclients / listclients / lists the available clients.
* changeclient / changeclient / gives option to select a new client from the list of available clients.
* findnewmovie / findnewmovie / if your block contains a random movie, and you want to find a different random movie, this command replaces that movie with a different one.
* randommovieblock (genre) / randommovieblock Action / gets and creates a 3 movie block using the genre specified
* randomtvblock (genre) / randomtvblock Action / gets and creates a 3 show block using the genre specified
* stopplayback / stopplayback / stops the current playaying feature
* pauseplayback / pauseplayback / stops the current playing feature
* playcheckstart / playcheckstart / starts the play checking for automatic playback *relies on optional scripts
* playcheckstop / playcheckstop / stops the play checking for automatic playback *relies on optional scripts
* playchecksleep / playckecksleep /stops playchecking when the current playing feature ends. useful if you add custom actions to shut things off. *relies on optional scripts
* queueshow / queueshow / shows what is in your queue
* queueremove (item in queue) / queueremove "Deadwood" / removes the specified item from the queue.
* queuefix / queuefix / if for somereason your queue gets messed up this command can be used to kill and rebuild it(does not preseve queue.)
* whatupnext / whatupnext / lists the next item in your queue. returns single item.
* setupnext / setupnext "movie.Predator" / sets the next up item in your queue to be the specified item.
* startnextprogram / startnextprogram / starts the next item from your queue
* skipthat / skipthat / skips the next item in your queue
* seriesskipahead (show) / seriesskipahead Psych / Sets the specified shows playqueue ahead one episode.
* seriesskipback (show) / seriesskipback psych / Sets the specified shows playqueue back one episode.
* skipahead / skipahead / skips ahead 30 seconds in the current feature.
* skipback / skipback / skipts back 15 seconds in the current feature.
* findsomethingelse / findsomethingelse / replaces the next item in your queue with something else
* suggestmovie (genre/rating./actor./) / suggestmovie Action / Suggests a random movie. If genre given movie is of that genre.
* suggesttv (genre/rating./duration.) / suggesttv Action / Suggests a random TV show. If genre given, show is of that genre. 
* addsuggestion / addsuggestion / adds the previously suggested media to the queue, if something was previously suggested. 
* whatispending / whatispending / lists what has previously been suggested but not added to the queue. 
* availableblocks / availableblocks / lists the user created block packages
* restartblock / restartblock / if a block package is active, resets its counter so it restarts from the beginning. 
* explainblock (block) / explainblock monday_am_block / lists what items will play as part of the specified block. 
* **CASE 1 ** addblock / addblock / walks the user through creating a block package. 
* **CASE 2 ** addblock (name) (media name) / addblock monday_am_block "Married with Children" / creates a block using the name given and addes the media title to it. Can only add a single item upon create. If block exists will give an error and not create. 
* addtoblock (block) (media name) / addtoblock monday_am_block "My Name Is Earl" / Adds the specified media to an already existing block
* removeblock (block) / removeblock monday_am_block / removes the specified block
* removefromblock (block) (media title) / removefromblock monday_am_block "Married with Children" / removes the specified title from the specified block
* replaceinblock (block) (newitem) (olditem) / replaceinblock Test1 Psych Deadwood / replaces the old item with the new item in the specified block. 
* rearrangeblock (block) / rearragneblock Test1 / Walks you through rearranging the specified block.
* moviegenres / moviegenres / gets a list of the available movie genres.
* tvgenres / tvgenres / gets a list of the available tv genres.
* playwhereleftoff (movie/show) / playwhereleftoff Predator / plays the specified items from where you last left off.
* nextep / nextep "My Name Is Earl" / Lists the episode that will play next from the specified series.
* epdetails (Show) (Season) (Episode) / epdetails "My Name Is Earl" 1 2 / gets the details for the specified episode.
* setnextep (Show) (Season) (Episode) / setnextep "My Name Is Earl" 1 2 / sets the next episode to play from the given show to the specified season and episode. 
* moviedetails (movie) / moviedetails Predator / gets the details for the specified movie.
* showdetails (show) / showdetails Deadwood / gets the details for the specified show.
* muteaudio / muteaudio / if supported by the client, mutes audio.
* unmuteaudio / unmuteaudio / if supported by the client, sets client volume to 100%.
* mtagline (movie) / mtagline Predator / gets the tagline for the specified movie.
* msummary (movie) / msummary "The Quick and the Dead" / gets the summary for the specified movie.
* mrating (movie) / mrating "The Matrix" / gets the rating for the specified movie.
* findshow (text) / findshow Eureka / finds TV show names containing the given text.
* findmovie (text) / findmovie Terminator / finds movies with names containing the given text.
* findnewmovie / findnewmovie / when using a play mode with a random movie option, this command will replace that pending movie with a new selection of the same genre type. 
* getplaymode / getplaymode / gets the current playmode
* setplaymode (normal / block.(usercreatedblock) / marathon.(tvshownameinlibrary)) / setplaymode normal OR setplaymode block.monday_am_block OR setplaymode "marathon.Married with Children" / sets the playmode of the system to the specified playmode.
* nowplaying / nowplaying / returns what is currently playing
* listwildcard / listwildcard / lists the show currently set as the Wild Card show
* changewildcard (show)/ changewildcard OR changewildcard "My Name Is Earl" / if a show is given it will set the wild card to that show, otherwise it will walk you through choosing a new wildcard show.
* showminithonmax / showminithonmax / Shows the current Mini-Marathon Maximum settings.
* setminithonmax (number) / setminithonmax 4 / Sets the Mini-Marathon Maximum settings to the specified value. Defauls to 3.
* updatedb (updatemovies/updateshows/updateall) / updatedb updateshows / updates your TBN-Plex db.
* changeplexpw password / changeplexpw passwordhere / changes the plexpw for your user in TBN Ples
* enablecommercials / enablecommercials / enables random commercial between programs
* disablecommercials / disablecommercials / disables commercials between programs
* commercialcheck / commercialcheck / checks status of commercial mode
* listcommercials / listcommercials /lists available commercials
* listprerolls / listprerolls/ lists available prerolls
* playcommercial [title]/ playcommercial "deadwood mr wu"/plays a commercial
* showrejected / showrejected / shows movies/shows in the rejected queue(not kids approved.)
* showapproved / showapproved / shows movies/shows in the approved queue(kids approved without regard for rating.)
* addapproved title / addapproved "deadwood" / adds the specified show/movie to the approved list.
* addrejected title / addrejected "deadwood" / adds the specified title to the rejected list.
* approvedratings / approvedratings / shows the approved ratings for kids mode.
* addapprovedrating / addapprovedrating R / adds the given rating to the appvoed ratings list.
* removeapprovedrating / removeapprovedrating R / removes the specified rating from the approved list.
* addholiday holiday title / addholiday xmas 'Psych 2 4' / adds the specified epispode or movie to be associated with the given holiday.
* checkholidays / checkholidays / lists the available holidays and associated content.
* removefromholiday holiday title / removefromholiday xmas tron / disaccociates the given title from the given holiday.
* removeholiday holiday / removeholiday xmas / removes the given holiday from the available holiday list.
* resumestatus / resumestatus / checks the status for resumeplayback option.
* setresumestatus on/off / setresumestatus off / changes the state of the resumestatus setting.
* versioncheck / versioncheck / gets the current version of the TBN system script. 
* replacestatus title / replacestatus firefly / checks if the given title will be replaced in a block.
* replaceshowinblock oldtitle newtitle block playstate / replaceshowinblock deadwood psych Test4 yes / sets the new show to replace the old show in the given block.
* awaystop / awaystop / stops the current feature, sets it to upnext in the queue. Stops the play check scripts.
* checkblockrandom / checkblockrandom / checks the state of the blockrandom setting.
* setblockrandom on/off / setblockrandom on / changes the state of the blockrandom setting.
* statuscheck / statuscheck / gets the state of the various TBN-Plex options.
* getcustomtable (table) / getcustomtable fights / lists contents of specified custom table.
* listcustomtables / listcustomtables / lists available custom tables.
* enablekidsmode / enablekidsmode / enables kids mode.
* disablekidsmode / disablekidsmode / disables kids mode. Note: password required. Default: supersneaky
* pausemusic / pausemusic / pauses music on the music client
* stopmusic / stopmusic / stops music on the music client
* setmusicclient / setmusicclient (client) / sets the music client to the specified client. Can be different than your video client.
* playmusic (artist) [title] / playmusic "willie nelson" "georgia on my mind" / plays the specific artist or song
* musicstartnext / musicstartnext / start the next song on the music client
* playplaylist / playplaylist 123 / starts the specified plex playlist on your music client.
* getartists / getartists / lists the music artists off your server.
* listplexplaylists / listplexplaylists / lists playlists saved on your server for your user. 
* blocktoplist / blocktoplist cop_drama_block / converts the specified block into a plex playlist named TBNqueue.
* queuetoplaylist / queuetoplaylist / converts your TBN-Plex queue to a plex playlist named TBNqueue.
* setqueuetoplex (on/off) / setqueuetoplex on / enables or disables the automatic queue to plex function. Note: impacts performance when enabled.


###Using the crappy UI:###
There are 3 .php files and a jpg that can be used in the event you desire a UI and are worse than I at making such things. Drop them in your apache web directory and have at it. I've setup the TBN scripts and its DB such that others should be able to easily interact with them and make a custom UI, voice controller, mobile app,... whatever that makes use of them as one sees fit. 
