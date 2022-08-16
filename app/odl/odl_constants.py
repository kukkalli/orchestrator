import logging

from configuration_constants import ConfigurationConstants

LOG = logging.getLogger(__name__)


class ODLConstants(object):
    # OpenDayLight Constants
    TOPOLOGY = ConfigurationConstants.ODL_URL + "/restconf/operational/network-topology:network-topology"
    SWITCHES = ConfigurationConstants.ODL_URL + "/restconf/operational/opendaylight-inventory:nodes"
    SWITCH = SWITCHES + "/node/{switch_id}"
    PORT = SWITCH + '/node-connector/{port_id}'

    HEADER = {"Content-Type": "application/json", "Accept": "application/json"}

    PUT_FLOW_URL = ConfigurationConstants.ODL_URL + '/restconf/config/opendaylight-inventory:nodes/node/{' \
                                                    'node_id}/table/{table}/flow/{flow_id}'
    PUT_XML_HEADER = {"content-type": "application/xml", "Accept": "application/json"}

    ETHER_TYPE_ARP_MATCHER = "2054"  # constant decimal value of 0x0806 that matches with only ARP frames
    ETHER_TYPE_IP_MATCHER = "2048"  # constant decimal value of 0x0800 used to match IP
    ARP_REQUEST_OP = "1"  # this opcode is for ARP request
    ARP_REPLY_OP = "2"  # This opcode is only for ARP reply

    # It is very important to consider that the string should not start with an empty line or so.
    # The following is the correct one
    # Other important point is to use "_" instead of "-" for naming the keys inside {} as python can not read -
    FLOW_XML = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>  
<flow xmlns="urn:opendaylight:flow:inventory">
    <hard-timeout>{hard_timeout}</hard-timeout>
    <idle-timeout>{idle_timeout}</idle-timeout>
    <cookie>{cookie}</cookie>
    <priority>{priority}</priority>
    <id>{flow_id}</id>
    <table_id>{table}</table_id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <output-action>
                        <output-node-connector>{output_action}</output-node-connector>
                    </output-action>
                    <order>0</order>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
</flow>
"""

    # the original xml which also has the matching part.
    FLOW_XML_backup = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>  
<flow xmlns="urn:opendaylight:flow:inventory">
    <hard-timeout>{hard_timeout}</hard-timeout>
    <idle-timeout>{idle_timeout}</idle-timeout>
    <cookie>{cookie}</cookie>
    <priority>{priority}</priority>
    <match>
        <in-port>{in_port}</in-port>
    </match>
    <id>{flow_id}</id>
    <table_id>{table}</table_id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <output-action>
                        <output-node-connector>{output_action}</output-node-connector>
                    </output-action>
                    <order>0</order>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
</flow>
"""

    FLOW_JSON = """
    {"flow-node-inventory:flow": [
         {
             "id": "{flow_id}",
             "table_id": "{table_id}",
             "idle-timeout": "{idle_timeout}",
             "priority": "{priority}",
             "hard-timeout": "{hard_timeout}",
             "match": {
                 "ipv4-source": "{src_ip}",
                 "ipv4-destination": "{dst_ip}",
                 "ethernet-match": {
                     "ethernet-type": {
                         "type": 2048
                     }
                 }
             },
             "cookie": 1,
             "instructions": {
                 "instruction": [
                     {
                         "order": 0,
                         "apply-actions": {
                             "action": [
                                {
                                     "order": 0,
                                     "output-action": {
                                         "output-node-connector": "3"}
                                }
                             ]
                         }
                     }
                 ]
             }
         }
     ]
}
"""
