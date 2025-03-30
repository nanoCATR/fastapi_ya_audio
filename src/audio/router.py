from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, update, delete

from models.models import audio
from audio.schemas import Audio

router = APIRouter()


@router.post("/", summary="Добавить аудио", description="Добавить аудио.")
async def post_addaudio(request: Request, name: str, file: UploadFile = File(...), session : AsyncSession = Depends(get_async_session)):
    user_owner = request.cookies.get("user_id")
    if user_owner:
        file_types = ['audio/ogg', 'audio/mpeg']
        if file.content_type in file_types:
            file_folder = "/files"
            location = f"{file_folder}/{name}.{file.content_type.split('/')[-1]}"

            os.makedirs(file_folder, exist_ok=True)
            with open(location, 'wb') as buffer:
                buffer.write(await file.read())

            data = {'filename':name, 'location':location, 'user_owner':int(user_owner)}
            query = insert(audio).values(data)
            await session.execute(query)
            await session.commit()
            return {"status": "success"}
        else:
            return {"detail": "wrong audio format"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/", summary="Вывести аудио текущего пользователя", response_model=list[Audio])
async def get_my_audio(request: Request, session : AsyncSession = Depends(get_async_session)):
    user_id = request.cookies.get("user_id")
    if user_id:
        query = select(audio).where(audio.c.user_owner == int(user_id))
        result = await session.execute(query)
        return result.all()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
   