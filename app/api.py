import json
from flask import Blueprint, current_app, jsonify, request, g, send_from_directory
from flask_cors import CORS
from . import db
import time

api = Blueprint("api", __name__, static_folder="./static", static_url_path="/")
# CORS(api, resources=r"/api/*", origins=["http://localhost:5173"])

@api.route("/")
def index():
  print(api.static_folder)
  return send_from_directory(api.static_folder, "index.html")

@api.route("/traffic")
def traffic():
  from .utils.get_road_segments import get_road_segments
  
  road_segments = get_road_segments(current_app.roads, current_app.nodes)

  return jsonify(road_segments)

@api.route("/navigate", methods=["GET", "POST"])
def navigate():
  if request.method == "GET":
    from .utils.get_intersections import get_intersections

    intersections = get_intersections()
    return jsonify(intersections)

  if request.method == "POST":
    from .utils.get_route import get_route
    start, end, priority = request.json

    startTime = time.time()
    route, distance = get_route(int(start), int(end), priority)
    endTime = time.time()
    
    print(endTime - startTime)
    return jsonify({"route": route, "distance": distance})

@api.route("/visualize")
def test():
  from .utils.get_visuals import get_visuals

  startTime = time.time()
  results = get_visuals()
  endTime = time.time()
  print(endTime - startTime)

  return jsonify(results)