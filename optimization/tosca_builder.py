from typing import List

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.nova.nova_details import Nova
from tosca.tosca_input import TOSCAInput
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement


class TOSCABuilder:

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.vm_requirements: List[VMRequirement] = []
        self.v_links: List[VirtualLink] = []
        self.nova = Nova(AuthenticateConnection().get_connection())

    def __create_test_server_requirements(self):
        hss = VMRequirement(0, self.request_id+"-hss", self.nova.get_flavor_by_id("1"),
                            image_id="c761dd72-eba8-4b73-8f07-b6e575115bff",
                            network_id="9e373e2c-0372-4a06-81a1-bc1cb4c62b85", ip_address="10.11.1.21")
        self.vm_requirements.append(hss)

        mme = VMRequirement(1, self.request_id+"-mme", self.nova.get_flavor_by_id("3"),
                            image_id="c82a2ad8-cb21-44c0-8daa-7bf8a03bf138",
                            network_id="9e373e2c-0372-4a06-81a1-bc1cb4c62b85", ip_address="10.11.1.22")
        self.vm_requirements.append(mme)

        spgw = VMRequirement(2, self.request_id+"-spgw", self.nova.get_flavor_by_id("3"),
                             image_id="49bb635a-d8c2-4d28-b439-e7c7e1c2b275",
                             network_id="9e373e2c-0372-4a06-81a1-bc1cb4c62b85", ip_address="10.11.1.23")
        self.vm_requirements.append(spgw)

        """
        spgw01 = VMRequirement(3, "spgw01", self.nova.get_flavor_by_id("4"), "0af72659-a5c0-40a3-8b55-0b398e6b94f2",
                               "9e373e2c-0372-4a06-81a1-bc1cb4c62b85", ip_address="10.11.1.24")
        self.vm_requirements.append(spgw01)
        spgw02 = VMRequirement(4, "spgw02", self.nova.get_flavor_by_id("4"), "0af72659-a5c0-40a3-8b55-0b398e6b94f2",
                               "9e373e2c-0372-4a06-81a1-bc1cb4c62b85", ip_address="10.11.1.25")
        self.vm_requirements.append(spgw02)
        spgw03 = VMRequirement(5, "spgw03", self.nova.get_flavor_by_id("4"), "0af72659-a5c0-40a3-8b55-0b398e6b94f2",
                               "9e373e2c-0372-4a06-81a1-bc1cb4c62b85", ip_address="10.11.1.26")
        self.vm_requirements.append(spgw03)
        """
        self.nova.close_connection()

    def __create_test_virtual_links(self):
        hss_mme = VirtualLink("hss-mme", 0, 1, 0, 1000, 30)
        self.v_links.append(hss_mme)
        mme_hss = VirtualLink("mme-hss", 1, 0, 1, 1000, 30)
        self.v_links.append(mme_hss)

        mme_spgw = VirtualLink("mme-spgw", 2, 2, 1, 1000, 10)
        self.v_links.append(mme_spgw)
        spgw_mme = VirtualLink("spgw-mme", 3, 1, 2, 1000, 10)
        self.v_links.append(spgw_mme)

        """
            Variable            X 
        -------------------------
               x_0_0            1 
               x_1_0            1 
               x_2_1            1 
            flow_3_0            1 
            flow_2_2            1 
            flow_2_5            1 
            flow_3_6            1 
            flow_2_8            1 
            flow_3_9            1 
           flow_3_10            1 
           flow_2_11            1 
                  mu     0.131291 
                   z            1 
        """

        """
        mme_spgw01 = VirtualLink("mme-spgw01", 4, 3, 1)
        self.v_links.append(mme_spgw01)
        spgw01_mme = VirtualLink("spgw01-mme", 5, 1, 3)
        self.v_links.append(spgw01_mme)

        mme_spgw02 = VirtualLink("mme-spgw02", 6, 4, 1)
        self.v_links.append(mme_spgw02)
        spgw02_mme = VirtualLink("spgw02-mme", 7, 1, 4)
        self.v_links.append(spgw02_mme)

        mme_spgw03 = VirtualLink("mme-spgw03", 8, 5, 1)
        self.v_links.append(mme_spgw03)
        spgw03_mme = VirtualLink("spgw03-mme", 9, 1, 5)
        self.v_links.append(spgw03_mme)
        """

    def build_tosca(self) -> TOSCAInput:
        self.__create_test_server_requirements()
        self.__create_test_virtual_links()
        tosca = TOSCAInput(self.request_id, self.vm_requirements, self.v_links)
        tosca.build()
        print("no of v_links: {}".format(len(tosca.v_links)))
        print("no of VMs: {}".format(len(tosca.vm_requirements)))
        for vm in tosca.vm_requirements:
            print("VM ID: {}, VM Name: {}, VM int_id: {}".format(vm.id, vm.hostname, vm.int_id))
            for v_link in vm.in_v_links:
                print("In v_link ID: {}, int_id: {}".format(v_link.id, v_link.int_id))
            for v_link in vm.out_v_links:
                print("Out v_link ID: {}, int_id: {}".format(v_link.id, v_link.int_id))
        return tosca


def main():
    builder = TOSCABuilder("hanif")
    builder.build_tosca()


if __name__ == "__main__":
    main()
