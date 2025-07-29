from .deepseek import LlmDeepseek

class LlmFactory:
    registry = {
        "deepseek": LlmDeepseek, 
        # 其他实现可在此注册
    }
    @staticmethod
    def instantiate(llm_name, config):
        cls = LlmFactory.registry.get(llm_name)
        if cls is None:
            raise ValueError(f"Unsupported LLM: {llm_name}")
        return cls.from_config(llm_name, config) 