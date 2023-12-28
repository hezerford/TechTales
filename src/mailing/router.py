from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Subscribers"])
templates = Jinja2Templates(directory="src/templates")

@router.post("/subscribe", response_class=HTMLResponse)
async def subscribe(request: Request, email: str = Form(...)):
    try:
        # Вызываем задачу Celery для сохранения подписчика
        # save_subscriber_task.delay(email)

        # Перенаправляем пользователя на главную страницу
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))