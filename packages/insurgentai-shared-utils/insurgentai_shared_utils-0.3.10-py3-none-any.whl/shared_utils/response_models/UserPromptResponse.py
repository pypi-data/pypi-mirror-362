from uuid import UUID
from ..sql_models.Graph import ChunkGraph
from typing import List
from pydantic import BaseModel, Field


class Reference(BaseModel):
    """
    Represents a reference in the user prompt response.
    """
    statement: str = Field(..., description="A statement related to the prompt.")
    chunk_id: UUID = Field(..., description="Unique identifier for the chunk.")
    subgraph: ChunkGraph = Field(..., description="Graph associated with the chunk.")
    page_number: int = Field(..., description="Page number the chunk is from.")


class UserPromptResponse(BaseModel):
    """
    Response model for user prompt operations.
    """
    response: str = Field(..., description="The response generated based on the user's prompt.")
    references: List[Reference] = Field(default_factory=list, description="List of references related to the response.")