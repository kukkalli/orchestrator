import logging

from templates.common_user_data import CommonUserData

LOG = logging.getLogger(__name__)


class SPGWUUserData:
    USERDATA = CommonUserData.USERDATA + """
echo "--------------- SPGW-U FQDN is: ---------------"
echo "SPGW-U FQDN $FQDN_HOSTNAME"
echo "--------------- SPGW-U FQDN is: ---------------"

SGWC_IP_ADDRESS="@@sgwc_ip_address@@"
SGWC_HOSTNAME="@@sgwc_hostname@@"
sudo -- sh -c "echo $SGWC_IP_ADDRESS $SGWC_HOSTNAME $SGWC_HOSTNAME.$DOMAIN >> /etc/hosts"

su - ubuntu

export MANAGEMENT_IP="$MANAGEMENT_IP"
export FABRIC_IP="$FABRIC_IP"
export FABRIC_IP="$MANAGEMENT_IP"

# DOCKER_PASS="@@docker_pass@@"
# docker login -u kukkalli -p ${DOCKER_PASS}

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/4g/spgw-u/ || exit

export DOMAIN="$DOMAIN"
echo "DOMAIN is: $DOMAIN"
export REALM="$DOMAIN"
echo "REALM is: $REALM"

MCC="@@mcc@@"
export MCC="$MCC"
echo "MCC is: $MCC"
MNC="@@mnc@@"
export MNC="$MNC"
echo "MNC is: $MNC"
GW_ID="@@gw_id@@" # 1
export GW_ID="$GW_ID"
echo "GW ID is: $GW_ID"
APN1="@@apn-1@@.ipv4" # tuckn.ipv4
export APN1="$APN1"
echo "APN 1 is: $APN1"
APN2="@@apn-2@@.ipv4" # tuckn2.ipv4
export APN2="$APN2"
echo "APN 2 is: $APN2"
INSTANCE="@@instance@@"
export INSTANCE="$INSTANCE"
echo "INSTANCE is: $INSTANCE"
NETWORK_UE_IP="@@network_ue_ip@@"
export NETWORK_UE_IP="$NETWORK_UE_IP"
echo "NETWORK_UE_IP is: $NETWORK_UE_IP"

SPGW_U_HOSTNAME="$(hostname -s)"
export SPGW_U_HOSTNAME="$SPGW_U_HOSTNAME"
echo "SPGW-U hostname is $SPGW_U_HOSTNAME"

export SGWC_IP_ADDRESS="$SGWC_IP_ADDRESS"
echo "SGWC_IP_ADDRESS is: $SGWC_IP_ADDRESS"

export TZ="Europe/Berlin"
echo "Timezone is $TZ"

# Wait for SPGW-C to be up and running
echo "Waiting for SPGW-C at IP: $SGWC_IP_ADDRESS to be up and running"
./wait-for-sgw-c.sh "$SGWC_IP_ADDRESS"
echo "SPGW-C at IP: $SGWC_IP_ADDRESS is up and running"
echo "-----------------------------------------------------------------------------------------------------"
echo "SPGW-C responding : $(date +"%T")"

docker-compose up -d oai_spgwu

docker ps

echo "-----------------------------------------------------------------------------------------------------"
echo "Started SPGW-U : $(date +"%T")"

exit 0

    """
