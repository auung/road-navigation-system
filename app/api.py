import json
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

@api.route("/navigate", methods=["GET", "POST"])
def navigate():
  if request.method == "GET":
    from .utils.get_intersections import get_intersections

    intersections = get_intersections()
    return jsonify(intersections);

  if request.method == "POST":
    from .utils.get_route import get_route

    start, end = request.json
    print(start, end)
    route = get_route(int(start), int(end))
    return jsonify(route)

@api.route("/test")
def test():
  return jsonify({ "message": "This is a test"})