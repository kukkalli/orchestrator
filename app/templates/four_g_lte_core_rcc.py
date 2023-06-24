import logging

from templates.four_g_lte_core import FourGLTECore
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class FourGLTECoreRCC(FourGLTECore):

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_link_delay: float = 1.0):
        super().__init__(prefix, domain_name, bandwidth)
        rcc = VMTemplate(self.prefix, "rcc", "3")
        self.network_functions.append(rcc)

        self.nfv_v_links_list.append({"out": "mme", "in": "rcc", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "rcc", "in": "mme", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "spgw-u", "in": "rcc", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "rcc", "in": "spgw-u", "delay": max_link_delay})


def main():
    service = FourGLTECoreRCC("test-rcc", "kukkalli.com", 1000, 1.0)
    service.build()
    for vm_request in service.get_vm_requirements_list():
        print(f"VM Requirement: {vm_request.hostname}, int_id: {vm_request.int_id}")
        for link in vm_request.out_v_links:
            print(f"out link: {link.id}, int_id: {link.int_id}")
        for link in vm_request.in_v_links:
            print(f"in link: {link.id}, int_id: {link.int_id}")

    for link in service.get_v_links_list():
        print(f"link name: {link.id}, int_id: {link.int_id}")


if __name__ == "__main__":
    main()
