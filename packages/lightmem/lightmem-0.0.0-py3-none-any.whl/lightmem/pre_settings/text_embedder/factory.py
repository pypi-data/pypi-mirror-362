class TextEmbedderFactory:
    registry = {
        "huggingface": TextEmbedderHuggingface, 
    }
    @staticmethod
    def instantiate(embedder_name, config):
        cls = TextEmbedderFactory.registry.get(embedder_name)
        if cls is None:
            raise ValueError(f"Unsupported text embedder: {embedder_name}")
        return cls.from_config(embedder_name, config)
