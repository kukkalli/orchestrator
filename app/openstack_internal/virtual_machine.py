import logging
from datetime import datetime

from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.clients.clients import Clients
from openstack_internal.neutron.neutron_details import Neutron

from novaclient.v2.client import Client as NovaV2Client

from templates.four_g_core.hss_template import HSSTemplate
from templates.four_g_core.hss_user_data import HSSUserData
from templates.four_g_core.mme_template import MMETemplate
from templates.four_g_core.mme_user_data import MMEUserData
from templates.four_g_core.spgwc_template import SPGWCTemplate
from templates.four_g_core.spgwc_user_data import SPGWCUserData
from templates.four_g_core.spgwu_template import SPGWUTemplate
from templates.four_g_core.spgwu_user_data import SPGWUUserData

from templates.four_g_lte_core import FourGLTECore

LOG = logging.getLogger(__name__)


class VirtualMachine:

    def __init__(self):
        self.authenticate = AuthenticateConnection()
        self.connection = self.authenticate.get_connection()
        self.__clients = Clients(self.authenticate)
        # self.__glance = Glance(self.connection)
        # self.__keypair = KeyPair(self.connection)
        # self.__neutron = Neutron(self.connection)
        # self.__nova = Nova(self.connection)
        # self.__project = Project(self.connection)
        # self.__user = User(self.connection)

    def create_virtual_machine(self, name: str, image: str, flavor="2", vm_count=1, security_groups: list = None,
                               userdata: str = "", key_pair=None, networks: list = None, host=None):
        if security_groups is None:
            security_groups = ["default"]
        """
        if networks is None:
            networks = [{"net-id": "4200c22b-80d3-48ea-9586-2a98140f1616", "v4-fixed-ip": "10.10.2.50"},
                        {"net-id": "ebe835d0-7c36-43fb-8c57-5b6b5872b0ce", "v4-fixed-ip": "10.11.2.50"}]
        """
        nova_client: NovaV2Client = self.__clients.get_nova_client()
        return nova_client.servers.create(name=name, image=image, flavor=flavor, min_count=vm_count, max_count=vm_count,
                                          # security_groups=security_groups,
                                          userdata=userdata, key_name=key_pair, admin_pass=None,
                                          nics=networks, access_ip_v4=None, access_ip_v6=None, host=host,
                                          hypervisor_hostname=None)

    def create_virtual_machine_with_port(self, name, image, flavor="2", vm_count=1, security_groups: list = None,
                                         userdata: str = "", key_pair=None, ports: list = None, host=None):
        if security_groups is None:
            security_groups = ["default"]
        if ports is None:
            self.create_virtual_machine(name, image, flavor, vm_count, security_groups, userdata, key_pair, None, host)
            return
        nova_client: NovaV2Client = self.__clients.get_nova_client()
        return nova_client.servers.create(name=name, image=image, flavor=flavor, min_count=vm_count, max_count=vm_count,
                                          security_groups=security_groups, userdata=userdata, key_name=key_pair,
                                          admin_pass=None,
                                          nics=ports, access_ip_v4=None, access_ip_v6=None, host=host,
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
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Service Chain Creation Start time: {current_time}")

    service_chain_name = "kn1"
    security_groups = ["default"]
    key_pair = "hanif-kukkalli"

    neutron = Neutron(AuthenticateConnection().get_connection())
    management_network_id = "4200c22b-80d3-48ea-9586-2a98140f1616"
    fabric_network_id = "ebe835d0-7c36-43fb-8c57-5b6b5872b0ce"
    vm_object = VirtualMachine()
    vm_object.create_virtual_machine_with_port("hss", )
    """
    """
    service = FourGLTECore(service_chain_name, "tu-chemnitz.de", 1000)
    service.build()
    hostnames_list: list[dict] = []
    # for network in networks
    for vnf in service.get_network_functions():
        print(f"VNF name: {vnf.get_name()}")
        hostnames_list.append({vnf.get_name(): vnf.get_vm_name()})
        for network in vnf.networks:
            print(f"network id: {network['net-id']}")
            network["v4-fixed-ip"] = neutron.get_available_ip(network_id=network["net-id"], is_delete=True)

            network["port-id"] = neutron.create_port(network_id=network["net-id"])
            vnf.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
        print(f"networks: {vnf.networks}")
        print(f"{vnf.get_name()} management network IP: {vnf.ip_addresses[management_network_id]}")
        print(f"{vnf.get_name()} management network IP: {vnf.ip_addresses[fabric_network_id]}")

    for hostname in hostnames_list:
        print(f"VNF name: {hostname['hss']}")
    hss = HSSTemplate(service_chain_name)
    mme = MMETemplate(service_chain_name)
    spgw_c = SPGWCTemplate(service_chain_name)
    spgw_u = SPGWUTemplate(service_chain_name)
    hss_hostname = hss.get_vm_name()
    print(f"hss hostname: {hss_hostname}")
    mme_hostname = mme.get_vm_name()
    print(f"mme hostname: {mme_hostname}")
    spgw_c_hostname = spgw_c.get_vm_name()
    print(f"spgw-c hostname: {spgw_c_hostname}")
    spgw_u_hostname = spgw_u.get_vm_name()
    print(f"spgw-u hostname: {spgw_u_hostname}")

    for network in mme.networks:
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
        mme.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    print(f"networks: {mme.networks}")
    print(f"MME management network IP: {mme.ip_addresses[management_network_id]}")

    for network in spgw_c.networks:
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
        spgw_c.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    print(f"networks: {spgw_c.networks}")
    print(f"SPGW-C management network IP: {spgw_c.ip_addresses[management_network_id]}")

    for network in spgw_u.networks:
        network["v4-fixed-ip"] = neutron.get_available_ip(network["net-id"])
        spgw_u.ip_addresses[network["net-id"]] = network["v4-fixed-ip"]
    print(f"networks: {spgw_u.networks}")
    print(f"SPGW-U management network IP: {spgw_u.ip_addresses[management_network_id]}")

    host1 = "compute01.etit.tu-chemnitz.de"
    host2 = "compute02.etit.tu-chemnitz.de"
    host3 = "compute03.etit.tu-chemnitz.de"
    domain = "tu-chemnitz.de"
    docker_pass = "c3360058-8abf-4091-b178-d3d94bc18636"

    hss_user_data = HSSUserData.USERDATA.replace("@@domain@@", domain).replace("@@docker_pass@@", docker_pass). \
        replace("@@mme_ip@@", mme.ip_addresses[management_network_id]).replace("@@mme_hostname@@", mme_hostname).\
        replace("@@op_key@@", "0123456789ABCDEF0123456789ABCDEF").\
        replace("@@lte_k@@", "0123456789ABCDEF0123456789ABCDEF").replace("@@apn-1@@", "tuckn").\
        replace("@@apn-2@@", "tuckn2").replace("@@first_imsi@@", "265820000038021")

    vm_object = VirtualMachine()
    hss_server = vm_object.create_virtual_machine(hss.get_vm_name(), hss.get_image_id(), flavor=hss.get_flavour(),
                                                  security_groups=security_groups, userdata=hss_user_data,
                                                  key_pair=key_pair, networks=hss.networks, host=host1)
    print("Created HSS Server: {}".format(hss_server))

    mme_user_data = MMEUserData.USERDATA.replace("@@domain@@", domain).replace("@@docker_pass@@", docker_pass). \
        replace("@@hss_ip@@", hss.ip_addresses[management_network_id]).replace("@@hss_hostname@@", hss_hostname). \
        replace("@@mcc@@", "265").replace("@@mnc@@", "82").replace("@@mme_gid@@", "32768"). \
        replace("@@mme_code@@", "3").replace("@@sgwc_ip_address@@", spgw_c.ip_addresses[management_network_id])

    mme_server = vm_object.create_virtual_machine(mme.get_vm_name(), mme.get_image_id(), flavor=mme.get_flavour(),
                                                  security_groups=security_groups, userdata=mme_user_data,
                                                  key_pair=key_pair, networks=mme.networks, host=host2)
    print("Created MME Server: {}".format(mme_server))

    spgw_c_user_data = SPGWCUserData.USERDATA.replace("@@domain@@", domain). \
        replace("@@docker_pass@@", docker_pass).replace("@@mcc@@", "265").replace("@@mnc@@", "82").\
        replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuckn").replace("@@apn-2@@", "tuckn2"). \
        replace("@@mme_ip@@", mme.ip_addresses[management_network_id]).replace("@@mme_hostname@@", mme_hostname)

    spgw_c_server = vm_object.create_virtual_machine(spgw_c.get_vm_name(), spgw_c.get_image_id(),
                                                     flavor=spgw_c.get_flavour(), security_groups=security_groups,
                                                     userdata=spgw_c_user_data, key_pair=key_pair,
                                                     networks=spgw_c.networks, host=host3)
    print("Created SPGW-C Server: {}".format(spgw_c_server))

    spgw_c_hostname_ip = spgw_c.ip_addresses[management_network_id]

    spgw_u_user_data = SPGWUUserData.USERDATA.replace("@@domain@@", domain).\
        replace("@@docker_pass@@", docker_pass).replace("@@mcc@@", "265").replace("@@mnc@@", "82").\
        replace("@@gw_id@@", "1").replace("@@apn-1@@", "tuckn").replace("@@apn-2@@", "tuckn2").\
        replace("@@sgwc_ip_address@@", spgw_c_hostname_ip).\
        replace("@@sgwc_hostname@@", spgw_c_hostname).replace("@@instance@@", "1").\
        replace("@@network_ue_ip@@", "12.1.1.0/24")

    spgw_u_server = vm_object.create_virtual_machine(spgw_u.get_vm_name(), spgw_u.get_image_id(),
                                                     flavor=spgw_u.get_flavour(), security_groups=security_groups,
                                                     userdata=spgw_u_user_data, key_pair=key_pair,
                                                     networks=spgw_u.networks, host=host3)

    vm_object.close_connection()
    print("Created SPGW-U Server: {}".format(spgw_u_server))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Service Chain Creation End time: {current_time}")


if __name__ == "__main__":
    main()
