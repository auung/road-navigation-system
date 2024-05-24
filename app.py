from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import Config
from flask_cors import CORS, cross_origin
from read_gpkg import read_gpkg
from get_road_segments import get_road_segments

app = Flask(__name__)
CORS(app, support_credentials=True)

app.gpkg = read_gpkg("./geopackage/navigation.gpkg")

app.config.from_object(Config)
mysql = MySQL(app)


@app.route("/")
@cross_origin(supports_credentials=True)
def index():
  intersections = [[intersection["geometry"]["coordinates"][1], intersection["geometry"]["coordinates"][0]] for intersection in   app.gpkg["intersections"]]
  road_segments = get_road_segments(app.gpkg["roads"], app.gpkg["nodes"])

  return jsonify(road_segments)


@app.route("/route", methods = ["POST"])
@cross_origin(supports_credentials=True)
def get_route():
	if request.method == "POST":
		start, end = request.get_json()
		ga = GA(G, start, end)
		best = ga.run()
		response = [x for x in map(lambda node: id_to_coords_map[node], best)]
		response = [list(x) for x in zip(response[:-1], response[1:])]
		return jsonify(response)


# @app.route("/navigate", methods = ["GET", "POST"])
# @cross_origin(supports_credentials=True)
# def navigate():

