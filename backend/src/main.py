import uvicorn
from sqladmin import Admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from core.config import config
from routers import auth_router, author_router, genre_router
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
    genre_router,
]

admin_tables = [
    UserAdmin,
    AuthorAdmin,
    BookAdmin,
    GenreAdmin,
    ReviewAdmin,
]

for table in admin_tables:
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
