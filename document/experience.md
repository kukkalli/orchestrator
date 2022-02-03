# UE problem with browsing video: MTU Problem
The UE could browse the internal webserver, but it could not open the video. Hence, it was not about communication problems or flow installation. The video/web could be accessible via the management network smoothly. 
## MTU Experiences
### MTU=1500 or 9000?
1. We set MTU=1500 on all switches (related ports) + VMs interfaces + Openstack Networking
2. Results: Even UE could not connect to the network.
3. Also, if we set MTU=1500 on Pica8 switches, we can not achieve the maximum throughput via a fiber connection. The default value is 9212, and we should keep it.
4. After seting MTU=1400 we could see the video on UE!! 1400+ spgw tunnel header < 1500, hence they are not consider jumbo frame
5. We set MTU=1500 on VM interfaces but for some reasons VM interfaces could not fragment jumbo frame. That is why we could not watch video (which has bigger frame) while we could browse the web server itself.
However [this](https://www.mirazon.com/jumbo-frames-do-you-really-need-them/) says if MTU set to 1500 the received Jumbo frames should be fragmented.
```
The problem comes from the fact that turning jumbo frames on basically raises the ceiling for the largest size frame you can send,
but what if another device on the path doesn’t have that higher ceiling? Well, the short answer is that device can’t process the larger frame, 
so the frame gets fragmented into smaller within-normal-spec frames that are then transmitted, which induces latency.
```
### MTU Size in OAI [document](https://kb.ettus.com/Getting_Started_with_4G_LTE_using_Eurecom_OpenAirInterface_(OAI)_on_the_USRP_2974) 
The following figure shows OAI recomendation over MTU.
![image](https://user-images.githubusercontent.com/62847451/144020568-b4d8ad75-0d87-4a3b-82a7-0b666d9811c9.png)

Also, the [following](https://openairinterface.org/docs/workshop/3_OAI_Workshop_20170427/training/CN_training_user_plane.pdf) tutorial suggests the MTU for OAI communication
![image](https://user-images.githubusercontent.com/62847451/144023923-d237cedf-818e-4483-9e16-2dbb4c8e670f.png)

### Why MTU=1500 would not work!!
#### Note: We are still not 100% sure but it seems it is because of the following reason
As different components use tunneling for communications, they will add addtional header which makes the header bigger than 1500 i.e, Jumbo frame. For some 
reason the VM interface would not fragment jumbo frames leads to communication problem.
##### But when we set MTU~1400 the video would play without problem. Because after adding the headers from the tunnel the total MTU is less than 1500 and it works without problem. But MTU=1500 + tunnel header is a jumbo frame that is not fragmented in our network and causes this problem.
## Unstable web server

#### We used a Python web server for our measurements, but it seems it is elementary for testing purposes. It has inconsistency during our measurements. Hence, we ran Apache, which is more stable.
---
# SSH Problem in Fabric--> MTU makes problem!
I have noticed I could not SSH from one VM in compute1 to other one in compute2 via Fabric. We can easily ssh through mng but not fabric. I check MTU size set on compute interfaces(brtuc1). They are 1500, hence when ssh add more header the jumbo frame can not communicate. I set those interfacec to be MTU=1400 and everything works!!!!

## How to set MTU on an interface

```
sudo ip link set dev brtuc11 mtu 1400
```
---
# Changing OpenStack Controller from blade server to PC
@Ole
I migrated the openstack controller from the blade server to the PC. It took longer than expected since the old PC is not able to boot via UEFI but only has the legacy BIOS boot.
The controller does not have access to the fabric right now, but as we discussed this might not be necessary.
```
@Mehrdad
We discussed that Openstack controller just want to send signalling to compute nodes via managemnet network.
Hence, it would not need to access fabric. In the case, we can directly connect it to fabric via ethernet over SFP.
The management network speed is now sufficient but it may cause some restriction when we conduct VM migration as it 
should be done via mng net.
```
The fabric bridge obviously complains about the missing fabric interface:
```
  Bridge "brtuc11"
        Controller "tcp:127.0.0.1:6633"
            is_connected: true
        fail_mode: secure
        datapath_type: system
        Port "brtuc11"
            Interface "brtuc11"
                type: internal
        Port "tuc11"
            Interface "tuc11"
                error: "could not open network device tuc11 (No such device)"
        Port "phy-brtuc11"
            Interface "phy-brtuc11"
                type: patch
                options: {peer="int-brtuc11"}
```
The mgmt bridge looks fine however and can be used properly
```
   Bridge brmgmt
        Controller "tcp:127.0.0.1:6633"
            is_connected: true
        fail_mode: secure
        datapath_type: system
        Port phy-brmgmt
            Interface phy-brmgmt
                type: patch
                options: {peer=int-brmgmt}
        Port brmgmt
            Interface brmgmt
                type: internal
        Port mgmt
            Interface mgmt
```
--- 
# Which USRP to buy for OAI?
@Sunil:
USRP N 310 / N320/ N321 could used. 
1) Currently only N310 is tested and used by OAI
2) They do have minor issues, but the OAI has informed the Ettus to modify / improve N310.
3) N210 : They have reduced bandwidth.
![image](https://user-images.githubusercontent.com/62847451/145816984-137236fe-7fcf-4e9c-94dc-20d735576392.png)
