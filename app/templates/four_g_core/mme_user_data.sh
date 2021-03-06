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

# : <<'END'
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

echo "MME FQDN $FQDN_HOSTNAME"

sudo -- sh -c "echo '' >>  /etc/hosts"

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

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

echo "--------------- docker-compose version is: ---------------"
docker-compose --version


HSS_IP="@@hss_ip@@"
HSS_HOSTNAME="@@hss_hostname@@"
sudo -- sh -c "echo $HSS_IP $HSS_HOSTNAME $HSS_HOSTNAME.$DOMAIN >> /etc/hosts"

su - ubuntu

export MANAGEMENT_IP="$MANAGEMENT_IP"
export FABRIC_IP="$FABRIC_IP"
export FABRIC_IP="$MANAGEMENT_IP"
sed -i -e "s@_fabric_ip_@$FABRIC_IP@" .env


# DOCKER_PASS="@@docker_pass@@"
# docker login -u kukkalli -p ${DOCKER_PASS}

cd /home/ubuntu/ || exit

git clone https://github.com/kukkalli/oai-docker-compose.git

chown ubuntu:ubuntu -R oai-docker-compose

cd oai-docker-compose/4g/mme/ || exit

export DOMAIN="$DOMAIN"
sed -i -e "s@_domain_@$DOMAIN@" .env
echo "DOMAIN is: $DOMAIN"
export REALM="$DOMAIN"
sed -i -e "s@_realm_@$DOMAIN@" .env
echo "REALM is: $REALM"
export HSS_IP="$HSS_IP"
sed -i -e "s@_hss_ip_@$HSS_IP@" .env
echo "HSS IP is: $HSS_IP"
export HSS_HOSTNAME="$HSS_HOSTNAME"
sed -i -e "s@_hss_hostname_@$HSS_HOSTNAME@" .env
echo "HSS HOSTNAME is:" $HSS_HOSTNAME
export HSS_FQDN="$HSS_HOSTNAME"."$DOMAIN"
sed -i -e "s@_hss_fqdn_@$HSS_FQDN@" .env
echo "HSS FQDN is: $HSS_FQDN"
MCC="@@mcc@@"
export MCC="$MCC"
sed -i -e "s@_mcc_@$MCC@" .env
echo "MCC is: $MCC"
MNC="@@mnc@@"
export MNC="$MNC"
sed -i -e "s@_mnc_@$MNC@" .env
echo "MNC is: $MNC"
MME_GID="@@mme_gid@@" # 32768
export MME_GID="$MME_GID"
sed -i -e "s@_mme_gid_@$MME_GID@" .env
echo "MME GID is: $MME_GID"
MME_CODE="@@mme_code@@" # 3
export MME_CODE="$MME_CODE"
sed -i -e "s@_mme_code_@$MME_CODE@" .env
echo "MME CODE is: $MME_CODE"
SGWC_IP_ADDRESS="@@sgwc_ip_address@@"
export SGWC_IP_ADDRESS="$SGWC_IP_ADDRESS"
sed -i -e "s@_sgwc_ip_address_@$SGWC_IP_ADDRESS@" .env
echo "SGWC IP is: $SGWC_IP_ADDRESS"

MME_HOSTNAME="$(hostname -s)"
export MME_HOSTNAME="$MME_HOSTNAME"
sed -i -e "s@_mme_hostname_@$MME_HOSTNAME@" .env
echo "MME hostname is $MME_HOSTNAME"

export TZ="Europe/Berlin"
sed -i -e "s@_tz_@$TZ@" .env
echo "Timezone is $TZ"

export HSS_REALM="$DOMAIN"
echo "HSS Realm is $HSS_REALM"

export MME_FQDN="$FQDN_HOSTNAME"
echo "MME FQDN is $MME_FQDN"

# Update mme.conf file before pushing it to docker
echo "Update mme.conf file before pushing it to docker"
./update_mme_conf.sh

# Wait for HSS to be up and running
echo "Waiting for HSS at IP: $HSS_IP to be up and running"
./wait-for-hss.sh "$HSS_IP"
echo "HSS at IP: $HSS_IP is up and running"

docker-compose up -d magma_mme

docker ps

exit 0
