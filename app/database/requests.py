from app.database.models import User, MoonPhase
from app.database.models import async_session
from sqlalchemy import select, update, delete

async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            user = User(tg_id=tg_id, username=username)
            session.add(user)
            # session.add(User(tg_id=tg_id), username=username)
            await session.commit()


async def get_moonPhase_by_id(phase_id: int):
    async with async_session() as session:
        phase = await session.scalar(select(MoonPhase).where(MoonPhase.id == phase_id))
        return phase

async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users