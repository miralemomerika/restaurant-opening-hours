# Restaurant Opening Hours API

## Versions Used
- Python 3.12

This application is an API that allows users to find which restaurants are open 
at a given date and time. It parses a CSV file containing restaurant names and 
their human-readable opening hours, stores the data in a database, and provides 
an endpoint to retrieve open restaurants based on a datetime string.

### Features
- Parses human-readable opening hours from a CSV file.
- Stores restaurant data in a relational database.
- Provides an API endpoint to retrieve open restaurants based on a datetime string.

### Getting Started
1. Clone the repository.
```bash
1. git clone git@github.com:miralemomerika/restaurant-opening-hours.git
2. cd restaurant-opening-hours
```
2. Build and Run with Docker Compose
```bash
1. docker-compose up --build
```
3. Once the services are up, try to access the API at `http://localhost:8015/docs`

### Running Tests Locally
1. You need to install dependencies first.
```bash
pip install -r requirements.txt
```
2. Set Up the Database
- Ensure that you have a PostgreSQL database running.

3. Run the tests.
```bash
pytest tests/tests.py
```