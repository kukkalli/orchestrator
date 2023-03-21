class MMEUserData:
    USERDATA = """


export HSS_HOSTNAME="@@hss_hostname@@"
export HSS_FQDN="@@hss_hostname@@"
export MME_IP="@@mme_ip@@"
export MME_HOSTNAME="@@mme_hostname@@"
export MME_FQDN="$MME_HOSTNAME.$DOMAIN"
export COUNTRY_CODE=@@country_code@@
export STATE_CODE=@@state_code@@
export COMPANY_SHORT_NAME=@@csn@@
export COMPANY_FULL_NAME=@@cfn@@
export SPGW_IP="@@spgw_ip@@"
export SPGW_HOSTNAME="@@spgw_hostname@@"
export SPGW_FQDN="$SPGW_HOSTNAME.$DOMAIN"

sudo -- sh -c "echo $HSS_IP $HSS_HOSTNAME $HSS_HOSTNAME.$DOMAIN >> /etc/hosts"
sudo -- sh -c "echo $MME_IP $MME_HOSTNAME $MME_HOSTNAME.$DOMAIN >> /etc/hosts"
sudo -- sh -c "echo $SPGW_IP $SPGW_HOSTNAME $SPGW_HOSTNAME.$DOMAIN >> /etc/hosts"

# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"
echo "export OPERATOR_KEY=@@operator_key@@" >> /home/ubuntu/env_var

cd /home/ubuntu/ || exit

# git clone https://github.com/kukkalli/oai-docker-compose.git

# chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/4g/hss/ || exit

export MANAGEMENT_IP="$MANAGEMENT_IP"
sed -i -e "s@_domain_@$DOMAIN@" .env
echo "The HSS_MANAGEMENT_IP is $HSS_MANAGEMENT_IP"
sed -i -e "s@_management_ip_@$MANAGEMENT_IP@" .env

export FABRIC_IP="$FABRIC_IP"
export FABRIC_IP="$MANAGEMENT_IP"
echo "The HSS_FABRIC_IP is $FABRIC_IP"
sed -i -e "s@_fabric_ip_@$FABRIC_IP@" .env
export HSS_FQDN="$FQDN_HOSTNAME"
sed -i -e "s@_hss_fqdn_@$HSS_FQDN@" .env

export OP_KEY="@@op_key@@"
sed -i -e "s@_op_key_@$OP_KEY@" .env
export LTE_K="@@lte_k@@"
sed -i -e "s@_lte_k_@$LTE_K@" .env
APN1="@@apn-1@@.ipv4" # tuckn.ipv4
export APN1="$APN1"
sed -i -e "s@_apn_1_@$APN1@" .env
echo "APN 1 is: $APN1"
APN2="@@apn-2@@.ipv4" # tuckn2.ipv4
export APN2="$APN2"
sed -i -e "s@_apn_2_@$APN2@" .env
echo "APN 2 is: $APN2"

export FIRST_IMSI="@@first_imsi@@"
sed -i -e "s@_first_imsi_@$FIRST_IMSI@" .env

echo "The HSS FQDN is $HSS_FQDN"

export REALM="$DOMAIN"
sed -i -e "s@_realm_@$DOMAIN@" .env


echo "The REALM is $REALM"

export HSS_HOSTNAME="$HOSTNAME"
sed -i -e "s@_hss_hostname_@$HSS_HOSTNAME@" .env

echo "The HSS HOSTNAME is $HSS_HOSTNAME"

docker-compose up -d db_init

docker-compose up -d cassandra_web

sleep 5

docker-compose up -d oai_hss

docker rm db-init

docker ps -a

echo "HSS started $(date +"%T.%N")"

exit 0

    """
