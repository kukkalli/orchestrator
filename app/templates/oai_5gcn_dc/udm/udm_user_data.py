class UDMUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/udm/ || exit

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

127.0.0.1	oai-udm

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
echo "export HOSTNAME=${HOSTNAME}" >> env_var

echo -e "export IMAGE_NAME='@@image_name@@'" >> env_var
echo -e "export TZ=@@tz@@" >> env_var
echo -e "export UDM_NAME=@@udm_name@@" >> env_var
echo -e "export SBI_IF_NAME=@@sbi_if_name@@" >> env_var
echo -e "export REGISTER_NRF=@@register_nrf@@" >> env_var
echo -e "export USE_FQDN_DNS=@@use_fqdn_dns@@" >> env_var
echo -e "export UDR_IPV4_ADDRESS=@@udr_ip@@" >> env_var
echo -e "export UDR_FQDN=@@udr_fqdn@@" >> env_var
echo -e "export NRF_IPV4_ADDRESS=@@nrf_ip@@" >> env_var
echo -e "export NRF_FQDN=@@nrf_fqdn@@" >> env_var

cat env_var

./deploy

sleep 2

docker ps -a

echo "UDM started $(date +'%F %T.%N %Z')"

exit 0

    """
