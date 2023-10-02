import logging
import re
import time
import uuid
import mysql.connector as database
from flask import abort

from db.maria_database import MariaDB
from templates.four_g_lte_core import FourGLTECore
from templates.four_g_lte_core_cass_db import FourGLTECoreCassDB
from templates.four_g_lte_core_rcc import FourGLTECoreRCC
from templates.four_g_vm_lte_core import FourGVMLTECore
from templates.serviceprofiles import ServiceProfiles
from templates.oai_5gcn_template import OAI5GCN
from templates.oai_5gcn_du_template import OAI5GCNAndDU

LOG = logging.getLogger(__name__)


class InputRequest:

    def __init__(self, name: str, service_profile: str, domain_name: str = "tu-chemnitz.de", bandwidth: int = 100,
                 max_link_delay: float = 50.0):
        self.name = name
        prefix = re.sub('[^a-zA-Z\d \n\.]', '', name)
        prefix = prefix.replace(" ", "-").lower()
        self.hostname_prefix = (prefix[:20]) if len(prefix) > 20 else prefix
        self.service_uuid = uuid.uuid4().hex
        self.service_profile: ServiceProfiles = ServiceProfiles(service_profile)
        self.domain_name = domain_name
        self.bandwidth = bandwidth
        self.max_link_delay = max_link_delay
        self.mariadb = MariaDB()
        # self.__add_service_chain()

    def __add_service_chain(self):

        try:
            LOG.debug(f"generated UUID: {self.service_uuid}")
            values_tuple = (self.service_uuid, self.name, "hanif", "hanif")
            sql_query = """INSERT INTO `service_chain` (`service_uuid`, `service_name`, `start_date`, `end_date`,
             `created_on`, `created_by`, `updated_on`, `updated_by`)
              VALUES (%s, %s, NOW(), NOW(), NOW(), %s, NOW(), %s)"""
            connection = self.mariadb.get_db_connection()
            cursor = connection.cursor(prepared=True)
            result = cursor.execute(sql_query, values_tuple)
            LOG.debug(f"Result after execute: {result}")
            connection.commit()
            LOG.debug("Data inserted successfully into service_chain table using the prepared statement")
            cursor.close()
        except database.Error as error:
            LOG.exception(f"Insert Operation failed due to \n {error}", exc_info=True)
        finally:
            self.mariadb.close_connection()
            LOG.debug("MariaDB connection is closed")
            self.__add_service_chain_values()

    def __add_service_chain_values(self):
        try:
            connection = self.mariadb.get_db_connection()
            if len(self.domain_name) > 0:
                LOG.debug(f"service_uuid: {self.service_uuid}, domain_name: {self.domain_name}")
                values_tuple = (self.service_uuid, "domain_name", self.domain_name)
                sql_query = """INSERT INTO `sc_parameters` (`service_uuid`, `key`, `value`)
                  VALUES (%s, %s, %s)"""
                cursor = connection.cursor(prepared=True)
                cursor.execute(sql_query, values_tuple)
            if self.bandwidth > 0:
                LOG.debug(f"service_uuid: {self.service_uuid}, bandwidth: {self.bandwidth}")
                values_tuple = (self.service_uuid, "bandwidth", self.bandwidth)
                sql_query = """INSERT INTO `sc_parameters` (`service_uuid`, `key`, `value`)
                  VALUES (%s, %s, %s)"""
                cursor = connection.cursor(prepared=True)
                cursor.execute(sql_query, values_tuple)
            if self.max_link_delay > 0:
                LOG.debug(f"service_uuid: {self.service_uuid}, max_link_delay: {self.max_link_delay}")
                values_tuple = (self.service_uuid, "max_link_delay", self.max_link_delay)
                sql_query = """INSERT INTO `sc_parameters` (`service_uuid`, `key`, `value`)
                  VALUES (%s, %s, %s)"""
                cursor = connection.cursor(prepared=True)
                cursor.execute(sql_query, values_tuple)

            connection.commit()
            LOG.debug("Data inserted successfully into sc_parameters table using the prepared statement")
        except database.Error as error:
            LOG.exception(f"Insert Operation failed due to \n {error}", exc_info=True)
        finally:
            self.mariadb.close_connection()
            LOG.info("MySQL connection is closed")

    def get_service_chains(self):
        try:
            sql_query = "SELECT * FROM `service-chain`"
            connection = self.mariadb.get_db_connection()

        except database.Error as error:
            LOG.error(f"Get Operation failed due to \n {error}")
        self.mariadb.close_connection()

    def get_service_chain_name(self):
        return self.name

    def get_service_profile(self):
        return self.service_profile

    def get_service_template(self):
        LOG.info(f"Fetch Service Profile Template: {time.time()}")
        service_profile = None
        if self.service_profile == ServiceProfiles.FOUR_G_LTE_CORE:
            service_profile = FourGLTECore(self.hostname_prefix, self.domain_name,
                                           self.bandwidth, self.max_link_delay)
        elif self.service_profile == ServiceProfiles.FOUR_G_LTE_CORE_CASS_DB:
            service_profile = FourGLTECoreCassDB(self.hostname_prefix, self.domain_name,
                                                 self.bandwidth, self.max_link_delay)
        elif self.service_profile == ServiceProfiles.FOUR_G_LTE_CORE_BBU:
            service_profile = FourGLTECoreRCC(self.hostname_prefix, self.domain_name, self.bandwidth)
        elif self.service_profile == ServiceProfiles.FOUR_G_LTE_CORE_BBU_CASS_DB:
            service_profile = FourGLTECoreRCC(self.hostname_prefix, self.domain_name, self.bandwidth)
        elif self.service_profile == ServiceProfiles.OAI_5GCN:
            service_profile = OAI5GCN(self.hostname_prefix, self.domain_name, self.bandwidth, self.max_link_delay)
        elif self.service_profile == ServiceProfiles.OAI_5GCN_DU:
            service_profile = OAI5GCNAndDU(self.hostname_prefix, self.domain_name, self.bandwidth, self.max_link_delay)
        elif self.service_profile == ServiceProfiles.FOUR_G_VM_LTE_CORE:
            service_profile = FourGVMLTECore(self.hostname_prefix, self.domain_name, self.bandwidth)
        else:
            LOG.error(f"Service Profile Template Not Found: {time.time()}")
            abort(404)
        service_profile.build()
        LOG.info(f"Service Profile Template Fetched: {time.time()}")
        return service_profile

    def get_domain_name(self):
        return self.domain_name

    def get_bandwidth(self):
        return self.bandwidth

    def get_max_link_delay(self):
        return self.max_link_delay


def main():
    input_request = InputRequest(name="Hanif testing orchestrator", service_profile="OAI_5GCN", bandwidth=150,
                                 max_link_delay=50)
    print(f"name: {input_request.get_service_chain_name()}, service_profile: {input_request.get_service_profile()}", )
    print(f'service template: {input_request.get_service_template()}')


if __name__ == "__main__":
    main()
