from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from audio import router as audio_router
from yandex_auth import router as yandex_router

load_dotenv()
app = FastAPI()

app.include_router(yandex_router.router, prefix="/yandex_auth", tags=["yandex auth"])
app.include_router(audio_router.router, prefix="/audio", tags=["audio"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5002, reload=True)