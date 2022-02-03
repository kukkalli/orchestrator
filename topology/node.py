class Node:

    def __init__(self, _id: str, int_id: int, is_switch=True):
        self.__id = _id
        self.__int_id = int_id
        self.__is_switch = is_switch

    @property
    def id(self):
        return self.__id

    @property
    def int_id(self):
        return self.__int_id

    @property
    def is_switch(self):
        return self.__is_switch

#    @id.setter
#    def id(self, _id):
#        self.__id = _id

#    @id.getter
#    def id(self):
#        return self.__id
