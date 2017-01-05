from flask import Flask
from flask import jsonify
import json
from urllib import request

app = Flask(__name__)

@app.route("/")
def hello():
    link = "http://localhost:5000" #get this from the input param

    f = request.urlopen(link)
    jsonString = f.read()
    jsonData = json.loads(jsonString)

    components = []
    print(jsonData)
    print(jsonData.items())
    for key, value in jsonData.items():
        components.append({"name": key, "status": value})
    print(components)

    return  jsonify({"components": components})

if __name__ == "__main__":
    app.run(port=5001)
