import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_session, engine
from app.db.base import Base
from sqlalchemy.orm import sessionmaker

# Setup test DB
TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
