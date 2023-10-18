class IMSUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/asterisk-ims/ || exit

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

127.0.0.1	${HOSTNAME}

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
echo "@@upf_ip@@\toai-spgwu" >> hosts
echo "@@trf_ip@@\toai-trf-gen" >> hosts
echo "" >> hosts

sudo cp hosts /etc/hosts

export IMAGE_NAME="@@image_name@@"
echo "export IMAGE_NAME=\"@@image_name@@\"" >> env_var

export DOMAIN="${DOMAIN}"
echo "export DOMAIN=${DOMAIN}" >> env_var

export HOSTNAME="${HOSTNAME}"
echo "export IMS_HOSTNAME=${HOSTNAME}" >> env_var

export IMS_FQDN="${FQDN_HOSTNAME}"
echo "export IMS_FQDN=${IMS_FQDN}" >> env_var

export FABRIC_IP="${FABRIC_IP}"
echo "export FABRIC_IP=${FABRIC_IP}" >> env_var

# export MANAGEMENT_IP="${MANAGEMENT_IP}"
# echo "export MANAGEMENT_IP=${MANAGEMENT_IP}" >> env_var

echo "export WEBSMSD_PORT=@@web_port@@" >> env_var
echo "# export SMS_PORT=8080" >> env_var
echo "export SMS_PORT=@@sms_port@@" >> env_var
echo -e "export TELE_SRV='${HOSTNAME}'" >> env_var
echo "# export DOMAIN=@@domain@@" >> env_var
echo "export DOMAIN=docker.localhost" >> env_var
echo "export SYSLOG_LEVEL=@@sys_log@@" >> env_var
echo "" >> env_var
echo "export UE_ID_01=@@ue_id_01@@" >> env_var
echo -e "export UE_USER_01_FULLNAME='@@ue_user_01_fullname@@'" >> env_var
echo "" >> env_var
echo "export UE_ID_02=@@ue_id_02@@" >> env_var
echo -e "export UE_USER_02_FULLNAME='@@ue_user_02_fullname@@'" >> env_var

cat env_var

./deploy

sleep 2

docker ps -a

echo "IMS started $(date +'%F %T.%N %Z')"

exit 0

    """
