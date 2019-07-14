from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.cli import with_appcontext
import os
import click

engine = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_app(app):
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)

def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)

def shutdown_session(exception=None):
    db_session.remove()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.command('Initialized the database.')