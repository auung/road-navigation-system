from flask import Blueprint, current_app, jsonify, request
from flask_cors import CORS

from . import db

api = Blueprint("api", __name__)
CORS(api, resources=r"/api/*", origins=["http://localhost:5173"])

@api.route("/")
def index():
  from .utils.get_road_segments import get_road_segments
  
  road_segments = get_road_segments(current_app.roads, current_app.nodes)

  return jsonify(road_segments)

@api.route("/navigate")
def navigate():
  if request.method == "GET":
    intersections = [[intersection["geometry"]["coordinates"][1], intersection["geometry"]["coordinates"][0]] for intersection in current_app.intersections]

  if request.method == "POST":
    start, end = request.get_json()
    return None

@api.route("/test")
def test():
  return None