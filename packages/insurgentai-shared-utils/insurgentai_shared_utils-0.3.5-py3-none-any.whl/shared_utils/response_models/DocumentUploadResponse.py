from uuid import UUID
from pydantic import BaseModel, Field

class DocumentUploadResponse(BaseModel):
    """
    Response model for the document upload operation.
    """
    document_id: UUID = Field(..., description="The id of the document.")
