from flask import Flask, request
import json
from haversine import  haversine
from pymongo import MongoClient
import datetime


app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_distance():

    connection = MongoClient('mongodb://Admin:Admin123@ds263927.mlab.com:63927/bus_stop', retryWrites=False)
    db = connection.get_database("bus_stop")
    stop_bus = db.get_collection("stop_bus")
    car_position = db.get_collection("car_position")
    cursor = stop_bus.find()

    dato = request.json
    json_data = json.loads(json.dumps(dato, sort_keys=True))

    lat_pos = json_data['latitud']
    lon_pos = json_data['longitud']
    date_time = str(datetime.datetime.now())
    point = (lat_pos, lon_pos)

    # car_position.insert({"latitud": lat_pos, "longitud": lon_pos, "hora_fecha": date_time})

    distances = []
    for i in cursor:
        lat_sta = i["latitud"]
        lon_sta = i["longitud"]
        stop_bus = (lat_sta, lon_sta)
        distance = haversine(stop_bus, point)
        dist = distance * 1000
        distances.append(dist)


    dist1 = "Distancia respecto a la parada 1 --> " + str(distances[0])
    dist2 = "Distancia respecto a la parada 2 --> " + str(distances[1])
    dist3 = "Distancia respecto a la parada 3 --> " + str(distances[2])


    """for i in range(1, len(distances)):
        distancia = "Distancia respecto a la parada " + str(i) + " --> " + str(distances[i])
        print(distancia)"""

    return dist1 + "\n" + dist2 + "\n" + dist3


if __name__ == '__main__':
    app.run()