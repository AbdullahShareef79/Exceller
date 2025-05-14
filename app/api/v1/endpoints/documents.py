import os
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.document import Document, ProcessingStatus
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentResponse
from app.tasks.document_processing import process_document
from app.api.v1.endpoints.auth import get_current_user
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def save_upload_file(upload_file: UploadFile) -> str:
    """Save an uploaded file and return its stored filename."""
    try:
        ext = os.path.splitext(upload_file.filename)[1]
        stored_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(settings.UPLOAD_FOLDER, stored_filename)
        
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
        
        # Read the file content
        content = upload_file.file.read()
        if not content:
            raise ValueError("File is empty")
        
        # Write the file
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        return stored_filename
    except Exception as e:
        logger.error(f"Error saving file {upload_file.filename}: {str(e)}")
        raise ValueError(f"Error saving file: {str(e)}")

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DocumentResponse:
    """
    Upload a document for processing.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
        
    if not file.filename.endswith(".docx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .docx files are supported"
        )
    
    stored_filename = None
    try:
        # Save the uploaded file
        stored_filename = save_upload_file(file)
        
        # Create document record
        document = Document(
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=file.content_type or "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            file_size=str(file.size),
            status=ProcessingStatus.PENDING,
            user_id=current_user.id
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Start processing task
        try:
            process_document.delay(document.id)
        except Exception as e:
            logger.error(f"Error queuing document {document.id} for processing: {str(e)}")
            document.status = ProcessingStatus.FAILED
            document.error_message = "Failed to queue document for processing"
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to queue document for processing"
            )
        
        return document
        
    except ValueError as e:
        if stored_filename:
            # Clean up file if it was saved
            file_path = os.path.join(settings.UPLOAD_FOLDER, stored_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        if stored_filename:
            # Clean up file if it was saved
            file_path = os.path.join(settings.UPLOAD_FOLDER, stored_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your document"
        )

@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[DocumentResponse]:
    """
    List all documents for the current user.
    """
    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DocumentResponse:
    """
    Get a specific document by ID.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document

@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Download the processed Excel file.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
        
    if document.status != ProcessingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document processing not completed. Current status: {document.status.value}"
        )
        
    file_path = os.path.join(settings.OUTPUT_FOLDER, document.output_filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Output file not found"
        )
        
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{os.path.splitext(document.original_filename)[0]}.xlsx"
    ) 