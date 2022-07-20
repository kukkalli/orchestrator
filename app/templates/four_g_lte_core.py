import logging

from templates.four_g_core.hss_user_data import HSSUserData
from templates.four_g_core.mme_user_data import MMEUserData
from templates.four_g_core.spgwc_user_data import SPGWCUserData
from templates.four_g_core.spgwu_user_data import SPGWUUserData
from templates.service_profile_template import ServiceProfileTemplate
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class FourGLTECore(ServiceProfileTemplate):

    def __init__(self, name: str, domain_name: str, bandwidth: int):
        super().__init__(name, domain_name, bandwidth)
        hss = VMTemplate(self.name, "hss", "2", HSSUserData.USERDATA)
        self.network_functions.append(hss)
        mme = VMTemplate(self.name, "mme", "3", MMEUserData.USERDATA)
        self.network_functions.append(mme)
        spgw_c = VMTemplate(self.name, "spgw-c", "2", SPGWCUserData.USERDATA)
        self.network_functions.append(spgw_c)
        spgw_u = VMTemplate(self.name, "spgw-u", "3", SPGWUUserData.USERDATA)
        self.network_functions.append(spgw_u)

        self.nfv_v_links_list.append({"out": "hss", "in": "mme", "delay": 50})
        self.nfv_v_links_list.append({"out": "mme", "in": "hss", "delay": 50})
        self.nfv_v_links_list.append({"out": "mme", "in": "spgw-c", "delay": 30})
        self.nfv_v_links_list.append({"out": "spgw-c", "in": "mme", "delay": 30})
        self.nfv_v_links_list.append({"out": "mme", "in": "spgw-u", "delay": 30})
        self.nfv_v_links_list.append({"out": "spgw-u", "in": "mme", "delay": 30})
        self.nfv_v_links_list.append({"out": "spgw-c", "in": "spgw-u", "delay": 30})
        self.nfv_v_links_list.append({"out": "spgw-u", "in": "spgw-c", "delay": 30})


def main():
    service = FourGLTECore("test", "kukkalli.com", 1000)
    service.build()
    flavor = service.flavor_id_map["2"]
    print(f"Flavor: id: {flavor.id}, name: {flavor.name},, vcpus: {flavor.vcpus}, ram: {flavor.ram}")
    for vm_request in service.get_vm_requirements_list():
        print(f"VM Requirement: {vm_request.hostname}, int_id: {vm_request.int_id}")

    for link in service.get_v_links_list():
        print(f"link name: {link.id}, int_id: {link.int_id}")


if __name__ == "__main__":
    main()
