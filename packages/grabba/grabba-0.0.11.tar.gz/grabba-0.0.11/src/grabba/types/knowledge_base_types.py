from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class KnowledgeBase(BaseModel):
    id: str = Field(..., alias='_id')
    user_id: str = Field(..., alias='userId')
    name: str
    description: Optional[str] = None
    size_in_bytes: int = Field(..., alias='sizeInBytes')
    max_size_in_bytes: int = Field(..., alias='maxSizeInBytes')
    created_at: str = Field(..., alias='createdAt')

class ContextResult(BaseModel):
    id: str = Field(..., alias='_id')
    kb_id: str = Field(..., alias='kbId')
    source: str
    source_type: str = Field(..., alias='sourceType')
    chunk_index: int = Field(..., alias='chunkIndex')
    content: str
    metadata: Dict
    created_at: str = Field(..., alias='createdAt')

class CreateKnowledgeBaseResponse(BaseModel):
    message: str
    knowledge_base: KnowledgeBase = Field(..., alias='knowledgeBase')

class GetKnowledgeBasesResponse(BaseModel):
    message: str
    knowledge_bases: List[KnowledgeBase] = Field(..., alias='knowledgeBases')

class GetKnowledgeBaseResponse(BaseModel):
    message: str
    knowledge_base: KnowledgeBase = Field(..., alias='knowledgeBase')

class StoreContextResponse(BaseModel):
    message: str
    context_ids: List[str] = Field(..., alias='contextIds')

class FetchContextResponse(BaseModel):
    message: str
    results: List[ContextResult]

class UpdateContextResponse(BaseModel):
    message: str
    context: ContextResult

class GatherContextResponse(BaseModel):
    message: str
    metadata: Dict
