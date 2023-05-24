import pytest

from app.db.connection import Base
from app.db.testing_connection import engine


@pytest.fixture
def db_engine():
    Base.metadata.create_all(bind=engine)


from app.tests.fixtures.comuna import comunas
