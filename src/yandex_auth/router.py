from fastapi import APIRouter, Depends, Response, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, update, delete
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ.get("YANDEX_CLIENT_ID")
secret_id = os.environ.get("YANDEX_CLIENT_SECRET")


from models.models import InsuranceRate

router = APIRouter()

@router.post("/get_token", summary="Получение токена yandexID", description="Перейдите на https://oauth.yandex.ru/authorize?response_type=code&client_id=11fe71c861384ddd9061e672c2935ffb, выберите аккаунт, скопируйте код.")
async def post_auth_token(code: str, response: Response, session : AsyncSession = Depends(get_async_session)):
    req_post = requests.post("https://oauth.yandex.ru/token", data={'grant_type': 'authorization_code', 'code': code, 'client_id': client_id, 'client_secret': secret_id})
    data = json.loads(req_post.text)
    token = data['access_token']
    response.set_cookie(key="yandex_token", value=token)
    return {"status": "success"}

async def get_token_cookie(request: Request):
    token = request.cookies.get("yandex_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

@router.get("/", summary="Получить информацию о пользователе")
async def post_addrate(token_cookie: str = Depends(get_token_cookie)):
    req = requests.get("https://login.yandex.ru/info?", headers={"Authorization":f"OAuth {token_cookie}"}, data={"format": "json"})
    user = json.loads(req.text)
    return user

@router.get("/delete_token", summary="Удалить токен")
async def post_addrate(response: Response, session : AsyncSession = Depends(get_async_session)):
    response.delete_cookie(key="yandex_token")
    return {"status": "success"}

