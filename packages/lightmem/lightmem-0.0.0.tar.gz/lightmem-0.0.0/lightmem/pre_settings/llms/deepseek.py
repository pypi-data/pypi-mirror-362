from .base import LlmBase

class LlmDeepseek(LlmBase):
    def __init__(self, config):
        super().__init__(config)
        self.model = config.get("model", None)
        self.api_key = config.get("api_key", None)
        self.base_url = config.get("deepseek_base_url", None)
        # 其他deepseek相关初始化

    @classmethod
    def from_config(cls, llm_name, config):
        # 可加配置校验
        return cls(config)

    def generate_response(self, *args, **kwargs):
        # 这里应调用deepseek模型生成回复，暂用pass或伪实现
        pass 