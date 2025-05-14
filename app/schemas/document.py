from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.document import ProcessingStatus

class DocumentBase(BaseModel):
    original_filename: str
    mime_type: str
    file_size: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    stored_filename: str
    output_filename: Optional[str] = None
    status: ProcessingStatus
    error_message: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 