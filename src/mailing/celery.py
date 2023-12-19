from celery import Celery
from decouple import config

celery_app = Celery(
    'tasks',
    broker=config("CELERY_BROKER"),
    backend=config("CELERY_RESULT_BACKEND"),
    include=["src.mailing.tasks"],
)