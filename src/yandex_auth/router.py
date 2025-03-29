from fastapi import APIRouter, Depends, Response, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ.get("YANDEX_CLIENT_ID")
secret_id = os.environ.get("YANDEX_CLIENT_SECRET")

router = APIRouter()
from models.models import user
from user.schemas import User

@router.get("/token", summary="Получение токена yandexID", description=f"Перейдите по [адресу своего приложения](https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id}), выберите аккаунт.")
async def post_auth_token(code: str, response: Response, session : AsyncSession = Depends(get_async_session)):
    req_post = requests.post("https://oauth.yandex.ru/token", data={'grant_type': 'authorization_code', 'code': code, 'client_id': client_id, 'client_secret': secret_id})
    data = json.loads(req_post.text)
    token = data['access_token']
    response.set_cookie(key="yandex_token", value=token)
    req = requests.get("https://login.yandex.ru/info?", headers={"Authorization":f"OAuth {token}"}, data={"format": "json"}) # Получаем id пользователя для удобства
    user = User.model_validate(json.loads(req.text))
    user_id = json.loads(req.text)['id']
    response.set_cookie(key="user_id", value=user_id)
    await add_user_to_db(user, session)
    return {"status": "success"}

async def add_user_to_db(data: User, session):
    data = data.model_dump()
    query = select(user).where(user.c.id == data["id"])
    result = await session.execute(query)
    if not result.scalar():
        query = insert(user).values(data)
        await session.execute(query)
        await session.commit()

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

@router.get("/delete_token", summary="Удалить токен и id текущего пользователя")
async def post_addrate(response: Response):
    response.delete_cookie(key="yandex_token")
    response.delete_cookie(key="user_id")
    return {"status": "success"}

