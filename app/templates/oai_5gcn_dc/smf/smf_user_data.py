class SMFUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/smf/ || exit

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

export IMAGE_NAME="@@image_name@@"
echo -e "export IMAGE_NAME=\"@@image_name@@\"" >> env_var

export DOMAIN="${DOMAIN}"
echo -e "export DOMAIN=${DOMAIN}" >> env_var

export HOSTNAME="${HOSTNAME}"
echo -e "export HOSTNAME=${HOSTNAME}" >> env_var

export TZ="@@tz@@"
echo -e "export TZ=@@tz@@" >> env_var

echo -e "# SMF Config
echo -e "export SMF_FQDN='@@SMF_FQDN@@'" >> env_var
echo -e "export SMF_PORT_FOR_SBI=@@SMF_PORT_FOR_SBI@@" >> env_var
echo -e "export SMF_HTTP2_PORT_FOR_SBI=@@SMF_HTTP2_PORT_FOR_SBI@@" >> env_var
echo -e "export SMF_API_VERSION_FOR_SBI=@@SMF_API_VERSION_FOR_SBI@@" >> env_var
echo -e "export AMF_PORT=@@AMF_PORT@@" >> env_var
echo -e "export AMF_API_VERSION=@@AMF_API_VERSION@@" >> env_var

echo -e "# Session Management Subscription List 01
echo -e "export SM_01_NSSAI_SST=@@SM_01_NSSAI_SST@@" >> env_var
echo -e "export SM_01_NSSAI_SD='@@SM_01_NSSAI_SD@@'" >> env_var
echo -e "export SM_01_DNN='@@SM_01_DNN@@'" >> env_var
echo -e "export SM_01_DEFAULT_SESSION_TYPE=@@SM_01_DEFAULT_SESSION_TYPE@@" >> env_var
echo -e "export SM_01_DEFAULT_SSC_MODE=@@SM_01_DEFAULT_SSC_MODE@@" >> env_var
echo -e "export SM_01_QOS_PROFILE_5QI=@@SM_01_QOS_PROFILE_5QI@@" >> env_var
echo -e "export SM_01_QOS_PROFILE_PRIORITY_LEVEL=@@SM_01_QOS_PROFILE_PRIORITY_LEVEL@@" >> env_var
echo -e "export SM_01_QOS_PROFILE_ARP_PRIORITY_LEVEL=@@SM_01_QOS_PROFILE_ARP_PRIORITY_LEVEL@@" >> env_var
echo -e "export SM_01_QOS_PROFILE_ARP_PREEMPTCAP=@@SM_01_QOS_PROFILE_ARP_PREEMPTCAP@@" >> env_var
echo -e "export SM_01_QOS_PROFILE_ARP_PREEMPTVULN=@@SM_01_QOS_PROFILE_ARP_PREEMPTVULN@@" >> env_var
echo -e "export SM_01_SESSION_AMBR_UL=@@SM_01_SESSION_AMBR_UL@@" >> env_var
echo -e "export SM_01_SESSION_AMBR_DL=@@SM_01_SESSION_AMBR_DL@@" >> env_var

echo -e "# Session Management Subscription List 02
echo -e "export SM_02_NSSAI_SST=@@SM_02_NSSAI_SST@@" >> env_var
echo -e "export SM_02_NSSAI_SD=@@SM_02_NSSAI_SD@@" >> env_var
echo -e "export SM_02_DNN=@@SM_02_DNN@@" >> env_var
echo -e "export SM_02_DEFAULT_SESSION_TYPE=@@SM_02_DEFAULT_SESSION_TYPE@@" >> env_var
echo -e "export SM_02_DEFAULT_SSC_MODE=@@SM_02_DEFAULT_SSC_MODE@@" >> env_var
echo -e "export SM_02_QOS_PROFILE_5QI=@@SM_02_QOS_PROFILE_5QI@@" >> env_var
echo -e "export SM_02_QOS_PROFILE_PRIORITY_LEVEL=@@SM_02_QOS_PROFILE_PRIORITY_LEVEL@@" >> env_var
echo -e "export SM_02_QOS_PROFILE_ARP_PRIORITY_LEVEL=@@SM_02_QOS_PROFILE_ARP_PRIORITY_LEVEL@@" >> env_var
echo -e "export SM_02_QOS_PROFILE_ARP_PREEMPTCAP=@@SM_02_QOS_PROFILE_ARP_PREEMPTCAP@@" >> env_var
echo -e "export SM_02_QOS_PROFILE_ARP_PREEMPTVULN=@@SM_02_QOS_PROFILE_ARP_PREEMPTVULN@@" >> env_var
echo -e "export SM_02_SESSION_AMBR_UL=@@SM_02_SESSION_AMBR_UL@@" >> env_var
echo -e "export SM_02_SESSION_AMBR_DL=@@SM_02_SESSION_AMBR_DL@@" >> env_var

