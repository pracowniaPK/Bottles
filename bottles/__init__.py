import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('bottles.config.Config')
    try:
        app.config.from_object(os.environ['APP_SETTINGS'])
    except:
        pass
    app.config.from_pyfile('config.py')

    db_path = os.path.join(app.instance_path, 'db.sqlite')
    db_path = 'sqlite:///' + db_path
    app.config.from_mapping(
        DATABASE=db_path,
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is not None:
        app.config.from_mapping(test_config)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')

    from bottles.db import get_db_session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session = get_db_session()
        db_session.remove()

    return app
