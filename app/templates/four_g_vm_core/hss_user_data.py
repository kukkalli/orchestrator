class HSSUserData:
    USERDATA = """
echo "HSS Main User Script: $(date +'%F %T.%N %Z')"
echo "HSS Main User Script: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log

export HSS_FQDN="$FQDN_HOSTNAME"
export MME_IP="@@mme_ip@@"
export MME_HOSTNAME="@@mme_hostname@@"
export MME_FQDN="$MME_HOSTNAME.$DOMAIN"
export OPERATOR_KEY=@@operator_key@@
export COUNTRY_CODE=@@country_code@@
export STATE_CODE=@@state_code@@
export COMPANY_SHORT_NAME=@@csn@@
export COMPANY_FULL_NAME=@@cfn@@
export APN=@@apn@@
export PDN_TYPE=@@pdn_type@@
export USER_IMSI=@@user_imsi@@
export SPGW_IP="@@spgw_ip@@"
export SPGW_HOSTNAME="@@spgw_hostname@@"
export SPGW_FQDN="$SPGW_HOSTNAME.$DOMAIN"
export SECURITY_KEY=@@security_key@@

sudo -- sh -c "echo $MME_IP $MME_HOSTNAME $MME_HOSTNAME.$DOMAIN >> /etc/hosts"
sudo -- sh -c "echo $SPGW_IP $SPGW_HOSTNAME $SPGW_HOSTNAME.$DOMAIN >> /etc/hosts"
echo "Host files: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "$(cat /etc/hosts)" >> /home/ubuntu/log_startup.log


# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit
rm -f env_var
echo "export HSS_IP=${MANAGEMENT_IP}" >> env_var
echo "export HSS_HOSTNAME=${HOSTNAME}" >> env_var
echo "export HSS_FQDN=${FQDN_HOSTNAME}" >> env_var

echo "export MME_IP=${MME_IP}" >> env_var

export MANAGEMENT_IP="$MANAGEMENT_IP"
echo "The MANAGEMENT_IP is $MANAGEMENT_IP" >> /home/ubuntu/log_startup.log

export REALM="$DOMAIN"
echo "export REALM=\"$REALM\"" >> env_var

echo "The REALM is $REALM" >> /home/ubuntu/log_startup.log

export HSS_HOSTNAME="$HOSTNAME"
echo "export HSS_HOSTNAME=\"$HSS_HOSTNAME\"" >> env_var
echo "The HSS HOSTNAME is $HSS_HOSTNAME" >> /home/ubuntu/log_startup.log

export FABRIC_IP="$FABRIC_IP"
export FABRIC_IP="$MANAGEMENT_IP" # To be commented

echo "The FABRIC_IP is $FABRIC_IP" >> /home/ubuntu/log_startup.log
export FABRIC_IP_SN="$FABRIC_IP_SN"
export FABRIC_IP_SN="$MANAGEMENT_IP_SN" # To be commented
export FABRIC_INTERFACE_NAME="$MANAGEMENT_INTERFACE_NAME" # To be commented

echo "export OPERATOR_KEY=${OPERATOR_KEY}" >> env_var
echo "export COUNTRY_CODE=${COUNTRY_CODE}" >> env_var
echo "export STATE_CODE=${STATE_CODE}" >> env_var
echo "export COMPANY_SHORT_NAME=${COMPANY_SHORT_NAME}" >> env_var
echo "export COMPANY_FULL_NAME=${COMPANY_FULL_NAME}" >> env_var
echo "export APN=${APN}" >> env_var
echo "export PDN_TYPE=${PDN_TYPE}" >> env_var
echo "export USER_IMSI=${USER_IMSI}" >> env_var
echo "export SPGW_IP=${SPGW_IP}" >> env_var
echo "export SECURITY_KEY=${SECURITY_KEY}" >> env_var

echo "export MME_HOSTNAME=${MME_HOSTNAME}" >> env_var
echo "export MME_FQDN=${MME_FQDN}" >> env_var
echo "export MANAGEMENT_IP=\"$MANAGEMENT_IP\"" >> env_var
echo "export MANAGEMENT_IP_SN=\"$MANAGEMENT_IP_SN\"" >> env_var
echo "export MANAGEMENT_INTERFACE_NAME=\"$MANAGEMENT_INTERFACE_NAME\"" >> env_var
echo "export FABRIC_IP=\"$FABRIC_IP\"" >> env_var
echo "export FABRIC_IP_SN=\"$FABRIC_IP_SN\"" >> env_var
echo "export FABRIC_INTERFACE_NAME=\"$FABRIC_INTERFACE_NAME\"" >> env_var
echo "The HSS_FABRIC_IP is $FABRIC_IP" >> /home/ubuntu/log_startup.log
echo "export HSS_FABRIC_IP=\"$FABRIC_IP\"" >> env_var

echo "env_var file: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "$(cat env_var)" >> /home/ubuntu/log_startup.log

echo "Starting HSS: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "Starting HSS: $(date +'%F %T.%N %Z')"
./initialize_oai_hss
echo "HSS started: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "HSS started: $(date +'%F %T.%N %Z')"

exit 0

    """
