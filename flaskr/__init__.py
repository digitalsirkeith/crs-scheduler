import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import database
    database.init_app(app)
    
    from . import root
    app.register_blueprint(root.bp)

    return app

app = create_app()