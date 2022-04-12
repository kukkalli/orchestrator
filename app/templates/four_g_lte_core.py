import logging
import time

from templates.hss_template import HSSTemplate
from templates.mme_template import MMETemplate
from templates.service_profile_template import ServiceProfileTemplate
from templates.spgwc_template import SPGWCTemplate
from templates.spgwu_template import SPGWUTemplate
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement

log = logging.getLogger(__name__)


class FourGLTECore(ServiceProfileTemplate):

    def __init__(self, name: str, domain_name: str, bandwidth: int):
        super().__init__(name, domain_name, bandwidth)
        self.hss = HSSTemplate(self.name)
        self.mme = MMETemplate(self.name)
        self.spgw_c = SPGWUTemplate(self.name)
        self.spgw_u = SPGWCTemplate(self.name)
        self.__build()

    def __build(self):
        log.info(f"Build FourGLTECore: {time.time()}")
        hss = VMRequirement(int_id=0, hostname=self.hss.vm_name, flavor=self.nova.get_flavor_by_id(self.hss.flavor),
                            image_id=self.hss.image_id, networks=self.hss.networks,
                            ip_addresses=self.hss.ip_addresses)
        self.vm_requirements.append(hss)

        mme = VMRequirement(1, self.mme.vm_name, self.nova.get_flavor_by_id(self.mme.flavor),
                            image_id=self.mme.image_id, networks=self.mme.networks,
                            ip_addresses=self.mme.ip_addresses)
        self.vm_requirements.append(mme)

        spgw_c = VMRequirement(2, self.spgw_c.vm_name, self.nova.get_flavor_by_id(self.spgw_c.flavor),
                               image_id=self.spgw_c.image_id, networks=self.spgw_c.networks,
                               ip_addresses=self.spgw_c.ip_addresses)
        self.vm_requirements.append(spgw_c)

        spgw_u = VMRequirement(3, self.spgw_u.vm_name, self.nova.get_flavor_by_id(self.spgw_c.flavor),
                               image_id=self.spgw_c.image_id, networks=self.spgw_c.networks,
                               ip_addresses=self.spgw_c.ip_addresses)
        self.vm_requirements.append(spgw_u)

        hss_mme = VirtualLink("hss-mme", 0, 1, 0, self.bandwidth, 30)
        self.v_links.append(hss_mme)
        mme_hss = VirtualLink("mme-hss", 1, 0, 1, self.bandwidth, 30)
        self.v_links.append(mme_hss)

        mme_spgw_c = VirtualLink("mme-spgw-c", 2, 2, 1, self.bandwidth, 10)
        self.v_links.append(mme_spgw_c)
        spgw_c_mme = VirtualLink("spgw-c-mme", 3, 1, 2, self.bandwidth, 10)
        self.v_links.append(spgw_c_mme)

        mme_spgw_u = VirtualLink("mme-spgw-u", 4, 2, 1, self.bandwidth, 10)
        self.v_links.append(mme_spgw_u)
        spgw_u_mme = VirtualLink("spgw-u-mme", 5, 1, 2, self.bandwidth, 10)
        self.v_links.append(spgw_u_mme)
        log.info(f"Built FourGLTECore: {time.time()}")

