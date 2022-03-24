import logging
import time
import uuid
import mysql.connector as database
from flask import abort

from db.maria_database import MariaDB
from templates.four_g_lte_core import FourGLTECore
from templates.four_g_lte_core_rcc import FourGLTECoreRCC
from templates.serviceprofiles import ServiceProfiles

log = logging.getLogger(__name__)


class InputRequest:

    def __init__(self, name: str, service_profile: str, domain_name: str = "tu-chemnitz.de", bandwidth: int = 100,
                 max_link_delay: int = 100):
        self.name = name.replace(" ", "-").lower()
        self.domain_name = domain_name
        self.service_profile: ServiceProfiles = ServiceProfiles(service_profile)
        self.bandwidth = bandwidth
        self.max_link_delay = max_link_delay
        self.mariadb = MariaDB()
        self.__add_service_chain()

    def __add_service_chain(self):
        service_uuid = uuid.uuid4().hex
        try:
            log.debug(f"generated UUID: {service_uuid}")
            values_tuple = (service_uuid, self.name, "hanif", "hanif")
            sql_query = """INSERT INTO `service_chain` (`service_uuid`, `service_name`, `start_date`, `end_date`,
             `created_on`, `created_by`, `updated_on`, `updated_by`)
              VALUES (%s, %s, NOW(), NOW(), NOW(), %s, NOW(), %s)"""
            connection = self.mariadb.get_db_connection()
            cursor = connection.cursor(prepared=True)
            result = cursor.execute(sql_query, values_tuple)
            log.debug(f"Result after execute: {result}")
            connection.commit()
            log.debug("Data inserted successfully into service_chain table using the prepared statement")
            cursor.close()
        except database.Error as error:
            log.exception(f"Insert Operation failed due to \n {error}", exc_info=True)
        finally:
            self.mariadb.close_connection()
            log.debug("MariaDB connection is closed")
            self.__add_service_chain_values(service_uuid)

    def __add_service_chain_values(self, service_uuid):
        try:
            connection = self.mariadb.get_db_connection()
            if not self.domain_name:
                parameter_id = uuid.uuid4().hex
                log.debug(f"parameter_id UUID: {parameter_id}")
                values_tuple = (parameter_id, service_uuid, "domain_name", self.domain_name)
                sql_query = """INSERT INTO `sc_parameters` (`parameter_id`, `service_uuid`, `key`, `value`)
                  VALUES (%s, %s, %s, %s)"""
                cursor = connection.cursor(prepared=True)
                cursor.execute(sql_query, values_tuple)
            if not self.bandwidth:
                parameter_id = uuid.uuid4().hex
                log.debug(f"parameter_id UUID: {parameter_id}")
                values_tuple = (parameter_id, service_uuid, "bandwidth", self.bandwidth)
                sql_query = """INSERT INTO `sc_parameters` (`parameter_id`, `service_uuid`, `key`, `value`)
                  VALUES (%s, %s, %s, %s)"""
                cursor = connection.cursor(prepared=True)
                cursor.execute(sql_query, values_tuple)
            if not self.max_link_delay:
                parameter_id = uuid.uuid4().hex
                log.debug(f"parameter_id UUID: {parameter_id}")
                values_tuple = (parameter_id, service_uuid, "max_link_delay", self.max_link_delay)
                sql_query = """INSERT INTO `sc_parameters` (`parameter_id`, `service_uuid`, `key`, `value`)
                  VALUES (%s, %s, %s, %s)"""
                cursor = connection.cursor(prepared=True)
                cursor.execute(sql_query, values_tuple)

            connection.commit()
            log.debug("Data inserted successfully into sc_parameters table using the prepared statement")
        except database.Error as error:
            log.exception(f"Insert Operation failed due to \n {error}", exc_info=True)
        finally:
            self.mariadb.close_connection()
            log.info("MySQL connection is closed")

    def get_service_chains(self):
        try:
            sql_query = "SELECT * FROM `service-chain`"
            connection = self.mariadb.get_db_connection()

        except database.Error as error:
            log.error(f"Get Operation failed due to \n {error}")
        self.mariadb.close_connection()

    def get_name(self):
        return self.name

    def get_service_profile(self):
        return self.service_profile

    def get_service_template(self):
        log.info(f"Fetch Service Profile Template: {time.time()}")
        if self.service_profile == ServiceProfiles.FOUR_G_LTE_CORE:
            four_g_lte_core = FourGLTECore(self.name, self.domain_name, self.bandwidth)
            four_g_lte_core.nova.close_connection()
            return four_g_lte_core
        elif self.service_profile == ServiceProfiles.FOUR_G_LTE_CORE_BBU:
            four_g_lte_core_rcc = FourGLTECoreRCC(self.name, self.domain_name, self.bandwidth)
            four_g_lte_core_rcc.nova.close_connection()
            return four_g_lte_core_rcc
        elif self.service_profile == ServiceProfiles.FIVE_G_CORE:
            return None
        elif self.service_profile == ServiceProfiles.FIVE_G_CORE_DU:
            return None
        else:
            abort(404)
        log.info(f"Service Profile Template Fetched: {time.time()}")

    def get_domain_name(self):
        return self.domain_name

    def get_bandwidth(self):
        return self.bandwidth

    def get_max_link_delay(self):
        return self.max_link_delay


def main():
    input_request = InputRequest("Hanif testinG kn", "FOUR_G_LTE_CORE", "", 150, 10)
    print(f"name: {input_request.get_name()}, service_profile: {input_request.get_service_profile()}", )
    print(f'service template: {input_request.get_service_template()}')


if __name__ == "__main__":
    main()
