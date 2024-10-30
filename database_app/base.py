# Import all the models, so that Base has them before being
# imported by Alembic
from database_app.database import Base  # noqa
from database_app.models import *  # noqa