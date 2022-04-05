"""
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client


class ConnectToNova:

    def __init__(self):
        self.auth = v3.Password(auth_url="http://10.10.0.21:5000/v3", username="admin",
                  user_domain_name="TUC",
                  password="tuckn2020",
                  project_name="admin",
                  project_domain_name="TUC"
                 )
        self.sess = session.Session(auth=self.auth)
        self.nova = client.Client(version='2',session=self.sess)

    def show_network_name(self, item):
        for elm in item:
            network_name = elm
        return network_name

    def show_all_servers_detail(self):
        for item in self.nova.servers.list():
            print('Server Name: ', item.name)
            print('Server ID: ', item.id)
            print('Server Network Name: ', self.show_network_name(item.addresses))
            print('Server IP: ', item.addresses[(self.show_network_name(item.addresses))][0].get('addr'))
            print('Server MAC: ', item.addresses[(self.show_network_name(item.addresses))][0].get('OS-EXT-IPS-MAC:mac_addr'))
            print('Server Compute Node: ', getattr(item, 'OS-EXT-SRV-ATTR:hypervisor_hostname'))
            print('----------------------------------------------------')

    def show_server_info(self,server_id):
        for item in self.nova.servers.list():
            if item.id==server_id:
                server_info = {"server_name": item.name, "server_id": item.id,
                               "server_network_name": self.show_network_name(item.addresses)
                    , "server_ip": item.addresses[(self.show_network_name(item.addresses))][0].get('addr'),
                               "server_mac": item.addresses[(self.show_network_name(item.addresses))][0].get(
                                   'OS-EXT-IPS-MAC:mac_addr'),
                               "server_compute_node": getattr(item, 'OS-EXT-SRV-ATTR:hypervisor_hostname')}
        return server_info

    def show_server_ip(self,server_id):
        for item in self.nova.servers.list():
            if item.id==server_id:
                return(item.addresses[(self.show_network_name(item.addresses))][0].get('addr'))

    def show_server_mac(self,server_id):
        for item in self.nova.servers.list():
            if item.id==server_id:
                return(item.addresses[(self.show_network_name(item.addresses))][0].get('OS-EXT-IPS-MAC:mac_addr'))

    def show_compute_node(self):
        compute_node=set()
        for item in self.nova.servers.list():
            compute_node.add(getattr(item, 'OS-EXT-SRV-ATTR:hypervisor_hostname')) #adding compute name to set to avoid duplicate
        return (compute_node)


#---------Example of using this class------------------
nova_client = ConnectToNova()
nova_client.show_all_servers_detail()
#print(nova_client.show_server_mac('94df548c-46e8-49f5-b94a-ab2f9fd9ffcb'))


"""
