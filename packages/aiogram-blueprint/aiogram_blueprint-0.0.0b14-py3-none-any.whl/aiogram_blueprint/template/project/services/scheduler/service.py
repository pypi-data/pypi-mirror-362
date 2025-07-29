from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..abstract import AbstractService
from ...config import TIMEZONE, SCHEDULER_URL


class SchedulerService(AbstractService):
    __slots__ = ["scheduler"]

    def __init__(self) -> None:
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone=TIMEZONE)

    async def start(self) -> None:
        self.scheduler.add_jobstore(SQLAlchemyJobStore(SCHEDULER_URL))
        self.scheduler.start()

    async def shutdown(self) -> None:
        self.scheduler.shutdown(wait=False)
