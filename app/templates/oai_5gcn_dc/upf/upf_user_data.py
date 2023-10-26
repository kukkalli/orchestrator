class UPFUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/upf/ || exit

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

127.0.0.1	@@UPF_FQDN@@

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
echo -e "export IMAGE_NAME=\"@@image_name@@\"" >> env_var

export DOMAIN="${DOMAIN}"
echo -e "export DOMAIN=${DOMAIN}" >> env_var

export HOSTNAME="${HOSTNAME}"
echo -e "export HOSTNAME=${HOSTNAME}" >> env_var

export TZ="@@tz@@"
echo -e "export TZ=@@tz@@" >> env_var

echo -e "export UPF_FQDN=@@UPF_FQDN@@" >> env_var
echo -e "export UPF_FQDN_5G=@@UPF_FQDN@@" >> env_var
echo -e "export SMF_IPV4_ADDRESS=@@smf_ip@@" >> env_var
echo -e "export NRF_IPV4_ADDRESS=@@nrf_ip@@" >> env_var
echo -e "export NRF_FQDN=@@NRF_FQDN@@" >> env_var

echo -e "# NSSAI Set 01@@" >> env_var
echo -e "export NSSAI_SST_01=@@NSSAI_SST_01@@" >> env_var
echo -e "export NSSAI_SD_01='@@NSSAI_SD_01@@'" >> env_var
echo -e "export DNN_01=@@DNN_01@@" >> env_var
echo -e "# NSSAI Set 02@@" >> env_var
echo -e "export NSSAI_SST_02=@@NSSAI_SST_02@@" >> env_var
echo -e "export NSSAI_SD_02='@@NSSAI_SD_02@@'" >> env_var
echo -e "export DNN_02=@@DNN_02@@" >> env_var
echo -e "# NSSAI Set 03@@" >> env_var
echo -e "export NSSAI_SST_03=@@NSSAI_SST_03@@" >> env_var
echo -e "export NSSAI_SD_03='@@NSSAI_SD_03@@'" >> env_var
echo -e "export DNN_03=@@DNN_03@@" >> env_var

cat env_var

./deploy

sleep 2

docker ps -a

echo "UPF started $(date +'%F %T.%N %Z')"

exit 0

    """
