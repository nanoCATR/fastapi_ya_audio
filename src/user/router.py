from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, delete, update

from models.models import user, audio
from user.schemas import User, UserEdit
from audio.schemas import Audio


router = APIRouter()

@router.get("/", summary="Возвращает всех пользователей", response_model=list[User])
async def get_user(session : AsyncSession = Depends(get_async_session)):
    query = select(user)
    result = await session.execute(query)
    return result.all()

@router.get("/{id}", summary="Возвращает пользователя с указанным id", response_model=list[User])
async def get_user_by_id(id: int, session : AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.id == id)
    result = await session.execute(query)
    return result.all()

@router.get("/audio/{id}", summary="Возвращает аудио пользователя с указанным id", response_model=list[Audio])
async def get_user_audio_by_id(id: int, session : AsyncSession = Depends(get_async_session)):
    query = select(audio).where(audio.c.user_owner == id)
    result = await session.execute(query)
    return result.all()


@router.put("/{id}", summary="Изменение информации о пользователе с указанным id")
async def get_user_by_id(id: int, data: UserEdit, session : AsyncSession = Depends(get_async_session)):
    query = update(user).where(user.c.id == id).values(**data.model_dump())
    await session.execute(query)
    await session.commit()
    return {"status": "success"}

@router.delete("/{id}", summary="Удаляет пользователя по id")
async def delete_user(id: int, session : AsyncSession = Depends(get_async_session)):
    query = delete(user).where(user.c.id == id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}