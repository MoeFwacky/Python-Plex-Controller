#!/bin/bash
#daily tasks
python /home/pi/hasystem/system.py addschedule "setplaymode commercialmode" HH:MM weekends #replace HH:MM with start of broadcast day in 24hr format
python /home/pi/hasystem/system.py addschedule "setplaymode commercialmode" HH:MM weekdays #replace HH:MM with start of broadcast day in 24hr format
echo Starting Scheduling
python /home/pi/hasystem/system.py addschedule "TITLE" HH:MM sunday #replace TITLE with desired title or "randommovieblock genre" and HH:MM with the desired time in 24hr format
echo Scheduling Complete