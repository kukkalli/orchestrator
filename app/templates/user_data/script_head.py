class ScriptHead:
    USERDATA = """#!/bin/bash

echo "-------------------------------------------------------------------------------------------------" >> /home/ubuntu/log_startup.log
echo "Start User Data Script: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "-------------------------------------------------------------------------------------------------" >> /home/ubuntu/log_startup.log
#echo "-- Clock Synchronization - Start: $(date +'%F %T.%N %Z') --"
#while timedatectl | grep 'System clock synchronized: no' > /dev/null; do
#    sleep 1
#    echo "waiting for clock synchronization...: $(date +'%F %T.%N %Z') --"
#done

#echo "-------------------------------------------------------------------------------------------------"
#echo "-- Clock Synchronization - End  : $(date +'%F %T.%N %Z') --"

echo "Setting password" >> /home/ubuntu/log_startup.log
echo -e 'password\npassword' | passwd ubuntu
echo "Password set to password" >> /home/ubuntu/log_startup.log

    """

