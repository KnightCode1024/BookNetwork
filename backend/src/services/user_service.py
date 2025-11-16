from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from email_validator import validate_email, EmailNotValidError

from models import User
from repositories.user_repository import UserRepository
from utils.auth_utils import (
    validate_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_jwt,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    def _validate_email(self, email: str) -> str:
        if not email:
            raise ValueError("Email cannot be empty")

        try:
            valid = validate_email(email, check_deliverability=False)
            return valid.email.lower()
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {str(e)}")

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None

        if not validate_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        return user

    async def login_user(
        self, username: str, password: str
    ) -> Optional[Tuple[str, str]]:
        user = await self.authenticate_user(username, password)
        if not user:
            return None

        jwt_payload = {
            "sub": user.username,
            "email": user.email,
            "user_id": user.id,
            "type": "access",
        }

        refresh_payload = {"sub": user.username, "user_id": user.id, "type": "refresh"}

        access_token = create_access_token(jwt_payload)
        refresh_token = create_refresh_token(refresh_payload)

        return access_token, refresh_token

    async def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        try:
            payload = decode_jwt(refresh_token)

            if payload.get("type") != "refresh":
                return None

            username = payload.get("sub")
            user_id = payload.get("user_id")

            if not username or not user_id:
                return None

            user = await self.user_repo.get_by_id(user_id)
            if not user or not user.is_active:
                return None

            jwt_payload = {
                "sub": user.username,
                "email": user.email,
                "user_id": user.id,
                "type": "access",
            }

            refresh_payload = {
                "sub": user.username,
                "user_id": user.id,
                "type": "refresh",
            }

            access_token = create_access_token(jwt_payload)
            refresh_token = create_refresh_token(refresh_payload)

            return access_token, refresh_token

        except Exception:
            return None

    async def create_user(self, user_data: dict) -> User:
        if user_data.get("email"):
            user_data["email"] = self._validate_email(user_data["email"])

        existing_user = await self.user_repo.get_by_username(user_data["username"])
        if existing_user:
            raise ValueError("Username already exists")

        if user_data.get("email"):
            existing_email = await self.user_repo.get_by_email(user_data["email"])
            if existing_email:
                raise ValueError("Email already exists")

        user_data["hashed_password"] = hash_password(user_data["password"])
        del user_data["password"]

        return await self.user_repo.create(user_data)

    async def verify_token(self, token: str) -> Optional[User]:
        try:
            from utils.auth_utils import decode_jwt

            payload = decode_jwt(token)

            if payload.get("type") != "access":
                return None

            user_id = payload.get("user_id")
            if not user_id:
                return None

            user = await self.user_repo.get_by_id(user_id)
            if not user or not user.is_active:
                return None

            return user

        except Exception as e:
            print(f"Token verification error: {e}")
            return None
