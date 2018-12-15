INSERT INTO user (username, password, nick)
VALUES
    ('test', 'pbkdf2:sha256:50000$mqwmbGt9$eb65f9cc5102cb2ffbc295150558b0ef330e553ea41efbf1c091db150e238f24', 'test_nick'),
    ('test2', 'pbkdf2:sha256:50000$aoEpy2N4$92f1d1e87c053b1f2df460f043e42bb8f5c45fca2b063025096a95791298a546', 'test2');

INSERT INTO subscription (subscriber_id, target_id)
VALUES (1 ,2);

INSERT INTO post (title, body, author_id, created)
VALUES ('my title', 'my post content' || x'0a' || 'and some more', 2, '2018-01-01 00:00:00');