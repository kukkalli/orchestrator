import logging
from typing import Dict

from templates.oai_5gcn.mysql.mysql import MySQL
from templates.service_profile_template import ServiceProfileTemplate
from templates.vm_template import VMTemplate
from test_scripts.service_build_test import service_built

LOG = logging.getLogger(__name__)


class OAI5GCN(ServiceProfileTemplate):
    MYSQL = "mysql"
    IMS = "asterisk-ims"
    NRF = "oai-nrf"
    UDR = "oai-udr"
    UDM = "oai-udm"
    AUSF = "oai-ausf"
    AMF = "oai-amf"
    SMF = "oai-smf"
    UPF = "oai-spgwu"
    TRF_GEN = "oai-trf-gen"

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(prefix, domain_name, bandwidth, max_delay)
        self.network_functions.append(MySQL(prefix, self.MYSQL))
        # self.network_functions.append(MMETemplate(prefix, self.MME))
        # self.network_functions.append(SPGWCTemplate(prefix, self.SPGW_C))
        # self.network_functions.append(SPGWUTemplate(prefix, self.SPGW_U))

    def populate_vm_ip(self, user_data: str, nf_ip_dict: Dict[str, str]) -> str:
        user_data = user_data.replace("@@mysql_ip@@", nf_ip_dict[self.MYSQL])
        user_data = user_data.replace("@@ims_ip@@", nf_ip_dict[self.IMS])
        user_data = user_data.replace("@@nrf_ip@@", nf_ip_dict[self.NRF])
        user_data = user_data.replace("@@udr_ip@@", nf_ip_dict[self.UDR])
        user_data = user_data.replace("@@udm_ip@@", nf_ip_dict[self.UDM])
        user_data = user_data.replace("@@ausf_ip@@", nf_ip_dict[self.AUSF])
        user_data = user_data.replace("@@amf_ip@@", nf_ip_dict[self.AMF])
        user_data = user_data.replace("@@smf_ip@@", nf_ip_dict[self.SMF])
        user_data = user_data.replace("@@upf_ip@@", nf_ip_dict[self.UPF])
        user_data = user_data.replace("@@trf_ip@@", nf_ip_dict[self.TRF_GEN])
        return user_data

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        LOG.debug(f"I am in OAI 5G CN, {self.domain_name}")
        vm_user_data_dict: Dict[str, str] = {}
        for network_function in self.get_network_functions():
            if network_function.name == self.MYSQL:
                vm_user_data_dict[self.MYSQL] = self.update_mysql(network_function, nf_ip_dict)
            elif network_function.name == self.IMS:
                vm_user_data_dict[self.IMS] = self.update_ims(network_function, nf_ip_dict)
            elif network_function.name == self.NRF:
                vm_user_data_dict[self.NRF] = self.update_nrf(network_function, nf_ip_dict)
            elif network_function.name == self.UDR:
                vm_user_data_dict[self.UDR] = self.update_udr(network_function, nf_ip_dict)
            elif network_function.name == self.UDM:
                vm_user_data_dict[self.UDM] = self.update_udm(network_function, nf_ip_dict)
            elif network_function.name == self.AUSF:
                vm_user_data_dict[self.AUSF] = self.update_ausf(network_function, nf_ip_dict)
            elif network_function.name == self.AMF:
                vm_user_data_dict[self.AMF] = self.update_amf(network_function, nf_ip_dict)
            elif network_function.name == self.SMF:
                vm_user_data_dict[self.SMF] = self.update_smf(network_function, nf_ip_dict)
            elif network_function.name == self.UPF:
                vm_user_data_dict[self.UPF] = self.update_upf(network_function, nf_ip_dict)
            elif network_function.name == self.TRF_GEN:
                vm_user_data_dict[self.TRF_GEN] = self.update_trf(network_function, nf_ip_dict)

        return vm_user_data_dict

    def update_mysql(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        user_data = user_data.replace("@@@@tz@@@@", "Europe/Berlin")
        # MySQL database values
        user_data = user_data.replace("@@mysql_database@@", "oai_db")
        user_data = user_data.replace("@@mysql_user@@", "oai_tuc")
        user_data = user_data.replace("@@mysql_password@@", "oai_tuc")
        user_data = user_data.replace("@@mysql_root_password@@", "oai_tuc")
        # Initial UE values
        user_data = user_data.replace("@@ue_id@@", "001010000000001")
        user_data = user_data.replace("@@enc_permanent_key@@", "fec86ba6eb707ed08905757b1bb44b8f")
        user_data = user_data.replace("@@protection_parameter_id@@", "fec86ba6eb707ed08905757b1bb44b8f")
        user_data = user_data.replace("@@enc_opc_key@@", "C42449363BBAD02B66D16BC975D77CC1")
        user_data = user_data.replace("@@serving_plmn_id@@", "00101")
        user_data = user_data.replace("@@sst@@", "1")
        user_data = user_data.replace("@@dnn@@", "{\"oai\":{\"pduSessionTypes\":{"
                                                 "\"defaultSessionType\": \"IPV4\"},"
                                                 "\"sscModes\": {\"defaultSscMode\": \"SSC_MODE_1\"},"
                                                 "\"5gQosProfile\": {\"5qi\": 6,\"arp\":{"
                                                 "\"priorityLevel\": 15,\"preemptCap\": \"NOT_PREEMPT\","
                                                 "\"preemptVuln\":\"PREEMPTABLE\"},\"priorityLevel\":1},"
                                                 "\"sessionAmbr\":{"
                                                 "\"uplink\":\"1000Mbps\", \"downlink\":\"1000Mbps\"},"
                                                 "\"staticIpAddress\":[{\"ipv4Addr\": \"12.1.1.99\"}]},"
                                                 "\"ims\":{\"pduSessionTypes\":{"
                                                 "\"defaultSessionType\": \"IPV4V6\"},\"sscModes\": {"
                                                 "\"defaultSscMode\": \"SSC_MODE_1\"},\"5gQosProfile\": {"
                                                 "\"5qi\": 2,\"arp\":{"
                                                 "\"priorityLevel\": 15,\"preemptCap\": \"NOT_PREEMPT\","
                                                 "\"preemptVuln\":\"PREEMPTABLE\"},\"priorityLevel\":1},"
                                                 "\"sessionAmbr\":{"
                                                 "\"uplink\":\"1000Mbps\", \"downlink\":\"1000Mbps\"}}}")
        user_data = self.populate_vm_ip(user_data, nf_ip_dict)
        return user_data

    def update_ims(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_nrf(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_udr(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_udm(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_ausf(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_amf(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_smf(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_upf(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_trf(self, network_function: VMTemplate, nf_ip_dict: Dict[str, str]) -> str:
        user_data = network_function.get_user_data()
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data


def main():
    service = OAI5GCN("test", "kukkalli.com", 1000)
    service_built(service)


if __name__ == "__main__":
    main()
