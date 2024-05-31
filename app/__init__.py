from flask import Flask, blueprints, g
from flask_mysqldb import MySQL
from config import Config
from pathlib import Path

from .utils.read_gpkg import read_gpkg

db = MySQL()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)

  app.gpkg = Path("geopackage\\navigation.gpkg").absolute()
  app.roads, app.intersections, app.nodes = read_gpkg(app.gpkg)

  @app.before_request
  def before_request():
    if "conn" not in g:
      g.conn = db.connection

    if "cursor" not in g:
      g.cursor = g.conn.cursor()

  from .api import api
  app.register_blueprint(api, url_prefix="/api")

  return app

