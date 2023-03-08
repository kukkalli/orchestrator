# Create a script to run on boot

| VM name  | IP Address |
|----------|------------|
| hss      | 10.10.2.96 |
| mme      | 10.10.2.52 |
| spgw     | 10.10.1.21 |

-----------

## HSS start-up on boot
1. Create a script `start_on_boot` to start the spgw on the path `/home/ubuntu/`
   ```
   #!/bin/bash
   
   cd /home/ubuntu/openair-cn/
   source oaienv
   cd scripts
   ./run_hss -k
   screen -S hss -d -m ./run_hss
   
   exit 0
   ```

2. Create a file `start_hss.service` under `/etc/systemd/system/`
   ```
   [Unit]
   Description="Start the HSS on boot"
   Requires=network-online.target
   After=network-online.target
   
   [Service]
   Type=oneshot
   RemainAfterExit=yes
   ExecStart=/home/ubuntu/start_on_boot
   
   [Install]
   WantedBy=multi-user.target
   ```

3. Enable the service
   ```
   # systemctl enable start_hss.service
   ```

4. Verify the service is enabled
   ```
   # systemctl is-enabled start_hss.service
   ```

5. Start the service by the command
   ```
   # systemctl start start_hss.service
   ```
6. Create kill HSS script
   ```
   #!/bin/bash
   
   cd /home/ubuntu/openair-cn/
   source oaienv
   cd scripts
   ./run_hss -k
   
   exit 0
   ```


## MME start-up on boot
1. Create a script `start_on_boot` to start the spgw on the path `/home/ubuntu/`
   ```
   #!/bin/bash

   cd /home/ubuntu/openair-cn/
   source oaienv
   cd scripts
   ./run_mme -k
   screen -S mme -d -m ./run_mme
   
   exit 0
   ```

2. Create a file `start_mme.service` under `/etc/systemd/system/`
   ```
   [Unit]
   Description="Start the MME on boot"
   Requires=network-online.target
   After=network-online.target
   
   [Service]
   Type=oneshot
   RemainAfterExit=yes
   ExecStart=/home/ubuntu/start_on_boot
   
   [Install]
   WantedBy=multi-user.target
   ```

3. Enable the service
   ```
   # systemctl enable start_mme.service
   ```

4. Verify the service is enabled
   ```
   # systemctl is-enabled start_mme.service
   ```

5. Start the service by the command
   ```
   # systemctl start start_mme.service
   ```

6. Create kill MME script
   ```
   #!/bin/bash
   
   cd /home/ubuntu/openair-cn/
   source oaienv
   cd scripts
   ./run_mme -k
   
   exit 0
   ```


## SPGW start-up on boot
1. Create a script `start_on_boot` to start the spgw on the path `/home/ubuntu/`
   ```
   #!/bin/bash
   
   cd /home/ubuntu/openair-cn/
   source oaienv
   cd scripts
   ./run_spgw -k
   screen -S spgw -d -m ./run_spgw
   
   exit 0
   ```

2. Create a file `start_spgw.service` under `/etc/systemd/system/`
   ```
   [Unit]
   Description="Start the SPGW on boot"
   Requires=network-online.target
   After=network-online.target
   
   [Service]
   Type=oneshot
   RemainAfterExit=yes
   ExecStart=/home/ubuntu/start_on_boot
   
   [Install]
   WantedBy=multi-user.target
   ```

3. Enable the service
   ```
   # systemctl enable start_spgw.service
   ```

4. Verify the service is enabled
   ```
   # systemctl is-enabled start_spgw.service
   ```

5. Start the service by the command
   ```
   # systemctl start start_spgw.service
   ```

6. Create kill SPGW script
   ```
   #!/bin/bash
   
   cd /home/ubuntu/openair-cn/
   source oaienv
   cd scripts
   ./run_spgw -k
   
   exit 0
   ```

```
openstack image save --file oai-hss.img oai-hss
openstack image create --container-format bare --disk-format qcow2 --min-disk 20 --min-ram 4096 --file oai-hss.img --public --progress oai-hss
```