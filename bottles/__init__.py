import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is not None:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')

    return app
