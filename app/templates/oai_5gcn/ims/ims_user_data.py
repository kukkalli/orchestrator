class IMSUserData:
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

rm -f env_var

export DOMAIN="${DOMAIN}"
echo "export DOMAIN=${DOMAIN}" >> /home/ubuntu/env_var

export HOSTNAME="${HOSTNAME}"
echo "export IMS_HOSTNAME=${HOSTNAME}" >> /home/ubuntu/env_var

export IMS_FQDN="${FQDN_HOSTNAME}"
echo "export IMS_FQDN=${IMS_FQDN}" >> /home/ubuntu/env_var

export FABRIC_IP="${FABRIC_IP}"
echo "export FABRIC_IP=${FABRIC_IP}" >> /home/ubuntu/env_var

export MANAGEMENT_IP="${MANAGEMENT_IP}"
echo "export MANAGEMENT_IP=${MANAGEMENT_IP}" >> /home/ubuntu/env_var

echo "export WEBSMSD_PORT=@@web_port@@" >> /home/ubuntu/env_var
echo "# export SMS_PORT=8080" >> /home/ubuntu/env_var
echo "export SMS_PORT=@@sms_port@@" >> /home/ubuntu/env_var
echo "export TELE_SRV=${HOSTNAME}" >> /home/ubuntu/env_var
echo "# export DOMAIN=@@domain@@" >> /home/ubuntu/env_var
echo "export DOMAIN=docker.localhost" >> /home/ubuntu/env_var
echo "export SYSLOG_LEVEL=@@sys_log@@" >> /home/ubuntu/env_var
echo "" >> /home/ubuntu/env_var
echo "export UE_ID_01=@@ue_id_01@@" >> /home/ubuntu/env_var
echo "export UE_USER_01_FULLNAME=@@ue_user_01_fullname@@" >> /home/ubuntu/env_var
echo "" >> /home/ubuntu/env_var
echo "export UE_ID_02=@@ue_id_02@@001010000000002" >> /home/ubuntu/env_var
echo "export UE_USER_02_FULLNAME=@@ue_user_02_fullname@@" >> /home/ubuntu/env_var

cat /home/ubuntu/env_var

./update_ims

sleep 2

docker ps -a

echo "IMS started $(date +'%F %T.%N %Z')"

exit 0

    """
