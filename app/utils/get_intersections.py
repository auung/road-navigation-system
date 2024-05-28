from flask import current_app

def get_intersections():
  intersections = []

  for intersection in current_app.intersections:
    intersections.append({
      "id": intersection["id"],
      "coords": [
        intersection["geometry"]["coordinates"][1],
        intersection["geometry"]["coordinates"][0]
      ]
    })

  return intersections