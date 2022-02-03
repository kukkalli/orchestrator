from neutronclient.v2_0 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session
import openstack_extract as ex
#import novaclient.v2.client as nvclient
from novaclient import client
auth = v3.Password(auth_url="http://10.10.0.21:5000/v3", username="admin",
                  user_domain_name="tuc",
                  password="tuckn2020",
                  project_name="admin",
                  project_domain_name="TUC"

                 )
sess = session.Session(auth=auth)
#neutron = client.Client(session=sess)
#netw = neutron.list_ports()
#print(netw)

#nova_client = client.Client(version='2.79',username="admin",password="tuckn2020", project_id="6b5e1b91ce6d40a082004e7b60b614c4",auth_url="http://10.10.0.21:5000/v3")
#print(nova_client.flavors.list())

#print(ex.extract_ip(netw,'94df548c-46e8-49f5-b94a-ab2f9fd9ffcb'))



#print(keystone.get_token(session=sess))
#neutron=neutronclient.client(endpoint_url='http://10.10.0.21:8774/v2.1/servers',token=token)


#'''

