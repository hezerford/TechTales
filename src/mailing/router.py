from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.mailing.tasks import save_subscriber_task, send_subscription_notification_task

router = APIRouter(tags=["Subscribers"])
templates = Jinja2Templates(directory="src/templates")

@router.post("/subscribe", response_class=HTMLResponse)
async def subscribe(request: Request, email: str = Form(...)):
    try:
        subscriber_data = {"email": email}

        # Вызов таски для сохранения подписчика в Celery
        result = save_subscriber_task.delay(subscriber_data)

        # Ожидание завершения задачи и получение результата
        task_result = result.get()

        # Вызов таски для отправки уведомления в Celery
        await send_subscription_notification_task.delay(email)

        return templates.TemplateResponse("index.html", {"request": request, "subscriber_email": email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))