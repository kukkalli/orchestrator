import logging

from templates.user_data.authorized_keys import AuthorizedKeys
from templates.user_data.script_head import ScriptHead

LOG = logging.getLogger(__name__)


class CommonUserData:
    USERDATA = ScriptHead.USERDATA + AuthorizedKeys.USERDATA + """

DOMAIN="@@domain@@"

echo "Configure networks: $(date +"%T")"
echo "Configure networks: $(date +"%T")" >> /home/ubuntu/log_startup.log

INTERFACES=$(find /sys/class/net -mindepth 1 -maxdepth 1 ! -name lo ! -name docker -printf "%P " -execdir cat {}/address \;)

first=true
interface_name=""
sudo rm /etc/network/interfaces.d/50-cloud-init.cfg
sudo -- sh -c "echo '# This file is generated from information provided by' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# the datasource.  Changes to it will not persist across an instance.' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# To disable cloud-init's network configuration capabilities, write a file' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# network: {config: disabled}' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '            ' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo 'auto lo' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo 'iface lo inet loopback' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '            ' >> /etc/network/interfaces.d/50-cloud-init.cfg"

# shellcheck disable=SC2068
for i in ${INTERFACES[@]};
do
    if ${first}
    then
        first=false
        interface_name=${i}
        sudo -- sh -c "echo 'auto ${interface_name}' >> /etc/network/interfaces.d/50-cloud-init.cfg"
        sudo -- sh -c "echo 'iface ${interface_name} inet dhcp' >> /etc/network/interfaces.d/50-cloud-init.cfg"
    else
        first=true
        sudo -- sh -c "echo '            ' >> /etc/network/interfaces.d/50-cloud-init.cfg"
    fi
done

sudo rm /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
sudo -- sh -c "echo '# network: {config: disabled}' >> /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"
sudo -- sh -c "echo 'network: {config: disabled}' >> /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"
echo "Configured networks: $(date +"%T")" >> /home/ubuntu/log_startup.log
echo "Configured networks: $(date +"%T")"

# sudo systemctl restart networking.service

export HOSTNAME=$(hostname -s)

sudo hostnamectl set-hostname "${HOSTNAME}"."${DOMAIN}"

FQDN_HOSTNAME=$(hostname)

echo "Add hosts file: $(date +"%T")" >> /home/ubuntu/log_startup.log
echo "Add hosts file: $(date +"%T")"

sudo rm /etc/hosts
cat >> /etc/hosts << EOF
127.0.0.1  localhost
127.0.1.1  ${FQDN_HOSTNAME} ${HOSTNAME}

# The following lines are desirable for IPv6 capable hosts'
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts


EOF

IP_ADDR=$(ip address |grep ens|grep inet|awk '{print $2}'| awk -F / '{print $1}')
sudo -- sh -c "echo '' >>  /etc/hosts"

for i in $IP_ADDR; do
    sudo -- sh -c "echo $i $HOSTNAME $FQDN_HOSTNAME >> /etc/hosts"
    if [[ $i == "10.10"* ]];
    then
      export MANAGEMENT_IP=$i
      export MANAGEMENT_INTERFACE_NAME=$(ip a | grep ens | grep $MANAGEMENT_IP | awk '{print $7}')
    fi
    if [[ $i == "10.11"* ]];
    then
      export FABRIC_IP=$i
      export FABRIC_INTERFACE_NAME=$(ip a | grep ens | grep $FABRIC_IP | awk '{print $7}')
    fi
done

ip -o -f inet addr show | awk '/scope global/ {print $4}'
IP_ADDRESS_SUBNET_MASK=$(ip -o -f inet addr show | awk '/scope global/ {print $4}')

for i in $IP_ADDRESS_SUBNET_MASK; do
    if [[ $i == "10.10"* ]];
    then
      echo "Management IP SN: $i"
      export MANAGEMENT_IP_SN=$i
    fi

    if [[ $i == "10.11"* ]];
    then
      echo "Fabric IP SN: $i"
      export FABRIC_IP_SN=$i
    fi
done

echo "MANAGEMENT_IP_SN: ${MANAGEMENT_IP_SN}"
echo "MANAGEMENT_INTERFACE_NAME: ${MANAGEMENT_INTERFACE_NAME}"
echo "FABRIC_IP_SN: ${FABRIC_IP_SN}"
echo "FABRIC_INTERFACE_NAME: ${FABRIC_INTERFACE_NAME}"
echo "IP_ADDRESS_SUBNET_MASK: ${IP_ADDRESS_SUBNET_MASK}"
echo "Added hosts file: $(date +"%T")" >> /home/ubuntu/log_startup.log


    """
