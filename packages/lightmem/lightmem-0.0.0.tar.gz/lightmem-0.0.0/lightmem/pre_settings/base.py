from pydantic import BaseModel, Field, field_validator
from .LLMs.base import LlmConfig
import os
from typing import Any, Dict, Optional
from pydantic import ValidationError
"""
解析用户输入，初步验证支持的工具
"""

class MemorySettings(BaseModel):
    vector_store_db: Optional[str] = Field(
        description="Configuration for the vector store"
    )
    vector_store_config: Optional[Dict[str,Any]] = Field(
        description="Configuration for the language model",
        default=None,
    )
    llm: Optional[str] = Field(
        description="Configuration for the language model"
    )
    llm_config: Optional[Dict[str,Any]] = Field(
        description="Configuration for the language model",
        default=None,
    )
    text_embedder: Optional[str] = Field(
        description="Configuration for the text embedding model"
    )
    text_embedder_config: Optional[Dict[str,Any]] = Field(
        description="Configuration for the language model",
        default=None,
    )
    multimodal_embedder: Optional[str] = Field(
        description="Configuration for the image embedding model",
        default=None,
    )
    multimodal_embedder_config: Optional[Dict[str,Any]] = Field(
        description="Configuration for the image embedding model",
        default=None,
    )
    history_db_path: Optional[str] = Field(
        description="Path to the history database",
        default=os.path.join(lightmem_dir, "history.db"),
    )
    graph_store: Optional[Dict[str,Any]] = Field(
        description="Configuration for the graph",
        default=None,
    )
    t2p_path: Optional[str] = Field(
        description="Local path for the text2lora model",
        default=None,
    )
    t2p_config: Optional[Dict[str,Any]] = Field(
        description="Configuration for the text2lora model",
        default=None,
    )
    version: Optional[str] = Field(
        description="The version of the API",
        default="v1.1",
    )
    is_extraction_system_prompt: Optional[str] = Field(
        description="Custom prompt for the text fact extraction",
        default=None,
    )
    text_fact_extraction_prompt: Optional[str] = Field(
        description="Custom prompt for the text fact extraction",
        default=None,
    )
    multimodal_fact_extraction_prompt: Optional[str] = Field(
        description="Custom prompt for the image fact extraction",
        default=None,
    )
    custom_update_memory_prompt: Optional[str] = Field(
        description="Custom prompt for the update memory",
        default=None,
    )

    
    # 验证提供商的支持程度，为用户没有指定的可选字段提前设置默认值