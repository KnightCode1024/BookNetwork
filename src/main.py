from fastapi import FastAPI
import uvicorn

from core.config import config
from routers.auth_router import router as auth_router

app = FastAPI()

@app.get("/")
def index():
    return {"message": "ok"}


app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=config.app.HOST, 
        port=config.app.PORT, 
        log_level=config.app.get_log_level, 
        reload=True,
        )