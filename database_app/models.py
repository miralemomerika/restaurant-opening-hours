from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Time,
)
from sqlalchemy.orm import relationship

from database_app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String)
    working_hours = Column(String)

    schedules = relationship("Schedule", cascade="all, delete-orphan")


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    days = Column(String)
    opening_time = Column(Time)
    closing_time = Column(Time)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete='CASCADE'))
    restaurant = relationship('Restaurant', back_populates='schedules')

    @staticmethod
    def days_list_to_string(days_list):
        return ','.join(days_list)

    @staticmethod
    def days_string_to_list(days_str):
        return days_str.split(',')


