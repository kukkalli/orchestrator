class MySQLUserData:
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

127.0.0.1	mysql

# OAI 5GCN VM IPs
EOF

echo "@@mysql_ip@@\tmysql" >> /home/ubuntu/hosts
echo "@@ims_ip@@\tasterisk-ims" >> /home/ubuntu/hosts
echo "@@nrf_ip@@\toai-nrf" >> /home/ubuntu/hosts
echo "@@udr_ip@@\toai-udr" >> /home/ubuntu/hosts
echo "@@udm_ip@@\toai-udm" >> /home/ubuntu/hosts
echo "@@ausf_ip@@\toai-ausf" >> /home/ubuntu/hosts
echo "@@amf_ip@@\toai-amf" >> /home/ubuntu/hosts
echo "@@smf_ip@@\toai-smf" >> /home/ubuntu/hosts
echo "@@upf_ip@@\toai-spgwu" >> /home/ubuntu/hosts
echo "@@trf_ip@@\toai-trf-gen" >> /home/ubuntu/hosts
echo "" >> /home/ubuntu/hosts

cp /home/ubuntu/hosts /etc/hosts

TZ="@@tz@@"
MYSQL_DATABASE="@@mysql_database@@"
MYSQL_USER="@@mysql_user@@"
MYSQL_PASSWORD="@@mysql_password@@"
MYSQL_ROOT_PASSWORD="@@mysql_root_password@@"

UE_ID="@@ue_id@@"
ENC_PERMANENT_KEY="@@enc_permanent_key@@"
PROTECTION_PARAMETER_ID="@@protection_parameter_id@@"
ENC_OPC_KEY="@@enc_opc_key@@"

SERVING_PLMN_ID="@@serving_plmn_id@@"
SST="@@sst@@"

DNN=@@dnn@@

# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

rm -f env_var

export DOMAIN="${DOMAIN}"
echo "export DOMAIN=${DOMAIN}" >> /home/ubuntu/env_var

export HOSTNAME="${HOSTNAME}"
echo "export MYSQL_HOSTNAME=${HOSTNAME}" >> /home/ubuntu/env_var

export MYSQL_FQDN="${FQDN_HOSTNAME}"
echo "export MYSQL_FQDN=${MYSQL_FQDN}" >> /home/ubuntu/env_var

echo "The MYSQL FQDN is ${MYSQL_FQDN}"
echo "The MYSQL HOSTNAME is ${MYSQL_HOSTNAME}"


export TZ="@@tz@@"
echo "export TZ=@@tz@@" >> /home/ubuntu/env_var

export MYSQL_DATABASE="@@mysql_database@@"
echo "export MYSQL_DATABASE=@@mysql_database@@" >> /home/ubuntu/env_var

export MYSQL_USER="@@mysql_user@@"
echo "export MYSQL_USER=@@mysql_user@@" >> /home/ubuntu/env_var

export MYSQL_PASSWORD="@@mysql_password@@"
echo "export MYSQL_PASSWORD=@@mysql_password@@" >> /home/ubuntu/env_var

export MYSQL_ROOT_PASSWORD="@@mysql_root_password@@"
echo "export MYSQL_ROOT_PASSWORD=@@mysql_root_password@@" >> /home/ubuntu/env_var

export FABRIC_IP="${FABRIC_IP}"
echo "export FABRIC_IP=${FABRIC_IP}" >> /home/ubuntu/env_var

export MANAGEMENT_IP="${MANAGEMENT_IP}"
echo "export MANAGEMENT_IP=${MANAGEMENT_IP}" >> /home/ubuntu/env_var

export UE_ID="@@ue_id@@"
echo "export UE_ID=@@ue_id@@" >> /home/ubuntu/env_var

export ENC_PERMANENT_KEY="@@enc_permanent_key@@"
echo "export ENC_PERMANENT_KEY=@@enc_permanent_key@@" >> /home/ubuntu/env_var

export PROTECTION_PARAMETER_ID="@@protection_parameter_id@@"
echo "export PROTECTION_PARAMETER_ID=@@protection_parameter_id@@" >> /home/ubuntu/env_var

export ENC_OPC_KEY="${ENC_OPC_KEY}"
echo "export ENC_OPC_KEY=${ENC_OPC_KEY}" >> /home/ubuntu/env_var

export SUPI="@@ue_id@@"
echo "export SUPI=@@ue_id@@" >> /home/ubuntu/env_var

export SERVING_PLMN_ID="@@serving_plmn_id@@"
echo "export SERVING_PLMN_ID=${SERVING_PLMN_ID}" >> /home/ubuntu/env_var

export SST="@@sst@@"
echo "export SST=${SST}" >> /home/ubuntu/env_var

export DNN='@@dnn@@'
echo -e "export DNN=@@dnn@@" >> /home/ubuntu/env_var

cat /home/ubuntu/env_var

./update_oai_sql

sleep 2

docker ps -a

echo "MySQL started $(date +'%F %T.%N %Z')"

exit 0

    """
