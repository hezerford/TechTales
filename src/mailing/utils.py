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
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Обеспечение шифрования
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