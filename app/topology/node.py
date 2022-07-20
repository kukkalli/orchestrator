import logging

LOG = logging.getLogger(__name__)


class Node:

    def __init__(self, int_id: int, str_id: str, name: str, is_switch=True):
        self.__int_id = int_id
        self.__id = str_id
        self.__name = name
        self.__is_switch = is_switch

    @property
    def int_id(self):
        return self.__int_id

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def is_switch(self):
        return self.__is_switch

