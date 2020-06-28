import os

from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from .sql_extensions import db as sql_db_extension
from .excel.excelController import excel
from .shows.showsController import shows
from .exceptionHandler import InvalidUsage
import omdb


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    omdb.set_default('apikey', '6623baf2')
    app.register_blueprint(excel)
    app.register_blueprint(shows)
    # the toolbar is only enabled in debug mode:
    app.debug = True

    # upload folder path
    app.config['MAX_CONTENT_PATH'] = 5000000
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@127.0.0.1/neo_theater'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.db'),
    )

    sql_db_extension.init_app(app)
    toolbar = DebugToolbarExtension(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('settings.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    from . import db
    db.init_app(app)

    return app