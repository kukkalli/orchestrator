import logging

from openstack_internal.nova.hypervisor_details import OSHypervisor
from topology.server import Server

LOG = logging.getLogger(__name__)


class ComputeServer(Server):

    def __init__(self, int_id: int, hypervisor: OSHypervisor):
        super().__init__(int_id=int_id, str_id=hypervisor.get_id(), name=hypervisor.get_name())
        LOG.debug(f"Compute Server Name: {self.name}")
        self.hostname = hypervisor.get_hostname()
        self.cpu = hypervisor.get_available_vcpus()
        self.hdd = hypervisor.get_available_disk_gb()
        self.ram = hypervisor.get_available_ram_mb()


"""
        self.in_links: Link or None = None
        self.out_links: Link or None = None

    def add_in_link(self, link: Link):
        self.in_links = link

    def add_out_link(self, link: Link):
        self.out_links = link

"""
