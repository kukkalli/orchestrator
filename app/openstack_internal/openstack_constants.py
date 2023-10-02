from typing import List

from configuration_constants import ConfigurationConstants


class OpenStackConstants(object):
    # OpenStack Constants
    KEYSTONE_URL: str = ConfigurationConstants.OS_BASE_OS_URL + ":5000/v3/"
    KEYSTONE_PORT: str = "5000"
    KEYSTONE_VERSION: str = "v3"

    GLANCE_URL: str = ConfigurationConstants.OS_BASE_OS_URL + ":9292/v2"
    GLANCE_PORT: str = "9292"
    GLANCE_VERSION: str = "2"

    NOVA_URL: str = ConfigurationConstants.OS_BASE_OS_URL + ":8774/v2.79"
    NOVA_PORT: str = "8774"
    NOVA_VERSION: str = "2.79"
    # 2.88

    NEUTRON_URL: str = ConfigurationConstants.OS_BASE_OS_URL + ":9696"
    NEUTRON_PORT: str = "9696"
    NEUTRON_VERSION: str = ""

    MANAGEMENT_NETWORK_NAME: str = "Management-Network"
    PROVIDER_NETWORK_NAME: str = "TUC11-Network"

    NETWORKS_LIST: List[str] = [MANAGEMENT_NETWORK_NAME, PROVIDER_NETWORK_NAME]

    UBUNTU_22_04 = "ubuntu-22.04-server-cloudimg"
    UBUNTU_20_04 = "focal-server-cloudimg-amd64"
    UBUNTU_18_04 = "bionic-server-cloudimg-amd64"
    CIRROS_0_5_2 = "cirros-0.5.2-x86_64"
    UBUNTU_18_04_LOW_LATENCY = "low-latency-bionic-server-min"
    UBUNTU_22_04_DOCKER_VM_LOW_LATENCY = "oai-5gcn-dockervm-llc-ubuntu-22.04"

    OAI_HSS_VMI = "oai-slsd-hss"
    OAI_MME_VMI = "oai-slsd-mme"
    OAI_SPGW_VMI = "oai-slsd-spgw"

    OAI_5GCN_MYSQL_VMI = "oai-5gcn-mysql-llc-ubuntu-22.04"
    OAI_5GCN_IMS_VMI = "oai-5gcn-ims-llc-ubuntu-22.04"
    OAI_5GCN_NRF_VMI = "oai-5gcn-nrf-llc-ubuntu-22.04"
    OAI_5GCN_UDR_VMI = "oai-5gcn-udr-llc-ubuntu-22.04"
    OAI_5GCN_UDM_VMI = "oai-5gcn-udm-llc-ubuntu-22.04"
    OAI_5GCN_AUSF_VMI = "oai-5gcn-ausf-llc-ubuntu-22.04"
    OAI_5GCN_AMF_VMI = "oai-5gcn-amf-llc-ubuntu-22.04"
    OAI_5GCN_SMF_VMI = "oai-5gcn-smf-llc-ubuntu-22.04"
    OAI_5GCN_UPF_VMI = "oai-5gcn-upf-llc-ubuntu-22.04"
    OAI_5GCN_TRF_GEN_VMI = "oai-5gcn-trf-llc-ubuntu-22.04"
