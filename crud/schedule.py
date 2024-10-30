import datetime

from crud.base import CRUDBase
from database_app.models import Schedule

from schemas.schedule import ScheduleCreate, ScheduleUpdate


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    pass


crud_schedule = CRUDSchedule(Schedule)
