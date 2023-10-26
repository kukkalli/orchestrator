import logging
from typing import Dict

from templates.service_profile_template import ServiceProfileTemplate

LOG = logging.getLogger(__name__)


class OAI5GCNDCBase(ServiceProfileTemplate):
    MYSQL = "mysql"
    NRF = "oai-nrf"
    IMS = "asterisk-ims"
    UDR = "oai-udr"
    UDM = "oai-udm"
    AUSF = "oai-ausf"
    AMF = "oai-amf"
    SMF = "oai-smf"
    UPF = "oai-spgwu-tiny"
    TRF_GEN = "oai-trf-gen"

    TimeZone = "Europe/Berlin"

    MySQL_Values = {
        "domain": "tu-chemnitz.de",
        "mysql_database": "oai_db",
        "mysql_user": "oai_tuc",
        "mysql_password": "oai_tuc",
        "mysql_root_password": "oai_tuc"
    }

    NRF_Values = {
        "log_level": "debug"
    }

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(prefix, domain_name, bandwidth, max_delay)
        self.add_nfv_vlinks_list(max_delay)

    def add_nfv_vlinks_list(self, max_delay: float):
        vlinks = [
            [self.MYSQL, self.NRF],
            [self.MYSQL, self.IMS],
            [self.MYSQL, self.UDR],
            [self.NRF, self.UDR],
            [self.NRF, self.UDM],
            [self.NRF, self.AUSF],
            [self.NRF, self.AMF],
            [self.NRF, self.SMF],
            [self.NRF, self.UPF],
            [self.NRF, self.TRF_GEN],
            [self.IMS, self.UPF],
            [self.UDR, self.UDM],
            [self.UDM, self.AUSF],
            [self.AUSF, self.AMF],
            [self.AMF, self.SMF],
            [self.SMF, self.UPF],
            [self.UPF, self.TRF_GEN]
        ]

        for vlink in vlinks:
            self.nfv_v_links_list.append({"out": vlink[0], "in": vlink[1], "delay": max_delay})
            self.nfv_v_links_list.append({"out": vlink[1], "in": vlink[0], "delay": max_delay})

    def populate_vm_ip(self, user_data: str, nf_ip_dict: Dict[str, str]) -> str:
        user_data = user_data.replace("@@domain@@", self.domain_name)
        user_data = user_data.replace("@@mysql_ip@@", nf_ip_dict[self.MYSQL])
        user_data = user_data.replace("@@nrf_ip@@", nf_ip_dict[self.NRF])
        user_data = user_data.replace("@@ims_ip@@", nf_ip_dict[self.IMS])
        user_data = user_data.replace("@@udr_ip@@", nf_ip_dict[self.UDR])
        user_data = user_data.replace("@@udm_ip@@", nf_ip_dict[self.UDM])
        user_data = user_data.replace("@@ausf_ip@@", nf_ip_dict[self.AUSF])
        user_data = user_data.replace("@@amf_ip@@", nf_ip_dict[self.AMF])
        user_data = user_data.replace("@@smf_ip@@", nf_ip_dict[self.SMF])
        user_data = user_data.replace("@@upf_ip@@", nf_ip_dict[self.UPF])
        user_data = user_data.replace("@@trf_ip@@", nf_ip_dict[self.TRF_GEN])
        return user_data

