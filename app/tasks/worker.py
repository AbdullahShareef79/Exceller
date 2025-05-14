from app.core.celery_app import celery_app
from .document_processing import process_document

# Register tasks
celery_app.tasks.register(process_document)

if __name__ == '__main__':
    celery_app.start() 