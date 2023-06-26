import logging

from templates.user_data.authorized_keys import AuthorizedKeys
from templates.user_data.script_head import ScriptHead

LOG = logging.getLogger(__name__)


class CommonUserData:
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
#        if [[ ${interface_name} == "ens3" ]]; then
#            sudo -- sh -c "echo '            gateway4: 10.10.0.1' >> /etc/netplan/50-cloud-init.yaml"
#            sudo -- sh -c "echo '            nameservers:' >> /etc/netplan/50-cloud-init.yaml"
#            sudo -- sh -c "echo '                addresses:' >> /etc/netplan/50-cloud-init.yaml"
#            sudo -- sh -c "echo '                - 8.8.8.8' >> /etc/netplan/50-cloud-init.yaml"
#        fi
   fi
done

sudo -- sh -c "echo '    version: 2' >> /etc/netplan/50-cloud-init.yaml"

echo "-------------- Netplan Yaml --------------"
cat /etc/netplan/50-cloud-init.yaml
echo "-------------- Netplan Yaml --------------"

sudo -- sh -c "echo 'network: {config: disabled}' >> /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"

sudo netplan apply

#sudo ip route del default
#sudo ip route add default via 10.10.0.1 

ip r

HOSTNAME=$(hostname -s)

sudo hostnamectl set-hostname "$HOSTNAME"."$DOMAIN"

FQDN_HOSTNAME=$(hostname)

while true; do
    wget -q --spider https://google.com

    if [ $? -eq 0 ]; then
        echo "Network is Online : $(date +"%T.%N") --"
        break
    else
        echo "Network is Offline: $(date +"%T.%N") --"
        sleep 2
    fi
done

sudo rm /etc/hosts
cat > /etc/hosts << EOF
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

sudo apt-get update

sudo apt-get install ca-certificates curl gnupg lsb-release -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor \
 -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io -y

docker --version

cat > /etc/docker/daemon.json << EOF
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "1m",
        "max-file": "9"
    },
    "ipv6": true,
    "fixed-cidr-v6": "2001:db8:1::/64"
}
EOF
echo "Configured docker daemon.json file to set log outputs"

sudo usermod -aG docker ubuntu
echo "Allow docker to be run using user as: ubuntu"

sudo systemctl daemon-reload
sudo systemctl restart docker

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

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

echo "--------------- docker-compose version is: ---------------"
docker-compose --version
echo "--------------- docker-compose version is: ---------------"

    """
