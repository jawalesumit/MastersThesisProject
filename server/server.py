from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import sys
import pickle
import json
import csv
import numpy as np

import sentimentAnalysis as sa

app = Flask(__name__)
CORS(app)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
serverFile = os.path.join(THIS_FOLDER, 'server_config.json')
with open(serverFile) as f:
    configData = json.load(f)

# gloabal variables
SERVER_PORT = configData["server_port"]
SERVER_IP = configData["server_ip"]

# ************************

# routes
@app.route("/getSentiment")
def test():
    print('in server test connection')

    vQueries = request.args.get("Queries")

    vQueries = vQueries.lower()

    print('vQueries :: ' + vQueries)

    mnb_sentiment, svm_sentiment, lr_sentiment = sa.analyzeSentiment(vQueries)

    msg = {
        'mnb_sentiment': mnb_sentiment,
        'svm_sentiment': svm_sentiment,
        'lr_sentiment': lr_sentiment
    }

    return jsonify(msg)


if __name__ == "__main__":
    # run app in debug mode on port 5000
    app.run(host=SERVER_IP, port=SERVER_PORT)
