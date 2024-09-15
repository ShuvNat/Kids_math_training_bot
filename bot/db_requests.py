from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import User, Tasks


async def add_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
):

    stmt = upsert(User).values(
        {
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_=dict(
            first_name=first_name,
            last_name=last_name,
        ),
    )
    await session.execute(stmt)
    await session.commit()


async def add_or_update_task(
    session: AsyncSession,
    telegram_id: int,
    task_type: str,
    mistakes: int
):
    async with session.begin():
        stmt = select(Tasks).filter_by(user_id=telegram_id, created_at=date.today())
        result = await session.execute(stmt)

        try:
            task_record = result.scalar_one()
            current_value = getattr(task_record, task_type)
            setattr(task_record, task_type, current_value+1)
            task_record.mistakes += mistakes
            await session.commit()

        except NoResultFound:
            new_task = Tasks(
                user_id=telegram_id,
                scales_and_fruis=1 if task_type == "scales_and_fruis" else 0,
                fruit_picking=1 if task_type == "fruit_picking" else 0,
                linear_equasion=1 if task_type == "linear_equasion" else 0,
                area_and_perimeter=1 if task_type == "area_and_perimeter" else 0,
                mistakes=mistakes
            )
            session.add(new_task)
            await session.commit()


async def get_daily_results(
    session: AsyncSession,
    telegram_id: int,
):
    stmt = select(Tasks).filter_by(user_id=telegram_id, created_at=date.today())
    result = await session.execute(stmt)
    task_record = result.scalar_one_or_none()
    return task_record


async def get_weekly_results(
    session: AsyncSession,
    telegram_id: int,
):
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    stmt = (
        select(
            func.sum(Tasks.scales_and_fruis).label('scales_and_fruis'),
            func.sum(Tasks.fruit_picking).label('fruit_picking'),
            func.sum(Tasks.linear_equasion).label('linear_equasion'),
            func.sum(Tasks.area_and_perimeter).label('area_and_perimeter'),
            func.sum(Tasks.total).label('total'),
            func.sum(Tasks.mistakes).label('mistakes')
        )
        .filter(Tasks.user_id == telegram_id)
        .filter(Tasks.created_at.between(start_date, end_date))
    )
    result = await session.execute(stmt)
    task_records = result.fetchone()
    return task_records
