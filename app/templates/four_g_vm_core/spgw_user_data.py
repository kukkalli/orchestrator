class SPGWUserData:
    USERDATA = """
echo "SPGW Main User Script: $(date +'%T.%N')"
echo "SPGW Main User Script: $(date +'%T.%N')" >> log_startup.log

HSS_IP=@@hss_ip@@
HSS_HOSTNAME="@@hss_hostname@@"
MME_IP="@@mme_ip@@"
MME_HOSTNAME="@@mme_hostname@@"

sudo -- sh -c "echo $HSS_IP $HSS_HOSTNAME $HSS_HOSTNAME.$DOMAIN >> /etc/hosts"
sudo -- sh -c "echo $MME_IP $MME_HOSTNAME $MME_HOSTNAME.$DOMAIN >> /etc/hosts"

# Change user to ubuntu
echo "Changing user to ubuntu"
su - ubuntu
echo "Changed user to $USER"

cd /home/ubuntu/ || exit
rm -f env_var
export REALM="$DOMAIN"
echo "export REALM=${REALM}" >> env_var
echo "export HSS_IP=${HSS_IP}" >> env_var
echo "export HSS_HOSTNAME=${HSS_HOSTNAME}" >> env_var
echo "export MME_IP=${MME_IP}" >> env_var
echo "export MME_HOSTNAME=${MME_HOSTNAME}" >> env_var
echo "export FABRIC_IP=${MANAGEMENT_IP}" >> env_var
echo "export FABRIC_INTERFACE_NAME=${FABRIC_INTERFACE_NAME}" >> env_var

echo "Starting SPGW: $(date +'%T.%N')" >> log_startup.log
echo "Starting SPGW: $(date +'%T.%N')"
./initialize_oai_spgw
echo "SPGW started: $(date +'%T.%N')" >> log_startup.log
echo "SPGW started: $(date +'%T.%N')"

exit 0

    """
