from typing import Union
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_db_session
from services.user_service import UserService
from models import MyUserRole


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        session_generator = get_db_session()
        session = await anext(session_generator)
        
        try:
            user_service = UserService(session)
            user = await user_service.authenticate_user(username, password)
            
            if user and user.role == MyUserRole.ADMIN:
                request.session.update({
                    "user_id": user.id,
                    "username": user.username,
                    "role": user.role.value
                })
                return True
            return False
        except Exception:
            return False
        finally:
            await session.close()
            try:
                await anext(session_generator)
            except StopAsyncIteration:
                pass

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Union[bool, RedirectResponse]:
        user_id = request.session.get("user_id")
        role = request.session.get("role")
        
        if not user_id or role != MyUserRole.ADMIN.value:
            return False
            
        return True