echo -e "# Session Management Subscription List 03
echo -e "export SM_03_NSSAI_SST=@@SM_03_NSSAI_SST@@" >> env_var
echo -e "export SM_03_NSSAI_SD=@@SM_03_NSSAI_SD@@" >> env_var
echo -e "export SM_03_DNN=@@SM_03_DNN@@" >> env_var
echo -e "export SM_03_DEFAULT_SESSION_TYPE=@@SM_03_DEFAULT_SESSION_TYPE@@" >> env_var
echo -e "export SM_03_DEFAULT_SSC_MODE=@@SM_03_DEFAULT_SSC_MODE@@" >> env_var
echo -e "export SM_03_QOS_PROFILE_5QI=@@SM_03_QOS_PROFILE_5QI@@" >> env_var
echo -e "export SM_03_QOS_PROFILE_PRIORITY_LEVEL=@@SM_03_QOS_PROFILE_PRIORITY_LEVEL@@" >> env_var
echo -e "export SM_03_QOS_PROFILE_ARP_PRIORITY_LEVEL=@@SM_03_QOS_PROFILE_ARP_PRIORITY_LEVEL@@" >> env_var
echo -e "export SM_03_QOS_PROFILE_ARP_PREEMPTCAP=@@SM_03_QOS_PROFILE_ARP_PREEMPTCAP@@" >> env_var
echo -e "export SM_03_QOS_PROFILE_ARP_PREEMPTVULN=@@SM_03_QOS_PROFILE_ARP_PREEMPTVULN@@" >> env_var
echo -e "export SM_03_SESSION_AMBR_UL=@@SM_03_SESSION_AMBR_UL@@" >> env_var
echo -e "export SM_03_SESSION_AMBR_DL=@@SM_03_SESSION_AMBR_DL@@" >> env_var

echo -e "# Docker config variables
echo -e "export SMF_INTERFACE_NAME_FOR_N4=@@SMF_INTERFACE_NAME_FOR_N4@@" >> env_var
echo -e "export SMF_INTERFACE_NAME_FOR_SBI=@@SMF_INTERFACE_NAME_FOR_SBI@@" >> env_var
echo -e "export DEFAULT_DNS_IPV4_ADDRESS='@@DEFAULT_DNS_IPV4_ADDRESS@@'" >> env_var
echo -e "export DEFAULT_DNS_SEC_IPV4_ADDRESS='@@DEFAULT_DNS_SEC_IPV4_ADDRESS@@'" >> env_var
echo -e "export AMF_IPV4_ADDRESS=@@amf_ip@@" >> env_var
echo -e "export AMF_FQDN=@@AMF_FQDN@@" >> env_var
echo -e "export UDM_IPV4_ADDRESS=@@udm_ip@@" >> env_var
echo -e "export UDM_FQDN=@@UDM_FQDN@@" >> env_var
echo -e "export UPF_IPV4_ADDRESS=@@upf_ip@@" >> env_var
echo -e "export UPF_FQDN_0=@@UPF_FQDN_0@@" >> env_var
echo -e "export NRF_IPV4_ADDRESS=@@nrf_ip@@" >> env_var
echo -e "export NRF_FQDN=@@NRF_FQDN@@" >> env_var
echo -e "export USE_LOCAL_SUBSCRIPTION_INFO=@@USE_LOCAL_SUBSCRIPTION_INFO@@" >> env_var
echo -e "export REGISTER_NRF=@@REGISTER_NRF@@" >> env_var
echo -e "export DISCOVER_UPF=@@DISCOVER_UPF@@" >> env_var
echo -e "export USE_FQDN_DNS=@@USE_FQDN_DNS@@" >> env_var
echo -e "export UE_MTU=@@UE_MTU@@" >> env_var

echo -e "# Slice 0 (1, 0xFFFFFF)
echo -e "export DNN_NI0=@@DNN_NI0@@" >> env_var
echo -e "export TYPE0=@@TYPE0@@" >> env_var
echo -e "export DNN_RANGE0='@@DNN_RANGE0@@'" >> env_var
echo -e "export NSSAI_SST0=@@NSSAI_SST0@@" >> env_var
echo -e "export SESSION_AMBR_UL0=@@SESSION_AMBR_UL0@@" >> env_var
echo -e "export SESSION_AMBR_DL0=@@SESSION_AMBR_DL0@@" >> env_var
echo -e "# Slice 1 (1, 0xFFFFFF)
echo -e "export DNN_NI1=@@DNN_NI1@@" >> env_var
echo -e "export TYPE1=@@TYPE1@@" >> env_var
echo -e "export DNN_RANGE1='@@DNN_RANGE1@@'" >> env_var
echo -e "export NSSAI_SST1=@@NSSAI_SST1@@" >> env_var
echo -e "export SESSION_AMBR_UL1=@@SESSION_AMBR_UL1@@" >> env_var
echo -e "export SESSION_AMBR_DL1=@@SESSION_AMBR_DL1@@" >> env_var
echo -e "# Slice 2 for ims
echo -e "export DNN_NI2=@@DNN_NI2@@" >> env_var
echo -e "export TYPE2=@@TYPE2@@" >> env_var
echo -e "export DNN_RANGE2='@@DNN_RANGE2@@'" >> env_var
echo -e "export NSSAI_SST2=@@NSSAI_SST2@@" >> env_var
echo -e "export SESSION_AMBR_UL2=@@SESSION_AMBR_UL2@@" >> env_var
echo -e "export SESSION_AMBR_DL2=@@SESSION_AMBR_DL2@@" >> env_var

echo -e "# IMS server
echo -e "export DEFAULT_CSCF_IPV4_ADDRESS=@@ims_ip@@" >> env_var

cat env_var

./deploy

sleep 2

docker ps -a

echo "SMF started $(date +'%F %T.%N %Z')"

exit 0

    """
