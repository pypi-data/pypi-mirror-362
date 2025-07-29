from .base import TextEmbedderBase

class TextEmbedderHuggingface(TextEmbedderBase):
    def __init__(self, config):
        super().__init__(config)
        self.model = config.get("model", None)
        self.model_kwargs = config.get("model_kwargs", {})
        # 其他huggingface相关初始化

    @classmethod
    def from_config(cls, embedder_name, config):
        # 可加配置校验
        return cls(config)

    def embed(self, text, **kwargs):
        # 这里应调用huggingface模型生成embedding，暂用pass或伪实现
        pass 