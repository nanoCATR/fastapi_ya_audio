from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, update, delete

from models.models import audio
from audio.schemas import Audio

router = APIRouter()


@router.post("/", summary="Добавить аудио", description="Добавить аудио.")
async def post_addaudio(request: Request, name: str, file: UploadFile = File(...), session : AsyncSession = Depends(get_async_session)):
    print(file)
    file_types = ['audio/ogg', 'audio/mpeg']
    if file.content_type in file_types:
        location = f"folder/{name}.{file.content_type.split('/')[-1]}"
        data = {'filename':name, 'location':location, 'user_owner':int(request.cookies.get("user_id"))}
        query = insert(audio).values(data)
        await session.execute(query)
        await session.commit()
        return {"status": "success"}
    else:
        return {"detail": "wrong audio format"}

@router.get("/", summary="Вывести аудио текущего пользователя", response_model=list[Audio])
async def get_my_audio(request: Request, session : AsyncSession = Depends(get_async_session)):
    user_id = int(request.cookies.get("user_id"))
    query = select(audio).where(audio.c.user_owner == user_id)
    result = await session.execute(query)
    return result.all()
   