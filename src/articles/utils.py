from decouple import config
from fastapi import HTTPException
import httpx

async def verify_recaptcha(g_recaptcha_response: str):
    recaptcha_secret_key = config("CAPTCHA_SECRET_KEY")
    verify_url = f"https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': recaptcha_secret_key,
        'response': g_recaptcha_response,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(verify_url, data=params)

    data = response.json()

    if data["success"] == True:
        raise HTTPException(status_code=400, detail="reCAPTCHA verification failed")