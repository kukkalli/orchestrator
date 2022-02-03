# Connect BBU to SW4 in SDN-rack (Mehrdad 27-8-2021)
To connect BBU, I have added port s4/11 to br-tuc11 using followig command 
ovs-vsctl add-port br-tuc11 te-1/1/11 vlan_mode=access tag=1 -- set Interface te-1/1/11 type=pica8
Then I have manually added flows on SW4 for ARP request/reply to/from port 11 + a flow for l3 forwarding
BBU can ping mme 
###### Note
If we run the forwarding APP it would not run as we have added a new interface which optimizer would not accept it.
## The current lab setup topology SDN Rack + Mobile Network 
![lab setup topology](https://user-images.githubusercontent.com/62847451/131166432-429db1f8-058b-4979-9b49-a2584a2295f2.png)
## Add Web server 
We add a webserver and add flows on switches manually to enable comminucation between spgw and the webserver. This gonna use for test if celphone to load pages internally.
## The current lab setup topology SDN Rack + Mobile Network 
![Slide1](https://user-images.githubusercontent.com/62847451/133447596-1b05e5fe-8657-4110-9696-85596e8c8106.PNG)

---
# Mobile phone connectivity problem, 16.11.2021
### The problems have solved , so they were 
1. OAI software commit version (newer builds were needed)
2. Harness were wrongly inter connected.
3. UDP flows were to be configured accurately 
---
# [Migrate](https://github.com/Mehrdad-hajizadeh/Forwarding_Orchestrator_App/blob/main/document/experience.md#changing-openstack-controller-from-blade-server-to-pc) Openstack Controller to PC 30.11.2021
---
