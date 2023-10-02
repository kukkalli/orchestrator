import logging

from templates.oai_5gcn.mysql.mysql import MySQL
from templates.service_profile_template import ServiceProfileTemplate

LOG = logging.getLogger(__name__)


class OAI5GCNAndDU(ServiceProfileTemplate):
    MYSQL = "mysql"
    IMS = "ims"
    NRF = "nrf"
    UDR = "udr"
    UDM = "udm"
    AUSF = "ausf"
    AMF = "amf"
    SMF = "smf"
    SPGW_U = "spgwu"
    TRF_GEN = "trf-gen-cn5g"

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(prefix, domain_name, bandwidth)
        self.network_functions.append(MySQL(prefix, self.MYSQL))
        # self.network_functions.append(MMETemplate(prefix, self.MME))
        # self.network_functions.append(SPGWCTemplate(prefix, self.SPGW_C))
        # self.network_functions.append(SPGWUTemplate(prefix, self.SPGW_U))


def main():
    pass


if __name__ == "__main__":
    main()
