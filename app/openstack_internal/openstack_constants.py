import logging

from configuration_constants import ConfigurationConstants

LOG = logging.getLogger(__name__)


class OpenStackConstants(object):

    # OpenStack Constants
    KEYSTONE_URL = ConfigurationConstants.OS_BASE_OS_URL + ":5000/v3/"
    KEYSTONE_PORT = "5000"
    KEYSTONE_VERSION = "v3"

    GLANCE_URL = ConfigurationConstants.OS_BASE_OS_URL + ":9292/v2"
    GLANCE_PORT = "9292"
    GLANCE_VERSION = "2"

    NOVA_URL = ConfigurationConstants.OS_BASE_OS_URL + ":8774/v2.79"
    NOVA_PORT = "8774"
    NOVA_VERSION = "2.79"

    NEUTRON_URL = ConfigurationConstants.OS_BASE_OS_URL + ":9696"
    NEUTRON_PORT = "9696"
    NEUTRON_VERSION = ""

