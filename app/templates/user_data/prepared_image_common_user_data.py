import logging

from templates.user_data.authorized_keys import AuthorizedKeys
from templates.user_data.script_head import ScriptHead

LOG = logging.getLogger(__name__)


class CommonOAI5GCNUserData:
    USERDATA = ScriptHead.USERDATA + AuthorizedKeys.USERDATA + """
DOMAIN="@@domain@@"

echo "Domain: ${DOMAIN}"

INTERFACES=$(find /sys/class/net -mindepth 1 -maxdepth 1 ! -name lo ! -name docker -printf "%P " -execdir cat {}/address \;)

echo "The interfaces: ${INTERFACES}"

first=true
interface_name=""
# sudo rm /etc/netplan/50-cloud-init.yaml
sudo -- sh -c "echo 'network:' > /etc/netplan/50-cloud-init.yaml"
sudo -- sh -c "echo '    ethernets:' >> /etc/netplan/50-cloud-init.yaml"

# shellcheck disable=SC2068
for i in ${INTERFACES[@]};
do
    if ${first}
    then
        first=false
        interface_name=${i}
        sudo -- sh -c "echo '        ${interface_name}:' >> /etc/netplan/50-cloud-init.yaml"
        sudo -- sh -c "echo '            dhcp4: true' >> /etc/netplan/50-cloud-init.yaml"
    else
        first=true
        sudo -- sh -c "echo '            match:' >> /etc/netplan/50-cloud-init.yaml"
        sudo -- sh -c "echo '                macaddress: ${i}' >> /etc/netplan/50-cloud-init.yaml"
        sudo -- sh -c "echo '            set-name: ${interface_name}' >> /etc/netplan/50-cloud-init.yaml"
   fi
done

sudo -- sh -c "echo '    version: 2' >> /etc/netplan/50-cloud-init.yaml"

echo "-------------- Netplan Yaml --------------"
cat /etc/netplan/50-cloud-init.yaml
echo "-------------- Netplan Yaml --------------"

sudo -- sh -c "echo 'network: {config: disabled}' >> /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"

sudo netplan apply

HOSTNAME=$(hostname -s)

sudo hostnamectl set-hostname "$HOSTNAME"."$DOMAIN"

FQDN_HOSTNAME=$(hostname)

sudo rm /etc/hosts
cat > /etc/hosts << EOF
127.0.0.1  localhost
127.0.1.1  ${HOSTNAME} ${FQDN_HOSTNAME}

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
echo "IP Address: $IP_ADDR"

for i in $IP_ADDR; do
    sudo -- sh -c "echo $i $HOSTNAME $FQDN_HOSTNAME >> /etc/hosts"
    if [[ $i == "10.10"* ]];
    then
      MANAGEMENT_IP=$i
    fi
    if [[ $i == "10.11"* ]];
    then
      export FABRIC_IP=$i
    fi
done

cat /etc/hosts

echo "--------------- docker compose version is: ---------------"
docker compose version
echo "--------------- docker compose version is: $(docker compose version)" >> /home/ubuntu/log_startup.log

    """
