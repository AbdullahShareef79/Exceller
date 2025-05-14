from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class ProcessingStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Document(BaseModel):
    __tablename__ = "documents"

    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, nullable=False, unique=True)
    output_filename = Column(String)
    mime_type = Column(String, nullable=False)
    file_size = Column(String, nullable=False)
    status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING)
    error_message = Column(String)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document {self.original_filename} ({self.status.value})>" 