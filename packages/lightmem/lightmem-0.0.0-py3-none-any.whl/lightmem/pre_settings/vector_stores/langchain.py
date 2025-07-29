from .basesettings import VectorStoreBase

class VectorStoreLangchain(VectorStoreBase):
    
    @staticmethod
    def validate_config(config):
        required_keys = ["client"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"缺少必要的配置项: {key}")
        return True

    @classmethod
    def from_config(cls, vector_store_db, vector_store_config):
        cls.validate_config(vector_store_config)
        return cls(vector_store_config)

    def add(self, data, **kwargs):
        # 实现具体逻辑
        pass

    def search(self, query, **kwargs):
        # 实现具体逻辑
        pass