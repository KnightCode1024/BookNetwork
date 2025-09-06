from typing import Optional

from db.models.user import User
from db.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_or_update_user(
        self,
        tg_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ):
        user = await self.user_repository.get_by_tg_id(tg_id)

        if not user:
            new_user = User(
                tg_id=tg_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            user = await self.user_repository.add(new_user)
            return {"action": "created", "user": user}

        needs_update = False
        update_data = {}

        if username is not None and user.username != username:
            update_data["username"] = username
            needs_update = True

        if first_name is not None and user.first_name != first_name:
            update_data["first_name"] = first_name
            needs_update = True

        if last_name is not None and user.last_name != last_name:
            update_data["last_name"] = last_name
            needs_update = True

        if needs_update:
            updated_user = await self.user_repository.update(
                user.id,
                **update_data,
            )
            return {"action": "updated", "user": updated_user}

        return {"action": "skipped", "user": user}


# user_repo = UserRepository(UserRepository)
# user_service = UserService(user_repo)
