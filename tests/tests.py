import unittest
from datetime import time

from fastapi.testclient import TestClient

from core.utils import parse_days, parse_time, parse_times, parse_opening_hours
from main import app

from .fixtures import test_db


client = TestClient(app)


def test_get_restaurants_open_valid_datetime(test_db):
    response = client.get("api/v1/restaurants/2022-01-01T12:00:00")
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) > 0

    restaurant_names = [restaurant['restaurant_name'] for restaurant in data['data']]
    assert "Test Restaurant" in restaurant_names


def test_get_restaurants_closed_valid_datetime(test_db):
    response = client.get("api/v1/restaurants/2023-10-30 05:00")
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == "Restaurants not found"


def test_get_restaurants_invalid_datetime_format():
    response = client.get("api/v1/restaurants/invalid-datetime")
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == "Invalid opening_hours datetime format"


def test_get_restaurants_edge_case_opening_time(test_db):
    response = client.get("api/v1/restaurants/2023-10-30 09:00")
    assert response.status_code == 200
    data = response.json()
    restaurant_names = [restaurant['restaurant_name'] for restaurant in data['data']]
    assert "Test Restaurant" in restaurant_names


def test_get_restaurants_edge_case_closing_time(test_db):
    response = client.get("api/v1/restaurants/2023-10-30 17:00")
    assert response.status_code == 200
    data = response.json()
    restaurant_names = [restaurant['restaurant_name'] for restaurant in data['data']]
    assert "Test Restaurant" in restaurant_names


def test_get_restaurants_edge_case_after_closing(test_db):
    response = client.get("api/v1/restaurants/2023-10-30 17:01")
    assert response.status_code == 200
    data = response.json()
    restaurant_names = [restaurant['restaurant_name'] for restaurant in data['data']]
    assert "Test Restaurant" not in restaurant_names


class TestUtils(unittest.TestCase):
    # parse_days tests
    def test_parse_days_single_day(self):
        input_str = "Mon"
        expected_output = ["Monday"]
        self.assertEqual(parse_days(input_str), expected_output)

    def test_parse_days_multiple_days(self):
        input_str = "Mon, Tue, Wed"
        expected_output = ["Monday", "Tuesday", "Wednesday"]
        self.assertEqual(parse_days(input_str), expected_output)

    def test_parse_days_day_range(self):
        input_str = "Mon-Fri"
        expected_output = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.assertEqual(parse_days(input_str), expected_output)

    def test_parse_days_day_range_with_commas(self):
        input_str = "Mon, Wed-Fri, Sun"
        expected_output = ["Monday", "Wednesday", "Thursday", "Friday", "Sunday"]
        self.assertEqual(parse_days(input_str), expected_output)

    def test_parse_days_invalid_day(self):
        input_str = "Funday"
        expected_output = []
        self.assertEqual(parse_days(input_str), expected_output)

    def test_parse_days_range_with_invalid_day(self):
        input_str = "Mon-Funday"
        expected_output = []
        self.assertEqual(parse_days(input_str), expected_output)

    # parse_time tests
    def test_parse_time_standard_format(self):
        input_str = "11:00 am"
        expected_output = time(11, 0)
        self.assertEqual(parse_time(input_str), expected_output)

    def test_parse_time_no_minutes(self):
        input_str = "5 pm"
        expected_output = time(17, 0)
        self.assertEqual(parse_time(input_str), expected_output)

    def test_parse_time_with_minutes(self):
        input_str = "3:30 pm"
        expected_output = time(15, 30)
        self.assertEqual(parse_time(input_str), expected_output)

    def test_parse_time_24_hour_format(self):
        input_str = "23:15"
        expected_output = time(23, 15)
        self.assertEqual(parse_time(input_str), expected_output)

    def test_parse_time_invalid_format(self):
        input_str = "25:00 pm"
        with self.assertRaises(ValueError):
            parse_time(input_str)

    # parse_times tests
    def test_parse_times_standard(self):
        input_str = "11:00 am - 10 pm"
        expected_output = (time(11, 0), time(22, 0))
        self.assertEqual(parse_times(input_str), expected_output)

    def test_parse_times_with_minutes(self):
        input_str = "9:30 am - 5:45 pm"
        expected_output = (time(9, 30), time(17, 45))
        self.assertEqual(parse_times(input_str), expected_output)

    def test_parse_times_invalid_time(self):
        input_str = "9:00 am - 25:00 pm"
        with self.assertRaises(ValueError):
            parse_times(input_str)

    # parse_opening_hours tests
    def test_parse_opening_hours_simple(self):
        input_str = "Mon-Fri 9 am - 5 pm"
        expected_output = [{
            'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'opening_time': time(9, 0),
            'closing_time': time(17, 0),
        }]
        self.assertEqual(parse_opening_hours(input_str), expected_output)

    def test_parse_opening_hours_multiple_periods(self):
        input_str = "Mon-Fri 9 am - 5 pm / Sat-Sun 10 am - 4 pm"
        expected_output = [
            {
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opening_time': time(9, 0),
                'closing_time': time(17, 0),
            },
            {
                'days': ['Saturday', 'Sunday'],
                'opening_time': time(10, 0),
                'closing_time': time(16, 0),
            }
        ]
        self.assertEqual(parse_opening_hours(input_str), expected_output)

    def test_parse_opening_hours_with_commas_and_ranges(self):
        input_str = "Mon, Wed-Fri 10 am - 6 pm / Sun 12 pm - 8 pm"
        expected_output = [
            {
                'days': ['Monday', 'Wednesday', 'Thursday', 'Friday'],
                'opening_time': time(10, 0),
                'closing_time': time(18, 0),
            },
            {
                'days': ['Sunday'],
                'opening_time': time(12, 0),
                'closing_time': time(20, 0),
            }
        ]
        self.assertEqual(parse_opening_hours(input_str), expected_output)

    def test_parse_opening_hours_invalid_input(self):
        input_str = "Invalid data"
        expected_output = []
        self.assertEqual(parse_opening_hours(input_str), expected_output)

    def test_parse_opening_hours_with_overlapping_times(self):
        input_str = "Mon-Fri 9 am - 5 pm / Mon-Fri 6 pm - 10 pm"
        expected_output = [
            {
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opening_time': time(9, 0),
                'closing_time': time(17, 0),
            },
            {
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opening_time': time(18, 0),
                'closing_time': time(22, 0),
            }
        ]
        self.assertEqual(parse_opening_hours(input_str), expected_output)

    def test_parse_opening_hours_with_different_day_formats(self):
        input_str = "Tues-Thur 9 am - 5 pm"
        expected_output = [{
            'days': ['Tuesday', 'Wednesday', 'Thursday'],
            'opening_time': time(9, 0),
            'closing_time': time(17, 0),
        }]
        self.assertEqual(parse_opening_hours(input_str), expected_output)

    def test_parse_opening_hours_with_wrap_around_days(self):
        input_str = "Fri-Mon 10 am - 2 am"
        expected_output = [{
            'days': ['Friday', 'Saturday', 'Sunday', 'Monday'],
            'opening_time': time(10, 0),
            'closing_time': time(2, 0),
        }]
        self.assertEqual(parse_opening_hours(input_str), expected_output)
