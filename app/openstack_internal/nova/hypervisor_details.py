from openstack.compute.v2.hypervisor import Hypervisor


class OSHypervisor:
    def __init__(self, hypervisor: Hypervisor):
        self.__hypervisor = hypervisor

    def get_hypervisor(self):
        return self.__hypervisor

    def get_id(self):
        return self.__hypervisor.id

    def get_name(self):
        return self.__hypervisor.name

    def get_state(self):
        return self.__hypervisor.state

    def get_status(self):
        return self.__hypervisor.status

    def get_total_vcpus(self):
        return self.__hypervisor.vcpus

    def get_total_memory_mb(self):
        return self.__hypervisor.memory_mb

    def get_total_local_gb(self):
        return self.__hypervisor.local_gb

    def get_vcpus_used(self):
        return self.__hypervisor.vcpus_used

    def get_memory_mb_used(self):
        return self.__hypervisor.memory_mb_used

    def get_local_gb_used(self):
        return self.__hypervisor.local_gb_used

    def get_hypervisor_type(self):
        return self.__hypervisor.hypervisor_type

    def get_available_ram_mb(self):
        return self.__hypervisor.memory_free

    def get_available_disk_gb(self):
        return self.__hypervisor.local_disk_free

    def get_available_vcpus(self):
        return self.get_total_vcpus() - self.get_vcpus_used()

    def get_running_vms_count(self):
        return self.__hypervisor.running_vms

    def get_disk_available_least(self):
        return self.__hypervisor.disk_available_least

    def get_host_ip(self):
        return self.__hypervisor.host_ip

    def get_cpu_info(self):
        return self.__hypervisor.cpu_info


"""
def main():
    _nova = Nova(AuthenticateConnection().get_connection())
    hypervisor = OSHypervisor(_nova.get_hypervisor_by_id('b755b8b1-363f-40dc-ba6e-8b55dd3a4767'))

    print("Get hypervisor name: {}, hypervisor id: {}, total vcpus: {}".format(
            hypervisor.get_name(), hypervisor.get_id(), hypervisor.get_cpu_info()))


if __name__ == "__main__":
    main()
"""
