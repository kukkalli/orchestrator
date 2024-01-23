import logging
from typing import Dict

from templates.oai_5gcn_base import OAI5GCNDCBase
from templates.oai_5gcn_dc.amf.amf import AMF
from templates.oai_5gcn_dc.ausf.ausf import AUSF
from templates.oai_5gcn_dc.ims.ims import IMS
from templates.oai_5gcn_dc.mysql.mysql import MySQL
from templates.oai_5gcn_dc.nrf.nrf import NRF
from templates.oai_5gcn_dc.smf.smf import SMF
from templates.oai_5gcn_dc.udm.udm import UDM
from templates.oai_5gcn_dc.udr.udr import UDR
from templates.oai_5gcn_dc.upf.upf import UPF
from templates.user_data.oai_5gcn_constants import OAI5GConstants
from test_scripts.service_build_test import service_built

LOG = logging.getLogger(__name__)


class OAI5GCNDC(OAI5GCNDCBase):
    IMS_Values = {
        "web_port": "80",
        "sms_port": "80",
        "sys_log": "4",
        "ue_id_01": "001010000000001",
        "ue_user_01_fullname": "Ameya Joshi",
        "ue_id_02": "001010000000002",
        "ue_user_02_fullname": "Syed Tasnimul Islam"
    }

    CONF_Values = {
        "MYSQL_SERVER": "mysql",
        "MYSQL_USER": "oai_tuc",
        "MYSQL_PASS": "oai_tuc",
        "MYSQL_DB": "oai_db",
        "DB_CONNECTION_TIMEOUT": "300",
        "WAIT_MYSQL": "120",
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
        "DNN_DEF_5QI": "9",
        "DNN_DEF_SESSION_AMBR_UL": "50Mbps",
        "DNN_DEF_SESSION_AMBR_DL": "100Mbps",
        "DNN_DEF_PDU_SESSION_TYPE": "IPV4",
        "DNN_IMS": "ims",
        "DNN_IMS_PDU_SESSION_TYPE": "IPV4V6"
    }

    UDR_Values = {
        "TZ": "Europe/Berlin",
        "UDR_NAME": "OAI_UDR",
        "UDR_INTERFACE_NAME_FOR_NUDR": "eth0",
        "WAIT_MYSQL": "120",
        "USE_FQDN_DNS": "yes",
        "REGISTER_NRF": "yes"
    }

    UDM_Values = {
        "UDM_NAME": "OAI_UDM",
        "SBI_IF_NAME": "eth0",
        "USE_FQDN_DNS": "yes",
        "REGISTER_NRF": "yes"
    }

    AUSF_Values = {
        "AUSF_NAME": "OAI_AUSF",
        "SBI_IF_NAME": "eth0",
        "USE_FQDN_DNS": "yes",
        "REGISTER_NRF": "yes"
    }

    AMF_Values = {
        "AMF_NAME": "OAI-AMF",
        "LOG_LEVEL": "debug",
        "AMF_INTERFACE_NAME_FOR_NGAP": "eth0",
        "AMF_PORT_NGAP": "38412",
        "AMF_INTERFACE_NAME_FOR_SBI": "eth0",
        "AMF_PORT_SBI": "80",
        "AMF_API_VERSION_SBI": "v1",
        "AMF_HTTP2_PORT_SBI": "8080",
        "USE_FQDN_DNS": "yes",
        "REGISTER_NRF": "yes",
        "EXTERNAL_AUSF": "yes",
        # SMF Info
        "SMF_01_INSTANCE_ID": "1",
        "SMF_01_PORT": "80",
        "SMF_01_HTTP2_PORT": "8080",
        "SMF_01_VERSION": "v1",
        "SMF_01_SELECTED": "true",
        # NRF Info
        "NRF_PORT": "80",
        "NRF_API_VERSION": "v1",
        # AUSF Info
        "AUSF_PORT": "80",
        "AUSF_API_VERSION": "v1",
        # UDM Info
        "UDM_PORT": "80",
        "UDM_API_VERSION": "v1",
        # MySQL Info
        "MYSQL_USER": "oai_tuc",
        "MYSQL_PASS": "oai_tuc",
        "MYSQL_DB": "oai_db",
        # PLMN list 01
        "MCC_01": "208",
        "MNC_01": "95",
        "AMF_REGION_ID_01": "128",
        "AMF_SET_ID_01": "1",
        "AMF_POINTER_01": "1",
        # PLMN Support List
        "PLMN_SL_MCC": "208",
        "PLMN_SL_MNC": "95",
        "PLMN_SL_TAC": "0xa000",
        # "PLMN_SL_TAC": "0x0001",
        # NSSAI Set 01
        "NSSAI_SST_01": "1"
    }

    SMF_Values = {
        # SMF Config
        "SMF_FQDN": "oai-smf-svc",
        "SMF_PORT_FOR_SBI": "80",
        "SMF_HTTP2_PORT_FOR_SBI": "8080",
        "SMF_API_VERSION_FOR_SBI": "v1",
        "AMF_PORT": "80",
        "AMF_API_VERSION": "v1",

        # Session Management Subscription List 01
        "SM_01_NSSAI_SST": "1",
        "SM_01_NSSAI_SD": "0xFFFFFF",
        "SM_01_DNN": "oai",
        "SM_01_DEFAULT_SESSION_TYPE": "IPv4",
        "SM_01_DEFAULT_SSC_MODE": "1",
        "SM_01_QOS_PROFILE_5QI": "6",
        "SM_01_QOS_PROFILE_PRIORITY_LEVEL": "1",
        "SM_01_QOS_PROFILE_ARP_PRIORITY_LEVEL": "1",
        "SM_01_QOS_PROFILE_ARP_PREEMPTCAP": "NOT_PREEMPT",
        "SM_01_QOS_PROFILE_ARP_PREEMPTVULN": "NOT_PREEMPTABLE",
        "SM_01_SESSION_AMBR_UL": "10Gbps",
        "SM_01_SESSION_AMBR_DL": "10Gbps",

        # Session Management Subscription List 02
        "SM_02_NSSAI_SST": "1",
        "SM_02_NSSAI_SD": "0xFFFFFF",
        "SM_02_DNN": "openairinterface",
        "SM_02_DEFAULT_SESSION_TYPE": "IPv4v6",
        "SM_02_DEFAULT_SSC_MODE": "1",
        "SM_02_QOS_PROFILE_5QI": "7",
        "SM_02_QOS_PROFILE_PRIORITY_LEVEL": "1",
        "SM_02_QOS_PROFILE_ARP_PRIORITY_LEVEL": "1",
        "SM_02_QOS_PROFILE_ARP_PREEMPTCAP": "NOT_PREEMPT",
        "SM_02_QOS_PROFILE_ARP_PREEMPTVULN": "NOT_PREEMPTABLE",
        "SM_02_SESSION_AMBR_UL": "10Gbps",
        "SM_02_SESSION_AMBR_DL": "10Gbps",

        # Session Management Subscription List 02
        "SM_03_NSSAI_SST": "1",
        "SM_03_NSSAI_SD": "0xFFFFFF",
        "SM_03_DNN": "ims",
        "SM_03_DEFAULT_SESSION_TYPE": "IPv4v6",
        "SM_03_DEFAULT_SSC_MODE": "1",
        "SM_03_QOS_PROFILE_5QI": "8",
        "SM_03_QOS_PROFILE_PRIORITY_LEVEL": "1",
        "SM_03_QOS_PROFILE_ARP_PRIORITY_LEVEL": "1",
        "SM_03_QOS_PROFILE_ARP_PREEMPTCAP": "NOT_PREEMPT",
        "SM_03_QOS_PROFILE_ARP_PREEMPTVULN": "NOT_PREEMPTABLE",
        "SM_03_SESSION_AMBR_UL": "10Gbps",
        "SM_03_SESSION_AMBR_DL": "10Gbps",

        # Docker config variables
        "SMF_INTERFACE_NAME_FOR_N4": "eth0",
        "SMF_INTERFACE_NAME_FOR_SBI": "eth0",
        "DEFAULT_DNS_IPV4_ADDRESS": "8.8.8.8",
        "DEFAULT_DNS_SEC_IPV4_ADDRESS": "4.4.4.4",
        "AMF_FQDN": "oai-amf",
        "UDM_FQDN": "oai-udm",
        "UPF_FQDN_0": "oai-spgwu-tiny",
        "NRF_FQDN": "oai-nrf",
        "USE_LOCAL_SUBSCRIPTION_INFO": "yes",
        "REGISTER_NRF": "yes",
        "DISCOVER_UPF": "yes",
        "USE_FQDN_DNS": "yes",
        "UE_MTU": "1500",

        # Slice 0 (1, 0xFFFFFF)
        "DNN_NI0": "oai",
        "TYPE0": "IPv4",
        "DNN_RANGE0": "12.1.1.2 - 12.1.1.254",
        "NSSAI_SST0": "1",
        "SESSION_AMBR_UL0": "10Gbps",
        "SESSION_AMBR_DL0": "10Gbps",
        # Slice 1 (1, 0xFFFFFF)
        "DNN_NI1": "openairinterface",
        "TYPE1": "IPv4v6",
        "DNN_RANGE1": "12.1.2.2 - 12.1.2.254",
        "NSSAI_SST1": "1",
        "SESSION_AMBR_UL1": "10Gbps",
        "SESSION_AMBR_DL1": "10Gbps",
        # Slice 2 for ims
        "DNN_NI2": "ims",
        "TYPE2": "IPv4v6",
        "DNN_RANGE2": "12.1.9.2 - 12.1.9.254",
        "NSSAI_SST2": "1",
        "SESSION_AMBR_UL2": "10Gbps",
        "SESSION_AMBR_DL2": "10Gbps"
    }

    UPF_Values = {
        # NSSAI Set 01
        "NSSAI_SST_01": "1",
        "NSSAI_SD_01": "0xFFFFFF",
        "DNN_01": "oai",
        # NSSAI Set 02
        "NSSAI_SST_02": "1",
        "NSSAI_SD_02": "0xFFFFFF",
        "DNN_02": "openairinterface",
        # NSSAI Set 03
        "NSSAI_SST_03": "1",
        "NSSAI_SD_03": "0xFFFFFF",
        "DNN_03": "ims"
    }

    def __init__(self, prefix: str, domain_name: str, bandwidth: int, max_delay: float = 1.0):
        super().__init__(prefix, domain_name, bandwidth, max_delay)
        self.add_network_function_list(prefix)
        self.add_nfv_vlinks_list(max_delay)

    def add_network_function_list(self, prefix: str):
        self.network_functions.append(MySQL(prefix, self.MYSQL))
        self.network_functions.append(NRF(prefix, self.NRF))
        self.network_functions.append(IMS(prefix, self.IMS))
        self.network_functions.append(UDR(prefix, self.UDR))
        self.network_functions.append(UDM(prefix, self.UDM))
        self.network_functions.append(AUSF(prefix, self.AUSF))
        self.network_functions.append(AMF(prefix, self.AMF))
        self.network_functions.append(SMF(prefix, self.SMF))
        self.network_functions.append(UPF(prefix, self.UPF))
        # self.network_functions.append(TRF(prefix, self.TRF_GEN))

    def populate_user_data(self, nf_ip_dict: Dict[str, str]) -> Dict[str, str]:
        LOG.debug(f"I am in OAI 5G CN Docker, {self.domain_name}")
        vm_user_data_dict: Dict[str, str] = {}
        for network_function in self.get_network_functions():
            user_data = network_function.get_user_data()
            user_data = self.populate_vm_ip(user_data, nf_ip_dict)
            user_data = user_data.replace("@@domain@@", self.domain_name)
            user_data = user_data.replace("@@tz@@", self.TimeZone)
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
            # elif network_function.name == self.TRF_GEN:
            #     vm_user_data_dict[self.TRF_GEN] = self.update_trf(user_data)

        return vm_user_data_dict

    def update_mysql(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_MYSQL_DOCKER)
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
        user_data = user_data.replace("@@mysql_server@@", self.CONF_Values.get("MYSQL_SERVER"))
        # user_data = user_data.replace("@@mysql_ipv4_address@@", self.CONF_Values.get("MYSQL_IPV4_ADDRESS"))
        user_data = user_data.replace("@@mysql_user@@", self.CONF_Values.get("MYSQL_USER"))
        user_data = user_data.replace("@@mysql_pass@@", self.CONF_Values.get("MYSQL_PASS"))
        user_data = user_data.replace("@@mysql_db@@", self.CONF_Values.get("MYSQL_DB"))
        user_data = user_data.replace("@@db_connection_timeout@@", self.CONF_Values.get("DB_CONNECTION_TIMEOUT"))
        # PLMN list 01
        user_data = user_data.replace("@@mcc_01@@", self.CONF_Values.get("MCC_01"))
        user_data = user_data.replace("@@mnc_01@@", self.CONF_Values.get("MNC_01"))
        user_data = user_data.replace("@@amf_region_id_01@@", self.CONF_Values.get("AMF_REGION_ID_01"))
        user_data = user_data.replace("@@amf_set_id_01@@", self.CONF_Values.get("AMF_SET_ID_01"))
        user_data = user_data.replace("@@amf_pointer_01@@", self.CONF_Values.get("AMF_POINTER_01"))
        # PLMN list 02
        user_data = user_data.replace("@@mcc_02@@", self.CONF_Values.get("MCC_02"))
        user_data = user_data.replace("@@mnc_02@@", self.CONF_Values.get("MNC_02"))
        user_data = user_data.replace("@@amf_region_id_02@@", self.CONF_Values.get("AMF_REGION_ID_02"))
        user_data = user_data.replace("@@amf_set_id_02@@", self.CONF_Values.get("AMF_SET_ID_02"))
        user_data = user_data.replace("@@amf_pointer_02@@", self.CONF_Values.get("AMF_POINTER_02"))
        # PLMN Support List
        user_data = user_data.replace("@@plmn_sl_mcc@@", self.CONF_Values.get("PLMN_SL_MCC"))
        user_data = user_data.replace("@@plmn_sl_mnc@@", self.CONF_Values.get("PLMN_SL_MNC"))
        user_data = user_data.replace("@@plmn_sl_tac@@", self.CONF_Values.get("PLMN_SL_TAC"))
        # NSSAI Set 01
        user_data = user_data.replace("@@nssai_sst_01@@", self.CONF_Values.get("NSSAI_SST_01"))
        # NSSAI Set 02
        user_data = user_data.replace("@@nssai_sst_02@@", self.CONF_Values.get("NSSAI_SST_02"))
        user_data = user_data.replace("@@nssai_sd_02@@", self.CONF_Values.get("NSSAI_SD_02"))
        # NSSAI Set 03
        user_data = user_data.replace("@@nssai_sst_03@@", self.CONF_Values.get("NSSAI_SST_03"))
        user_data = user_data.replace("@@nssai_sd_03@@", self.CONF_Values.get("NSSAI_SD_03"))
        # # IMS IPv4
        # user_data = user_data.replace("@@ims_ipv4@@", self.CONF_Values.get("IMS_IPV4"))
        # DNN List
        # DNN 01
        user_data = user_data.replace("@@dnn_01_sst@@", self.CONF_Values.get("DNN_01_SST"))
        user_data = user_data.replace("@@dnn_01_dnn@@", self.CONF_Values.get("DNN_01_DNN"))
        user_data = user_data.replace("@@dnn_01_5qi@@", self.CONF_Values.get("DNN_01_5QI"))
        user_data = user_data.replace("@@dnn_01_session_ambr_ul@@",
                                      self.CONF_Values.get("DNN_01_SESSION_AMBR_UL"))
        user_data = user_data.replace("@@dnn_01_session_ambr_dl@@",
                                      self.CONF_Values.get("DNN_01_SESSION_AMBR_DL"))
        user_data = user_data.replace("@@dnn_01_pdu_session_type@@",
                                      self.CONF_Values.get("DNN_01_PDU_SESSION_TYPE"))
        # DNN 02
        user_data = user_data.replace("@@dnn_02_sst@@", self.CONF_Values.get("DNN_02_SST"))
        user_data = user_data.replace("@@dnn_02_sd@@", self.CONF_Values.get("DNN_02_SD"))
        user_data = user_data.replace("@@dnn_02_dnn@@", self.CONF_Values.get("DNN_02_DNN"))
        user_data = user_data.replace("@@dnn_02_5qi@@", self.CONF_Values.get("DNN_02_5QI"))
        user_data = user_data.replace("@@dnn_02_session_ambr_ul@@",
                                      self.CONF_Values.get("DNN_02_SESSION_AMBR_UL"))
        user_data = user_data.replace("@@dnn_02_session_ambr_dl@@",
                                      self.CONF_Values.get("DNN_02_SESSION_AMBR_DL"))
        user_data = user_data.replace("@@dnn_02_pdu_session_type@@",
                                      self.CONF_Values.get("DNN_02_PDU_SESSION_TYPE"))
        # Default DNN
        user_data = user_data.replace("@@dnn_def_sst@@", self.CONF_Values.get("DNN_DEF_SST"))
        user_data = user_data.replace("@@dnn_def_sd@@", self.CONF_Values.get("DNN_DEF_SD"))
        user_data = user_data.replace("@@dnn_def_dnn@@", self.CONF_Values.get("DNN_DEF_DNN"))
        user_data = user_data.replace("@@dnn_def_5qi@@", self.CONF_Values.get("DNN_DEF_5QI"))
        user_data = user_data.replace("@@dnn_def_session_ambr_ul@@",
                                      self.CONF_Values.get("DNN_DEF_SESSION_AMBR_UL"))
        user_data = user_data.replace("@@dnn_def_session_ambr_dl@@",
                                      self.CONF_Values.get("DNN_DEF_SESSION_AMBR_DL"))
        user_data = user_data.replace("@@dnn_def_pdu_session_type@@",
                                      self.CONF_Values.get("DNN_DEF_PDU_SESSION_TYPE"))
        # IMS
        user_data = user_data.replace("@@dnn_ims@@", self.CONF_Values.get("DNN_IMS"))
        user_data = user_data.replace("@@dnn_ims_pdu_session_type@@",
                                      self.CONF_Values.get("DNN_IMS_PDU_SESSION_TYPE"))
        return user_data

    def update_udr(self, user_data: str) -> str:
        user_data = self.update_config(user_data)
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_UDR_DOCKER)
        user_data = user_data.replace("@@udr_name@@", self.UDR_Values.get("UDR_NAME"))
        user_data = user_data.replace("@@udr_interface_name_for_nudr@@",
                                      self.UDR_Values.get("UDR_INTERFACE_NAME_FOR_NUDR"))
        user_data = user_data.replace("@@wait_mysql@@", self.UDR_Values.get("WAIT_MYSQL"))
        user_data = user_data.replace("@@use_fqdn_dns@@", self.UDR_Values.get("USE_FQDN_DNS"))
        user_data = user_data.replace("@@register_nrf@@", self.UDR_Values.get("REGISTER_NRF"))
        user_data = user_data.replace("@@nrf_hostname@@", self.NRF)
        user_data = user_data.replace("@@nrf_fqdn@@", self.NRF)
        return user_data

    def update_udm(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_UDM_DOCKER)
        user_data = user_data.replace("@@udm_name@@", self.UDM_Values.get("UDM_NAME"))
        user_data = user_data.replace("@@sbi_if_name@@", self.UDM_Values.get("SBI_IF_NAME"))
        user_data = user_data.replace("@@register_nrf@@", self.UDM_Values.get("REGISTER_NRF"))
        user_data = user_data.replace("@@use_fqdn_dns@@", self.UDM_Values.get("USE_FQDN_DNS"))
        user_data = user_data.replace("@@udr_fqdn@@", self.UDR)
        user_data = user_data.replace("@@nrf_fqdn@@", self.NRF)
        return user_data

    def update_ausf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_AUSF_DOCKER)
        user_data = user_data.replace("@@ausf_name@@", self.AUSF_Values.get("AUSF_NAME"))
        user_data = user_data.replace("@@sbi_if_name@@", self.AUSF_Values.get("SBI_IF_NAME"))
        user_data = user_data.replace("@@register_nrf@@", self.AUSF_Values.get("REGISTER_NRF"))
        user_data = user_data.replace("@@use_fqdn_dns@@", self.AUSF_Values.get("USE_FQDN_DNS"))
        user_data = user_data.replace("@@udm_fqdn@@", self.UDM)
        user_data = user_data.replace("@@nrf_fqdn@@", self.NRF)
        return user_data

    def update_amf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_AMF_DOCKER)
        user_data = user_data.replace("@@amf_name@@", self.AMF_Values.get("AMF_NAME"))
        user_data = user_data.replace("@@log_level@@", self.AMF_Values.get("LOG_LEVEL"))
        user_data = user_data.replace("@@AMF_INTERFACE_NAME_FOR_NGAP@@",
                                      self.AMF_Values.get("AMF_INTERFACE_NAME_FOR_NGAP"))
        user_data = user_data.replace("@@AMF_PORT_NGAP@@", self.AMF_Values.get("AMF_PORT_NGAP"))
        user_data = user_data.replace("@@AMF_INTERFACE_NAME_FOR_SBI@@",
                                      self.AMF_Values.get("AMF_INTERFACE_NAME_FOR_SBI"))
        user_data = user_data.replace("@@AMF_PORT_SBI@@", self.AMF_Values.get("AMF_PORT_SBI"))
        user_data = user_data.replace("@@AMF_API_VERSION_SBI@@", self.AMF_Values.get("AMF_API_VERSION_SBI"))
        user_data = user_data.replace("@@AMF_HTTP2_PORT_SBI@@", self.AMF_Values.get("AMF_HTTP2_PORT_SBI"))
        user_data = user_data.replace("@@USE_FQDN_DNS@@", self.AMF_Values.get("USE_FQDN_DNS"))
        user_data = user_data.replace("@@REGISTER_NRF@@", self.AMF_Values.get("REGISTER_NRF"))
        user_data = user_data.replace("@@EXTERNAL_AUSF@@", self.AMF_Values.get("EXTERNAL_AUSF"))
        # SMF Info
        user_data = user_data.replace("@@SMF_01_INSTANCE_ID@@", self.AMF_Values.get("SMF_01_INSTANCE_ID"))
        user_data = user_data.replace("@@SMF_01_PORT@@", self.AMF_Values.get("SMF_01_PORT"))
        user_data = user_data.replace("@@SMF_01_HTTP2_PORT@@", self.AMF_Values.get("SMF_01_HTTP2_PORT"))
        user_data = user_data.replace("@@SMF_01_VERSION@@", self.AMF_Values.get("SMF_01_VERSION"))
        user_data = user_data.replace("@@SMF_01_FQDN@@", self.SMF)
        user_data = user_data.replace("@@SMF_01_SELECTED@@", self.AMF_Values.get("SMF_01_SELECTED"))
        # NRF Info
        user_data = user_data.replace("@@NRF_PORT@@", self.AMF_Values.get("NRF_PORT"))
        user_data = user_data.replace("@@NRF_API_VERSION@@", self.AMF_Values.get("NRF_API_VERSION"))
        user_data = user_data.replace("@@NRF_FQDN@@", self.NRF)
        # AUSF Info
        user_data = user_data.replace("@@AUSF_PORT@@", self.AMF_Values.get("AUSF_PORT"))
        user_data = user_data.replace("@@AUSF_API_VERSION@@", self.AMF_Values.get("AUSF_API_VERSION"))
        user_data = user_data.replace("@@AUSF_FQDN@@", self.AUSF)
        # UDM Info
        user_data = user_data.replace("@@UDM_PORT@@", self.AMF_Values.get("UDM_PORT"))
        user_data = user_data.replace("@@UDM_API_VERSION@@", self.AMF_Values.get("UDM_API_VERSION"))
        user_data = user_data.replace("@@UDM_FQDN@@", self.UDM)
        # MySQL Info
        user_data = user_data.replace("@@MYSQL_SERVER@@", self.MYSQL)
        user_data = user_data.replace("@@MYSQL_USER@@", self.AMF_Values.get("MYSQL_USER"))
        user_data = user_data.replace("@@MYSQL_PASS@@", self.AMF_Values.get("MYSQL_PASS"))
        user_data = user_data.replace("@@MYSQL_DB@@", self.AMF_Values.get("MYSQL_DB"))
        # PLMN list 01
        user_data = user_data.replace("@@MCC_01@@", self.AMF_Values.get("MCC_01"))
        user_data = user_data.replace("@@MNC_01@@", self.AMF_Values.get("MNC_01"))
        user_data = user_data.replace("@@AMF_REGION_ID_01@@", self.AMF_Values.get("AMF_REGION_ID_01"))
        user_data = user_data.replace("@@AMF_SET_ID_01@@", self.AMF_Values.get("AMF_SET_ID_01"))
        user_data = user_data.replace("@@AMF_POINTER_01@@", self.AMF_Values.get("AMF_POINTER_01"))
        # PLMN Support List
        user_data = user_data.replace("@@PLMN_SL_MCC@@", self.AMF_Values.get("PLMN_SL_MCC"))
        user_data = user_data.replace("@@PLMN_SL_MNC@@", self.AMF_Values.get("PLMN_SL_MNC"))
        user_data = user_data.replace("@@PLMN_SL_TAC@@", self.AMF_Values.get("PLMN_SL_TAC"))
        # NSSAI Set 01
        user_data = user_data.replace("@@NSSAI_SST_01@@", self.AMF_Values.get("NSSAI_SST_01"))
        return user_data

    def update_smf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_SMF_DOCKER)
        # SMF Config
        user_data = user_data.replace("@@SMF_FQDN@@", self.SMF_Values.get("SMF_FQDN"))
        user_data = user_data.replace("@@SMF_PORT_FOR_SBI@@", self.SMF_Values.get("SMF_PORT_FOR_SBI"))
        user_data = user_data.replace("@@SMF_HTTP2_PORT_FOR_SBI@@", self.SMF_Values.get("SMF_HTTP2_PORT_FOR_SBI"))
        user_data = user_data.replace("@@SMF_API_VERSION_FOR_SBI@@", self.SMF_Values.get("SMF_API_VERSION_FOR_SBI"))
        user_data = user_data.replace("@@AMF_PORT@@", self.SMF_Values.get("AMF_PORT"))
        user_data = user_data.replace("@@AMF_API_VERSION@@", self.SMF_Values.get("AMF_API_VERSION"))

        # Session Management Subscription List 01
        user_data = user_data.replace("@@SM_01_NSSAI_SST@@", self.SMF_Values.get("SM_01_NSSAI_SST"))
        user_data = user_data.replace("@@SM_01_NSSAI_SD@@", self.SMF_Values.get("SM_01_NSSAI_SD"))
        user_data = user_data.replace("@@SM_01_DNN@@", self.SMF_Values.get("SM_01_DNN"))
        user_data = user_data.replace("@@SM_01_DEFAULT_SESSION_TYPE@@",
                                      self.SMF_Values.get("SM_01_DEFAULT_SESSION_TYPE"))
        user_data = user_data.replace("@@SM_01_DEFAULT_SSC_MODE@@", self.SMF_Values.get("SM_01_DEFAULT_SSC_MODE"))
        user_data = user_data.replace("@@SM_01_QOS_PROFILE_5QI@@", self.SMF_Values.get("SM_01_QOS_PROFILE_5QI"))
        user_data = user_data.replace("@@SM_01_QOS_PROFILE_PRIORITY_LEVEL@@",
                                      self.SMF_Values.get("SM_01_QOS_PROFILE_PRIORITY_LEVEL"))
        user_data = user_data.replace("@@SM_01_QOS_PROFILE_ARP_PRIORITY_LEVEL@@",
                                      self.SMF_Values.get("SM_01_QOS_PROFILE_ARP_PRIORITY_LEVEL"))
        user_data = user_data.replace("@@SM_01_QOS_PROFILE_ARP_PREEMPTCAP@@",
                                      self.SMF_Values.get("SM_01_QOS_PROFILE_ARP_PREEMPTCAP"))
        user_data = user_data.replace("@@SM_01_QOS_PROFILE_ARP_PREEMPTVULN@@",
                                      self.SMF_Values.get("SM_01_QOS_PROFILE_ARP_PREEMPTVULN"))
        user_data = user_data.replace("@@SM_01_SESSION_AMBR_UL@@", self.SMF_Values.get("SM_01_SESSION_AMBR_UL"))
        user_data = user_data.replace("@@SM_01_SESSION_AMBR_DL@@", self.SMF_Values.get("SM_01_SESSION_AMBR_DL"))

        # Session Management Subscription List 02
        user_data = user_data.replace("@@SM_02_NSSAI_SST@@", self.SMF_Values.get("SM_02_NSSAI_SST"))
        user_data = user_data.replace("@@SM_02_NSSAI_SD@@", self.SMF_Values.get("SM_02_NSSAI_SD"))
        user_data = user_data.replace("@@SM_02_DNN@@", self.SMF_Values.get("SM_02_DNN"))
        user_data = user_data.replace("@@SM_02_DEFAULT_SESSION_TYPE@@",
                                      self.SMF_Values.get("SM_02_DEFAULT_SESSION_TYPE"))
        user_data = user_data.replace("@@SM_02_DEFAULT_SSC_MODE@@", self.SMF_Values.get("SM_02_DEFAULT_SSC_MODE"))
        user_data = user_data.replace("@@SM_02_QOS_PROFILE_5QI@@", self.SMF_Values.get("SM_02_QOS_PROFILE_5QI"))
        user_data = user_data.replace("@@SM_02_QOS_PROFILE_PRIORITY_LEVEL@@",
                                      self.SMF_Values.get("SM_02_QOS_PROFILE_PRIORITY_LEVEL"))
        user_data = user_data.replace("@@SM_02_QOS_PROFILE_ARP_PRIORITY_LEVEL@@",
                                      self.SMF_Values.get("SM_02_QOS_PROFILE_ARP_PRIORITY_LEVEL"))
        user_data = user_data.replace("@@SM_02_QOS_PROFILE_ARP_PREEMPTCAP@@",
                                      self.SMF_Values.get("SM_02_QOS_PROFILE_ARP_PREEMPTCAP"))
        user_data = user_data.replace("@@SM_02_QOS_PROFILE_ARP_PREEMPTVULN@@",
                                      self.SMF_Values.get("SM_02_QOS_PROFILE_ARP_PREEMPTVULN"))
        user_data = user_data.replace("@@SM_02_SESSION_AMBR_UL@@", self.SMF_Values.get("SM_02_SESSION_AMBR_UL"))
        user_data = user_data.replace("@@SM_02_SESSION_AMBR_DL@@", self.SMF_Values.get("SM_02_SESSION_AMBR_DL"))

        # Session Management Subscription List 02
        user_data = user_data.replace("@@SM_03_NSSAI_SST@@", self.SMF_Values.get("SM_03_NSSAI_SST"))
        user_data = user_data.replace("@@SM_03_NSSAI_SD@@", self.SMF_Values.get("SM_03_NSSAI_SD"))
        user_data = user_data.replace("@@SM_03_DNN@@", self.SMF_Values.get("SM_03_DNN"))
        user_data = user_data.replace("@@SM_03_DEFAULT_SESSION_TYPE@@",
                                      self.SMF_Values.get("SM_03_DEFAULT_SESSION_TYPE"))
        user_data = user_data.replace("@@SM_03_DEFAULT_SSC_MODE@@", self.SMF_Values.get("SM_03_DEFAULT_SSC_MODE"))
        user_data = user_data.replace("@@SM_03_QOS_PROFILE_5QI@@", self.SMF_Values.get("SM_03_QOS_PROFILE_5QI"))
        user_data = user_data.replace("@@SM_03_QOS_PROFILE_PRIORITY_LEVEL@@",
                                      self.SMF_Values.get("SM_03_QOS_PROFILE_PRIORITY_LEVEL"))
        user_data = user_data.replace("@@SM_03_QOS_PROFILE_ARP_PRIORITY_LEVEL@@",
                                      self.SMF_Values.get("SM_03_QOS_PROFILE_ARP_PRIORITY_LEVEL"))
        user_data = user_data.replace("@@SM_03_QOS_PROFILE_ARP_PREEMPTCAP@@",
                                      self.SMF_Values.get("SM_03_QOS_PROFILE_ARP_PREEMPTCAP"))
        user_data = user_data.replace("@@SM_03_QOS_PROFILE_ARP_PREEMPTVULN@@",
                                      self.SMF_Values.get("SM_03_QOS_PROFILE_ARP_PREEMPTVULN"))
        user_data = user_data.replace("@@SM_03_SESSION_AMBR_UL@@", self.SMF_Values.get("SM_03_SESSION_AMBR_UL"))
        user_data = user_data.replace("@@SM_03_SESSION_AMBR_DL@@", self.SMF_Values.get("SM_03_SESSION_AMBR_DL"))

        # Docker config variables
        user_data = user_data.replace("@@SMF_INTERFACE_NAME_FOR_N4@@", self.SMF_Values.get("SMF_INTERFACE_NAME_FOR_N4"))
        user_data = user_data.replace("@@SMF_INTERFACE_NAME_FOR_SBI@@",
                                      self.SMF_Values.get("SMF_INTERFACE_NAME_FOR_SBI"))
        user_data = user_data.replace("@@DEFAULT_DNS_IPV4_ADDRESS@@", self.SMF_Values.get("DEFAULT_DNS_IPV4_ADDRESS"))
        user_data = user_data.replace("@@DEFAULT_DNS_SEC_IPV4_ADDRESS@@",
                                      self.SMF_Values.get("DEFAULT_DNS_SEC_IPV4_ADDRESS"))
        user_data = user_data.replace("@@AMF_FQDN@@", self.AMF)
        user_data = user_data.replace("@@UDM_FQDN@@", self.UDM)
        user_data = user_data.replace("@@UPF_FQDN_0@@", self.UPF)
        user_data = user_data.replace("@@NRF_FQDN@@", self.NRF)
        user_data = user_data.replace("@@USE_LOCAL_SUBSCRIPTION_INFO@@",
                                      self.SMF_Values.get("USE_LOCAL_SUBSCRIPTION_INFO"))
        user_data = user_data.replace("@@REGISTER_NRF@@", self.SMF_Values.get("REGISTER_NRF"))
        user_data = user_data.replace("@@DISCOVER_UPF@@", self.SMF_Values.get("DISCOVER_UPF"))
        user_data = user_data.replace("@@USE_FQDN_DNS@@", self.SMF_Values.get("USE_FQDN_DNS"))
        user_data = user_data.replace("@@UE_MTU@@", self.SMF_Values.get("UE_MTU"))

        # Slice 0 (1, 0xFFFFFF)
        user_data = user_data.replace("@@DNN_NI0@@", self.SMF_Values.get("DNN_NI0"))
        user_data = user_data.replace("@@TYPE0@@", self.SMF_Values.get("TYPE0"))
        user_data = user_data.replace("@@DNN_RANGE0@@", self.SMF_Values.get("DNN_RANGE0"))
        user_data = user_data.replace("@@NSSAI_SST0@@", self.SMF_Values.get("NSSAI_SST0"))
        user_data = user_data.replace("@@SESSION_AMBR_UL0@@", self.SMF_Values.get("SESSION_AMBR_UL0"))
        user_data = user_data.replace("@@SESSION_AMBR_DL0@@", self.SMF_Values.get("SESSION_AMBR_DL0"))
        # Slice 1 (1, 0xFFFFFF)
        user_data = user_data.replace("@@DNN_NI1@@", self.SMF_Values.get("DNN_NI1"))
        user_data = user_data.replace("@@TYPE1@@", self.SMF_Values.get("TYPE1"))
        user_data = user_data.replace("@@DNN_RANGE1@@", self.SMF_Values.get("DNN_RANGE1"))
        user_data = user_data.replace("@@NSSAI_SST1@@", self.SMF_Values.get("NSSAI_SST1"))
        user_data = user_data.replace("@@SESSION_AMBR_UL1@@", self.SMF_Values.get("SESSION_AMBR_UL1"))
        user_data = user_data.replace("@@SESSION_AMBR_DL1@@", self.SMF_Values.get("SESSION_AMBR_DL1"))
        # Slice 2 for ims
        user_data = user_data.replace("@@DNN_NI2@@", self.SMF_Values.get("DNN_NI2"))
        user_data = user_data.replace("@@TYPE2@@", self.SMF_Values.get("TYPE2"))
        user_data = user_data.replace("@@DNN_RANGE2@@", self.SMF_Values.get("DNN_RANGE2"))
        user_data = user_data.replace("@@NSSAI_SST2@@", self.SMF_Values.get("NSSAI_SST2"))
        user_data = user_data.replace("@@SESSION_AMBR_UL2@@", self.SMF_Values.get("SESSION_AMBR_UL2"))
        user_data = user_data.replace("@@SESSION_AMBR_DL2@@", self.SMF_Values.get("SESSION_AMBR_DL2"))

        return user_data

    def update_upf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_UPF_DOCKER)

        user_data = user_data.replace("@@UPF_FQDN@@", self.UPF)
        user_data = user_data.replace("@@NRF_FQDN@@", self.NRF)

        # NSSAI Set 01
        user_data = user_data.replace("@@NSSAI_SST_01@@", self.UPF_Values.get("NSSAI_SST_01"))
        user_data = user_data.replace("@@NSSAI_SD_01@@", self.UPF_Values.get("NSSAI_SD_01"))
        user_data = user_data.replace("@@DNN_01@@", self.UPF_Values.get("DNN_01"))
        # NSSAI Set 02
        user_data = user_data.replace("@@NSSAI_SST_02@@", self.UPF_Values.get("NSSAI_SST_02"))
        user_data = user_data.replace("@@NSSAI_SD_02@@", self.UPF_Values.get("NSSAI_SD_02"))
        user_data = user_data.replace("@@DNN_02@@", self.UPF_Values.get("DNN_02"))
        # NSSAI Set 03
        user_data = user_data.replace("@@NSSAI_SST_03@@", self.UPF_Values.get("NSSAI_SST_03"))
        user_data = user_data.replace("@@NSSAI_SD_03@@", self.UPF_Values.get("NSSAI_SD_03"))
        user_data = user_data.replace("@@DNN_03@@", self.UPF_Values.get("DNN_03"))

        return user_data

    def update_trf(self, user_data: str) -> str:
        user_data = user_data.replace("@@image_name@@", OAI5GConstants.OAI_5GCN_TRF_GEN_DOCKER)
        user_data = user_data.replace("@@TRF_FQDN@@", self.TRF_GEN)

        return user_data


def main():
    service = OAI5GCNDC("TUC 5g CN", "kukkalli.com", 1000)
    service_built(service)
    exit()


if __name__ == "__main__":
    main()
