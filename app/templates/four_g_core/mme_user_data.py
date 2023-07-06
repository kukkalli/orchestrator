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
sed -i -e "s@_domain_@$DOMAIN@" .env
echo "DOMAIN is: $DOMAIN"

MME_HOSTNAME="$(hostname -s)"
export MME_HOSTNAME="$MME_HOSTNAME"
sed -i -e "s@_mme_hostname_@$MME_HOSTNAME@" .env
echo "MME hostname is $MME_HOSTNAME"

sed -i -e "s@_fabric_ip_@$FABRIC_IP@" .env
echo "Fabric IP is $FABRIC_IP"

export TZ="Europe/Berlin"
sed -i -e "s@_tz_@$TZ@" .env
echo "Timezone is $TZ"

export REALM="$DOMAIN"
sed -i -e "s@_realm_@$DOMAIN@" .env
echo "REALM is: $REALM"

export HSS_HOSTNAME="$HSS_HOSTNAME"
sed -i -e "s@_hss_hostname_@$HSS_HOSTNAME@" .env
echo "HSS HOSTNAME is: $HSS_HOSTNAME"

export HSS_FQDN="$HSS_HOSTNAME"."$DOMAIN"
sed -i -e "s@_hss_fqdn_@$HSS_FQDN@" .env
echo "HSS FQDN is: $HSS_FQDN"

export HSS_IP="$HSS_IP"
sed -i -e "s@_hss_ip_@$HSS_IP@" .env
echo "HSS IP is: $HSS_IP"

MCC="@@mcc@@"
export MCC="$MCC"
sed -i -e "s@_mcc_@$MCC@" .env
echo "MCC is: $MCC"

MNC="@@mnc@@"
export MNC="$MNC"
sed -i -e "s@_mnc_@$MNC@" .env
echo "MNC is: $MNC"

MME_GID="@@mme_gid@@" # 32768
export MME_GID="$MME_GID"
sed -i -e "s@_mme_gid_@$MME_GID@" .env
echo "MME GID is: $MME_GID"

MME_CODE="@@mme_code@@" # 3
export MME_CODE="$MME_CODE"
sed -i -e "s@_mme_code_@$MME_CODE@" .env
echo "MME CODE is: $MME_CODE"

SGWC_IP_ADDRESS="@@sgwc_ip_address@@"
export SGWC_IP_ADDRESS="$SGWC_IP_ADDRESS"
sed -i -e "s@_sgwc_ip_address_@$SGWC_IP_ADDRESS@" .env
echo "SGWC IP is: $SGWC_IP_ADDRESS"

export HSS_REALM="$DOMAIN"
sed -i -e "s@_hss_realm_@$HSS_REALM@" .env
echo "HSS Realm is $HSS_REALM"

export MME_FQDN="$FQDN_HOSTNAME"
sed -i -e "s@_mme_fqdn_@$MME_FQDN@" .env
echo "MME FQDN is $MME_FQDN"

# Update mme.conf file before pushing it to docker
echo "Update mme.conf file before pushing it to docker"
./update_mme_conf.sh

docker pull redis:6.0.5
docker pull kukkalli/magma-mme:1.0.0

# Wait for HSS to be up and running
echo "-----------------------------------------------------------"
echo "Waiting for HSS at IP: $HSS_IP to be up and running: $(date +'%F %T.%N %Z')"
echo "-----------------------------------------------------------"
./wait-for-hss.sh "$HSS_IP"
echo "-----------------------------------------------------------"
echo "HSS at IP: $HSS_IP is up and running"
echo "-----------------------------------------------------------"
echo "HSS is responding: $(date +'%F %T.%N %Z')"
echo "-----------------------------------------------------------"

docker-compose up -d magma_mme

docker-compose ps -a

echo "MME started $(date +'%F %T.%N %Z')"

exit 0

    """
