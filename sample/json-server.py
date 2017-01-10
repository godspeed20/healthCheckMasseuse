from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def basic_json():
    return jsonify(tuna=True, salmon=False)


if __name__ == "__main__":
    app.run()
