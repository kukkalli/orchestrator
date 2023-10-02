import logging

from templates.four_g_core.spgwc_template import SPGWCTemplate
from templates.four_g_core.spgwu_template import SPGWUTemplate
from templates.four_g_core_cass_db.cassandra_db import CassandraDB
from templates.four_g_core_cass_db.cassandra_user_data import CassandraDBUserData
from templates.four_g_core_cass_db.hss import HSS
from templates.four_g_core_cass_db.hss_user_data import HSSUserData
from templates.four_g_core_cass_db.mme import MME
from templates.four_g_core_cass_db.mme_user_data import MMEUserData
from templates.four_g_core_cass_db.spgwc_user_data import SPGWCUserData
from templates.four_g_core_cass_db.spgwu_user_data import SPGWUUserData
from templates.service_profile_template import ServiceProfileTemplate
from templates.vm_template import VMTemplate
from test_scripts.service_build_test import service_built

LOG = logging.getLogger(__name__)


class FourGLTECoreCassDB(ServiceProfileTemplate):

    CASS_DB = "cassandra"
    HSS = "hss"
    MME = "mme"
    SPGW_C = "spgw-c"
    SPGW_U = "spgw-u"

    def __init__(self, name: str, domain_name: str, bandwidth: int, max_link_delay: float = 1.0):
        super().__init__(name, domain_name, bandwidth, max_link_delay)
        # self.network_functions.append(CassandraDB(name, self.CASS_DB))
        # self.network_functions.append(HSSTemplate(prefix, self.HSS))
        # self.network_functions.append(MMETemplate(prefix, self.MME))
        # self.network_functions.append(SPGWCTemplate(prefix, self.SPGW_C))
        # self.network_functions.append(SPGWUTemplate(prefix, self.SPGW_U))
        # self.cass_db = CassandraDB(self.name)

        self.hss = HSS(self.name)
        self.mme = MME(self.name)
        self.spgw_c = SPGWUTemplate(self.name)
        self.spgw_u = SPGWCTemplate(self.name)
        self.__build()
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


def main():
    service = FourGLTECoreCassDB("test", "kukkalli.com", 1000)
    service_built(service)


if __name__ == "__main__":
    main()
