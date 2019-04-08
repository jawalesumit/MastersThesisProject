from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import json
import pandas as pd

import fetchTweets as ft
import sentimentAnalysis as sa

app = Flask(__name__)
CORS(app)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
tmpFilePath = os.path.join(THIS_FOLDER, 'tempFiles')

serverFile = os.path.join(THIS_FOLDER, 'server_config.json')
with open(serverFile) as f:
    configData = json.load(f)

# gloabal variables
SERVER_PORT = configData["server_details"]["server_port"]
SERVER_IP = configData["server_details"]["server_ip"]

TWEET_LIMIT = configData["tweet_limit"]

# routes
@app.route("/")
def test():
    return "Hello world!"


@app.route("/getSentiment")
def getSentiment():
    print('in server getSentiment')

    vQueries = request.args.get("Queries")
    print(vQueries)

    vQueryTerms = []
    for x in vQueries.split(';'):
        vQueryTerms.append(x.strip())
    print(vQueryTerms)

    vFilename = request.args.get("Filename")
    vFilename = str(vFilename) + ".csv"
    print(vFilename)

    f = open(os.path.join(tmpFilePath, vFilename), 'w')
    f.close()

    print('fetching tweets...')
    ft.streamTweets(vQueryTerms, vFilename)
    print('all tweets fetched!!!')
    df = pd.read_csv(os.path.join(tmpFilePath, vFilename), header=None)
    print(len(df.index))

    print("analyzing sentiment...")

    mnb_positive, mnb_negative, svm_positive, svm_negative, lr_positive, lr_negative = sa.analyzeSentiment(
        df)

    msg = {
        'mnb_positive': mnb_positive,
        'mnb_negative': mnb_negative,
        'svm_positive': svm_positive,
        'svm_negative': svm_negative,
        'lr_positive': lr_positive,
        'lr_negative': lr_negative
    }

    print('removing file : ' + str(vFilename))
    os.remove(os.path.join(tmpFilePath, vFilename))

    return jsonify(msg)


if __name__ == "__main__":
    # run app in debug mode on port 5000
    app.run(host=SERVER_IP, port=SERVER_PORT)
