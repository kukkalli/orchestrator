#!/bin/bash

echo "Start HSS: $(date +"%T")"

cat > /home/ubuntu/.ssh/authorized_keys << EOF
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAGxlZsduAGeKqz3UhzHeXiJOsRlBQTZIyOxA0DrXso9ncDveooDqUr+Xw5XZx44nHFNjWocoQowDdaA8jj0DYEs9wF5ELGj/rm4n6a1b6tXVAlb3Vojb5C0mZfx2gUA6i5GNnNXONRttaW53XeOoD/VDM9tlgBnpa04bBQ1naTiLbQsQg== os@controller
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAFJ/TSfJegktNbVbCF2L1hte8qfDtgk/zArlNq4vgEAKRePSEYnoFldlGVn5zDqnvLP2xy6WrcFUjO2TOeTnmqQ1gEzcBOjUXeYdA7LO1J8yARvvAMOk4IiuVTvGUdCIW8uDpXwfqCxqeKbSudo3LVLgt/ZcRg1QENyRLP/zqixIJoEsA== os@compute01
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACnHtnIvTXuTG2I5ngNXKUYu/h7izkEGPmfZpqIeuXcQIY0miX7k+9snBvPXKuxp5nYspOZuOzsHs4JEE3l/+ftcgHvF7w3SD5CtdTfGMhUwGHtcpWtKfj18+FiDwh9wK4m6exBChpfBTU1q14LPZBR7xg9KZULWGddugmffUK1SMoWdg== os@compute02
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAG6PCMQcMNvSA4yRmHETOYdj60fsJo4n8FOBKmlw2fJR7xWMND0DQWTVvPssv3bw1iKn5zLbx4aeVd7idKT00HsjwB4mX1/+UBVUeP/21tp50J3XsG5Pdwz4JL6LeRWvurKoU66bpBR5u0Iuo9VrJlHfn3GbCiHzke7uUt3QBmBWkxroQ== sdn@sdnc
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACU7DStTMa4kHmnZ6kiNkQHrW4CYW9kOKkR8xQa3yBvPDG0IYv0MuUJg2lY5TfdhmXNWELPYHlZxieOC60HTD/vzACoV3268mlJNYGE+ju4iQq+QXaUSwog4YkQs4aDCpylyDRJYWFe8YP97/xFOzR5P5bxCYcJZQLlwWa/+294kW29hQ== hanif@openstack
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAEBCbxZcyGw+PD3S/HoPx/WKhfGOz4Mos3OGQ4Q2rvh7UpNBE4UVp/xOBcFoL0WveHI+WskQV0jKa7TnErjVwEsOAAX6O4DxaskATGq6XioPv2XmRGKb5UZ28NUCE+VLhUvnFLLn2IMiCSiNzCU8hX0rjsU6/hHjDyV01Iahq2gAY6E7Q== hanif@openstack
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAHLT0AS5MHwwJ6hX1Up5stfz361+IWA/8/MhZBH+mYA32h/Bp5hSWkQDXow4aDiHRlxVV1WLlHHup+GPBBA9XLTRwHP8gAjbP5EM4EVxR9EbDh5Hz13xcN0/n9J9rasefHS8UgTJUgRrWeNRCSAhkbNfDfSeQzk8NWlzhiwwCIUacKnzg== hanif@kukkalli
EOF


DOMAIN="tu-chemnitz.de"

INTERFACES=$(find /sys/class/net -mindepth 1 -maxdepth 1 ! -name lo ! -name docker -printf "%P " -execdir cat {}/address \;)

first=true
interface_name=""
sudo rm /etc/network/interfaces.d/50-cloud-init.cfg
sudo -- sh -c "echo '# This file is generated from information provided by' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# the datasource.  Changes to it will not persist across an instance.' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# To disable cloud-init's network configuration capabilities, write a file' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo '# network: {config: disabled}' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo 'auto lo' >> /etc/network/interfaces.d/50-cloud-init.cfg"
sudo -- sh -c "echo 'iface lo inet loopback' >> /etc/network/interfaces.d/50-cloud-init.cfg"

# shellcheck disable=SC2068
for i in ${INTERFACES[@]};
do
    if ${first}
    then
        first=false
        interface_name=${i}
        sudo -- sh -c "echo 'auto ${interface_name}' >> /etc/network/interfaces.d/50-cloud-init.cfg"
        sudo -- sh -c "echo 'iface ${interface_name} inet dhcp4' >> /etc/network/interfaces.d/50-cloud-init.cfg"
    else
        first=true
        sudo -- sh -c "echo '            ' >> /etc/network/interfaces.d/50-cloud-init.cfg"
    fi
done

sudo rm /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
sudo -- sh -c "echo '# network: {config: disabled}' >> /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"
sudo -- sh -c "echo 'network: {config: disabled}' >> /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"

sudo systemctl restart networking.service

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

echo "HSS started $(date +"%T")"

exit 0
