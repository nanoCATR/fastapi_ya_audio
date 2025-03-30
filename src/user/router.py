from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, delete, update

from models.models import user, audio
from user.schemas import User, UserEdit
from audio.schemas import Audio


router = APIRouter()

async def get_user_role(request: Request, session : AsyncSession = Depends(get_async_session)):
    if request.cookies.get("user_id"):
        user_id = int(request.cookies.get("user_id"))
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        row = result.mappings().one()
        if row['is_admin'] == True:
            return True
        else:
            raise HTTPException(status_code=403, detail="Not an admin")
    else:
            raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/", summary="Возвращает всех пользователей", response_model=list[User])
async def get_user(session : AsyncSession = Depends(get_async_session), is_admin : None = Depends(get_user_role)):
    query = select(user)
    result = await session.execute(query)
    return result.all()

@router.get("/{id}", summary="Возвращает пользователя с указанным id", response_model=list[User])
async def get_user_by_id(id: int, session : AsyncSession = Depends(get_async_session), is_admin : None = Depends(get_user_role)):
    query = select(user).where(user.c.id == id)
    result = await session.execute(query)
    return result.all()

@router.get("/audio/{id}", summary="Возвращает аудио пользователя с указанным id", response_model=list[Audio])
async def get_user_audio_by_id(id: int, session : AsyncSession = Depends(get_async_session), is_admin : None = Depends(get_user_role)):
    query = select(audio).where(audio.c.user_owner == id)
    result = await session.execute(query)
    return result.all()


@router.put("/{id}", summary="Изменение информации о пользователе с указанным id")
async def get_user_by_id(id: int, data: UserEdit, session : AsyncSession = Depends(get_async_session), is_admin : None = Depends(get_user_role)):
    query = update(user).where(user.c.id == id).values(**data.model_dump())
    await session.execute(query)
    await session.commit()
    return {"status": "success"}

@router.delete("/{id}", summary="Удаляет пользователя по id")
async def delete_user(id: int, session : AsyncSession = Depends(get_async_session), is_admin : None = Depends(get_user_role)):
    query = delete(user).where(user.c.id == id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}