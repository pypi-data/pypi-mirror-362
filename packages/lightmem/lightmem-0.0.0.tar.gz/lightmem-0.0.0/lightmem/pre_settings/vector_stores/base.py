from abc import ABC, abstractmethod

class VectorStoreBase(ABC):
    def __init__(self, config):
        self.config = config
        # 可以定义一些通用属性，比如存储路径、collection名等
        self.collection_name = config.get("collection_name", "default")
        self.persist_directory = config.get("persist_directory", None)
        # ... 其他通用属性

    @abstractmethod
    def add(self, data, **kwargs):
        pass

    @abstractmethod
    def search(self, query, **kwargs):
        pass

    # 可以加一些通用方法
    def info(self):
        return {
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory,
        }