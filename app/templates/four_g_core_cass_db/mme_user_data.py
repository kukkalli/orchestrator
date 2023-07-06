class MMEUserData:
    USERDATA = """

HSS_IP="@@hss_ip@@"
HSS_HOSTNAME="@@hss_hostname@@"
sudo -- sh -c "echo $HSS_IP $HSS_HOSTNAME $HSS_HOSTNAME.$DOMAIN >> /etc/hosts"

su - ubuntu

export MANAGEMENT_IP="$MANAGEMENT_IP"
export FABRIC_IP="$FABRIC_IP"
export FABRIC_IP="$MANAGEMENT_IP"

# DOCKER_PASS="@@docker_pass@@"
# docker login -u kukkalli -p ${DOCKER_PASS}

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/4g/mme/ || exit

export DOMAIN="$DOMAIN"
echo "DOMAIN is: $DOMAIN"
export REALM="$DOMAIN"
echo "REALM is: $REALM"
export HSS_IP="$HSS_IP"
echo "HSS IP is: $HSS_IP"
export HSS_HOSTNAME="$HSS_HOSTNAME"
echo "HSS HOSTNAME is:" $HSS_HOSTNAME
export HSS_FQDN="$HSS_HOSTNAME"."$DOMAIN"
echo "HSS FQDN is: $HSS_FQDN"
MCC="@@mcc@@"
export MCC="$MCC"
echo "MCC is: $MCC"
MNC="@@mnc@@"
export MNC="$MNC"
echo "MNC is: $MNC"
MME_GID="@@mme_gid@@" # 32768
export MME_GID="$MME_GID"
echo "MME GID is: $MME_GID"
MME_CODE="@@mme_code@@" # 3
export MME_CODE="$MME_CODE"
echo "MME CODE is: $MME_CODE"
SGWC_IP_ADDRESS="@@sgwc_ip_address@@"
export SGWC_IP_ADDRESS="$SGWC_IP_ADDRESS"
echo "SGWC IP is: $SGWC_IP_ADDRESS"

MME_HOSTNAME="$(hostname -s)"
export MME_HOSTNAME="$MME_HOSTNAME"
echo "MME hostname is $MME_HOSTNAME"

export TZ="Europe/Berlin"
echo "Timezone is $TZ"

export HSS_REALM="$DOMAIN"
echo "HSS Realm is $HSS_REALM"

export MME_FQDN="$FQDN_HOSTNAME"
echo "MME FQDN is $MME_FQDN"

# Update mme.conf file before pushing it to docker
echo "Update mme.conf file before pushing it to docker"
./update_mme_conf.sh

# Wait for HSS to be up and running
echo "-----------------------------------------------------------"
echo "Waiting for HSS at IP: $HSS_IP to be up and running"
echo "-----------------------------------------------------------"
./wait-for-hss.sh "$HSS_IP"
echo "-----------------------------------------------------------"
echo "HSS at IP: $HSS_IP is up and running"
echo "-----------------------------------------------------------"
echo "HSS is responding: $(date +'%F %T.%N %Z')"
echo "-----------------------------------------------------------"

docker-compose up -d magma_mme

docker ps

echo "MME started $(date +'%F %T.%N %Z')"

exit 0

    """
