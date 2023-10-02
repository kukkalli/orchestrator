import logging

from templates.four_g_core_cass_db.cassandra_user_data import CassandraDBUserData
from templates.vm_template import VMTemplate

LOG = logging.getLogger(__name__)


class CassandraDB(VMTemplate):

    def __init__(self, prefix: str, nf_name: str):
        super().__init__(prefix, nf_name)
        self.flavor = "2"
        self.user_data = self.get_user_data() + CassandraDBUserData.USERDATA
        # super().__init__()
        # self.flavor = "2"
        # self.vm_name = name+"-cassandra-db"
        # self.name = "cassandra-db"
        # self.user_data = self.get_user_data() + CassandraDBUserData.USERDATA
