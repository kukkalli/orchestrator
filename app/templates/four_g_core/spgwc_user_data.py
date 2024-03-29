class SPGWCUserData:
    USERDATA = """
echo "--------------- SPGW-C FQDN is: ---------------"
echo "SPGW-C FQDN $FQDN_HOSTNAME"
echo "--------------- SPGW-C FQDN is: ---------------"

MME_IP="@@mme_ip@@"
MME_HOSTNAME="@@mme_hostname@@"
sudo -- sh -c "echo $MME_IP $MME_HOSTNAME $MME_HOSTNAME.$DOMAIN >> /etc/hosts"

su - ubuntu

export MANAGEMENT_IP="$MANAGEMENT_IP"
export FABRIC_IP="$FABRIC_IP"
export FABRIC_IP="$MANAGEMENT_IP"


cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/4g/spgw-c/ || exit

echo "MANAGEMENT_IP='${MANAGEMENT_IP}'" >> .env
echo "FABRIC_IP='${FABRIC_IP}'" >> .env
export DOMAIN="$DOMAIN"
echo "DOMAIN is: $DOMAIN"
echo "DOMAIN='${DOMAIN}'" >> .env
export REALM="$DOMAIN"
echo "REALM is: $REALM"
echo "REALM='${REALM}'" >> .env

MME_IP="@@mme_ip@@"
echo "MME_IP='${MME_IP}'" >> .env


MCC="@@mcc@@"
export MCC="$MCC"
echo "MCC is: $MCC"
echo "MCC='${MCC}'" >> .env
MNC="@@mnc@@"
export MNC="$MNC"
echo "MNC is: $MNC"
echo "MNC='${MNC}'" >> .env
GW_ID="@@gw_id@@" # 1
export GW_ID="$GW_ID"
echo "GW ID is: $GW_ID"
echo "GW_ID='${GW_ID}'" >> .env
APN1="@@apn-1@@.ipv4" # tuckn.ipv4
export APN1="$APN1"
echo "APN 1 is: $APN1"
echo "APN1='${APN1}'" >> .env
APN2="@@apn-2@@.ipv4" # tuckn2.ipv4
export APN2="$APN2"
echo "APN 2 is: $APN2"
echo "APN2='${APN2}'" >> .env

SPGW_C_HOSTNAME="$(hostname -s)"
export SPGW_C_HOSTNAME="$SPGW_C_HOSTNAME"
echo "SPGW-C hostname is $SPGW_C_HOSTNAME"
echo "SPGW_C_HOSTNAME='${SPGW_C_HOSTNAME}'" >> .env

export TZ="Europe/Berlin"
echo "Timezone is $TZ"
echo "TZ='${TZ}'" >> .env

docker pull kukkalli/oai-spgwc:v1.2.0

# Wait for MME to be up and running
echo "Waiting for MME at IP: $MME_IP to be up and running: $(date +'%F %T.%N %Z')"
./wait-for-mme.sh "$MME_IP"
echo "MME at IP: $MME_IP is up and running"
echo "----------------------------------------------------------------------------------------"
echo "MME responding : $(date +'%F %T.%N %Z')"

docker-compose up -d oai_spgwc

docker-compose ps -a
echo "----------------------------------------------------------------------------------------"
echo "Started SPGW-C : $(date +'%F %T.%N %Z')"

exit 0

    """
