import datetime

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from database_app.models import Restaurant, Schedule

from schemas.restaurant import RestaurantCreate, RestaurantUpdate


class CRUDRestaurant(CRUDBase[Restaurant, RestaurantCreate, RestaurantUpdate]):

    def get_by_opening_hours(self, db: Session, opening_hours: datetime):
        check_day = opening_hours.strftime('%A')  # Get the day of the week
        check_time = opening_hours.time()

        query = db.query(self.model).join(self.model.schedules).filter(
            # Check if the day is in the Schedule.days string
            or_(
                Schedule.days == check_day,
                Schedule.days.like(f'{check_day},%'),
                Schedule.days.like(f'%,{check_day},%'),
                Schedule.days.like(f'%,{check_day}')
            ),
            or_(
                # Case where closing_time > opening_time (normal hours)
                and_(
                    Schedule.closing_time > Schedule.opening_time,
                    Schedule.opening_time <= check_time,
                    check_time <= Schedule.closing_time
                ),
                # Case where closing_time <= opening_time (overnight hours)
                and_(
                    Schedule.closing_time <= Schedule.opening_time,
                    or_(
                        check_time >= Schedule.opening_time,
                        check_time <= Schedule.closing_time
                    )
                )
            )
        )

        return query.all()


crud_restaurant = CRUDRestaurant(Restaurant)
