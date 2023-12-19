from email.message import EmailMessage
import smtplib
from src.articles.models import ArticleModel
from datetime import datetime
from decouple import config
from src.database import blog_collection

from email.message import EmailMessage
import smtplib
from src.articles.models import ArticleModel
from datetime import datetime
from decouple import config
from src.database import blog_collection

async def send_email(to_email, subject, message):
    smtp_server = config('SMTP_SERVER')
    smtp_port = config('SMTP_PORT')
    smtp_username = config('SMTP_USERNAME')
    smtp_password = config('SMTP_PASSWORD')
    sender_email = config('SENDER_EMAIL')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, [to_email], msg=message)
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

async def get_latest_article():
    latest_article = await blog_collection.find_one(
        {},  # Пустой фильтр выбирает все записи
        sort=[("publication_date", -1)]  # Сортировка по дате публикации в обратном порядке (-1)
    )

    if latest_article:
        return ArticleModel(**latest_article)
    else:
        return None

async def save_subscriber(subscriber):
    subscriber_dict = dict(subscriber)
    subscriber_dict['subscribed_at'] = datetime.utcnow()

    # Отложенный импорт
    from src.mailing.tasks import save_subscriber_task

    # Запуск задачи асинхронно
    result = await save_subscriber_task.delay(subscriber_dict)

    # Ожидание завершения задачи и получение результата
    task_result = await result.get()

    return task_result