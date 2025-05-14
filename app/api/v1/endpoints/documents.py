import os
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.document import Document, ProcessingStatus
from app.schemas.document import DocumentCreate, DocumentResponse
from app.tasks.document_processing import process_document
import uuid

router = APIRouter()

def save_upload_file(upload_file: UploadFile) -> str:
    """Save an uploaded file and return its stored filename."""
    ext = os.path.splitext(upload_file.filename)[1]
    stored_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(settings.UPLOAD_FOLDER, stored_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    
    return stored_filename

@router.post("/", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> DocumentResponse:
    """
    Upload a document for processing.
    """
    if not file.filename.endswith(".docx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .docx files are supported"
        )
    
    # Save the uploaded file
    stored_filename = save_upload_file(file)
    
    # Create document record
    document = Document(
        original_filename=file.filename,
        stored_filename=stored_filename,
        mime_type=file.content_type,
        file_size=str(file.size),
        status=ProcessingStatus.PENDING
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Start processing task
    process_document.delay(document.id)
    
    return document

@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[DocumentResponse]:
    """
    List all documents.
    """
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
) -> DocumentResponse:
    """
    Get a specific document by ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document

@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Download the processed Excel file.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
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