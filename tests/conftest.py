from datetime import datetime, timezone
import pytest
from blueprintapp.app import create_app, db
from blueprintapp.blueprints.api.models import Alert


@pytest.fixture
def app():
    app = create_app(config_class="config.config.TestingConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(app):
    # Create some example alerts
    alert1 = Alert(
        email="user1@example.com",
        threshold=30000.0,
        active=True,
        created_at=datetime.now(timezone.utc),
    )
    alert2 = Alert(
        email="user2@example.com",
        threshold=35000.0,
        active=True,
        created_at=datetime.now(timezone.utc),
    )

    db.session.add_all([alert1, alert2])
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
