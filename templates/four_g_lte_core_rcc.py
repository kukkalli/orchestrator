from templates.four_g_lte_core import FourGLTECore
from templates.rcc_template import RCCTemplate
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement


class FourGLTECoreRCC(FourGLTECore):

    def __init__(self, name: str, domain_name: str, bandwidth: int):
        super().__init__(name, domain_name, bandwidth)
        self.rcc = RCCTemplate(name)
        self.__build()

    def __build(self):
        rcc = VMRequirement(3, self.rcc.vm_name, self.nova.get_flavor_by_id(self.rcc.flavor),
                            image_id=self.rcc.image_id, network_id=self.rcc.network_id, ip_address=self.rcc.ip_address)
        self.vm_requirements.append(rcc)

        mme_rcc = VirtualLink("mme-rcc", 4, 3, 1, self.bandwidth, 10)
        self.v_links.append(mme_rcc)
        rcc_mme = VirtualLink("rcc-mme", 5, 1, 3, self.bandwidth, 10)
        self.v_links.append(rcc_mme)

        spgw_rcc = VirtualLink("spgw-rcc", 7, 1, 2, self.bandwidth, 10)
        self.v_links.append(spgw_rcc)
        rcc_spgw = VirtualLink("rcc-spgw", 6, 2, 1, self.bandwidth, 10)
        self.v_links.append(rcc_spgw)

