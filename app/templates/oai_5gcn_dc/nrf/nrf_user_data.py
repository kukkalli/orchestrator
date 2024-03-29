class NRFUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/nrf/ || exit

rm -f env_var

cat > hosts << EOF
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts

127.0.0.1	oai-nrf

# OAI 5GCN VM IPs
EOF

echo "@@mysql_ip@@\tmysql" >> hosts
echo "@@nrf_ip@@\toai-nrf" >> hosts
echo "@@ims_ip@@\tasterisk-ims" >> hosts
echo "@@udr_ip@@\toai-udr" >> hosts
echo "@@udm_ip@@\toai-udm" >> hosts
echo "@@ausf_ip@@\toai-ausf" >> hosts
echo "@@amf_ip@@\toai-amf" >> hosts
echo "@@smf_ip@@\toai-smf" >> hosts
echo "@@upf_ip@@\toai-spgwu-tiny" >> hosts
echo "@@trf_ip@@\toai-trf-gen" >> hosts
echo "" >> hosts

sudo cp hosts /etc/hosts

export IMAGE_NAME="@@image_name@@"
echo "export IMAGE_NAME=\"@@image_name@@\"" >> env_var

export DOMAIN="${DOMAIN}"
echo "export DOMAIN=${DOMAIN}" >> env_var

export HOSTNAME="${HOSTNAME}"
echo "export HOSTNAME=${HOSTNAME}" >> env_var

export NRF_FQDN="${FQDN_HOSTNAME}"
echo "export NRF_FQDN=${NRF_FQDN}" >> env_var

export TZ="@@tz@@"
echo "export TZ=@@tz@@" >> env_var

export LOG_LEVEL=@@log_level@@
echo "export LOG_LEVEL=@@log_level@@" >> env_var

export NRF_INTERFACE_NAME_FOR_SBI=eth0
echo "export NRF_INTERFACE_NAME_FOR_SBI=eth0" >> env_var

export FABRIC_IP="${FABRIC_IP}"
echo "export FABRIC_IP=${FABRIC_IP}" >> env_var

# export MANAGEMENT_IP="${MANAGEMENT_IP}"
# echo "export MANAGEMENT_IP=${MANAGEMENT_IP}" >> env_var

cat env_var

./deploy

sleep 2

docker ps -a

echo "NRF started $(date +'%F %T.%N %Z')"

exit 0

    """
