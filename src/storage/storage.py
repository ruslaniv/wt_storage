from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def type(self):
        raise NotImplementedError

    @abstractmethod
    def read(self, document):
        raise NotImplementedError

    @abstractmethod
    def write(self, document):
        raise NotImplementedError


class HotStorage(Storage):
    def type(self):
        pass

    def read(self, document):
        pass

    def write(self, document):
        pass


class ColdStorage(Storage):
    def type(self):
        pass

    def read(self, document):
        pass

    def write(self, document):
        pass


class StorageFactory:
    @staticmethod
    def get_storage(storage_type):
        if storage_type == "hot":
            return HotStorage()
        elif storage_type == "cold":
            return ColdStorage()
        else:
            raise Exception("Unknown storage type")


c
