import json

from urllib.request import urlopen

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/single-layer")
def single_layer():
    health_check_url = request.args.get('healthCheckUrl')
    app_name = request.args.get('appName')
    if health_check_url is None or app_name is None: return "Params healthCheckUrl and appName are mandatory", 400

    f = urlopen(health_check_url)
    json_data = json.loads(f.read().decode("utf-8"))

    components = [{"name": key, "status": value} for key, value in json_data.items()]

    return jsonify({"name": app_name, "components": components})


if __name__ == "__main__":
    app.run(port=5001)
