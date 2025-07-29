from .langchain import VectorStoreLangchain

class VectorStoreFactory:
    registry = {
        "langchain": VectorStoreLangchain,
        # ...
    }
    @staticmethod
    def instantiate(db_name, config):
        cls = VectorStoreFactory.registry.get(db_name)
        if cls is None:
            raise ValueError(f"Unsupported vector store db:{db_name}")
        return cls.from_config(db_name, config)