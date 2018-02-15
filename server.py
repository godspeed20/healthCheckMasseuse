import json

from urllib.request import urlopen

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/single-layer", methods=['GET'])
def single_layer():
    health_check_url = request.args.get('healthCheckUrl')
    app_name = request.args.get('appName')
    if not health_check_url or not app_name: return "Params healthCheckUrl and appName are mandatory", 400

    f = urlopen(health_check_url)
    decoded_json_string = f.read().decode("utf-8")
    if not decoded_json_string: return jsonify({"name": app_name})
    json_data = json.loads(decoded_json_string)

    components = [{"name": key, "status": value} for key, value in json_data.items()]

    return jsonify({"name": app_name, "components": components})


if __name__ == "__main__":
    app.run(port=5001)
