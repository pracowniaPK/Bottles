import os

from flask import Flask

from .config import *

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if os.environ['FLASK_ENV'] == 'development':
        app.config.from_object(DevelopmentConfig)
    if os.environ['FLASK_ENV'] == 'production':
        app.config.from_object(ProductionConfig)
    if config:
        if config.get('TESTING'):
            app.config.from_object(TestingConfig)
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import blog
    app.register_blueprint(blog.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')

    from bottles.db import get_db_session, init_db_command, reset_db_command
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session = get_db_session()
        db_session.remove()
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)

    return app
