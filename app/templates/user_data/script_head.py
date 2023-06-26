class ScriptHead:
    USERDATA = """#!/bin/bash

echo "-------------------------------------------------------------------------------------------------"
echo "Start User Data Script: $(date +"%T.%N")"
echo "-------------------------------------------------------------------------------------------------"
#echo "-- Clock Synchronization - Start: $(date +"%T.%N") --"
#while timedatectl | grep 'System clock synchronized: no' > /dev/null; do
#    sleep 1
#    echo "waiting for clock synchronization...: $(date +"%T.%N") --"
#done

#echo "-------------------------------------------------------------------------------------------------"
#echo "-- Clock Synchronization - End  : $(date +"%T.%N") --"

    """

