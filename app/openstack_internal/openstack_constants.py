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

    UBUNTU_20_04 = "focal-server-cloudimg-amd64"
    UBUNTU_18_04 = "bionic-server-cloudimg-amd64"
    CIRROS_0_5_2 = "cirros-0.5.2-x86_64"

    OAI_HSS_VMI = "oai-hk-hss"
    OAI_MME_VMI = "oai-hk-mme"
    OAI_SPGW_VMI = "oai-hk-spgw"
