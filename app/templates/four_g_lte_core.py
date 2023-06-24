import logging
from typing import Dict

from templates.four_g_core.hss_template import HSSTemplate
from templates.four_g_core.mme_template import MMETemplate
from templates.four_g_core.spgwc_template import SPGWCTemplate
from templates.four_g_core.spgwu_template import SPGWUTemplate
from templates.service_profile_template import ServiceProfileTemplate
from test_scripts.service_build_test import service_built

LOG = logging.getLogger(__name__)


class FourGLTECore(ServiceProfileTemplate):
    HSS = "hss"
    MME = "mme"
    SPGW_C = "spgw-c"
    SPGW_U = "spgw-u"

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(prefix, domain_name, bandwidth)
        self.network_functions.append(HSSTemplate(prefix, self.HSS))
        self.network_functions.append(MMETemplate(prefix, self.MME))
        self.network_functions.append(SPGWCTemplate(prefix, self.SPGW_C))
        self.network_functions.append(SPGWUTemplate(prefix, self.SPGW_U))

        self.nfv_v_links_list.append({"out": self.HSS, "in": self.MME, "delay": max_delay })
        self.nfv_v_links_list.append({"out": self.MME, "in": self.HSS, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.MME, "in": self.SPGW_C, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.SPGW_C, "in": self.MME, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.MME, "in": self.SPGW_U, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.SPGW_U, "in": self.MME, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.SPGW_C, "in": self.SPGW_U, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.SPGW_U, "in": self.SPGW_C, "delay": max_delay})

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        LOG.debug(f"I am in 4G LTE Core, {self.domain_name}")
        vm_user_data_dict: Dict[str, str] = {}
        for network_function in self.get_network_functions():
            if network_function.name == self.HSS:
                mme_ip = nf_ip_dict[self.MME]
                user_data = network_function.get_user_data()
                user_data = user_data.replace("@@domain@@", self.domain_name)
                user_data = user_data.replace("@@mme_ip@@", mme_ip)
                user_data = user_data.replace("@@mme_hostname@@", self.vnf_vm_map[self.MME].hostname)
                user_data = user_data.replace("@@op_key@@", "0123456789ABCDEF0123456789ABCDEF")
                user_data = user_data.replace("@@lte_k@@", "0123456789ABCDEF0123456789ABCDEF")
                user_data = user_data.replace("@@apn-1@@", "tuc")
                user_data = user_data.replace("@@apn-2@@", "tuc2")
                user_data = user_data.replace("@@first_imsi@@", "265820000038021")
                vm_user_data_dict[self.HSS] = user_data

            elif network_function.name == self.MME:
                hss_ip = nf_ip_dict[self.HSS]
                spgw_c_ip = nf_ip_dict[self.SPGW_C]

                user_data = network_function.get_user_data()
                user_data = user_data.replace("@@domain@@", self.domain_name)
                user_data = user_data.replace("@@hss_ip@@", hss_ip)
                user_data = user_data.replace("@@hss_hostname@@", self.vnf_vm_map[self.HSS].hostname)
                user_data = user_data.replace("@@mcc@@", "265")
                user_data = user_data.replace("@@mnc@@", "82")
                user_data = user_data.replace("@@mme_gid@@", "32768")
                user_data = user_data.replace("@@mme_code@@", "3")
                user_data = user_data.replace("@@sgwc_ip_address@@", spgw_c_ip)
                vm_user_data_dict[self.MME] = user_data

            elif network_function.name == self.SPGW_C:
                user_data = network_function.get_user_data()
                user_data = user_data.replace("@@domain@@", self.domain_name). \
                    replace("@@mcc@@", "265").\
                    replace("@@mnc@@", "82"). \
                    replace("@@gw_id@@", "1").\
                    replace("@@apn-1@@", "tuc").\
                    replace("@@apn-2@@", "tuc2"). \
                    replace("@@mme_ip@@", nf_ip_dict[self.MME]).\
                    replace("@@mme_hostname@@", self.vnf_vm_map[self.MME].hostname)
                vm_user_data_dict[self.SPGW_C] = user_data
#
            elif network_function.name == self.SPGW_U:
                spgw_c = self.vnf_vm_map[self.SPGW_C]
                spgw_c_ip = nf_ip_dict[self.SPGW_C]
                user_data = network_function.get_user_data()
                user_data = user_data.replace("@@domain@@", self.domain_name). \
                    replace("@@mcc@@", "265").replace("@@mnc@@", "82"). \
                    replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuc").replace("@@apn-2@@", "tuc2"). \
                    replace("@@sgwc_ip_address@@", spgw_c_ip). \
                    replace("@@sgwc_hostname@@", spgw_c.hostname).replace("@@instance@@", "1"). \
                    replace("@@network_ue_ip@@", "172.1.1.0/16")
                vm_user_data_dict[self.SPGW_U] = user_data

        return vm_user_data_dict


def main():
    service = FourGLTECore("test", "kukkalli.com", 1000)
    service_built(service)


if __name__ == "__main__":
    main()
