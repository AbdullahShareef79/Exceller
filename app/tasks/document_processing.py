import os
from celery import Task
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.document import Document, ProcessingStatus
from app.services.document_processor import DocumentProcessor
import logging

logger = logging.getLogger(__name__)

class DocumentProcessingTask(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, *args, **kwargs):
        if self._db is not None:
            self._db.close()
            self._db = None

@celery_app.task(bind=True, base=DocumentProcessingTask)
def process_document(self, document_id: int) -> dict:
    """Process a document and convert it to Excel format."""
    try:
        # Get document from database
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")

        # Update status to processing
        document.status = ProcessingStatus.PROCESSING
        self.db.commit()

        # Initialize document processor
        processor = DocumentProcessor()
        
        # Process document
        output_path = processor.process(
            input_path=os.path.join("uploads", document.stored_filename)
        )

        # Update document status
        document.status = ProcessingStatus.COMPLETED
        document.output_filename = os.path.basename(output_path)
        self.db.commit()

        return {
            "status": "success",
            "document_id": document_id,
            "output_path": output_path
        }

    except Exception as e:
        logger.exception(f"Error processing document {document_id}")
        
        # Update document status to failed
        document.status = ProcessingStatus.FAILED
        document.error_message = str(e)
        self.db.commit()

        return {
            "status": "error",
            "document_id": document_id,
            "error": str(e)
        } 