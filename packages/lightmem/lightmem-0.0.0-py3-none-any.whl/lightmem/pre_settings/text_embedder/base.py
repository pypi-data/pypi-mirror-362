from abc import ABC, abstractmethod

class TextEmbedderBase(ABC):
    def __init__(self, config):
        self.config = config
        self.embedding_dim = config.get("embedding_dim", None)
        # 其他通用属性可按需添加

    @abstractmethod
    def embed(self, text, **kwargs):
        pass

    def info(self):
        return {
            "embedding_dim": self.embedding_dim,
        }
