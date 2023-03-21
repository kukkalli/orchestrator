class ScriptHead:
    USERDATA = """#!/bin/bash

echo "Start User Data Script: $(date +"%T.%N")" >> boot.log
echo "-------------------------------------------------------------------------------------------------" >> boot.log
echo "-------------------------------------------------------------------------------------------------" >> boot.log
echo "-------------------------------------------------------------------------------------------------" >> boot.log
echo "-- Clock Synchronization - Start: $(date +"%T.%N") --" >> boot.log
while timedatectl | grep 'System clock synchronized: no' > /dev/null; do
    sleep 1
    echo "waiting for clock synchronization..." >> boot.log
done 

echo "-------------------------------------------------------------------------------------------------" >> boot.log
echo "-------------------------------------------------------------------------------------------------" >> boot.log
echo "-- Clock Synchronization - End  : $(date +"%T.%N") --" >> boot.log
    """