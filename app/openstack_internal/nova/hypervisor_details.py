import logging

LOG = logging.getLogger(__name__)


class OSHypervisor:

    def __init__(self, hypervisor):
        # LOG.info(f"In OSHypervisor: hypervisor: {hypervisor}")
        self.hypervisor = hypervisor
        self.id = hypervisor.id
        # self._info = hypervisor._info
        self.api_version = hypervisor.api_version
        self.append_request_ids = hypervisor.append_request_ids
        self.cpu_info = hypervisor.cpu_info
        self.current_workload = hypervisor.current_workload
        self.disk_available_least = hypervisor.disk_available_least
        self.free_disk_gb = hypervisor.free_disk_gb
        self.human_id = hypervisor.human_id
        self.free_ram_mb = hypervisor.free_ram_mb
        self.hypervisor_type = hypervisor.hypervisor_type
        self.host_ip = hypervisor.host_ip
        self.human_id = hypervisor.human_id
        self.hypervisor_hostname = hypervisor.hypervisor_hostname
        name: str = hypervisor.hypervisor_hostname
        self.name = name.split(".")[0]
        self.hypervisor_type = hypervisor.hypervisor_type
        self.hypervisor_version = hypervisor.hypervisor_version
        self.is_loaded = hypervisor.is_loaded()
        self.local_gb = hypervisor.local_gb
        self.local_gb_used = hypervisor.local_gb_used
        self.manager = hypervisor.manager
        self.memory_mb = hypervisor.memory_mb
        self.memory_mb_used = hypervisor.memory_mb_used
        self.request_ids = hypervisor.request_ids
        self.request_ids_setup = hypervisor.request_ids_setup
        self.running_vms = hypervisor.running_vms
        self.service = hypervisor.service
        self.state = hypervisor.state
        self.status = hypervisor.status
        self.vcpus = hypervisor.vcpus
        self.vcpus_used = hypervisor.vcpus_used
        self.x_openstack_request_ids = hypervisor.x_openstack_request_ids

        # LOG.debug(f"cpus: total: {hypervisor.vcpus}, used: {hypervisor.vcpus_used}")
        # LOG.debug(f'Hypervisor: {dir(hypervisor)}')
        # LOG.debug(f'Hypervisor ID: {hypervisor.id}')
        # LOG.debug(f'Hypervisor api_version: {hypervisor.api_version}')
        # LOG.debug(f'Hypervisor append_request_ids: {hypervisor.append_request_ids}')
        # LOG.debug(f'Hypervisor cpu_info: {hypervisor.cpu_info}')
        # LOG.debug(f'Hypervisor current_workload: {hypervisor.current_workload}')
        # LOG.debug(f'Hypervisor disk_available_least: {hypervisor.disk_available_least}')
        # LOG.debug(f'Hypervisor free_disk_gb: {hypervisor.free_disk_gb}')
        # LOG.debug(f'Hypervisor human_id: {hypervisor.human_id}')
        # LOG.debug(f'Hypervisor free_ram_mb: {hypervisor.free_ram_mb}')
        # LOG.debug(f'Hypervisor hypervisor_type: {hypervisor.hypervisor_type}')
        # LOG.debug(f'Hypervisor host_ip: {hypervisor.host_ip}')
        # LOG.debug(f'Hypervisor human_id: {hypervisor.human_id}')
        # LOG.debug(f'Hypervisor hypervisor_hostname: {hypervisor.hypervisor_hostname}')
        # LOG.debug(f'Hypervisor hypervisor_type: {hypervisor.hypervisor_type}')
        # LOG.debug(f'Hypervisor hypervisor_version: {hypervisor.hypervisor_version}')
        # LOG.debug(f'Hypervisor is_loaded(): {hypervisor.is_loaded()}')
        # LOG.debug(f'Hypervisor local_gb: {hypervisor.local_gb}')
        # LOG.debug(f'Hypervisor local_gb_used: {hypervisor.local_gb_used}')
        # LOG.debug(f'Hypervisor manager: {hypervisor.manager}')
        # LOG.debug(f'Hypervisor memory_mb: {hypervisor.memory_mb}')
        # LOG.debug(f'Hypervisor memory_mb_used: {hypervisor.memory_mb_used}')
        # LOG.debug(f'Hypervisor name: {self.name}')
        # LOG.debug(f'Hypervisor request_ids: {hypervisor.request_ids}')
        # LOG.debug(f'Hypervisor request_ids_setup: {hypervisor.request_ids_setup}')
        # LOG.debug(f'Hypervisor running_vms: {hypervisor.running_vms}')
        # LOG.debug(f'Hypervisor service: {hypervisor.service}')
        # LOG.debug(f'Hypervisor state: {hypervisor.state}')
        # LOG.debug(f'Hypervisor status: {hypervisor.status}')
        # LOG.debug(f'Hypervisor vcpus: {hypervisor.vcpus}')
        # LOG.debug(f'Hypervisor vcpus_used: {hypervisor.vcpus_used}')
        # LOG.debug(f'Hypervisor x_openstack_request_ids: {hypervisor.x_openstack_request_ids}')
        # LOG.debug(f"cpus: total: {hypervisor.vcpus}, used: {hypervisor.vcpus_used}")

        # print('Hypervisor: ', hypervisor)
        # print('Hypervisor ID: ', hypervisor.id)
        # print('Hypervisor api_version: ', hypervisor.api_version)
        # print('Hypervisor append_request_ids: ', hypervisor.append_request_ids)
        # print('Hypervisor cpu_info: ', hypervisor.cpu_info)
        # print('Hypervisor current_workload: ', hypervisor.current_workload)
        # print('Hypervisor disk_available_least: ', hypervisor.disk_available_least)
        # print('Hypervisor free_disk_gb: ', hypervisor.free_disk_gb)
        # print('Hypervisor human_id: ', hypervisor.human_id)
        # print('Hypervisor free_ram_mb: ', hypervisor.free_ram_mb)
        # print('Hypervisor hypervisor_type: ', hypervisor.hypervisor_type)
        # print('Hypervisor host_ip: ', hypervisor.host_ip)
        # print('Hypervisor human_id: ', hypervisor.human_id)
        # print('Hypervisor hypervisor_hostname: ', hypervisor.hypervisor_hostname)
        # print('Hypervisor hypervisor_type: ', hypervisor.hypervisor_type)
        # print('Hypervisor hypervisor_version: ', hypervisor.hypervisor_version)
        # print('Hypervisor is_loaded(): ', hypervisor.is_loaded())
        # print('Hypervisor local_gb: ', hypervisor.local_gb)
        # print('Hypervisor local_gb_used: ', hypervisor.local_gb_used)
        # print('Hypervisor manager: ', hypervisor.manager)
        # print('Hypervisor memory_mb: ', hypervisor.memory_mb)
        # print('Hypervisor memory_mb_used: ', hypervisor.memory_mb_used)
        # print('Hypervisor name: ', self.name)
        # print('Hypervisor request_ids: ', hypervisor.request_ids)
        # print('Hypervisor request_ids_setup: ', hypervisor.request_ids_setup)
        # print('Hypervisor running_vms: ', hypervisor.running_vms)
        # print('Hypervisor service: ', hypervisor.service)
        # print('Hypervisor state: ', hypervisor.state)
        # print('Hypervisor status: ', hypervisor.status)
        # print('Hypervisor vcpus: ', hypervisor.vcpus)
        # print('Hypervisor vcpus_used: ', hypervisor.vcpus_used)
        # print('Hypervisor x_openstack_request_ids: ', hypervisor.x_openstack_request_ids)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_hostname(self):
        return self.hypervisor_hostname

    def get_available_disk_gb(self):
        # LOG.info(f"In OSHypervisor.get_available_disk_gb: {self.free_disk_gb}")
        LOG.info(f"In OSHypervisor.get_available_disk_gb: {self.disk_available_least}")
        # return self.free_disk_gb
        return self.disk_available_least

    def get_available_ram_mb(self):
        LOG.info(f"In OSHypervisor.get_available_ram_mb: {self.free_ram_mb}")
        return self.free_ram_mb

    def get_available_vcpus(self):
        free_vcpus = self.vcpus - self.vcpus_used
        LOG.info(f"In OSHypervisor.get_available_vcpus: {free_vcpus}")
        return free_vcpus
