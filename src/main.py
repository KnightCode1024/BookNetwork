import uvicorn
from sqladmin import Admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware 

from core.config import config
from routers.auth_router import router as auth_router
from routers.author_router import router as author_router
from core.database import engine
from admin import (
    UserAdmin, 
    AuthorAdmin, 
    BookAdmin, 
    GenreAdmin, 
    ReviewAdmin, 
    AdminAuth,
)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=config.app.SECRET_KEY)
authentication_backend = AdminAuth(secret_key=config.app.SECRET_KEY)

admin = Admin(
    app, 
    engine,
    authentication_backend=authentication_backend, 
    title="Админка Переплёта",
    base_url="/admin",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


routers = [
    auth_router, 
    author_router,
    ]

tables = [
    UserAdmin, 
    AuthorAdmin, 
    BookAdmin, 
    GenreAdmin, 
    ReviewAdmin,
]

for table in tables:
    admin.add_view(table)

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