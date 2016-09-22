# TBN-Plex
TheBaconNation Plex Controller
<br><a href = "https://youtu.be/YQRKUmyjEcQ">A link to the demo setup video.</a>
<br><a href = "https://youtu.be/HRJbNHRQO6I">A link to a demo of the controller in action.</a>
<br><a href = "https://youtu.be/a5lOLjzunMQ">How To Create a Block Package.</a>
<br><a href=  "http://thebaconnation.com">Our Homepage.</a>
<br><a href= "https://youtu.be/u0ur4koeDFM">The Beginnings of a bad web ui.</a>
<br><a href= "https://youtu.be/oMDl-6GRK30">How to use replaceshowinblock feature.</a>

<br><a href= "https://discordapp.com/channels/206249843209797632/206249843209797632">The TBN-Plex Discord Channel.</a>

<br>TheBaconNation Plex Controller Help Document
<br>
<br>Before You Begin-
<br>
<br>The following librarys are needed:
<br>enchant. You can use "pip install pyenchant" to get it.
<br>The python plex api. User "pip install plexapi"
<br>
<br>Do to some recent changes, it is recommended you remove the following files, rerun the new system_setup script, and let it refresh your library. Files to remove: aliases, system.py. If you have not updated in a while, also replace the setup_system.py and upddated_db.py files.<br>
<br>3 scripts are necessary to use the TBN Plex Controller:
<br>system.py - this is the main script used by the controller.
<br>upddatedb_pi.py - this is the script used to update the controllers database. 
<br>system_setup.py - this script creates the necessary files, database, and prompts the user for the information the controller needs to do its job. 
<br>
<br>There is one optional script- piplaystate.py. This script uses the API access to check the playback status of the client you are using at a regular interval. When the mode is "On," when a program stopps the system will automatically launch a new progarm, and continue to do so untill it is in eithr "Off" or "Sleep" mode. While this option used to only be supported by a Raspberry Pi running raslplex, it should ideally work for most/all clients that support api access and report their timeline. 
<br>
<br>piplaystate.py - Gets the playback state from your client.
<br>playstatus.py - Runs in the background. When enabled uses piplaystate.py to get the status of your client. 
<br>
<br>Currently the TBN Plex Controller is currently designed to work on a linux based OS, however, it can also run on a windows environment without modification, though you may not be able to use the aliases.
<br>
<br>To install the TBN Plex Controller, place the system_setup.py script files in your home directory. The system_setup.py script will make a directory in your home folder, "hasystem/", or prompt your for a directory, depending on your OS, which it will store its necessary files and database in.
<br>
<br>Install the TBN Plex Controller by running "python system_setup.py" The system setup script will ask you a few questions to get the data it needs to proceed. Once it is ready it will ask you if you want to update your database. You need to update your database before the system will find and choose media. 
<br>
<br>NOTE: If you enter an incorrect value during setup, which prevents some element from either getting data or working, you can run "python system_setup.py reset" and it will delete the previously stored data and prompt you for it again.  

<br>Regarding Database Updates:
<br>The upddatedb_pi.py script will update your TBN Plex DB. The TBN Plex Controller uses a separate database so you do not need to worry about corrupting your existing Plex Database. 

