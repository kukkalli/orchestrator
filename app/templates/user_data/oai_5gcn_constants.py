class OAI5GConstants(object):
    # Default Ubuntu 22.04 Low Latency Image with docker pre-installed
    UBUNTU_22_04_DOCKER_VM_LOW_LATENCY = "oai-5gcn-dockervm-llc-ubuntu-22.04"
    UBUNTU_22_04_DOCKER_VM_LOW_LATENCY_ID = "93bc0093-c109-4cab-9e3b-28f584090830"

    # Images for OAI 5G Core Network Functions
    OAI_5GCN_MYSQL_VMI = "oai-5gcn-mysql-llc-ubuntu-22.04"
    OAI_5GCN_NRF_VMI = "oai-5gcn-nrf-llc-ubuntu-22.04"
    OAI_5GCN_IMS_VMI = "oai-5gcn-ims-llc-ubuntu-22.04"
    OAI_5GCN_UDR_VMI = "oai-5gcn-udr-llc-ubuntu-22.04"
    OAI_5GCN_UDM_VMI = "oai-5gcn-udm-llc-ubuntu-22.04"
    OAI_5GCN_AUSF_VMI = "oai-5gcn-ausf-llc-ubuntu-22.04"
    OAI_5GCN_AMF_VMI = "oai-5gcn-amf-llc-ubuntu-22.04"
    OAI_5GCN_SMF_VMI = "oai-5gcn-smf-llc-ubuntu-22.04"
    OAI_5GCN_UPF_VMI = "oai-5gcn-upf-llc-ubuntu-22.04"
    OAI_5GCN_TRF_GEN_VMI = "oai-5gcn-trf-llc-ubuntu-22.04"

    # Docker images for 5G Core network functions
    OAI_5GCN_MYSQL_DOCKER = "mysql:8.0"
    OAI_5GCN_NRF_DOCKER = "oaisoftwarealliance/oai-nrf:v1.5.1"
    OAI_5GCN_IMS_DOCKER = "kukkalli/asterisk-ims:1.0.0"
    OAI_5GCN_UDR_DOCKER = "oaisoftwarealliance/oai-udr:develop"
    OAI_5GCN_UDM_DOCKER = "oaisoftwarealliance/oai-udm:develop"
    OAI_5GCN_AUSF_DOCKER = "oaisoftwarealliance/oai-ausf:develop"
    OAI_5GCN_AMF_DOCKER = "oaisoftwarealliance/oai-amf:v1.5.1"
    OAI_5GCN_SMF_DOCKER = "oaisoftwarealliance/oai-smf:v1.5.1"
    OAI_5GCN_UPF_DOCKER = "oaisoftwarealliance/oai-spgwu-tiny:v1.5.1"
    OAI_5GCN_TRF_GEN_DOCKER = "oaisoftwarealliance/trf-gen-cn5g:latest"
