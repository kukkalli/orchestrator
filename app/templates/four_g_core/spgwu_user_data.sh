#!/bin/bash

cat > /home/ubuntu/.ssh/authorized_keys << EOF
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAGxlZsduAGeKqz3UhzHeXiJOsRlBQTZIyOxA0DrXso9ncDveooDqUr+Xw5XZx44nHFNjWocoQowDdaA8jj0DYEs9wF5ELGj/rm4n6a1b6tXVAlb3Vojb5C0mZfx2gUA6i5GNnNXONRttaW53XeOoD/VDM9tlgBnpa04bBQ1naTiLbQsQg== os@controller
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAFJ/TSfJegktNbVbCF2L1hte8qfDtgk/zArlNq4vgEAKRePSEYnoFldlGVn5zDqnvLP2xy6WrcFUjO2TOeTnmqQ1gEzcBOjUXeYdA7LO1J8yARvvAMOk4IiuVTvGUdCIW8uDpXwfqCxqeKbSudo3LVLgt/ZcRg1QENyRLP/zqixIJoEsA== os@compute01
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACnHtnIvTXuTG2I5ngNXKUYu/h7izkEGPmfZpqIeuXcQIY0miX7k+9snBvPXKuxp5nYspOZuOzsHs4JEE3l/+ftcgHvF7w3SD5CtdTfGMhUwGHtcpWtKfj18+FiDwh9wK4m6exBChpfBTU1q14LPZBR7xg9KZULWGddugmffUK1SMoWdg== os@compute02
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAG6PCMQcMNvSA4yRmHETOYdj60fsJo4n8FOBKmlw2fJR7xWMND0DQWTVvPssv3bw1iKn5zLbx4aeVd7idKT00HsjwB4mX1/+UBVUeP/21tp50J3XsG5Pdwz4JL6LeRWvurKoU66bpBR5u0Iuo9VrJlHfn3GbCiHzke7uUt3QBmBWkxroQ== sdn@sdnc
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACU7DStTMa4kHmnZ6kiNkQHrW4CYW9kOKkR8xQa3yBvPDG0IYv0MuUJg2lY5TfdhmXNWELPYHlZxieOC60HTD/vzACoV3268mlJNYGE+ju4iQq+QXaUSwog4YkQs4aDCpylyDRJYWFe8YP97/xFOzR5P5bxCYcJZQLlwWa/+294kW29hQ== hanif@openstack
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAEBCbxZcyGw+PD3S/HoPx/WKhfGOz4Mos3OGQ4Q2rvh7UpNBE4UVp/xOBcFoL0WveHI+WskQV0jKa7TnErjVwEsOAAX6O4DxaskATGq6XioPv2XmRGKb5UZ28NUCE+VLhUvnFLLn2IMiCSiNzCU8hX0rjsU6/hHjDyV01Iahq2gAY6E7Q== hanif@openstack
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAHLT0AS5MHwwJ6hX1Up5stfz361+IWA/8/MhZBH+mYA32h/Bp5hSWkQDXow4aDiHRlxVV1WLlHHup+GPBBA9XLTRwHP8gAjbP5EM4EVxR9EbDh5Hz13xcN0/n9J9rasefHS8UgTJUgRrWeNRCSAhkbNfDfSeQzk8NWlzhiwwCIUacKnzg== hanif@kukkalli
EOF

DOMAIN="@@domain@@"

INTERFACES=$(find /sys/class/net -mindepth 1 -maxdepth 1 ! -name lo ! -name docker -printf "%P " -execdir cat {}/address \;)

first=true
interface_name=""
sudo rm /etc/netplan/50-cloud-init.yaml
sudo -- sh -c "echo 'network:' >> /etc/netplan/50-cloud-init.yaml"
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

sudo -- sh -c "echo 'network: {config: disabled}' >> /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"

sudo netplan apply

HOSTNAME=$(hostname -s)

sudo hostnamectl set-hostname "$HOSTNAME"."$DOMAIN"

FQDN_HOSTNAME=$(hostname)

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

sudo apt-get install ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
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

sudo usermod -aG docker ubuntu

sudo systemctl daemon-reload
sudo systemctl restart docker

IP_ADDR=$(ip address |grep ens|grep inet|awk '{print $2}'| awk -F / '{print $1}')

sudo -- sh -c "echo '' >>  /etc/hosts"

for i in $IP_ADDR; do
    sudo -- sh -c "echo $i $HOSTNAME $FQDN_HOSTNAME >> /etc/hosts"
    if [[ $i == "10.10"* ]];
    then
      export MANAGEMENT_IP=$i
    fi
    if [[ $i == "10.11"* ]];
    then
      export FABRIC_IP=$i
    fi
done

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

echo "--------------- docker-compose version is: ---------------"
docker-compose --version
echo "--------------- docker-compose version is: ---------------"


echo "--------------- SPGW-U FQDN is: ---------------"
echo "SPGW-U FQDN $FQDN_HOSTNAME"
echo "--------------- SPGW-U FQDN is: ---------------"

export SGWC_IP_ADDRESS="@@sgwc_ip_address@@"
export SGWC_HOSTNAME="@@sgwc_hostname@@"
sudo -- sh -c "echo $SGWC_IP_ADDRESS $SGWC_HOSTNAME $SGWC_HOSTNAME.$DOMAIN >> /etc/hosts"

su - ubuntu

export MANAGEMENT_IP="$MANAGEMENT_IP"
export FABRIC_IP="$FABRIC_IP"
export FABRIC_IP="$MANAGEMENT_IP"

# DOCKER_PASS="@@docker_pass@@"
# docker login -u kukkalli -p ${DOCKER_PASS}

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/4g/spgw-u/ || exit

export DOMAIN="$DOMAIN"
echo "DOMAIN is: $DOMAIN"
export REALM="$DOMAIN"
echo "REALM is: $REALM"

MCC="@@mcc@@"
export MCC="$MCC"
echo "MCC is: $MCC"
MNC="@@mnc@@"
export MNC="$MNC"
echo "MNC is: $MNC"
GW_ID="@@gw_id@@" # 1
export GW_ID="$GW_ID"
echo "GW ID is: $GW_ID"
APN1="@@apn-1@@.ipv4" # tuckn.ipv4
export APN1="$APN1"
echo "APN 1 is: $APN1"
APN2="@@apn-2@@.ipv4" # tuckn2.ipv4
export APN2="$APN2"
echo "APN 2 is: $APN2"
INSTANCE="@@instance@@"
export INSTANCE="$INSTANCE"
echo "INSTANCE is: $INSTANCE"
NETWORK_UE_IP="@@network_ue_ip@@"
export NETWORK_UE_IP="$NETWORK_UE_IP"
echo "NETWORK_UE_IP is: $NETWORK_UE_IP"

SPGW_U_HOSTNAME="$(hostname -s)"
export SPGW_U_HOSTNAME="$SPGW_U_HOSTNAME"
echo "SPGW-U hostname is $SPGW_U_HOSTNAME"

export SGWC_IP_ADDRESS="$SGWC_IP_ADDRESS"
echo "SGWC_IP_ADDRESS is: $SGWC_IP_ADDRESS"

export TZ="Europe/Berlin"
echo "Timezone is $TZ"

# Wait for SPGW-C to be up and running
echo "Waiting for SPGW-C at IP: $SGWC_IP_ADDRESS to be up and running"
./wait-for-sgw-c.sh "$SGWC_IP_ADDRESS"
echo "SPGW-C at IP: $SGWC_IP_ADDRESS is up and running"

docker-compose up -d oai_spgwu

docker ps

exit 0
