from app.db.testing_connection import TestingSessionLocal


# Dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
