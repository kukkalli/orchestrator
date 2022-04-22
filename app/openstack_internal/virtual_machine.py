import logging

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.clients.clients import Clients
from openstack_internal.neutron.neutron_details import Neutron

from novaclient.v2.client import Client as NovaV2Client

from templates.four_g_core.hss_template import HSSTemplate
from templates.four_g_core.hss_user_data import HSSUserData
from templates.four_g_core.mme_template import MMETemplate
from templates.four_g_core.mme_user_data import MMEUserData
from templates.four_g_core.spgwc_user_data import SPGWCUserData
from templates.four_g_core.spgwc_template import SPGWCTemplate
from templates.four_g_core.spgwu_template import SPGWUTemplate
from templates.four_g_core.spgwu_user_data import SPGWUUserData

LOG = logging.getLogger(__name__)


class VirtualMachine(object):

    def __init__(self, vm_id: str):
        self.__id = vm_id
        self.authenticate = AuthenticateConnection()
        self.connection = self.authenticate.get_connection()
        self.__clients = Clients(self.authenticate)
        # self.__glance = Glance(self.connection)
        # self.__keypair = KeyPair(self.connection)
        # self.__neutron = Neutron(self.connection)
        # self.__nova = Nova(self.connection)
        # self.__project = Project(self.connection)
        # self.__user = User(self.connection)

    def get_id(self):
        return self.__id

    def create_virtual_machine(self, name, image, flavor="2", vm_count=1, security_groups: list = None,
                               userdata: str = "", key_pair=None, networks: list = None, host=None):
        if security_groups is None:
            security_groups = ["default"]
        if networks is None:
            networks = [{"net-id": "a0ebb620-d0e6-44d9-b584-489e841bc796", "v4-fixed-ip": "10.10.2.50"},
                        {"net-id": "9e373e2c-0372-4a06-81a1-bc1cb4c62b85", "v4-fixed-ip": "10.11.2.50"}]
        nova_client: NovaV2Client = self.__clients.get_nova_client()
        return nova_client.servers.create(name=name, image=image, flavor=flavor, min_count=vm_count, max_count=vm_count,
                                          security_groups=security_groups, userdata=userdata, key_name=key_pair,
                                          admin_pass=None,
                                          nics=networks, access_ip_v4=None, access_ip_v6=None, host=host,
                                          hypervisor_hostname=None)

    """
    def get_vm_info(self):
        nova = self.__get_nova_api()
        return nova.get_hypervisor_by_id(self.__id)

    def get_image_info(self):
        self.get_glance_api().get_image_by_id()
        return

    def get_vm_host(self):
        self.__get_nova_api()
        return

    def get_ips(self):
        nova = self.__get_nova_api()
        nova.get_hypervisor_by_id(self.__id)

        return

    def get_glance_api(self):
        return self.__glance

    def get_keypair_api(self):
        return self.__keypair

    def get_neutron_api(self):
        return self.__neutron

    def __get_nova_api(self):
        return self.__nova

    def get_project_api(self):
        return self.__project

    def get_user_api(self):
        return self.__user
    """

    def close_connection(self):
        self.authenticate.close_connection()


