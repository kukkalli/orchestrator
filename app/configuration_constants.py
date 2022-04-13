import logging

LOG = logging.getLogger(__name__)


class ConfigurationConstants(object):
    # OpenDayLight Constants
    ODL_URL = "http://10.10.0.10:8181"
    ODL_USERNAME = "admin"
    ODL_PASSWORD = "admin"

    # OpenStack Constants
    OS_BASE_OS_URL = "http://10.10.0.21"
    OS_USERNAME = "admin"
    OS_PASSWORD = "tuckn2020"
    OS_DOMAIN_NAME = "TUC"
    OS_PROJECT_NAME = "admin"
    OS_REGION = "TUCKN"
