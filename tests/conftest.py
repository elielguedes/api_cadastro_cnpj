import pytest
from app.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables before the test session and drop them after.

    This ensures tests run against a schema created from the current models
    even if alembic migrations or previous runs left the DB in a different state.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Ensure tables exist at import time so modules that create TestClient(app)
# won't fail due to missing tables during import-time side-effects.
try:
    # import models so they are registered on Base.metadata
    import app.models.models  # noqa: F401 - side-effect: registers tables
    Base.metadata.create_all(bind=engine)
except Exception:
    # If engine isn't configured yet or another race, let the fixture handle it.
    pass
