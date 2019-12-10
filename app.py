from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/test', methods=["POST"])
def prelim():
    form = request.form
    return {
        "message": "hit the endpoint",
        "data": form
    }

if __name__ == "__main__":
    app.run()