def main():
    service_chain_name = "kn"
    hss = HSSTemplate(service_chain_name)
    mme = MMETemplate(service_chain_name)
    spgw_c = SPGWCTemplate(service_chain_name)
    spgw_u = SPGWUTemplate(service_chain_name)
    security_groups = ["default"]
    key_pair = "compute01"
    neutron = Neutron(AuthenticateConnection().get_connection())
    management_network_id = "a0ebb620-d0e6-44d9-b584-489e841bc796"
    hss_hostname = hss.get_vm_name()
    print(f"hss hostname: {hss_hostname}")
    mme_hostname = mme.get_vm_name()
    print(f"mme hostname: {mme_hostname}")
    spgw_c_hostname = spgw_c.get_vm_name()
    print(f"spgw-c hostname: {spgw_c_hostname}")
    spgw_u_hostname = spgw_u.get_vm_name()
    print(f"spgw-u hostname: {spgw_u_hostname}")

    """
    for network in hss.networks:
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
        hss.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    print(f"networks: {hss.networks}")
    print(f"HSS management network IP: {hss.ip_addresses[management_network_id]}")
    """

    """
    for network in mme.networks:
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
        mme.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    print(f"networks: {mme.networks}")
    print(f"MME management network IP: {mme.ip_addresses[management_network_id]}")
    """

    """
    for network in spgw_c.networks:
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
        spgw_c.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    print(f"networks: {spgw_c.networks}")
    print(f"SPGW-C management network IP: {spgw_c.ip_addresses[management_network_id]}")
    """

    """
    """
    for network in spgw_u.networks:
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
        spgw_u.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    print(f"networks: {spgw_c.networks}")
    print(f"SPGW-U management network IP: {spgw_u.ip_addresses[management_network_id]}")
    """

    """
    host = "compute01.etit.tu-chemnitz.de"
    domain = "tu-chemnitz.de"
    docker_pass = "c3360058-8abf-4091-b178-d3d94bc18636"
    """

    """
    """
    hss_user_data = HSSUserData.USERDATA.replace("@@domain@@", domain).replace("@@docker_pass@@", docker_pass). \
        replace("@@mme_ip@@", mme.ip_addresses[management_network_id]).replace("@@mme_hostname@@", mme_hostname)

    vm_hss = VirtualMachine(hss.get_vm_name())
    hss_server = vm_hss.create_virtual_machine(hss.get_vm_name(), hss.get_image_id(), flavor=hss.get_flavour(),
                                               security_groups=security_groups, userdata=hss_user_data,
                                               key_pair=key_pair,
                                               networks=hss.networks, host=host)
    vm_hss.close_connection()
    print("Created HSS Server: {}".format(hss_server))
    """

    """
    mme_user_data = MMEUserData.USERDATA.replace("@@domain@@", domain).replace("@@docker_pass@@", docker_pass). \
        replace("@@hss_ip@@", hss.ip_addresses[management_network_id]).replace("@@hss_hostname@@", hss_hostname). \
        replace("@@mcc@@", "265").replace("@@mnc@@", "82").replace("@@mme_gid@@", "32768"). \
        replace("@@mme_code@@", "3").replace("@@sgwc_ip_address@@", spgw_c.ip_addresses[management_network_id])

    vm_mme = VirtualMachine(mme.get_vm_name())
    mme_server = vm_mme.create_virtual_machine(mme.get_vm_name(), mme.get_image_id(), flavor=mme.get_flavour(),
                                               security_groups=security_groups, userdata=mme_user_data,
                                               key_pair=key_pair,
                                               networks=mme.networks, host=host)
    vm_mme.close_connection()
    print("Created MME Server: {}".format(mme_server))
    """

    """
    spgw_c_user_data = SPGWCUserData.USERDATA.replace("@@domain@@", domain). \
        replace("@@docker_pass@@", docker_pass).replace("@@mcc@@", "265").replace("@@mnc@@", "82").\
        replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuckn").replace("@@apn-2@@", "tuckn2"). \
        replace("@@mme_ip@@", mme.ip_addresses[management_network_id]).replace("@@mme_hostname@@", mme_hostname)

    vm_spgw_c = VirtualMachine(spgw_c.get_vm_name())
    spgw_c_server = vm_spgw_c.create_virtual_machine(spgw_c.get_vm_name(), spgw_c.get_image_id(),
                                                     flavor=spgw_c.get_flavour(), security_groups=security_groups,
                                                     userdata=spgw_c_user_data, key_pair=key_pair,
                                                     networks=spgw_c.networks, host=host)
    vm_spgw_c.close_connection()
    print("Created SPGW-C Server: {}".format(spgw_c_server))
    """

    """
    """
    spgw_c_hostname = "kn-spgw-c"
    spgw_c_hostname_ip = "10.10.2.108"
    domain = "tu-chemnitz.de"
    spgw_u_user_data = SPGWUUserData.USERDATA.replace("@@domain@@", domain).\
        replace("@@docker_pass@@", docker_pass).replace("@@mcc@@", "265").replace("@@mnc@@", "82").\
        replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuckn").replace("@@apn-2@@", "tuckn2").\
        replace("@@sgwc_ip_address@@", spgw_c_hostname_ip).\
        replace("@@sgwc_hostname@@", spgw_c_hostname).replace("@@instance@@", "1").\
        replace("@@network_ue_ip@@", "12.1.1.0/24")

    vm_spgw_u = VirtualMachine(spgw_u.get_vm_name())
    spgw_u_server = vm_spgw_u.create_virtual_machine(spgw_u.get_vm_name(), spgw_u.get_image_id(),
                                                     flavor=spgw_u.get_flavour(), security_groups=security_groups,
                                                     userdata=spgw_u_user_data, key_pair=key_pair,
                                                     networks=spgw_u.networks, host=host)
    vm_spgw_u.close_connection()
    print("Created SPGW-U Server: {}".format(spgw_u_server))
    """
    """


if __name__ == "__main__":
    main()
