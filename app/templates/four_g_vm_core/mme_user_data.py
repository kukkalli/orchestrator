class MMEUserData:
    USERDATA = """
echo "MME Main User Script: $(date +'%F %T.%N %Z')"
echo "MME Main User Script: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log

export HSS_IP=@@hss_ip@@
export HSS_HOSTNAME="@@hss_hostname@@"
export HSS_FQDN="@@hss_hostname@@.$DOMAIN"
export MME_IP="@@mme_ip@@"
export MME_HOSTNAME=$HOSTNAME
export MME_FQDN="$MME_HOSTNAME.$DOMAIN"
export COUNTRY_CODE=@@country_code@@
export STATE_CODE=@@state_code@@
export COMPANY_SHORT_NAME=@@csn@@
export COMPANY_FULL_NAME=@@cfn@@
export SPGW_IP="@@spgw_ip@@"
export SPGW_HOSTNAME="@@spgw_hostname@@"
export SPGW_FQDN="$SPGW_HOSTNAME.$DOMAIN"
export SPGW_IP_SN=@@spgw_ip_sn@@
export MCC=@@mcc@@
export MNC=@@mnc@@
export MME_GID=@@mme_gid@@
export MME_CODE=@@mme_code@@
export TAC=@@tac@@

sudo -- sh -c "echo $HSS_IP $HSS_HOSTNAME $HSS_FQDN >> /etc/hosts"
sudo -- sh -c "echo $SPGW_IP $SPGW_HOSTNAME $SPGW_FQDN >> /etc/hosts"
echo "Host files: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "$(cat /etc/hosts)" >> /home/ubuntu/log_startup.log

# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

echo "export OPERATOR_KEY=@@operator_key@@" >> /home/ubuntu/env_var

cd /home/ubuntu/ || exit
rm -f env_var
echo "HSS IP is ${HSS_IP}" >> /home/ubuntu/env_var

export REALM="$DOMAIN"
echo "export REALM=${REALM}" >> env_var
echo "export HSS_IP=${HSS_IP}" >> env_var
echo "export HSS_HOSTNAME=${HSS_HOSTNAME}" >> env_var
echo "export HSS_FQDN=\"$HSS_FQDN\"" >> env_var
echo "export MME_IP=\"${MME_IP}\"" >> env_var
echo "export MME_HOSTNAME=${MME_HOSTNAME}" >> env_var
echo "export MME_FQDN=\"${MME_FQDN}\"" >> env_var
echo "export COUNTRY_CODE=${COUNTRY_CODE}" >> env_var
echo "export STATE_CODE=${STATE_CODE}" >> env_var
echo "export COMPANY_SHORT_NAME=${COMPANY_SHORT_NAME}" >> env_var
echo "export COMPANY_FULL_NAME=${COMPANY_FULL_NAME}" >> env_var
echo "export SPGW_IP=\"${SPGW_IP}\"" >> env_var
echo "export SPGW_HOSTNAME=\"${SPGW_HOSTNAME}\"" >> env_var
echo "export SPGW_FQDN=\"${SPGW_FQDN}\"" >> env_var
echo "export MCC=${MCC}" >> env_var
echo "export MNC=${MNC}" >> env_var
echo "export MME_GID=${MME_GID}" >> env_var
echo "export MME_CODE=${MME_CODE}" >> env_var
echo "export TAC=${TAC}" >> env_var
FABRIC_INTERFACE_NAME=${MANAGEMENT_INTERFACE_NAME}
echo "export FABRIC_INTERFACE_NAME=${FABRIC_INTERFACE_NAME}" >> env_var
MME_IP_SN=\"${MANAGEMENT_IP_SN}\"
echo "export MME_IP_SN=\"${MME_IP_SN}\"" >> env_var
echo "export SPGW_IP_SN=\"$SPGW_IP_SN\"" >> env_var

echo "env_var file: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "$(cat env_var)" >> /home/ubuntu/log_startup.log

echo "Starting MME: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "Starting MME: $(date +'%F %T.%N %Z')"
./initialize_oai_mme
echo "MME started: $(date +'%F %T.%N %Z')" >> /home/ubuntu/log_startup.log
echo "MME started: $(date +'%F %T.%N %Z')"

exit 0

    """
