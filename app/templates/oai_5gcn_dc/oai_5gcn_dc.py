import logging
from typing import Dict

from templates.oai_5gcn_dc.ims.ims import IMS
from templates.oai_5gcn_dc.mysql.mysql import MySQL
from templates.oai_5gcn_dc.nrf.nrf import NRF
from templates.service_profile_template import ServiceProfileTemplate
from templates.user_data.oai_5gcn_constants import OAI5GConstants
from templates.user_data.prepared_image_template import PreparedImageVMTemplate
from test_scripts.service_build_test import service_built

LOG = logging.getLogger(__name__)


class OAI5GCNDC(ServiceProfileTemplate):
    MYSQL = "mysql"
    NRF = "oai-nrf"
    IMS = "asterisk-ims"
    UDR = "oai-udr"
    UDM = "oai-udm"
    AUSF = "oai-ausf"
    AMF = "oai-amf"
    SMF = "oai-smf"
    UPF = "oai-spgwu"
    TRF_GEN = "oai-trf-gen"

    MySQL_Values = {"domain": "tu-chemnitz.de",
                    "timezone": "Europe/Berlin",
                    "mysql_database": "oai_db",
                    "mysql_user": "oai_tuc",
                    "mysql_password": "oai_tuc",
                    "mysql_root_password": "oai_tuc"}

    NRF_Values = {"timezone": "Europe/Berlin",
                  "log_level": "debug"}

    IMS_Values = {"web_port": "80",
                  "sms_port": "80",
                  "sys_log": "4",
                  "ue_id_01": "001010000000001",
                  "ue_user_01_fullname": "Ameya Joshi",
                  "ue_id_02": "001010000000002",
                  "ue_user_02_fullname": "Syed Tasnimul Islam"}

    CONFIG_Values = {
        "MYSQL_SERVER": "mysql",
        "MYSQL_IPV4_ADDRESS": "10.11.2.160",
        "MYSQL_USER": "oai_tuc",
        "MYSQL_PASS": "oai_tuc",
        "MYSQL_DB": "oai_db",
        "DB_CONNECTION_TIMEOUT": "300",
        "WAIT_MYSQL": "120",
        "USE_FQDN_DNS": "yes",
        "REGISTER_NRF": "yes",
        "NRF_HOSTNAME": "oai-nrf",
        "NRF_IPV4_ADDRESS": "10.11.1.41",
        "NRF_FQDN": "oai-nrf",
        "DOMAIN": "tu-chemnitz.de",
        # PLMN list 01
        "MCC_01": "208",
        "MNC_01": "95",
        "AMF_REGION_ID_01": "128",
        "AMF_SET_ID_01": "1",
        "AMF_POINTER_01": "1",
        # PLMN list 02
        "MCC_02": "460",
        "MNC_02": "11",
        "AMF_REGION_ID_02": "10",
        "AMF_SET_ID_02": "1",
        "AMF_POINTER_02": "1",
        # PLMN Support List
        "PLMN_SL_MCC": "208",
        "PLMN_SL_MNC": "95",
        "PLMN_SL_TAC": "0xa000",
        # NSSAI Set 01
        "NSSAI_SST_01": "1",
        # NSSAI Set 02
        "NSSAI_SST_02": "1",
        "NSSAI_SD_02": "1",
        # NSSAI Set 03
        "NSSAI_SST_03": "222",
        "NSSAI_SD_03": "123",
        # IMS IPv4
        "IMS_IPV4": "10.11.1.118",
        # DNN List
        # DNN 01
        "DNN_01_SST": "1",
        "DNN_01_DNN": "oai",
        "DNN_01_5QI": "9",
        "DNN_01_SESSION_AMBR_UL": "200Mbps",
        "DNN_01_SESSION_AMBR_DL": "400Mbps",
        "DNN_01_PDU_SESSION_TYPE": "IPV4",
        # DNN 02
        "DNN_02_SST": "1",
        "DNN_02_SD": "1",
        "DNN_02_DNN": "oai.ipv4",
        "DNN_02_5QI": "9",
        "DNN_02_SESSION_AMBR_UL": "100Mbps",
        "DNN_02_SESSION_AMBR_DL": "200Mbps",
        "DNN_02_PDU_SESSION_TYPE": "IPV4",
        # Default DNN
        "DNN_DEF_SST": "222",
        "DNN_DEF_SD": "123",
        "DNN_DEF_DNN": "default",
        "DNN_DEF_5QI": 9,
        "DNN_DEF_SESSION_AMBR_UL": "50Mbps",
        "DNN_DEF_SESSION_AMBR_Dl": "100Mbps",
        "DNN_DEF_PDU_SESSION_TYPE": "IPV4",
        "DNN_IMS": "ims",
        "DNN_IMS_PDU_SESSION_TYPE": "IPV4V6"
    }

    UDR_Values = {
        "TZ": "Europe/Berlin",
        "UDR_NAME": "OAI_UDR",
        "UDR_INTERFACE_NAME_FOR_NUDR": "eth0",
        "MYSQL_SERVER": "mysql",
        "MYSQL_IPV4_ADDRESS": "10.11.2.160",
        "MYSQL_USER": "oai_tuc",
        "MYSQL_PASS": "oai_tuc",
        "MYSQL_DB": "oai_db",
        "DB_CONNECTION_TIMEOUT": "300",
        "WAIT_MYSQL": "120",
        "USE_FQDN_DNS": "yes",
        "REGISTER_NRF": "yes",
        "NRF_HOSTNAME": "oai-nrf",
        "NRF_IPV4_ADDRESS": "10.11.1.41",
        "NRF_FQDN": "oai-nrf",
        "DOMAIN": "tu-chemnitz.de",
        # PLMN list 01
        "MCC_01": "208",
        "MNC_01": "95",
        "AMF_REGION_ID_01": "128",
        "AMF_SET_ID_01": "1",
        "AMF_POINTER_01": "1",
        # PLMN list 02
        "MCC_02": "460",
        "MNC_02": "11",
        "AMF_REGION_ID_02": "10",
        "AMF_SET_ID_02": "1",
        "AMF_POINTER_02": "1",
        # PLMN Support List
        "PLMN_SL_MCC": "208",
        "PLMN_SL_MNC": "95",
        "PLMN_SL_TAC": "0xa000",
        # NSSAI Set 01
        "NSSAI_SST_01": "1",
        # NSSAI Set 02
        "NSSAI_SST_02": "1",
        "NSSAI_SD_02": "1",
        # NSSAI Set 03
        "NSSAI_SST_03": "222",
        "NSSAI_SD_03": "123",
        # IMS IPv4
        "IMS_IPV4": "10.11.1.118",
        # DNN List
        # DNN 01
        "DNN_01_SST": "1",
        "DNN_01_DNN": "oai",
        "DNN_01_5QI": "9",
        "DNN_01_SESSION_AMBR_UL": "200Mbps",
        "DNN_01_SESSION_AMBR_DL": "400Mbps",
        "DNN_01_PDU_SESSION_TYPE": "IPV4",
        # DNN 02
        "DNN_02_SST": "1",
        "DNN_02_SD": "1",
        "DNN_02_DNN": "oai.ipv4",
        "DNN_02_5QI": "9",
        "DNN_02_SESSION_AMBR_UL": "100Mbps",
        "DNN_02_SESSION_AMBR_DL": "200Mbps",
        "DNN_02_PDU_SESSION_TYPE": "IPV4",
        # Default DNN
        "DNN_DEF_SST": "222",
        "DNN_DEF_SD": "123",
        "DNN_DEF_DNN": "default",
        "DNN_DEF_5QI": 9,
        "DNN_DEF_SESSION_AMBR_UL": "50Mbps",
        "DNN_DEF_SESSION_AMBR_Dl": "100Mbps",
        "DNN_DEF_PDU_SESSION_TYPE": "IPV4",
        "DNN_IMS": "ims",
        "DNN_IMS_PDU_SESSION_TYPE": "IPV4V6"
    }

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(prefix, domain_name, bandwidth, max_delay)
        self.add_network_function_list(prefix)
        self.add_nfv_vlinks_list(max_delay)

    def add_network_function_list(self, prefix: str):
        self.network_functions.append(MySQL(prefix, self.MYSQL))
        self.network_functions.append(NRF(prefix, self.NRF))
        self.network_functions.append(IMS(prefix, self.IMS))
        self.network_functions.append(PreparedImageVMTemplate(prefix, self.UDR))
        # self.network_functions.append(PreparedImageVMTemplate(prefix, self.UDM))
        # self.network_functions.append(PreparedImageVMTemplate(prefix, self.AUSF))
        # self.network_functions.append(PreparedImageVMTemplate(prefix, self.AMF))
        # self.network_functions.append(PreparedImageVMTemplate(prefix, self.SMF))
        # self.network_functions.append(PreparedImageVMTemplate(prefix, self.UPF))
        # self.network_functions.append(PreparedImageVMTemplate(prefix, self.TRF_GEN))

    def add_nfv_vlinks_list(self, max_delay: float):
        vlinks = [[self.MYSQL, self.NRF],
                  [self.MYSQL, self.UDR],
                  [self.MYSQL, self.IMS],
                  # [self.MYSQL, self.UDM],
                  # [self.MYSQL, self.AUSF],
                  # [self.MYSQL, self.AMF],
                  # [self.MYSQL, self.SMF],
                  # [self.MYSQL, self.UPF],
                  # [self.MYSQL, self.TRF_GEN],
                  [self.NRF, self.UDR]
                  # [self.NRF, self.UDM],
                  # [self.NRF, self.AUSF],
                  # [self.NRF, self.AMF],
                  # [self.NRF, self.SMF],
                  # [self.NRF, self.UPF],
                  # [self.NRF, self.TRF_GEN],
                  # [self.IMS, self.UPF],
                  # [self.UDR, self.UDM],
                  # [self.UDM, self.AUSF],
                  # [self.AUSF, self.AMF],
                  # [self.AMF, self.SMF],
                  # [self.SMF, self.UPF],
                  # [self.UPF, self.TRF_GEN]
                  ]

        for vlink in vlinks:
            self.nfv_v_links_list.append({"out": vlink[0], "in": vlink[1], "delay": max_delay})
            self.nfv_v_links_list.append({"out": vlink[1], "in": vlink[0], "delay": max_delay})

    def populate_vm_ip(self, user_data: str, nf_ip_dict: Dict[str, str]) -> str:
        user_data = user_data.replace("@@domain@@", self.domain_name)
        user_data = user_data.replace("@@mysql_ip@@", nf_ip_dict[self.MYSQL])
        user_data = user_data.replace("@@mysql_ip@@", nf_ip_dict[self.MYSQL])
        user_data = user_data.replace("@@nrf_ip@@", nf_ip_dict[self.NRF])
        user_data = user_data.replace("@@ims_ip@@", nf_ip_dict[self.IMS])
        user_data = user_data.replace("@@udr_ip@@", nf_ip_dict[self.UDR])
        # user_data = user_data.replace("@@udm_ip@@", nf_ip_dict[self.UDM])
        # user_data = user_data.replace("@@ausf_ip@@", nf_ip_dict[self.AUSF])
        # user_data = user_data.replace("@@amf_ip@@", nf_ip_dict[self.AMF])
        # user_data = user_data.replace("@@smf_ip@@", nf_ip_dict[self.SMF])
        # user_data = user_data.replace("@@upf_ip@@", nf_ip_dict[self.UPF])
        # user_data = user_data.replace("@@trf_ip@@", nf_ip_dict[self.TRF_GEN])
        return user_data

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        LOG.debug(f"I am in OAI 5G CN, {self.domain_name}")
        vm_user_data_dict: Dict[str, str] = {}
        for network_function in self.get_network_functions():
            user_data = network_function.get_user_data()
            user_data = self.populate_vm_ip(user_data, nf_ip_dict)
            user_data = user_data.replace("@@domain@@", self.domain_name)
            if network_function.name == self.MYSQL:
                vm_user_data_dict[self.MYSQL] = self.update_mysql(user_data)
            elif network_function.name == self.NRF:
                vm_user_data_dict[self.NRF] = self.update_nrf(user_data)
            elif network_function.name == self.IMS:
                vm_user_data_dict[self.IMS] = self.update_ims(user_data)
            elif network_function.name == self.UDR:
                vm_user_data_dict[self.UDR] = self.update_udr(user_data)
            elif network_function.name == self.UDM:
                vm_user_data_dict[self.UDM] = self.update_udm(user_data)
            elif network_function.name == self.AUSF:
                vm_user_data_dict[self.AUSF] = self.update_ausf(user_data)
            elif network_function.name == self.AMF:
                vm_user_data_dict[self.AMF] = self.update_amf(user_data)
            elif network_function.name == self.SMF:
                vm_user_data_dict[self.SMF] = self.update_smf(user_data)
            elif network_function.name == self.UPF:
                vm_user_data_dict[self.UPF] = self.update_upf(user_data)
            elif network_function.name == self.TRF_GEN:
                vm_user_data_dict[self.TRF_GEN] = self.update_trf(user_data)

        return vm_user_data_dict

    def update_mysql(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_MYSQL_DOCKER)
        user_data = user_data.replace("@@tz@@", self.MySQL_Values.get("timezone"))
        # MySQL database values
        user_data = user_data.replace("@@mysql_database@@", self.MySQL_Values.get("mysql_database"))
        user_data = user_data.replace("@@mysql_user@@", self.MySQL_Values.get("mysql_user"))
        user_data = user_data.replace("@@mysql_password@@", self.MySQL_Values.get("mysql_password"))
        user_data = user_data.replace("@@mysql_root_password@@", self.MySQL_Values.get("mysql_root_password"))
        # Initial UE values
        user_data = user_data.replace("@@ue_id@@", "001010000000001")
        user_data = user_data.replace("@@enc_permanent_key@@", "fec86ba6eb707ed08905757b1bb44b8f")
        user_data = user_data.replace("@@protection_parameter_id@@", "fec86ba6eb707ed08905757b1bb44b8f")
        user_data = user_data.replace("@@enc_opc_key@@", "C42449363BBAD02B66D16BC975D77CC1")
        user_data = user_data.replace("@@serving_plmn_id@@", "00101")
        user_data = user_data.replace("@@sst@@", "1")
        user_data = user_data.replace("@@dnn@@", "{\\\"oai\\\":{\\\"pduSessionTypes\\\":{"
                                                 "\\\"defaultSessionType\\\": \\\"IPV4\\\"},"
                                                 "\\\"sscModes\\\": {\\\"defaultSscMode\\\": \\\"SSC_MODE_1\\\"},"
                                                 "\\\"5gQosProfile\\\": {\\\"5qi\\\": 6,\\\"arp\\\":{"
                                                 "\\\"priorityLevel\\\": 15,\\\"preemptCap\\\": \\\"NOT_PREEMPT\\\","
                                                 "\\\"preemptVuln\\\":\\\"PREEMPTABLE\\\"},\\\"priorityLevel\\\":1},"
                                                 "\\\"sessionAmbr\\\":{"
                                                 "\\\"uplink\\\":\\\"1000Mbps\\\",\\\"downlink\\\":\\\"1000Mbps\\\"},"
                                                 "\\\"staticIpAddress\\\":[{\\\"ipv4Addr\\\": \\\"12.1.1.99\\\"}]},"
                                                 "\\\"ims\\\":{\\\"pduSessionTypes\\\":{"
                                                 "\\\"defaultSessionType\\\": \\\"IPV4V6\\\"},\\\"sscModes\\\": {"
                                                 "\\\"defaultSscMode\\\": \\\"SSC_MODE_1\\\"},\\\"5gQosProfile\\\": {"
                                                 "\\\"5qi\\\": 2,\\\"arp\\\":{"
                                                 "\\\"priorityLevel\\\": 15,\\\"preemptCap\\\": \\\"NOT_PREEMPT\\\","
                                                 "\\\"preemptVuln\\\":\\\"PREEMPTABLE\\\"},\\\"priorityLevel\\\":1},"
                                                 "\\\"sessionAmbr\\\":{"
                                                 "\\\"uplink\\\":\\\"1000Mbps\\\",\\\"downlink\\\":\\\"1000Mbps\\\"}}}")
        return user_data

    def update_nrf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_NRF_DOCKER)
        user_data = user_data.replace("@@tz@@", self.NRF_Values.get("timezone"))
        user_data = user_data.replace("@@log_level@@", self.NRF_Values.get("log_level"))
        return user_data

    def update_ims(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_IMS_DOCKER)
        user_data = user_data.replace("@@web_port@@", self.IMS_Values.get("web_port"))
        user_data = user_data.replace("@@sms_port@@", self.IMS_Values.get("sms_port"))
        user_data = user_data.replace("@@sys_log@@", self.IMS_Values.get("sys_log"))
        user_data = user_data.replace("@@ue_id_01@@", self.IMS_Values.get("ue_id_01"))
        user_data = user_data.replace("@@ue_user_01_fullname@@", self.IMS_Values.get("ue_user_01_fullname"))
        user_data = user_data.replace("@@ue_id_02@@", self.IMS_Values.get("ue_id_02"))
        user_data = user_data.replace("@@ue_user_02_fullname@@", self.IMS_Values.get("ue_user_02_fullname"))
        return user_data

    def update_config(self, user_data: str) -> str:

        return user_data
    def update_udr(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_UDR_DOCKER)
        user_data = user_data.replace("@@tz@@", self.UDR_Values.get("TZ"))
        user_data = user_data.replace("@@web_port@@", "80")
        user_data = user_data.replace("@@sms_port@@", "80")
        user_data = user_data.replace("@@sys_log@@", "4")
        user_data = user_data.replace("@@ue_id_01@@", "001010000000001")
        user_data = user_data.replace("@@ue_user_01_fullname@@", "User01")
        user_data = user_data.replace("@@ue_id_02@@", "001010000000002")
        user_data = user_data.replace("@@ue_user_02_fullname@@", "User02")
        return user_data

    def update_udm(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_UDM_DOCKER)
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_ausf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_AUSF_DOCKER)
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_amf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_AMF_DOCKER)
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_smf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_SMF_DOCKER)
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_upf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_SMF_DOCKER)
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data

    def update_trf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_TRF_GEN_DOCKER)
        user_data = user_data.replace("@@domain@@", self.domain_name)
        return user_data


def main():
    service = OAI5GCNDC("TUC 5g CN", "kukkalli.com", 1000)
    service_built(service)
    exit()


if __name__ == "__main__":
    main()
