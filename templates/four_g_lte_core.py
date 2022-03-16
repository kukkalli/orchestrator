from templates.hss_template import HSSTemplate
from templates.mme_template import MMETemplate
from templates.service_profile_template import ServiceProfileTemplate
from templates.spgw_template import SPGWTemplate
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement


class FourGLTECore(ServiceProfileTemplate):

    def __init__(self, name: str, domain_name: str, bandwidth: int):
        super().__init__(name, domain_name, bandwidth)
        self.hss = HSSTemplate(self.name)
        self.mme = MMETemplate(self.name)
        self.spgw = SPGWTemplate(self.name)
        self.__build()

    def __build(self):
        hss = VMRequirement(0, self.hss.vm_name, self.nova.get_flavor_by_id(self.hss.flavor),
                            image_id=self.hss.image_id, network_id=self.hss.network_id, ip_address=self.hss.ip_address)
        self.vm_requirements.append(hss)

        mme = VMRequirement(1, self.mme.vm_name, self.nova.get_flavor_by_id(self.mme.flavor),
                            image_id=self.mme.image_id, network_id=self.mme.network_id, ip_address=self.mme.ip_address)
        self.vm_requirements.append(mme)

        spgw = VMRequirement(2, self.spgw.vm_name, self.nova.get_flavor_by_id(self.spgw.flavor),
                             image_id=self.spgw.image_id, network_id=self.spgw.network_id,
                             ip_address=self.spgw.ip_address)
        self.vm_requirements.append(spgw)

        hss_mme = VirtualLink("hss-mme", 0, 1, 0, self.bandwidth, 30)
        self.v_links.append(hss_mme)
        mme_hss = VirtualLink("mme-hss", 1, 0, 1, self.bandwidth, 30)
        self.v_links.append(mme_hss)

        mme_spgw = VirtualLink("mme-spgw", 2, 2, 1, self.bandwidth, 10)
        self.v_links.append(mme_spgw)
        spgw_mme = VirtualLink("spgw-mme", 3, 1, 2, self.bandwidth, 10)
        self.v_links.append(spgw_mme)

