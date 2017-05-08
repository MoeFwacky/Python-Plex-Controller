#!/bin/bash
# add 0 1 * * * pi sh /location/of/file/movies.sh to /etc/crontab to run this check each day

if [ ${mDate} -eq YYYYMMDD ]; then #replace YYYYMMDD with the desired date in the same format
 python /home/pi/hasystem/system.py addschedule "TITLE" HH:MM today #replace TITLE with the desired title and HH:MM with the time in 24hr format
fi
exit
