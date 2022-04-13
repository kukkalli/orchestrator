import logging

from openstack.compute.v2.hypervisor import Hypervisor

LOG = logging.getLogger(__name__)


class OSHypervisor:
    def __init__(self, hypervisor: Hypervisor):
        self.__hypervisor = hypervisor
        self.__id = hypervisor.id
        self.__hypervisor_hostname = hypervisor.name
        name: str = hypervisor.name
        self.__name = name.split(".")[0]
        self.__cpu_info = hypervisor.cpu_info
        self.__host_ip = hypervisor.host_ip
        self.__hypervisor_type = hypervisor.hypervisor_type
        self.__hypervisor_version = hypervisor.hypervisor_version
        self.__service_details = hypervisor.service_details
        self.__servers = hypervisor.servers
        self.__state = hypervisor.state
        self.__status = hypervisor.status
        self.__uptime = hypervisor.uptime
        self.__current_workload = hypervisor.current_workload

        self.__available_disk_gb = hypervisor.disk_available
        self.__used_disk_gb = hypervisor.local_disk_used
        self.__total_disk_gb = hypervisor.local_disk_size
        self.__free_disk_gb = hypervisor.local_disk_free

        self.__used_ram_mb = hypervisor.memory_used
        self.__total_ram_mb = hypervisor.memory_size
        self.__available_ram_mb = hypervisor.memory_free

        self.__running_vms_count = hypervisor.running_vms

        self.__used_vcpus = hypervisor.vcpus_used
        self.__total_vcpus = hypervisor.vcpus

        self.__disk_available_least = hypervisor.disk_available

    def get_hypervisor(self):
        return self.__hypervisor

    def get_id(self):
        return self.__id

    def get_full_name(self):
        return self.__hypervisor_hostname

    def get_name(self):
        return self.__name

    def get_cpu_info(self):
        return self.__cpu_info

    def get_host_ip(self):
        return self.__host_ip

    def get_hypervisor_type(self):
        return self.__hypervisor_type

    def get_hypervisor_version(self):
        return self.__hypervisor_version

    def get_service_details(self):
        return self.__service_details

    def get_servers(self):
        return self.__servers

    def get_state(self):
        return self.__state

    def get_status(self):
        return self.__status

    def get_uptime(self):
        return self.__uptime

    def get_current_workload(self):
        return self.__current_workload

    def get_available_disk_gb(self):
        return self.__available_disk_gb

    def get_used_disk_gb(self):
        return self.__used_disk_gb

    def get_total_disk_gb(self):
        return self.__total_disk_gb

    def get_free_disk_gb(self):
        return self.__free_disk_gb

    def get_used_ram_mb(self):
        return self.__used_ram_mb

    def get_total_memory_mb(self):
        return self.__total_ram_mb

    def get_available_ram_mb(self):
        return self.__available_ram_mb

    def get_running_vms_count(self):
        return self.__running_vms_count

    def get_used_vcpus(self):
        return self.__used_vcpus

    def get_total_vcpus(self):
        return self.__total_vcpus

    def get_available_vcpus(self):
        return self.__total_vcpus - self.__used_vcpus

    def get_disk_available_least(self):
        return self.__disk_available_least


"""
def main():
    _nova = Nova(AuthenticateConnection().get_connection())
    hypervisor = OSHypervisor(_nova.get_hypervisor_by_id('b755b8b1-363f-40dc-ba6e-8b55dd3a4767'))

    print("Get hypervisor name: {}, hypervisor id: {}, total vcpus: {}".format(
            hypervisor.get_name(), hypervisor.get_id(), hypervisor.get_cpu_info()))


if __name__ == "__main__":
    main()
"""
