import logging
import time

from templates.four_g_core_cass_db.cassandra_db import CassandraDB
from templates.four_g_core_cass_db.cassandra_user_data import CassandraDBUserData
from templates.four_g_core_cass_db.hss import HSS
from templates.four_g_core_cass_db.hss_user_data import HSSUserData
from templates.four_g_core_cass_db.mme import MME
from templates.four_g_core_cass_db.mme_user_data import MMEUserData
from templates.four_g_core_cass_db.spgwc_user_data import SPGWCUserData
from templates.four_g_core_cass_db.spgwu_user_data import SPGWUUserData
from templates.service_profile_template import ServiceProfileTemplate
from templates.four_g_core.spgwc_template import SPGWCTemplate
from templates.four_g_core.spgwu_template import SPGWUTemplate
from templates.vm_template import VMTemplate
from tosca.virtual_link import VirtualLink
from tosca.vm_requirement import VMRequirement

LOG = logging.getLogger(__name__)


class FourGLTECoreCassDB(ServiceProfileTemplate):

    def __init__(self, name: str, domain_name: str, bandwidth: int, max_link_delay: float = 1.0):
        super().__init__(name, domain_name, bandwidth, max_link_delay)
        """
        self.cass_db = CassandraDB(self.name)
        self.hss = HSS(self.name)
        self.mme = MME(self.name)
        self.spgw_c = SPGWUTemplate(self.name)
        self.spgw_u = SPGWCTemplate(self.name)
        self.__build()
        """
        cass = VMTemplate(self.name, "cassandra", "2", CassandraDBUserData.USERDATA)
        self.network_functions.append(cass)
        hss = VMTemplate(self.name, "hss", "2", HSSUserData.USERDATA)
        self.network_functions.append(hss)
        mme = VMTemplate(self.name, "mme", "3", MMEUserData.USERDATA)
        self.network_functions.append(mme)
        spgw_c = VMTemplate(self.name, "spgw-c", "2", SPGWCUserData.USERDATA)
        self.network_functions.append(spgw_c)
        spgw_u = VMTemplate(self.name, "spgw-u", "3", SPGWUUserData.USERDATA)
        self.network_functions.append(spgw_u)

        self.nfv_v_links_list.append({"out": "cassandra", "in": "hss", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "hss", "in": "cassandra", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "hss", "in": "mme", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "mme", "in": "hss", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "mme", "in": "spgw-c", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "spgw-c", "in": "mme", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "mme", "in": "spgw-u", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "spgw-u", "in": "mme", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "spgw-c", "in": "spgw-u", "delay": max_link_delay})
        self.nfv_v_links_list.append({"out": "spgw-u", "in": "spgw-c", "delay": max_link_delay})

    """
    def __build(self):
        LOG.info(f"Build FourGLTECoreCassDB: {time.time()}")

        cass_db = VMRequirement(int_id=0, hostname=self.cass_db.vm_name, flavor=self.cass_db.flavor,
                                image_id=self.cass_db.image_id, networks=self.cass_db.networks,
                                ip_addresses=self.cass_db.ip_addresses)
        self.vm_requirements_list.append(cass_db)

        hss = VMRequirement(int_id=1, hostname=self.hss.vm_name, flavor=self.hss.flavor,
                            image_id=self.hss.image_id, networks=self.hss.networks,
                            ip_addresses=self.hss.ip_addresses)
        self.vm_requirements_list.append(hss)

        mme = VMRequirement(int_id=2, hostname=self.mme.vm_name, flavor=self.mme.flavor,
                            image_id=self.mme.image_id, networks=self.mme.networks,
                            ip_addresses=self.mme.ip_addresses)
        self.vm_requirements_list.append(mme)

        spgw_c = VMRequirement(int_id=3, hostname=self.spgw_c.vm_name, flavor=self.spgw_c.flavor,
                               image_id=self.spgw_c.image_id, networks=self.spgw_c.networks,
                               ip_addresses=self.spgw_c.ip_addresses)
        self.vm_requirements_list.append(spgw_c)

        spgw_u = VMRequirement(int_id=4, hostname=self.spgw_u.vm_name, flavor=self.spgw_c.flavor,
                               image_id=self.spgw_c.image_id, networks=self.spgw_c.networks,
                               ip_addresses=self.spgw_c.ip_addresses)
        self.vm_requirements_list.append(spgw_u)

        db_hss = VirtualLink("db-hss", 0, 1, 0, self.bandwidth, 30)
        self.v_links.append(db_hss)
        hss_db = VirtualLink("hss-db", 1, 0, 1, self.bandwidth, 30)
        self.v_links.append(hss_db)

        hss_mme = VirtualLink("hss-mme", 2, 2, 1, self.bandwidth, 30)
        self.v_links.append(hss_mme)
        mme_hss = VirtualLink("mme-hss", 3, 1, 2, self.bandwidth, 30)
        self.v_links.append(mme_hss)

        mme_spgw_c = VirtualLink("mme-spgw-c", 4, 3, 2, self.bandwidth, 10)
        self.v_links.append(mme_spgw_c)
        spgw_c_mme = VirtualLink("spgw-c-mme", 5, 2, 3, self.bandwidth, 10)
        self.v_links.append(spgw_c_mme)

        mme_spgw_u = VirtualLink("mme-spgw-u", 6, 4, 2, self.bandwidth, 10)
        self.v_links.append(mme_spgw_u)
        spgw_u_mme = VirtualLink("spgw-u-mme", 7, 2, 4, self.bandwidth, 10)
        self.v_links.append(spgw_u_mme)

        spgw_c_u = VirtualLink("spgw-c-u", 8, 4, 3, self.bandwidth, 10)
        self.v_links.append(spgw_c_u)
        spgw_u_c = VirtualLink("spgw-u-c", 9, 3, 4, self.bandwidth, 10)
        self.v_links.append(spgw_u_c)
        LOG.info(f"Built FourGLTECoreCassDB: {time.time()}")
    """


def main():
    service = FourGLTECoreCassDB("test", "kukkalli.com", 1000)
    service.build()
    flavor = service.flavor_id_map["2"]
    print(f"Flavor: id: {flavor.id}, name: {flavor.name}, vcpus: {flavor.vcpus}, ram: {flavor.ram}")
    for vm_request in service.get_vm_requirements_list():
        print(f"VM Requirement: {vm_request.hostname}, int_id: {vm_request.int_id}")

    for link in service.get_v_links_list():
        print(f"link name: {link.id}, int_id: {link.int_id}")


if __name__ == "__main__":
    main()
