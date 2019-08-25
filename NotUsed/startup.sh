#!bin/bash
touch /tmp/REMOVE_TO_BREAK_RESTART.dummy

cd /home/pi/Desktop/OP1_File_Organizer/

while [ 1 ]
do

sudo python3 ./run.py # > ./log.py
sleep 1
echo " -- ERROR RESTARTING python process exit --"
if [ ! -f /tmp/REMOVE_TO_BREAK_RESTART.dummy ]; then
        echo "REMOVE_TO_BREAK_RESTART was removed stop autorerun after error"
        break
    fi


done
