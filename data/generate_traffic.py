import random
from db import cnx, cursor

def generate_traffic():
  sql = "SELECT id FROM segments"
  cursor.execute(sql)

  segments = [result[0] for result in cursor]

  for segment_id in segments:
    traffic_density = round(random.triangular(0, 100, 15)) / 100
    sql = f"INSERT INTO traffic (id, segment_id, traffic_density, time) VALUES (NULL, {segment_id}, {traffic_density}, 1)"
    cursor.execute(sql)

  cnx.commit()
  cursor.close()
  cnx.close()


# generate_traffic()