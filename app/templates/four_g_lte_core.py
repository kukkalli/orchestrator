import logging
from typing import Dict

from templates.common_user_data import CommonUserData
from templates.four_g_core.hss_user_data import HSSUserData
from templates.four_g_core.mme_user_data import MMEUserData
from templates.four_g_core.spgwc_user_data import SPGWCUserData
from templates.four_g_core.spgwu_user_data import SPGWUUserData
from templates.service_profile_template import ServiceProfileTemplate
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class FourGLTECore(ServiceProfileTemplate):
    HSS = "hss"
    MME = "mme"
    SPGW_C = "spgw-c"
    SPGW_U = "spgw-u"

    def __init__(self, name: str, domain_name: str, bandwidth: int, max_delay: float = 50.0):
        super().__init__(name, domain_name, bandwidth)
        hss = VMTemplate(self.name, "hss", "2", HSSUserData.USERDATA)
        self.network_functions.append(hss)
        mme = VMTemplate(self.name, "mme", "3", MMEUserData.USERDATA)
        self.network_functions.append(mme)
        spgw_c = VMTemplate(self.name, "spgw-c", "2", SPGWCUserData.USERDATA)
        self.network_functions.append(spgw_c)
        spgw_u = VMTemplate(self.name, "spgw-u", "3", SPGWUUserData.USERDATA)
        self.network_functions.append(spgw_u)

        self.nfv_v_links_list.append({"out": "hss", "in": "mme", "delay": max_delay * 0.4})
        self.nfv_v_links_list.append({"out": "mme", "in": "hss", "delay": max_delay * 0.4})
        self.nfv_v_links_list.append({"out": "mme", "in": "spgw-c", "delay": max_delay * 0.25})
        self.nfv_v_links_list.append({"out": "spgw-c", "in": "mme", "delay": max_delay * 0.25})
        self.nfv_v_links_list.append({"out": "mme", "in": "spgw-u", "delay": max_delay * 0.25})
        self.nfv_v_links_list.append({"out": "spgw-u", "in": "mme", "delay": max_delay * 0.25})
        self.nfv_v_links_list.append({"out": "spgw-c", "in": "spgw-u", "delay": max_delay * 0.1})
        self.nfv_v_links_list.append({"out": "spgw-u", "in": "spgw-c", "delay": max_delay * 0.1})

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        print(f"I am in 4G LTE Core, {self.domain_name}")
        vm_user_data_dict: Dict[str, str] = {}
        for network_function in self.get_network_functions():
            if network_function.name == self.HSS:
                mme = self.vnf_vm_map[self.MME]
                mme_ip = nf_ip_dict[self.MME]
                user_data = network_function.user_data
                user_data = user_data.replace("@@domain@@", self.domain_name)
                user_data = user_data.replace("@@mme_ip@@", mme_ip)
                user_data = user_data.replace("@@mme_hostname@@", mme.hostname)
                user_data = user_data.replace("@@op_key@@", "0123456789ABCDEF0123456789ABCDEF")
                user_data = user_data.replace("@@lte_k@@", "0123456789ABCDEF0123456789ABCDEF")
                user_data = user_data.replace("@@apn-1@@", "tuckn")
                user_data = user_data.replace("@@apn-2@@", "tuckn2")
                user_data = user_data.replace("@@first_imsi@@", "265820000038021")

                print(f"hss user data: {user_data}")
                vm_user_data_dict[self.HSS] = user_data
            elif network_function.name == self.MME:
                hss_ip = nf_ip_dict[self.HSS]
                hss = self.vnf_vm_map[self.HSS]
                spgw_c_ip = nf_ip_dict[self.SPGW_C]

                user_data = network_function.user_data
                user_data = user_data.replace("@@domain@@", self.domain_name)
                user_data = user_data.replace("@@hss_ip@@", hss_ip)
                user_data = user_data.replace("@@hss_hostname@@", hss.hostname)
                user_data = user_data.replace("@@mcc@@", "265")
                user_data = user_data.replace("@@mnc@@", "82")
                user_data = user_data.replace("@@mme_gid@@", "32768")
                user_data = user_data.replace("@@mme_code@@", "3")
                user_data = user_data.replace("@@sgwc_ip_address@@", spgw_c_ip)
                vm_user_data_dict[self.MME] = user_data
            elif network_function.name == self.SPGW_C:
                mme = self.vnf_vm_map[self.MME]
                mme_ip = nf_ip_dict[self.MME]
                user_data = network_function.user_data
                user_data = user_data.replace("@@domain@@", self.domain_name). \
                    replace("@@mcc@@", "265").replace("@@mnc@@", "82"). \
                    replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuckn").replace("@@apn-2@@", "tuckn2"). \
                    replace("@@mme_ip@@", mme_ip).replace("@@mme_hostname@@", mme.hostname)
                vm_user_data_dict[self.SPGW_C] = user_data
            elif network_function.name == self.SPGW_U:
                spgw_c = self.vnf_vm_map[self.SPGW_C]
                spgw_c_ip = nf_ip_dict[self.SPGW_C]
                user_data = network_function.user_data
                user_data = user_data.replace("@@domain@@", self.domain_name). \
                    replace("@@mcc@@", "265").replace("@@mnc@@", "82"). \
                    replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuckn").replace("@@apn-2@@", "tuckn2"). \
                    replace("@@sgwc_ip_address@@", spgw_c_ip). \
                    replace("@@sgwc_hostname@@", spgw_c.hostname).replace("@@instance@@", "1"). \
                    replace("@@network_ue_ip@@", "12.1.1.0/24")
                vm_user_data_dict[self.SPGW_U] = user_data

        return vm_user_data_dict


def main():
    domain_name = "tu-chemnitz.de"
    user_data = CommonUserData.USERDATA  + HSSUserData.USERDATA
    user_data = user_data.replace("@@domain@@", domain_name)
    print(f'after: {user_data}')
    # print(f'user data: {user_data.replace("@@domain@@", domain_name)}')

    """
    service = FourGLTECore("test", "kukkalli.com", 1000)
    service.build()
    flavor = service.flavor_id_map["2"]
    print(f"Flavor: id: {flavor.id}, name: {flavor.name},, vcpus: {flavor.vcpus}, ram: {flavor.ram}")
    for vm_request in service.get_vm_requirements_list():
        print(f"VM Requirement: {vm_request.hostname}, int_id: {vm_request.int_id}")

    for link in service.get_v_links_list():
        print(f"link name: {link.id}, int_id: {link.int_id}")
    """


if __name__ == "__main__":
    main()
