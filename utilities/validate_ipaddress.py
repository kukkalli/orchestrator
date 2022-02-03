import ipaddress


class IPAddress(object):
    def __init__(self, ip: str):
        self.__json = ip
        self.ip = None
        self.ip_subnet = None
        self.version = 0
        self.ip_reverse_pointer = None
        self.subnet_or_ip(ip)

    def subnet_or_ip(self, ip: str) -> None:
        try:
            self.verify_valid_network_address(ip)
        except ValueError as err:
            self.try_ip(ip, err)
        finally:
            self.try_ip(ip)

    def try_ip(self, ip: str, err: ValueError = None):
        try:
            self.verify_valid_ip(ip)
        except ValueError as err_ip:
            if err is None:
                pass
            else:
                raise err_ip

    def verify_valid_ip(self, ip: str) -> None:
        try:
            _ip = ipaddress.ip_address(ip)
            self.ip = str(_ip)
            self.version = _ip.version
            self.ip_reverse_pointer = _ip.reverse_pointer
        except ValueError as err:
            raise err

    def verify_valid_network_address(self, ip_subnet) -> None:
        try:
            _ip_subnet = ipaddress.ip_network(ip_subnet)
            self.ip_subnet = _ip_subnet.network_address
        except ValueError as err:
            raise ValueError("The subnet {} is invalid".format(ip_subnet))

    def to_string(self) -> str:
        return self.__json


def main():
    ip_list = ["127.0.0.1", "255.0.0.255", "hanif", "250.0.0.0/32", "192.0.0.0/16", "256.256.256.256",
               "127.0.0.a", "10.10.1.241", "10,10,10,10", "2001:db8::", "2001:db8::/64"]
    for ip in ip_list:
        try:
            _ip = IPAddress(ip)
            print(_ip.ip)
            print(_ip.ip_subnet)
            print(_ip.ip_reverse_pointer)
            print(_ip.version)
        except ValueError as err:
            print(f"Exception: {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
