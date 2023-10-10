class MySQLUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/mysql/ || exit

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

127.0.0.1	mysql

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

export DOMAIN="${DOMAIN}"
echo "export DOMAIN=${DOMAIN}" >> env_var

export HOSTNAME="${HOSTNAME}"
echo "export MYSQL_HOSTNAME=${HOSTNAME}" >> env_var

export MYSQL_FQDN="${FQDN_HOSTNAME}"
echo "export MYSQL_FQDN=${MYSQL_FQDN}" >> env_var

echo "The MYSQL FQDN is ${MYSQL_FQDN}"
echo "The MYSQL HOSTNAME is ${MYSQL_HOSTNAME}"


export TZ="@@tz@@"
echo "export TZ=@@tz@@" >> env_var

export MYSQL_DATABASE="@@mysql_database@@"
echo "export MYSQL_DATABASE=@@mysql_database@@" >> env_var

export MYSQL_USER="@@mysql_user@@"
echo "export MYSQL_USER=@@mysql_user@@" >> env_var

export MYSQL_PASSWORD="@@mysql_password@@"
echo "export MYSQL_PASSWORD=@@mysql_password@@" >> env_var

export MYSQL_ROOT_PASSWORD="@@mysql_root_password@@"
echo "export MYSQL_ROOT_PASSWORD=@@mysql_root_password@@" >> env_var

export FABRIC_IP="${FABRIC_IP}"
echo "export FABRIC_IP=${FABRIC_IP}" >> env_var

export MANAGEMENT_IP="${MANAGEMENT_IP}"
echo "export MANAGEMENT_IP=${MANAGEMENT_IP}" >> env_var

export UE_ID="@@ue_id@@"
echo "export UE_ID=@@ue_id@@" >> env_var

export ENC_PERMANENT_KEY="@@enc_permanent_key@@"
echo "export ENC_PERMANENT_KEY=@@enc_permanent_key@@" >> env_var

export PROTECTION_PARAMETER_ID="@@protection_parameter_id@@"
echo "export PROTECTION_PARAMETER_ID=@@protection_parameter_id@@" >> env_var

export ENC_OPC_KEY="@@enc_opc_key@@"
echo "export ENC_OPC_KEY=@@enc_opc_key@@" >> env_var

export SUPI="@@ue_id@@"
echo "export SUPI=@@ue_id@@" >> env_var

export SERVING_PLMN_ID="@@serving_plmn_id@@"
echo "export SERVING_PLMN_ID=@@serving_plmn_id@@" >> env_var

export SST="@@sst@@"
echo "export SST=@@sst@@" >> env_var

export DNN='@@dnn@@'
echo -e "export DNN='@@dnn@@'" >> env_var

cat env_var

./update_mysql

sleep 2

docker ps -a

echo "MySQL started $(date +'%F %T.%N %Z')"

exit 0

    """
