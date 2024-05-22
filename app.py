import json
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import Config
import geopandas as gpd
import momepy
from flask_cors import CORS, cross_origin
from graph import intersections_json, id_to_coords_map, GA, G

app = Flask(__name__)
CORS(app, support_credentials=True)



# app.config.from_object(Config)
# mysql = MySQL(app)


@app.route("/", methods = ["GET"])
@cross_origin(supports_credentials=True)
def index():
  
    # cursor = mysql.connection.cursor()
    # cursor.execute(f"INSERT INTO segments (NULL, test, 1.1, ST_GeomFromText('{type} '))")

    return jsonify(intersections_json["features"])

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

