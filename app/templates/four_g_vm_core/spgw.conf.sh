#!/bin/bash

rm spgw.conf

cat > spgw.conf << EOF
################################################################################
# Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The OpenAirInterface Software Alliance licenses this file to You under
# the Apache License, Version 2.0  (the "License"); you may not use this file
# except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-------------------------------------------------------------------------------
# For more information about the OpenAirInterface (OAI) Software Alliance:
#      contact@openairinterface.org
################################################################################

S-GW :
{
    NETWORK_INTERFACES :
    {
        # S-GW binded interface for S11 communication (GTPV2-C), if none selected the ITTI message interface is used
EOF

echo "        SGW_INTERFACE_NAME_FOR_S11              = \"${FABRIC_INTERFACE_NAME}\";                         # STRING, interface name, YOUR NETWORK CONFIG HERE" >> spgw.conf
echo "        SGW_IPV4_ADDRESS_FOR_S11                = \"${FABRIC_IP}\";               # STRING, CIDR, YOUR NETWORK CONFIG HERE" >> spgw.conf

cat >> spgw.conf << EOF

        # S-GW binded interface for S1-U communication (GTPV1-U) can be ethernet interface, virtual ethernet interface, we don't advise wireless interfaces
EOF

echo "        SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP    = \"${FABRIC_INTERFACE_NAME}\";                       # STRING, interface name, YOUR NETWORK CONFIG HERE, USE \"lo\" if S-GW run on eNB host" >> spgw.conf
echo "        SGW_IPV4_ADDRESS_FOR_S1U_S12_S4_UP      = \"${FABRIC_IP}\";              # STRING, CIDR, YOUR NETWORK CONFIG HERE" >> spgw.conf

cat >> spgw.conf << EOF
        SGW_IPV4_PORT_FOR_S1U_S12_S4_UP         = 2152;                         # INTEGER, port number, PREFER NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING

        # S-GW binded interface for S5 or S8 communication, not implemented, so leave it to none
        SGW_INTERFACE_NAME_FOR_S5_S8_UP         = "none";                       # STRING, interface name, DO NOT CHANGE (NOT IMPLEMENTED YET)
        SGW_IPV4_ADDRESS_FOR_S5_S8_UP           = "0.0.0.0/16";                 # STRING, CIDR, DO NOT CHANGE (NOT IMPLEMENTED YET)
    };

    INTERTASK_INTERFACE :
    {
        # max queue size per task
        ITTI_QUEUE_SIZE            = 2000000;                                   # INTEGER
    };

    LOGGING :
    {
        # OUTPUT choice in { "CONSOLE", "SYSLOG", \`path to file\`", "\`IPv4@\`:\`TCP port num\`"}
        # \`path to file\` must start with '.' or '/'
          # if TCP stream choice, then you can easily dump the traffic on the remote or local host: nc -l \`TCP port num\` > received.txt
        OUTPUT            = "CONSOLE";                                          # see 3 lines above
        #OUTPUT            = "SYSLOG";                                          # see 4 lines above
        #OUTPUT            = "/tmp/spgw.log";                                   # see 5 lines above
        #OUTPUT            = "127.0.0.1:5656";                                  # see 6 lines above

        # THREAD_SAFE choice in { "yes", "no" } means use of thread safe intermediate buffer then a single thread pick each message log one
        # by one to flush it to the chosen output
        THREAD_SAFE       = "no";

        # COLOR choice in { "yes", "no" } means use of ANSI styling codes or no
        COLOR              = "yes";

        # Log level choice in { "EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFO", "DEBUG", "TRACE"}
        UDP_LOG_LEVEL      = "TRACE";
        GTPV1U_LOG_LEVEL   = "TRACE";
        GTPV2C_LOG_LEVEL   = "TRACE";
        SPGW_APP_LOG_LEVEL = "TRACE";
        S11_LOG_LEVEL      = "TRACE";
    };
};

P-GW =
{
    NETWORK_INTERFACES :
    {
        # P-GW binded interface for S5 or S8 communication, not implemented, so leave it to none
        PGW_INTERFACE_NAME_FOR_S5_S8          = "none";                         # STRING, interface name, DO NOT CHANGE (NOT IMPLEMENTED YET)

        # P-GW binded interface for SGI (egress/ingress internet traffic)
EOF

echo "        PGW_INTERFACE_NAME_FOR_SGI            = \"${FABRIC_IP_PORT}\";                         # STRING, YOUR NETWORK CONFIG HERE" >> spgw.conf
cat >> spgw.conf << EOF
        PGW_MASQUERADE_SGI                    = "no";                           # STRING, {"yes", "no"}. YOUR NETWORK CONFIG HERE, will do NAT for you if you put "yes".
        UE_TCP_MSS_CLAMPING                   = "no";                           # STRING, {"yes", "no"}.
    };

    # Pool of UE assigned IP addresses
    # Do not make IP pools overlap
    # first IPv4 address X.Y.Z.1 is reserved for GTP network device on SPGW
    # Normally no more than 16 pools allowed, but since recent GTP kernel module use, only one pool allowed (TODO).
    IP_ADDRESS_POOL :
    {
        IPV4_LIST = (
                      "172.16.0.0/12"                                           # STRING, CIDR, YOUR NETWORK CONFIG HERE.
                    );
    };

    # DNS address communicated to UEs
    DEFAULT_DNS_IPV4_ADDRESS     = "8.8.8.8";                                   # YOUR NETWORK CONFIG HERE
    DEFAULT_DNS_SEC_IPV4_ADDRESS = "8.8.4.4";                                   # YOUR NETWORK CONFIG HERE

    # Non standard feature, normally should be set to "no", but you may need to set to yes for UE that do not explicitly request a PDN address through NAS signalling
    FORCE_PUSH_PROTOCOL_CONFIGURATION_OPTIONS = "no";                           # STRING, {"yes", "no"}.
    UE_MTU                                    = 1500                            # INTEGER
};
EOF

exit 0
