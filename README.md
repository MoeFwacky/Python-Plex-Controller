# TBN-Plex
TheBaconNation Plex Controller
<br><a href = "https://youtu.be/woH-00-YOX0">A link to the demo setup video.</a>
<br><a href = "https://youtu.be/HRJbNHRQO6I">A link to a demo of the controller in action.</a>
<br><a href=  "http://thebaconnation.com">Our Homepage.</a>

TheBaconNation Plex Controller Help Document

Before You Begin-

3 scripts are necessary to use the TBN Plex Controller:
system.py - this is the main script used by the controller.
upddatedb_pi.py - this is the script used to update the controllers database. 
system_setup.py - this script creates the necessary files, database, and prompts the user for the information the controller needs to do its job. 

2 scripts are optional. If you use raspberry pi running rasplex as a controller, these scripts can be used to detect its play state and react based on paused, stopped, and started playback. The system_setup.py script will throw a warning if you do not have these scripts. They are not necessary to use the controller, however, a few commands will not work- ie- playcheckstatus/playcheckstart/playcheckstop

piplaystate.py - Gets the playback state from your pi.
playstatus.py - Runs in the background. When enabled uses piplaystate.py to get the status of your pi. 

Note Regarding Playback Detection:
If you do not have a Pi running rasplex, but do run something like plexpy, you can configure that to launch a script when it detects playback has stopped on your client. The command to use for that is "python system.py startnextprogram". You may need to add the path to your system.py file to that command. 

Currently the TBN Plex Controller is currently designed to work on a linux based OS. I suppose it is possible to use it on a windows based machine, though you may need to modify some paths to suit that directory structure.

To install the TBN Plex Controller, place the 5 script files in your home directory. The system_setup.py script will make a directory in your home folder, "hasystem/", which it will store its necessary files and database in. If you make this folder first and place the necessary scripts in it first, it will not make a subdirectory. If you do not make the directory first, you can delete the files from your home directory once the setup is complete. 

Install the TBN Plex Controller by running "python system_setup.py" The system setup script will ask you a few questions to get the data it needs to proceed. Once it is ready it will ask you if you want to update your database. You need to update your database before the system will find and choose media. 

NOTE: If you enter an incorrect value during setup, which prevents some element from either getting data or working, you can run "python system_setup.py reset" and it will delete the previously stored data and prompt you for it again.  

Regarding Database Updates:
The upddatedb_pi.py script will update your TBN Plex DB. The TBN Plex Controller uses a separate database so you do not need to worry about corrupting your existing Plex Database. 

You can update your database independent of the system_setup.py script by running "python upddatedb_pi.py updatetv/updatemovies/all" The script accepts one of three options. You can update all, just your movies, or just your TV shows. This is to allow you to save time when you only need to update one side of your library. Larger libraries will take more time to scan versus smaller libraries. 

After Install Notes:
Before you can use the block package commands, or block package playback, you first need to create a block package. You can use the "addblock" modifier to create a block package. 

When you run system_setup.py the playmode is set/reset to normal, and your queue is set to " ". It is recommended you do a "whatupnext" after you run the system_setup.py script. From there your queue should never be empty. The controller is designed so something will always be up next. 


Available Commands:
If the system_setup.py script succeeded in adding commands to your bash shell, and after you have restarted it, you should be able to use the following commands without having "python system.py " in front of them. If that failed, or if say you do not use the bash shell, you will need to add "python system.py " in front of the following commands. Similarly, if you want to use this script in concert with something like a webserver or voice control agent, you can use "python system.py actionshere" to use any one of the following commands. 

Note- If the option you are giving contains a space(" ") you will need to put quotes ("" or '') around that option. 

Note- When adding movies to your queue, up next, or to play now, you need to append "movie." at the beginning. Example "movie.The Matrix"

Syntax:
Command (options, if any, don't use the parenthesis)/ Example Usage / Description

addfavoritemovie / addfavoritemovie "The Matrix" / adds the specified movie to the favorites list.
queueadd / queueadd psych OR queuadd "movie.The Matrix" / adds the specified item to the end of the queue.
whereat / whereat / Lists where you are at in the current feature. *relies on optional scripts
idtonightsmovie / idtonightsmovie / if your block package contains a random movie option, this should list that movie.
findnewmovie / findnewmovie / if your block contains a random movie, and you want to find a different random movie, this command replaces that movie with a different one.
randommovieblock (genre) / randommovieblock Action / gets and creates a 3 movie block using the genre specified
stopplayback / stopplayback / stops the current playaying feature
pauseplayback / pauseplayback / stops the current playing feature
playcheckstart / playcheckstart / starts the play checking for automatic playback *relies on optional scripts
playcheckstop / playcheckstop / stops the play checking for automatic playback *relies on optional scripts
playchecksleep / playckecksleep /stops playchecking when the current playing feature ends. useful if you add custom actions to shut things off. *relies on optional scripts
queueshow / queueshow / shows what is in your queue
whatupnext / whatupnext / lists the next item in your queue. returns single item.
setupnext / setupnext "movie.Predator" / sets the next up item in your queue to be the specified item.
startnextprogram / startnextprogram / starts the next item from your queue
skipthat / skipthat / skips the next item in your queue
findsomethingelse / findsomethingelse / replaces the next item in your queue with something else
suggestmovie (genre) / suggestmovie Action / Suggests a random movie. If genre given movie is of that genre.
suggesttv (genre) / suggesttv Action / Suggests a random TV show. If genre given, show is of that genre. 
addsuggestion / addsuggestion / adds the previously suggested media to the queue, if something was previously suggested. 
whatispending / whatispending / lists what has previously been suggested but not added to the queue. 
availableblocks / availableblocks / lists the user created block packages
restartblock / restartblock / if a block package is active, resets its counter so it restarts from the beginning. 
explainblock (block) / explainblock monday_am_block / lists what items will play as part of the specified block. 
**CASE 1 ** addblock / addblock / walks the user through creating a block package. 
**CASE 2 ** addblock (name) (media name) / addblock monday_am_block "Married with Children" / creates a block using the name given and addes the media title to it. Can only add a single item upon create. If block exists will give an error and not create. 
addtoblock (block) (media name) / addtoblock monday_am_block "My Name Is Earl" / Adds the specified media to an already existing block
removeblock (block) / removeblock monday_am_block / removes the specified block
removefromblock (block) (media title) / removefromblock monday_am_block "Married with Children" / removes the specified title from the specified block
nextep / nextep "My Name Is Earl" / Lists the episode that will play next from the specified series.
epdetails (Show) (Season) (Episode) / epdetails "My Name Is Earl" 1 2 / gets the details for the specified episode.
setnextep (Show) (Season) (Episode) / setnextep "My Name Is Earl" 1 2 / sets the next episode to play from the given show to the specified season and episode. 
moviedetails (movie) / moviedetails Predator / gets the details for the specified movie
findshow (text) / findshow Eureka / finds TV show names containing the given text.
findmovie (text) / findmovie Terminator / finds movies with names containing the given text.
getplaymode / getplaymode / gets the current playmode
setplaymode (normal / block.(usercreatedblock) / marathon.(tvshownameinlibrary)) / setplaymode normal OR setplaymode block.monday_am_block OR setplaymode "marathon.Married with Children" / sets the playmode of the system to the specified playmode.
nowplaying / nowplaying / returns what is currently playing
