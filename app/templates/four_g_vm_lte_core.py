import logging
from typing import Dict

from templates.common_user_data import CommonUserData
from templates.four_g_vm_core.hss_user_data import HSSUserData
from templates.four_g_vm_core.mme_user_data import MMEUserData
from templates.four_g_vm_core.spgw_user_data import SPGWUserData
from templates.service_profile_template import ServiceProfileTemplate
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class FourGVMLTECore(ServiceProfileTemplate):
    HSS = "hss"
    MME = "mme"
    SPGW = "spgw"

    def __init__(self, name: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(name, domain_name, bandwidth)
        hss = VMTemplate(self.name, self.HSS, "2", HSSUserData.USERDATA)
        self.network_functions.append(hss)
        mme = VMTemplate(self.name, self.MME, "3", MMEUserData.USERDATA)
        self.network_functions.append(mme)
        spgw = VMTemplate(self.name, self.SPGW, "3", SPGWUserData.USERDATA)
        self.network_functions.append(spgw)

        self.nfv_v_links_list.append({"out": self.HSS, "in": self.MME, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.MME, "in": self.HSS, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.MME, "in": self.SPGW, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.SPGW, "in": self.MME, "delay": max_delay})

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        super().populate_user_data()
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
                user_data = user_data.replace("@@first_imsi@@", "265820000038021")

                # print(f"hss user data: {user_data}")
                self.vm_user_data_dict[self.HSS] = user_data

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
                self.vm_user_data_dict[self.MME] = user_data

            elif network_function.name == self.SPGW:
                mme = self.vnf_vm_map[self.MME]
                mme_ip = nf_ip_dict[self.MME]
                user_data = network_function.user_data

                user_data = user_data.replace("@@domain@@", self.domain_name). \
                    replace("@@mcc@@", "265").replace("@@mnc@@", "82"). \
                    replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuckn").replace("@@apn-2@@", "tuckn2"). \
                    replace("@@mme_ip@@", mme_ip).replace("@@mme_hostname@@", mme.hostname)
                self.vm_user_data_dict[self.SPGW] = user_data

        return self.vm_user_data_dict

    def hss_user_data(self):
        mme = self.vnf_vm_map[self.MME]
        mme_ip = nf_ip_dict[self.MME]
        user_data = network_function.user_data
        user_data = user_data.replace("@@domain@@", self.domain_name)
        user_data = user_data.replace("@@mme_ip@@", mme_ip)
        user_data = user_data.replace("@@mme_hostname@@", mme.hostname)
        user_data = user_data.replace("@@op_key@@", "0123456789ABCDEF0123456789ABCDEF")
        user_data = user_data.replace("@@lte_k@@", "0123456789ABCDEF0123456789ABCDEF")
        user_data = user_data.replace("@@apn-1@@", "tuckn")
        user_data = user_data.replace("@@first_imsi@@", "265820000038021")


def main():
    domain_name = "tu-chemnitz.de"
    user_data = CommonUserData.USERDATA + HSSUserData.USERDATA
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