from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repository import UserRepository
from utils.auth_utils import validate_password, hash_password, encode_jwt

class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None

        if not validate_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user

    async def login_user(self, username: str, password: str):
        user = await self.authenticate_user(username, password)
        if not user:
            return None
        
        jwt_payload = {
            "sub": user.username,
            "email": user.email,
            "user_id": user.id,
        }

        token = encode_jwt(jwt_payload)
        return token