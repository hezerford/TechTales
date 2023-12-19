from datetime import datetime
import logging
from src.mailing.utils import send_email, get_latest_article
from src.mailing.celery import celery_app
from src.database import subscribers_collection

logger = logging.getLogger(__name__)

from datetime import datetime
import logging
from src.mailing.utils import send_email, get_latest_article
from src.mailing.celery import celery_app
from src.database import subscribers_collection

logger = logging.getLogger(__name__)

@celery_app.task
async def send_subscription_notification_task(subscriber_email):
    try:
        latest_article = await get_latest_article()  
        
        if latest_article:
            subject = f"Новая статья в блоге: {latest_article.title}"
            message = f"Привет!\n\n{latest_article.title} была опубликована в блоге. Проверьте её по ссылке: {latest_article.url}"
            await send_email(subscriber_email, subject, message)
    except Exception as e:
        logger.exception(f"Error sending subscription notification: {e}")

@celery_app.task
async def save_subscriber_task(subscriber_data):
    try:
        # Сохранение подписчика в базе данных
        subscriber_dict = dict(subscriber_data)
        subscriber_dict['subscribed_at'] = datetime.utcnow()
        subscribers_collection.insert_one(subscriber_dict)
    except Exception as e:
        print(f"Error saving subscriber: {e}")