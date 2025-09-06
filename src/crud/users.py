from db.database import connection
from db.models import User


@connection
async def add_user(name: str, age: int, session):
    new_user = User(name=name, age=age)
    session.add(new_user)
    await session.commit()

    
