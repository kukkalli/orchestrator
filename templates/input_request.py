from flask import abort

from templates.four_g_lte_core import FourGLTECore
from templates.four_g_lte_core_rcc import FourGLTECoreRCC
from templates.service_profile_template import ServiceProfileTemplate
from templates.serviceprofiles import ServiceProfiles


class InputRequest:

    def __init__(self, name: str, service_profile: str, domain_name: str = "tu-chemnitz.de", bandwidth: int = 100,
                 max_link_delay: int = 100):
        self.name = name.replace(" ", "-").lower()
        self.domain_name = domain_name
        self.service_profile: ServiceProfiles = ServiceProfiles(service_profile)
        self.bandwidth = bandwidth
        self.max_link_delay = max_link_delay

    def get_name(self):
        return self.name

    def get_service_profile(self):
        return self.service_profile

    def get_service_template(self):
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

    def get_domain_name(self):
        return self.domain_name

    def get_bandwidth(self):
        return self.bandwidth

    def get_max_link_delay(self):
        return self.max_link_delay


def main():
    input_request = InputRequest("kn", "FOUR_G_LTE_CORE", "", 150, 10)
    print(f"name: {input_request.get_name()}, service_profile: {input_request.get_service_profile()}", )
    print(f'service template: {input_request.get_service_template()}')


if __name__ == "__main__":
    main()
