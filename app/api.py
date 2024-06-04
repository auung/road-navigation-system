import json
from flask import Blueprint, current_app, jsonify, request, g
from flask_cors import CORS
from . import db
import time

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
    return jsonify(intersections)

  if request.method == "POST":
    from .utils.get_route import get_route
    start, end = request.json

    startTime = time.time()
    route, distance = get_route(int(start), int(end))
    endTime = time.time()
    
    print(endTime - startTime)
    return jsonify({"route": route, "distance": distance})

@api.route("/test")
def test():

  return jsonify({ "message": "This is a test"})