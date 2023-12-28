# from datetime import datetime
# from src.mailing.utils import send_email, get_latest_article
# from src.mailing.celery import celery_app
# from src.database import subscribers_collection

# import logging
# from src.mailing.utils import send_email, get_latest_article
# from src.mailing.celery import celery_app
# from src.database import subscribers_collection
# from src.mailing.models import SubscriberModel

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# @celery_app.task
# async def send_subscription_notification_task(subscriber_email):
#     try:
#         latest_article = await get_latest_article()
        
#         if latest_article:
#             subject = f"Новая статья в блоге: {latest_article.title}"
#             message = f"Привет!\n\n{latest_article.title} была опубликована в блоге. Проверьте её по ссылке: {latest_article.url}"
#             await send_email(subscriber_email, subject, message)
#     except Exception as e:
#         logger.exception(f"Error sending subscription notification: {e}")

# @celery_app.task
# async def save_subscriber_task(email):
#     try:
#         # Сохранение подписчика в базе данных
#         subscriber_data = {"email": email, "subscribed_at": datetime}
#         result = subscribers_collection.insert_one(subscriber_data)
#     except Exception as e:
#         logger.exception(f"Error saving subscriber: {e}")
#         raise