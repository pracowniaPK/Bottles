import sqlite3

from bottles.db import get_db_session, reset_db
from bottles.models import User


def test_reset_db(app):
    with app.app_context():
        s = get_db_session()
        assert s.query(User).all()
        reset_db()
        assert not s.query(User).all()