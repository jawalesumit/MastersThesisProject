from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import json
import pandas as pd

import fetchTweets as ft
import processTweets as pt
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

    vTweetCount = request.args.get("TweetCount")
    print(vTweetCount)

    vTimeout = request.args.get("Timeout")
    print(vTimeout)

    vFilename = request.args.get("Filename")
    vFilename = str(vFilename) + ".csv"
    print(vFilename)

    print('fetching tweets...')
    ft.streamTweets(vQueryTerms, vFilename, vTweetCount, vTimeout)
    print('all tweets fetched!!!')

    print('processing tweets...')
    pt.processTweets(vFilename)
    print('all tweets processed!!!')

    df = pd.read_csv(os.path.join(tmpFilePath, vFilename), header=None)

    print("analyzing sentiment...")
    df = sa.analyzeSentiment(df)

    # print(df)

    msg = {
        'mnb_pos_count': int((df[4] == 4).sum()),
        'mnb_neg_count': int((df[4] == 0).sum()),
        'mnb_tweets': (df.groupby([4], as_index=True).apply(lambda x: x[[0, 1]].to_dict('r')).reset_index().rename(columns={0: 'Data'}).to_json(orient='records')),

        'svm_pos_count': int((df[3] == 4).sum()),
        'svm_neg_count': int((df[3] == 0).sum()),
        'svm_tweets': (df.groupby([3], as_index=True).apply(lambda x: x[[0, 1]].to_dict('r')).reset_index().rename(columns={0: 'Data'}).to_json(orient='records')),

        'lr_pos_count': int((df[5] == 4).sum()),
        'lr_neg_count': int((df[5] == 0).sum()),
        'lr_tweets': (df.groupby([5], as_index=True).apply(lambda x: x[[0, 1]].to_dict('r')).reset_index().rename(columns={0: 'Data'}).to_json(orient='records'))
    }

    print('removing file : ' + str(vFilename))
    os.remove(os.path.join(tmpFilePath, vFilename))

    return jsonify(msg)


if __name__ == "__main__":
    # run app in debug mode on port 5000
    app.run(host=SERVER_IP, port=SERVER_PORT)
