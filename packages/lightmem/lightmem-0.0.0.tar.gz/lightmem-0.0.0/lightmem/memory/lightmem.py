from typing import Any, Dict, Optional
from ..pre_settings.base import MemorySettings
from pydantic import ValidationError
from ..pre_settings.vector_stores.factory import VectorStoreFactory
from ..pre_settings.llms.factory import LlmFactory
from ..pre_settings.text_embedder.factory import TextEmbedderFactory
# from ..pre_settings.multimodal_embedder.factory import MultimodalEmbedderFactory
# from ..pre_settings.graph_stores.factory import GraphStoreFactory

class LightMemory:
    def __init__(self, config: MemorySettings = MemorySettings()):
        
        """

        Initialize a LightMemory instance.

        This constructor initializes various memory-related components based on the provided configuration (`config`), 
        including the vector store, large language model (LLM), text embedder, optional multimodal embedder, 
        optional graph store, and optional text-to-parameter (t2p) model. 
        This design supports flexible extension of the memory system, making it easy to integrate 
        different storage and reasoning capabilities.

        Args:
            config (MemorySettings): The configuration object for the memory system, 
                containing initialization parameters for all submodules.

        Components initialized:
            - vector_store: Vector database for memory storage and retrieval
            - llm: Large language model for reasoning and generation
            - text_embedder: Text embedding model
            - multimodal_embedder (optional): Multimodal embedding model
            - graph (optional): Graph memory store
            - paramem (optional): Text-to-parameter model

        """
        self.config = config
        self.vector_store = VectorStoreFactory.instantiate(self.config.vector_store_db, self.config.vector_store_config)
        self.llm = LlmFactory.instantiate(self.config.llm, self.config.llm_config)
        self.text_embedder = TextEmbedderFactory.instantiate(self.config.text_embedder,self.config.text_embedder_config)
        if self.config.multimodal_embedder:
            self.multimodal_embedder = MultimodalEmbedderFactory.instantiate(self.config.multimodal_embedder,self.config.multimodal_embedder_config)
        if self.config.graph_store:
            from .graph import GraphMem
            self.graph = GraphMem(self.config.graph_store)
        else:
            self.graph = None
        if self.config.t2p_path:
            from .t2p import ParaMem
            self.paramem = ParaMem(self.config.t2p_path,self.config.t2p_config)
        else:
            self.paramem = None
    
    @classmethod
    def from_config(cls, config: Dict[str,Any]):
        try:
            settings = MemorySettings(**config)
        except ValidationError as e:
            print(f"Configuration validation error: {e}")
            raise
        return cls(settings)
    
    def add(
        self,
        messages,
        *,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        infer: bool = True,
        memory_type: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        """
        Create a new memory.

        Adds new memories scoped to a single session id (e.g. `user_id`, `agent_id`, or `run_id`). One of those ids is required.

        Args:
            messages (str or List[Dict[str, str]]): The message content or list of messages
                (e.g., `[{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]`)
                to be processed and stored.
            user_id (str, optional): ID of the user creating the memory. Defaults to None.
            agent_id (str, optional): ID of the agent creating the memory. Defaults to None.
            run_id (str, optional): ID of the run creating the memory. Defaults to None.
            metadata (dict, optional): Metadata to store with the memory. Defaults to None.
            infer (bool, optional): If True (default), an LLM is used to extract key facts from
                'messages' and decide whether to add, update, or delete related memories.
                If False, 'messages' are added as raw memories directly.
            memory_type (str, optional): Specifies the type of memory. Currently, only
                `MemoryType.PROCEDURAL.value` ("procedural_memory") is explicitly handled for
                creating procedural memories (typically requires 'agent_id'). Otherwise, memories
                are treated as general conversational/factual memories.memory_type (str, optional): Type of memory to create. Defaults to None. By default, it creates the short term memories and long term (semantic and episodic) memories. Pass "procedural_memory" to create procedural memories.
            prompt (str, optional): Prompt to use for the memory creation. Defaults to None.


        Returns:
            dict: A dictionary containing the result of the memory addition operation, typically
                  including a list of memory items affected (added, updated) under a "results" key,
                  and potentially "relations" if graph store is enabled.
                  Example for v1.1+: `{"results": [{"id": "...", "memory": "...", "event": "ADD"}]}`
        """
        
        # 先is_extraction_system_prompt调用大模型判断是否需要调用后面的事实提取，gate

        # 需要就调大模型进行summarize、extract
        old_memories_vector = self.vector_search(messages)

        if self.graph:
            old_memories_graph = self.graph_search(messages)
        
        # 将old memory的文本与new_memory组织到一起，调用大模型进行比较看看调用什么函数
        event = self.llm.generate_response(
            old_memories_vector,
            old_memories_graph
        )

        if event == 'add':
            states = self.add_to_vector(extracted_messages)
            if self.config.t2l_path:
                states = self.add_to_paramem(extracted_messages)
            if self.graph:
                states = self.add_to_graph(extracted_graph)
        
        if event == 'update':
            

    async def add_to_vector(self, massages):
        pass

    async def add_to_graph(self, messages):
        pass

    async def add_to_paramem(self, massages):
        pass

    async def vector_search(self, messages):
        pass

    async def graph_search(self,messages):
        pass

    def search(self,query,user_id):
        pass

    def update(self,messages):
        pass

    def delete(self,messages):
        pass

