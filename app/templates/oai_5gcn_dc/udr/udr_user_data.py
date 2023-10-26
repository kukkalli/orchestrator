class UDRUserData:
    USERDATA = """
# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/5g/udr/ || exit

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

127.0.0.1	oai-udr

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

export TZ="@@tz@@"
echo "export TZ=@@tz@@" >> env_var

export LOG_LEVEL=@@log_level@@
echo "export LOG_LEVEL=@@log_level@@" >> env_var

echo -e "# Database Parameters" >> env_var
echo -e "export MYSQL_SERVER='@@mysql_server@@'" >> env_var
echo -e "export MYSQL_IPV4_ADDRESS='@@mysql_ip@@'" >> env_var
echo -e "export MYSQL_USER='@@mysql_user@@'" >> env_var
echo -e "export MYSQL_PASS='@@mysql_pass@@'" >> env_var
echo -e "export MYSQL_DB='@@mysql_db@@'" >> env_var

echo -e "# Docker Compose Parameters" >> env_var
echo -e "export UDR_NAME='@@udr_name@@'" >> env_var
echo -e "export UDR_INTERFACE_NAME_FOR_NUDR='@@udr_interface_name_for_nudr@@'" >> env_var
echo -e "export DB_CONNECTION_TIMEOUT='@@db_connection_timeout@@'" >> env_var
echo -e "export WAIT_MYSQL='@@wait_mysql@@'" >> env_var
echo -e "export USE_FQDN_DNS='@@use_fqdn_dns@@'" >> env_var
echo -e "export REGISTER_NRF='@@register_nrf@@'" >> env_var
echo -e "export NRF_HOSTNAME='@@nrf_hostname@@'" >> env_var
echo -e "export NRF_IPV4_ADDRESS='@@nrf_ip@@'" >> env_var
echo -e "export NRF_FQDN='@@nrf_fqdn@@'" >> env_var
echo -e "export DOMAIN='@@domain@@'" >> env_var
echo -e "" >> env_var

echo -e "# PLMN list 01" >> env_var
echo -e "export MCC_01='@@mcc_01@@'" >> env_var
echo -e "export MNC_01='@@mnc_01@@'" >> env_var
echo -e "export AMF_REGION_ID_01='@@amf_region_id_01@@'" >> env_var
echo -e "export AMF_SET_ID_01='@@amf_set_id_01@@'" >> env_var
echo -e "export AMF_POINTER_01='@@amf_pointer_01@@'" >> env_var
echo -e "" >> env_var

echo -e "# PLMN list 02" >> env_var
echo -e "export MCC_02='@@mcc_02@@'" >> env_var
echo -e "export MNC_02='@@mnc_02@@'" >> env_var
echo -e "export AMF_REGION_ID_02='@@amf_region_id_02@@'" >> env_var
echo -e "export AMF_SET_ID_02='@@amf_set_id_02@@'" >> env_var
echo -e "export AMF_POINTER_02='@@amf_pointer_02@@'" >> env_var
echo -e "" >> env_var

echo -e "# PLMN Support List" >> env_var
echo -e "export PLMN_SL_MCC='@@plmn_sl_mcc@@'" >> env_var
echo -e "export PLMN_SL_MNC='@@plmn_sl_mnc@@'" >> env_var
echo -e "export PLMN_SL_TAC='@@plmn_sl_tac@@'" >> env_var
echo -e "" >> env_var

echo -e "# NSSAI Set 01" >> env_var
echo -e "export NSSAI_SST_01='@@nssai_sst_01@@'" >> env_var
echo -e "" >> env_var

echo -e "# NSSAI Set 02" >> env_var
echo -e "export NSSAI_SST_02='@@nssai_sst_02@@'" >> env_var
echo -e "export NSSAI_SD_02='@@nssai_sd_02@@'" >> env_var
echo -e "" >> env_var

echo -e "# NSSAI Set 03" >> env_var
echo -e "export NSSAI_SST_03='@@nssai_sst_03@@'" >> env_var
echo -e "export NSSAI_SD_03='@@nssai_sd_03@@'" >> env_var
echo -e "" >> env_var

echo -e "# IMS IPv4" >> env_var
echo -e "export IMS_IPV4='@@ims_ip@@'" >> env_var
echo -e "" >> env_var

echo -e "# DNN List" >> env_var
echo -e "# DNN 01" >> env_var
echo -e "export DNN_01_SST='@@dnn_01_sst@@'" >> env_var
echo -e "export DNN_01_DNN='@@dnn_01_dnn@@'" >> env_var
echo -e "export DNN_01_5QI='@@dnn_01_5qi@@'" >> env_var
echo -e "export DNN_01_SESSION_AMBR_UL='@@dnn_01_session_ambr_ul@@'" >> env_var
echo -e "export DNN_01_SESSION_AMBR_DL='@@dnn_01_session_ambr_dl@@'" >> env_var
echo -e "export DNN_01_PDU_SESSION_TYPE='@@dnn_01_pdu_session_type@@'" >> env_var
echo -e "" >> env_var

echo -e "# DNN 02" >> env_var
echo -e "export DNN_02_SST='@@dnn_02_sst@@'" >> env_var
echo -e "export DNN_02_SD='@@dnn_02_sd@@'" >> env_var
echo -e "export DNN_02_DNN='@@dnn_02_dnn@@'" >> env_var
echo -e "export DNN_02_5QI='@@dnn_02_5qi@@'" >> env_var
echo -e "export DNN_02_SESSION_AMBR_UL='@@dnn_02_session_ambr_ul@@'" >> env_var
echo -e "export DNN_02_SESSION_AMBR_DL='@@dnn_02_session_ambr_dl@@'" >> env_var
echo -e "export DNN_02_PDU_SESSION_TYPE='@@dnn_02_pdu_session_type@@'" >> env_var
echo -e "" >> env_var

echo -e "# Default DNN" >> env_var
echo -e "export DNN_DEF_SST='@@dnn_def_sst@@'" >> env_var
echo -e "export DNN_DEF_SD='@@dnn_def_sd@@'" >> env_var
echo -e "export DNN_DEF_DNN='@@dnn_def_dnn@@'" >> env_var
echo -e "export DNN_DEF_5QI='@@dnn_def_5qi@@'" >> env_var
echo -e "export DNN_DEF_SESSION_AMBR_UL='@@dnn_def_session_ambr_ul@@'" >> env_var
echo -e "export DNN_DEF_SESSION_AMBR_DL='@@dnn_def_session_ambr_dl@@'" >> env_var
echo -e "export DNN_DEF_PDU_SESSION_TYPE='@@dnn_def_pdu_session_type@@'" >> env_var
echo -e "" >> env_var

echo -e "# IMS" >> env_var
echo -e "export DNN_IMS='@@dnn_ims@@'" >> env_var
echo -e "export DNN_IMS_PDU_SESSION_TYPE='@@dnn_ims_pdu_session_type@@'" >> env_var

cat env_var

sudo chown ubuntu:ubuntu $(pwd)/*

./deploy

sleep 2

docker ps -a

echo "UDR started $(date +'%F %T.%N %Z')"

exit 0

    """
