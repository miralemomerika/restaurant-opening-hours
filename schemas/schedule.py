from pydantic import BaseModel
from datetime import time


class ScheduleBase(BaseModel):
    days: str
    opening_time: time
    closing_time: time


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {
            time: lambda v: v.isoformat()
        }
