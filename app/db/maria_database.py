import logging
import os
import mysql.connector as database

LOG = logging.getLogger(__name__)


class MariaDB:

    def __init__(self):
        self.hostname = os.environ["MARIADB_HOSTNAME"]
        self.username = os.environ["MARIADB_USERNAME"]
        self.password = os.environ["MARIADB_PASSWORD"]
        self.database = os.environ["MARIADB_DATABASE"]
        LOG.debug(f"MariaDB username: {self.username}, hostname: {self.hostname}, database: {self.database}")
        self.connection = None

    def get_db_connection(self):
        try:
            LOG.debug(f"Get DB Connection.")
            self.connection = database.connect(
                user=self.username,
                password=self.password,
                host=self.hostname,
                database='orchestrator'
            )
            return self.connection
        except database.Error as error:
            LOG.exception(f"Connection failed:\n{error}", exc_info=True)

    def close_connection(self):
        self.connection.close()


def main():
    mariadb = MariaDB()
    LOG.debug(f"username: {mariadb.username}, password: {mariadb.password}")
    connection = mariadb.get_db_connection()
    LOG.debug(f"connection: {connection.is_connected()}, connection: {connection.close()}")


if __name__ == "__main__":
    main()
