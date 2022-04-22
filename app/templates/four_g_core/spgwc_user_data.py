import logging

from templates.common_user_data import CommonUserData

LOG = logging.getLogger(__name__)


class SPGWCUserData:
    USERDATA = CommonUserData.USERDATA + """
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

# DOCKER_PASS="@@docker_pass@@"
# docker login -u kukkalli -p ${DOCKER_PASS}

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/4g/spgw-c/ || exit

export DOMAIN="$DOMAIN"
echo "DOMAIN is: $DOMAIN"
export REALM="$DOMAIN"
echo "REALM is: $REALM"

MME_IP="@@mme_ip@@"


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

SPGW_C_HOSTNAME="$(hostname -s)"
export SPGW_C_HOSTNAME="$SPGW_C_HOSTNAME"
echo "SPGW-C hostname is $SPGW_C_HOSTNAME"

export TZ="Europe/Berlin"
echo "Timezone is $TZ"

# Wait for MME to be up and running
echo "Waiting for MME at IP: $MME_IP to be up and running"
./wait-for-mme.sh "$MME_IP"
echo "MME at IP: $MME_IP is up and running"

docker-compose up -d oai_spgwc

docker ps

exit 0

    """
