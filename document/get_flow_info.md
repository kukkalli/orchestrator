# How to solve E2E flow monitoring without access to ID?
![image](https://user-images.githubusercontent.com/62847451/148424070-2329f216-62be-42b8-99fa-197eb47c4552.png)


---
# Get Flows information via ODL (REST APIs)
### There are different abstract levels to see flow-tables information.
## Get all flow-tables in a switch
It gives us all information about switch:3 with all tables information
```
http://10.10.0.10:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:3
```
## Get aggregated info of specific table
To view the flow table and flow aggregated statistics for a connected node, send the following request to the controller:
```
http://10.10.0.10:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:3/table/0/
```
## Get info of a specific flow in a flow table via REST
### Important Note

In the examples below the flow ID fm-sr-link-discovery is internal to the controller and has to match the datastore configured flow ID. For more information see flow ID match section [Flow ID match function](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/operation.html#flow-id-match-function).

See more info, [link](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/operation.html#example-of-flow-description-and-flow-statistics)
![image](https://user-images.githubusercontent.com/62847451/146547146-4c9772c9-20a6-49d4-b3ec-0f751e686c92.png)

### Flow ID
![image](https://user-images.githubusercontent.com/62847451/146549769-356bb97f-af96-4933-a82e-e71146409b41.png)

```
<flow>
    <id>#UF$TABLE*0-555</id>
    <flow-statistics xmlns="urn:opendaylight:flow:statistics">
        <packet-count>5227</packet-count>
        <duration>
            <nanosecond>642000000</nanosecond>
            <second>26132</second>
        </duration>
        <byte-count>444295</byte-count>
    </flow-statistics>
    <priority>99</priority>
    <table_id>0</table_id>
    <cookie_mask>0</cookie_mask>
    <hard-timeout>0</hard-timeout>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>35020</type>
            </ethernet-type>
        </ethernet-match>
    </match>
    <cookie>1000000000000001</cookie>
    <flags></flags>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
                    <output-action>
                        <max-length>65535</max-length>
                        <output-node-connector>CONTROLLER</output-node-connector>
                    </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
    <idle-timeout>0</idle-timeout>
</flow>
```
---
# Get flow information via OVS/Pica8 Command
## Shows the hardware flow

![image](https://user-images.githubusercontent.com/62847451/146545400-f505cf3c-cb20-46cb-9a9e-12c1fb2d9e61.png)

## Shows all software flows

Including those flows not added by the user or switch.
![image](https://user-images.githubusercontent.com/62847451/146545601-262a208d-16c3-462c-851e-6f75cc841c4b.png)

## Show all flow entries
Prints to the console all flow entries in switch's  tables  that match  flows.   If flows is omitted, all flows in the switch are retrieved.  See Flow Syntax, below, for  the  syntax  of  flows. The output format is described in Table Entry Output. By default, ovs-ofctl prints flow entries in the same order that the switch sends them, which is unlikely to be intuitive or con‐ sistent.   Use --sort and --rsort to control display order.  The --names/--no-names and --stats/--no-stats  options  also  affect output formatting.  See the descriptions of these options, under OPTIONS below, for more information

![image](https://user-images.githubusercontent.com/62847451/146545915-24e04d30-3b04-45fa-8243-3bb716a2c519.png)
