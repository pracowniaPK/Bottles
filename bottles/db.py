import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def get_engine():
    engine = create_engine(current_app.config["DATABASE_URI"], convert_unicode=True)
    return engine

def get_db_session():
    if 'db_session' not in g:
        engine = get_engine()
        db_session = scoped_session(sessionmaker(autocommit=False,
                                                autoflush=False,
                                                bind=engine))
        g.db_session = db_session
    return g.db_session

Base = declarative_base()

def init_db():
    engine = get_engine()
    import bottles.models
    Base.metadata.create_all(bind=engine)

@click.command('init_db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialized')

def reset_db():
    engine = get_engine()
    import bottles.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@click.command('reset_db')
@with_appcontext
def reset_db_command():
    reset_db()
    click.echo('DB reseted')
