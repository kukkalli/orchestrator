class NRFUserData:
    USERDATA = """
cat > /home/ubuntu/hosts << EOF
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

echo "@@mysql_ip@@\tmysql" >> /home/ubuntu/hosts
echo "@@nrf_ip@@\toai-nrf" >> /home/ubuntu/hosts
echo "@@ims_ip@@\tasterisk-ims" >> /home/ubuntu/hosts
echo "@@udr_ip@@\toai-udr" >> /home/ubuntu/hosts
echo "@@udm_ip@@\toai-udm" >> /home/ubuntu/hosts
echo "@@ausf_ip@@\toai-ausf" >> /home/ubuntu/hosts
echo "@@amf_ip@@\toai-amf" >> /home/ubuntu/hosts
echo "@@smf_ip@@\toai-smf" >> /home/ubuntu/hosts
echo "@@upf_ip@@\toai-spgwu" >> /home/ubuntu/hosts
echo "@@trf_ip@@\toai-trf-gen" >> /home/ubuntu/hosts
echo "" >> /home/ubuntu/hosts

cp /home/ubuntu/hosts /etc/hosts

# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/oai-nrf/ || exit

rm -f env_var

export DOMAIN="${DOMAIN}"
echo "export DOMAIN=${DOMAIN}" >> /home/ubuntu/env_var

export HOSTNAME="${HOSTNAME}"
echo "export MYSQL_HOSTNAME=${HOSTNAME}" >> /home/ubuntu/env_var

export NRF_FQDN="${FQDN_HOSTNAME}"
echo "export NRF_FQDN=${NRF_FQDN}" >> /home/ubuntu/env_var

export TZ="@@tz@@"
echo "export TZ=@@tz@@" >> /home/ubuntu/env_var

export LOG_LEVEL=@@log_level@@
echo "LOG_LEVEL=@@log_level@@" >> /home/ubuntu/env_var

export NRF_INTERFACE_NAME_FOR_SBI=eth0
echo "export NRF_INTERFACE_NAME_FOR_SBI=eth0" >> /home/ubuntu/env_var

export FABRIC_IP="${FABRIC_IP}"
echo "export FABRIC_IP=${FABRIC_IP}" >> /home/ubuntu/env_var

export MANAGEMENT_IP="${MANAGEMENT_IP}"
echo "export MANAGEMENT_IP=${MANAGEMENT_IP}" >> /home/ubuntu/env_var

cat /home/ubuntu/env_var

./update_nrf

sleep 2

docker ps -a

echo "NRF started $(date +'%F %T.%N %Z')"

exit 0

    """
