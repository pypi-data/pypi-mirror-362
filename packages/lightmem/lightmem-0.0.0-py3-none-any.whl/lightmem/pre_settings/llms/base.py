from abc import ABC, abstractmethod

class LlmBase(ABC):
    def __init__(self, config):
        self.config = config
        # 可添加通用属性

    @abstractmethod
    def generate_response(self, *args, **kwargs):
        pass

    def info(self):
        return {
            # 可返回通用信息
        } 