<br>You can update your database independent of the system_setup.py script by running "python upddatedb_pi.py updatetv/updatemovies/all" The script accepts one of three options. You can update all, just your movies, or just your TV shows. This is to allow you to save time when you only need to update one side of your library. Larger libraries will take more time to scan versus smaller libraries. 
<br>
<br>After Install Notes:
<br>Before you can use the block package commands, or block package playback, you first need to create a block package. You can use the "addblock" modifier to create a block package. 
<br>
<br>When you run system_setup.py the playmode is set/reset to normal, and your queue is set to " ". It is recommended you do a "whatupnext" after you run the system_setup.py script. From there your queue should never be empty. The controller is designed so something will always be up next. 
<br>
<br>
<br>Available Commands:
<br>If the system_setup.py script succeeded in adding commands to your bash shell, and after you have restarted it, you should be able to use the following commands without having "python system.py " in front of them. If that failed, or if say you do not use the bash shell, you will need to add "python system.py " in front of the following commands. Similarly, if you want to use this script in concert with something like a webserver or voice control agent, you can use "python system.py actionshere" to use any one of the following commands. 
<br>
<br>Note- If the option you are giving contains a space(" ") you will need to put quotes ("" or '') around that option. 
<br>
<br>Syntax:
<br>Command (options, if any, don't use the parenthesis)/ Example Usage / Description
<br>
<br>playme (tvshow/movie) / playme "The Big Bang Theory" OR playme "movie.The Matrix" / plays the next episode from the specified show or the specified movie.
<br>addfavoritemovie / addfavoritemovie "The Matrix" / adds the specified movie to the favorites list.
<br>addfavoriteshow / addfavoriteshow "Marvels Daredevil" / adds the specified show to the favorites list.
<br>addgenreshow / addgenreshow "Good Eats" "Cooking" / adds a custom genre to the specified shows genre list.
<br>addgenremovie / addgenremovie "Deadpool" "Not Super Hero" / adds a custom genre to the specified movies genre list.
<br>queueadd / queueadd psych OR queuadd "movie.The Matrix" / adds the specified item to the end of the queue.
<br>whereat / whereat / Lists where you are at in the current feature. *relies on optional scripts
<br>idtonightsmovie / idtonightsmovie / if your block package contains a random movie option, this should list that movie.
<br>idtonightsshow / idtonightsshow / if your block package contains a random show option, this should list that show.
<br>getnewblock / getnewblock / if you are playing a random movie or show block, this command will generate a new block.
<br>listclients / listclients / lists the available clients.
<br>changeclient / changeclient / gives option to select a new client from the list of available clients.
<br>
<br>findnewmovie / findnewmovie / if your block contains a random movie, and you want to find a different random movie, this command replaces that movie with a different one.
<br>randommovieblock (genre) / randommovieblock Action / gets and creates a 3 movie block using the genre specified
<br>randomtvblock (genre) / randomtvblock Action / gets and creates a 3 show block using the genre specified
<br>stopplayback / stopplayback / stops the current playaying feature
<br>pauseplayback / pauseplayback / stops the current playing feature
<br>playcheckstart / playcheckstart / starts the play checking for automatic playback *relies on optional scripts
<br>playcheckstop / playcheckstop / stops the play checking for automatic playback *relies on optional scripts
<br>playchecksleep / playckecksleep /stops playchecking when the current playing feature ends. useful if you add custom actions to shut things off. *relies on optional scripts
<br>queueshow / queueshow / shows what is in your queue
<br>queueremove (item in queue) / queueremove "Deadwood" / removes the specified item from the queue.
<br>queuefix / queuefix / if for somereason your queue gets messed up this command can be used to kill and rebuild it(does not preseve queue.)
<br>whatupnext / whatupnext / lists the next item in your queue. returns single item.
<br>setupnext / setupnext "movie.Predator" / sets the next up item in your queue to be the specified item.
<br>startnextprogram / startnextprogram / starts the next item from your queue
<br>skipthat / skipthat / skips the next item in your queue
<br>seriesskipahead (show) / seriesskipahead Psych / Sets the specified shows playqueue ahead one episode.
<br>seriesskipback (show) / seriesskipback psych / Sets the specified shows playqueue back one episode.
<br>skipahead / skipahead / skips ahead 30 seconds in the current feature.
<br>skipback / skipback / skipts back 15 seconds in the current feature.
<br>findsomethingelse / findsomethingelse / replaces the next item in your queue with something else
<br>suggestmovie (genre/rating./actor./) / suggestmovie Action / Suggests a random movie. If genre given movie is of that genre.
<br>suggesttv (genre/rating./duration.) / suggesttv Action / Suggests a random TV show. If genre given, show is of that genre. 
<br>addsuggestion / addsuggestion / adds the previously suggested media to the queue, if something was previously suggested. 
<br>whatispending / whatispending / lists what has previously been suggested but not added to the queue. 
<br>availableblocks / availableblocks / lists the user created block packages
<br>restartblock / restartblock / if a block package is active, resets its counter so it restarts from the beginning. 
<br>explainblock (block) / explainblock monday_am_block / lists what items will play as part of the specified block. 
<br>**CASE 1 ** addblock / addblock / walks the user through creating a block package. 
<br>**CASE 2 ** addblock (name) (media name) / addblock monday_am_block "Married with Children" / creates a block using the name given and addes the media title to it. Can only add a single item upon create. If block exists will give an error and not create. 
<br>addtoblock (block) (media name) / addtoblock monday_am_block "My Name Is Earl" / Adds the specified media to an already existing block
<br>removeblock (block) / removeblock monday_am_block / removes the specified block
<br>removefromblock (block) (media title) / removefromblock monday_am_block "Married with Children" / removes the specified title from the specified block
<br>replaceinblock (block) (newitem) (olditem) / replaceinblock Test1 Psych Deadwood / replaces the old item with the new item in the specified block. 
<br>rearrangeblock (block) / rearragneblock Test1 / Walks you through rearranging the specified block.
<br>moviegenres / moviegenres / gets a list of the available movie genres.
<br>tvgenres / tvgenres / gets a list of the available tv genres.
<br>playwhereleftoff (movie/show) / playwhereleftoff Predator / plays the specified items from where you last left off.
<br>nextep / nextep "My Name Is Earl" / Lists the episode that will play next from the specified series.
<br>epdetails (Show) (Season) (Episode) / epdetails "My Name Is Earl" 1 2 / gets the details for the specified episode.
<br>setnextep (Show) (Season) (Episode) / setnextep "My Name Is Earl" 1 2 / sets the next episode to play from the given show to the specified season and episode. 
<br>moviedetails (movie) / moviedetails Predator / gets the details for the specified movie.
<br>showdetails (show) / showdetails Deadwood / gets the details for the specified show.
<br>muteaudio / muteaudio / if supported by the client, mutes audio.
<br>unmuteaudio / unmuteaudio / if supported by the client, sets client volume to 100%.
<br>mtagline (movie) / mtagline Predator / gets the tagline for the specified movie.
<br>msummary (movie) / msummary "The Quick and the Dead" / gets the summary for the specified movie.
<br>mrating (movie) / mrating "The Matrix" / gets the rating for the specified movie.
<br>findshow (text) / findshow Eureka / finds TV show names containing the given text.
<br>findmovie (text) / findmovie Terminator / finds movies with names containing the given text.
<br>findnewmovie / findnewmovie / when using a play mode with a random movie option, this command will replace that pending movie with a new selection of the same genre type. 
<br>getplaymode / getplaymode / gets the current playmode
<br>setplaymode (normal / block.(usercreatedblock) / marathon.(tvshownameinlibrary)) / setplaymode normal OR setplaymode block.monday_am_block OR setplaymode "marathon.Married with Children" / sets the playmode of the system to the specified playmode.
<br>nowplaying / nowplaying / returns what is currently playing
<br>listwildcard / listwildcard / lists the show currently set as the Wild Card show
<br>changewildcard (show)/ changewildcard OR changewildcard "My Name Is Earl" / if a show is given it will set the wild card to that show, otherwise it will walk you through choosing a new wildcard show.
<br>showminithonmax / showminithonmax / Shows the current Mini-Marathon Maximum settings.
<br>setminithonmax (number) / setminithonmax 4 / Sets the Mini-Marathon Maximum settings to the specified value. Defauls to 3.
<br>updatedb (updatemovies/updateshows/updateall) / updatedb updateshows / updates your TBN-Plex db.
<br>Commands exist that go here... I'm bad at updating this page.
<br>
<br>
<br>
Using the crappy UI:
<br>There are 3 .php files and a jpg that can be used in the event you desire a UI and are worse than I at making such things. Drop them in your apache web directory and have at it. I've setup the TBN scripts and its DB such that others should be able to easily interact with them and make a custom UI, voice controller, mobile app,... whatever that makes use of them as one sees fit. 
