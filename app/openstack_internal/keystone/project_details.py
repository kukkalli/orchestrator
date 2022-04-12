from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack.connection import Connection


class Project:
    def __init__(self, connection: Connection):
        self.__connection = connection

    def get_projects_list(self):
        return self.__connection.list_projects()

    def get_project_by_id_or_name(self, project_id_or_name):
        return self.__connection.get_project(project_id_or_name)


def main():
    auth = AuthenticateConnection()
    project = Project(auth.get_connection())

    for _project in project.get_projects_list():
        print("Get Project name: {}, project id: {}".format(_project.name, _project.id))

    _project = project.get_project_by_id_or_name('6b5e1b91ce6d40a082004e7b60b614c4')
    print("Get Project name: {}".format(_project))

    _project = project.get_project_by_id_or_name('admin')
    print("Get Project name: {}".format(_project))


if __name__ == "__main__":
    main()
