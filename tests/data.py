from flask import current_app

from bottles.db import get_db_session
from bottles.models import User, Subscription, Post


def create_test_data():
    s = get_db_session()

    s.add(User(username='test', password='pbkdf2:sha256:50000$mqwmbGt9$eb65f9cc5102cb2ffbc295150558b0ef330e553ea41efbf1c091db150e238f24', nick='test_nick'))
    s.add(User(username='test2', password='pbkdf2:sha256:50000$aoEpy2N4$92f1d1e87c053b1f2df460f043e42bb8f5c45fca2b063025096a95791298a546', nick='test2'))
    s.add(Subscription(subscriber_id=1, target_id=2))
    s.add(Post(title='my title', body='my post content\nand some more', author_id=2))
    
    s.commit()
