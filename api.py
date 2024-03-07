import json
from flask import Flask, jsonify

app = Flask(__name__)


def get_data(path):
    with open(f"{path}", "r") as file:
        data = json.load(file)
    return data


@app.route("/EV/all", methods=["GET"])
def get_json_data():
    json_data = get_data("EV_Charging_Stations/output.json")
    return jsonify(json_data)

if __name__ == "__main__":
    app.run()