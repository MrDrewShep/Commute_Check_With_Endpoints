from flask import Flask, request, jsonify
import json
from pprint import pprint

app = Flask(__name__)

@app.route('/test', methods=["POST"])
def prelim():
    google_response = json.loads(request.form["google_response"])
    print(google_response["routes"][0]["legs"][0]["distance"])
    return {
        "message": "hit the endpoint",
        "data": google_response
    }

if __name__ == "__main__":
    app.run()