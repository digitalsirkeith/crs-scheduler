import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Setup the Application, Database, and Migrations
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=os.environ['SECRET_KEY'], 
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy()
from flaskr.models import associations, schedule, instructor, class_schedule
db.init_app(app)
migrate = Migrate(app, db)

# Setup the Blueprints (Controllers)
from . import root
app.register_blueprint(root.bp)