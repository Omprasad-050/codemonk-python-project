from celery import Celery
from app.config import REDIS_URL

celery_app = Celery("tasks", broker=REDIS_URL)

@celery_app.task
def process_text(paragraph_id):
    # Add heavy text processing logic here
    pass
