from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
serverFile = os.path.join(THIS_FOLDER, 'server_config.json')
with open(serverFile) as f:
    configData = json.load(f)

# gloabal variables
SERVER_PORT = configData["server_port"]
SERVER_IP = configData["server_ip"]

# routes
@app.route("/testconnection")
def test():
    print('in server test connection')

    msg = {'text': 'Hi'}

    return jsonify(msg)


if __name__ == "__main__":
    # run app in debug mode on port 5000
    app.run(host=SERVER_IP, port=SERVER_PORT)
