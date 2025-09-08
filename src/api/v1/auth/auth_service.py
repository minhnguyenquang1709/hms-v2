from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.auth import User


class AuthService:
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()
