import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import config
from routers.auth_router import router as auth_router
from routers.author_router import router as author_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "ok"}


routers = [
    auth_router, 
    author_router,
    ]

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=config.app.HOST, 
        port=config.app.PORT, 
        log_level=config.app.get_log_level, 
        reload=True,
        )