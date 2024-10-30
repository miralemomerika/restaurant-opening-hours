import csv
import re
from dateutil.parser import parse

from sqlalchemy.orm import Session

from database_app.models import Restaurant, Schedule

DAY_ABBREVIATIONS = {
    'Mon': 'Monday',
    'Tue': 'Tuesday',
    'Wed': 'Wednesday',
    'Thu': 'Thursday',
    'Fri': 'Friday',
    'Sat': 'Saturday',
    'Sun': 'Sunday',
}


def read_csv_data(csv_file_path):
    restaurants = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, hours = row
            restaurants.append({
                'name': name.strip('"'),
                'hours': hours.strip()
            })
    return restaurants[1:]


def parse_days(days_str):
    days = []
    parts = [part.strip() for part in days_str.split(',')]
    for part in parts:
        # Handle ranges like 'Mon-Fri'
        if '-' in part:
            start_day, end_day = [d.strip() for d in part.split('-')]
            start_index = list(DAY_ABBREVIATIONS.keys()).index(start_day[:3])
            end_index = list(DAY_ABBREVIATIONS.keys()).index(end_day[:3])
            for i in range(start_index, end_index + 1):
                day_abbr = list(DAY_ABBREVIATIONS.keys())[i]
                days.append(DAY_ABBREVIATIONS[day_abbr])
        else:
            single_day = DAY_ABBREVIATIONS.get(part[:3])
            days.append(single_day) if single_day else None
    return days


def parse_times(times_str):
    # Split opening and closing times
    opening_str, closing_str = [t.strip() for t in times_str.split('-')]
    opening_time = parse_time(opening_str)
    closing_time = parse_time(closing_str)
    return opening_time, closing_time


def parse_time(time_str):
    time_str = time_str.strip()
    dt = parse(time_str)
    return dt.time()


def parse_opening_hours(hours_str):
    schedules = []
    parts = [part.strip() for part in hours_str.split('/')]
    for part in parts:
        # Extract days and times
        match = re.match(
            r'(.+?)\s+(\d{1,2}(:\d{2})?\s*(am|pm)?\s*-\s*\d{1,2}(:\d{2})?\s*(am|pm)?)',
            part,
            re.IGNORECASE
        )
        if not match:
            continue
        days_part, times_part = match.groups()[0], match.groups()[1]
        days = parse_days(days_part)
        opening_time, closing_time = parse_times(times_part)
        schedules.append({
            'days': days,
            'opening_time': opening_time,
            'closing_time': closing_time,
        })
    return schedules


def populate_database_with_restaurants(db: Session):
    """
    Load restaurant data at startup
    """
    restaurants_data = read_csv_data('restaurants.csv')

    for restaurant in restaurants_data:
        restaurant['schedules'] = parse_opening_hours(restaurant['hours'])

    for restaurant in restaurants_data:
        schedules = restaurant.pop('schedules')
        db_restaurant = Restaurant(
            restaurant_name=restaurant['name'],
            working_hours=restaurant['hours'],
        )
        db.add(db_restaurant)
        db.commit()
        for schedule in schedules:
            db_schedule = Schedule(
                days=Schedule.days_list_to_string(schedule['days']),
                opening_time=schedule['opening_time'],
                closing_time=schedule['closing_time'],
            )
            db_schedule.restaurant = db_restaurant
            db.add(db_schedule)

    db.commit()
