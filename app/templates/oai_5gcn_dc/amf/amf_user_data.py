class AMFUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/amf/ || exit

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
echo "@@upf_ip@@\toai-spgwu-tiny" >> hosts
echo "@@trf_ip@@\toai-trf-gen" >> hosts
echo "" >> hosts

sudo cp hosts /etc/hosts

echo -e "export IMAGE_NAME='@@image_name@@'" >> env_var
echo -e "export TZ=@@tz@@" >> env_var
echo -e "export AMF_NAME=@@amf_name@@" >> env_var
echo -e "export LOG_LEVEL=@@log_level@@" >> env_var
echo -e "export AMF_INTERFACE_NAME_FOR_NGAP=@@AMF_INTERFACE_NAME_FOR_NGAP@@" >> env_var
echo -e "export AMF_PORT_NGAP=@@AMF_PORT_NGAP@@" >> env_var
echo -e "export AMF_INTERFACE_NAME_FOR_SBI=@@AMF_INTERFACE_NAME_FOR_SBI@@" >> env_var
echo -e "export AMF_PORT_SBI=@@AMF_PORT_SBI@@" >> env_var
echo -e "export AMF_API_VERSION_SBI=@@AMF_API_VERSION_SBI@@" >> env_var
echo -e "export AMF_HTTP2_PORT_SBI=@@AMF_HTTP2_PORT_SBI@@" >> env_var
echo -e "export USE_FQDN_DNS=@@USE_FQDN_DNS@@" >> env_var
echo -e "export REGISTER_NRF=@@REGISTER_NRF@@" >> env_var
echo -e "export EXTERNAL_AUSF=@@EXTERNAL_AUSF@@" >> env_var

echo -e "# SMF Info" >> env_var
echo -e "export SMF_01_INSTANCE_ID=@@SMF_01_INSTANCE_ID@@" >> env_var
echo -e "export SMF_01_IPV4_ADDRESS=@@smf_ip@@" >> env_var
echo -e "export SMF_01_PORT=@@SMF_01_PORT@@" >> env_var
echo -e "export SMF_01_HTTP2_PORT=@@SMF_01_HTTP2_PORT@@" >> env_var
echo -e "export SMF_01_VERSION=@@SMF_01_VERSION@@" >> env_var
echo -e "export SMF_01_FQDN=@@SMF_01_FQDN@@" >> env_var
echo -e "export SMF_01_SELECTED=@@SMF_01_SELECTED@@" >> env_var

echo -e "# NRF Info" >> env_var
echo -e "export NRF_IPV4_ADDRESS=@@nrf_ip@@" >> env_var
echo -e "export NRF_PORT=@@NRF_PORT@@" >> env_var
echo -e "export NRF_API_VERSION=@@NRF_API_VERSION@@" >> env_var
echo -e "export NRF_FQDN=@@NRF_FQDN@@" >> env_var

echo -e "# AUSF Info" >> env_var
echo -e "export AUSF_IPV4_ADDRESS=@@ausf_ip@@" >> env_var
echo -e "export AUSF_PORT=@@AUSF_PORT@@" >> env_var
echo -e "export AUSF_API_VERSION=@@AUSF_API_VERSION@@" >> env_var
echo -e "export AUSF_FQDN=@@AUSF_FQDN@@" >> env_var

echo -e "# UDM Info" >> env_var
echo -e "export UDM_IPV4_ADDRESS=@@udm_ip@@" >> env_var
echo -e "export UDM_PORT=@@UDM_PORT@@" >> env_var
echo -e "export UDM_API_VERSION=@@UDM_API_VERSION@@" >> env_var
echo -e "export UDM_FQDN=@@UDM_FQDN@@" >> env_var

echo -e "# MySQL Info" >> env_var
echo -e "export MYSQL_IPV4_ADDRESS=@@mysql_ip@@" >> env_var
echo -e "export MYSQL_SERVER=@@MYSQL_SERVER@@" >> env_var
echo -e "export MYSQL_USER=@@MYSQL_USER@@" >> env_var
echo -e "export MYSQL_PASS=@@MYSQL_PASS@@" >> env_var
echo -e "export MYSQL_DB=@@MYSQL_DB@@" >> env_var

echo -e "export DOMAIN=@@domain@@" >> env_var

echo -e "# PLMN list 01" >> env_var
echo -e "export MCC_01=@@MCC_01@@" >> env_var
echo -e "export MNC_01=@@MNC_01@@" >> env_var
echo -e "export AMF_REGION_ID_01=@@AMF_REGION_ID_01@@" >> env_var
echo -e "export AMF_SET_ID_01=@@AMF_SET_ID_01@@" >> env_var
echo -e "export AMF_POINTER_01=@@AMF_POINTER_01@@" >> env_var

echo -e "# PLMN Support List" >> env_var
echo -e "export PLMN_SL_MCC=@@PLMN_SL_MCC@@" >> env_var
echo -e "export PLMN_SL_MNC=@@PLMN_SL_MNC@@" >> env_var
echo -e "export PLMN_SL_TAC=@@PLMN_SL_TAC@@" >> env_var
echo -e "#export "PLMN_SL_TAC=0x0001" >> env_var

echo -e "# NSSAI Set 01" >> env_var
echo -e "export NSSAI_SST_01=@@NSSAI_SST_01@@" >> env_var

cat env_var

./deploy

sleep 2

docker ps -a

echo "AMF started $(date +'%F %T.%N %Z')"

exit 0

    """
