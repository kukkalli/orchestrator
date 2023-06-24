import logging
from typing import Dict

from templates.common_user_data import CommonUserData
from templates.four_g_vm_core.hss_user_data import HSSUserData
from templates.four_g_vm_core.mme_user_data import MMEUserData
from templates.four_g_vm_core.spgw_user_data import SPGWUserData
from templates.pdn_type import PDNType
from templates.service_profile_template import ServiceProfileTemplate
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class FourGVMLTECore(ServiceProfileTemplate):
    HSS = "hss"
    MME = "mme"
    SPGW = "spgw"

    def __init__(self, name: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(name, domain_name, bandwidth)
        hss = VMTemplate(self.prefix, self.HSS, "2", HSSUserData.USERDATA)
        self.network_functions.append(hss)
        mme = VMTemplate(self.prefix, self.MME, "3", MMEUserData.USERDATA)
        self.network_functions.append(mme)
        spgw = VMTemplate(self.prefix, self.SPGW, "3", SPGWUserData.USERDATA)
        self.network_functions.append(spgw)

        self.nfv_v_links_list.append({"out": self.HSS, "in": self.MME, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.MME, "in": self.HSS, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.MME, "in": self.SPGW, "delay": max_delay})
        self.nfv_v_links_list.append({"out": self.SPGW, "in": self.MME, "delay": max_delay})

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        super().populate_user_data()
        for network_function in self.get_network_functions():
            if network_function.prefix == self.HSS:
                self.hss_user_data(network_function, nf_ip_dict)
            elif network_function.prefix == self.MME:
                self.mme_user_data(network_function, nf_ip_dict)
            elif network_function.prefix == self.SPGW:
                self.spgw_user_data(network_function, nf_ip_dict)

        return self.vm_user_data_dict

    def hss_user_data(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]):
        mme = self.vnf_vm_map[self.MME]
        mme_ip = nf_ip_dict[self.MME]
        spgw = self.vnf_vm_map[self.SPGW]
        spgw_ip = nf_ip_dict[self.SPGW]

        hss_user_data = network_function.user_data
        hss_user_data = hss_user_data.replace("@@domain@@", self.domain_name)
        hss_user_data = hss_user_data.replace("@@mme_ip@@", mme_ip)
        hss_user_data = hss_user_data.replace("@@mme_hostname@@", mme.hostname)
        hss_user_data = hss_user_data.replace("@@operator_key@@", "0123456789ABCDEF0123456789ABCDEF")
        hss_user_data = hss_user_data.replace("@@country_code@@", "DE")
        hss_user_data = hss_user_data.replace("@@state_code@@", "SN")
        hss_user_data = hss_user_data.replace("@@csn@@", "TUC")
        hss_user_data = hss_user_data.replace("@@cfn@@", "TU-Chemnitz")
        hss_user_data = hss_user_data.replace("@@apn@@", "tuc.ipv4")
        hss_user_data = hss_user_data.replace("@@pdn_type@@", PDNType.IPv4.value)
        hss_user_data = hss_user_data.replace("@@user_imsi@@", "265820000038021")
        hss_user_data = hss_user_data.replace("@@spgw_ip@@", spgw_ip)
        hss_user_data = hss_user_data.replace("@@spgw_hostname@@", spgw.hostname)
        hss_user_data = hss_user_data.replace("@@security_key@@", "0123456789ABCDEF0123456789ABCDEF")
        self.vm_user_data_dict[self.HSS] = hss_user_data

    def mme_user_data(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]):
        hss = self.vnf_vm_map[self.HSS]
        hss_ip = nf_ip_dict[self.HSS]
        mme_ip = nf_ip_dict[self.MME]
        spgw = self.vnf_vm_map[self.SPGW]
        spgw_ip = nf_ip_dict[self.SPGW]

        mme_user_data = network_function.user_data
        mme_user_data = mme_user_data.replace("@@domain@@", self.domain_name)
        mme_user_data = mme_user_data.replace("@@hss_ip@@", hss_ip)
        mme_user_data = mme_user_data.replace("@@hss_hostname@@", hss.hostname)
        mme_user_data = mme_user_data.replace("@@mme_ip@@", mme_ip)
        mme_user_data = mme_user_data.replace("@@mcc@@", "265")
        mme_user_data = mme_user_data.replace("@@mnc@@", "82")
        mme_user_data = mme_user_data.replace("@@mme_gid@@", "32768")
        mme_user_data = mme_user_data.replace("@@mme_code@@", "3")
        mme_user_data = mme_user_data.replace("@@spgw_ip@@", spgw_ip)
        mme_user_data = mme_user_data.replace("@@spgw_ip@@", spgw_ip)
        self.vm_user_data_dict[self.MME] = mme_user_data

    def spgw_user_data(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]):
        mme = self.vnf_vm_map[self.MME]
        mme_ip = nf_ip_dict[self.MME]
        spgw_user_data = network_function.user_data

        spgw_user_data = spgw_user_data.replace("@@domain@@", self.domain_name)
        spgw_user_data = spgw_user_data.replace("@@mcc@@", "265")
        spgw_user_data = spgw_user_data.replace("@@mnc@@", "82")
        spgw_user_data = spgw_user_data.replace("@@gw_id@@", "1")
        spgw_user_data = spgw_user_data.replace("@@apn-1@@", "tuckn")
        spgw_user_data = spgw_user_data.replace("@@apn-2@@", "tuckn2")
        spgw_user_data = spgw_user_data.replace("@@mme_ip@@", mme_ip)
        spgw_user_data = spgw_user_data.replace("@@mme_hostname@@", mme.hostname)
        self.vm_user_data_dict[self.SPGW] = spgw_user_data


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
