import pytest
from api.deps import get_db
from database_app.models import Restaurant, Schedule
from datetime import time


@pytest.fixture(scope='module')
def test_db():
    db_generator = get_db()
    db = next(db_generator)

    try:
        restaurant = Restaurant(
            restaurant_name="Test Restaurant",
        )
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)

        schedule = Schedule(
            restaurant_id=restaurant.id,
            days="Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday",
            opening_time=time(9, 0),
            closing_time=time(17, 0)
        )
        db.add(schedule)
        db.commit()

        yield db
    finally:
        # clean up the database
        db.query(Schedule).filter(Schedule.restaurant_id == restaurant.id).delete()
        db.query(Restaurant).filter(Restaurant.id == restaurant.id).delete()
        db.commit()

        try:
            next(db_generator)
        except StopIteration:
            pass
