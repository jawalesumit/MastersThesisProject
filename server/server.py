from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import sys
import pickle
import json
import csv
import numpy as np

from nltk.tokenize import TweetTokenizer

app = Flask(__name__)
CORS(app)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
serverFile = os.path.join(THIS_FOLDER, 'server_config.json')
with open(serverFile) as f:
    configData = json.load(f)

# gloabal variables
SERVER_PORT = configData["server_port"]
SERVER_IP = configData["server_ip"]


def tokenize(text):
    tknzr = TweetTokenizer()
    return tknzr.tokenize(text)


def nbSentiment(input1):
    input1 = input1.split()
    settweet = set(input1)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in settweet)

    sentiment = nb_model.classify(features)
    #print('nbSentiment() = ' + sentiment)
    return sentiment


def lstmSentiment(input1):
    """
    # vectorizing the tweet by the pre-fitted tokenizer instance
    input1 = tokenizer.texts_to_sequences(input1)
    # padding the tweet to have exactly the same shape as `embedding_2` input
    input1 = pad_sequences(input1, maxlen=33, dtype='int32', value=0)
    # print(input1)
    sentiment = lstm_model.predict(input1, batch_size=1, verbose=2)[0]
    if(np.argmax(sentiment) == 0):
        sentiment = "negative"
    elif (np.argmax(sentiment) == 1):
        sentiment = "positive"
    return sentiment
    """


def svmSentiment(input1):
    svm_sentiment = svm_model.predict([input1])
    if(svm_sentiment == ['positive']):
        svm_sentiment = 'positive'
    else:
        svm_sentiment = 'negative'
    return svm_sentiment

# ************************

# routes
@app.route("/getSentiment")
def test():
    print('in server test connection')

    vQueries = request.args.get("Queries")

    vQueries = vQueries.lower()

    print('vQueries :: ' + vQueries)

    nb_sentiment = nbSentiment(vQueries)
    lstm_sentiment = ''  # lstmSentiment(vQueries)
    svm_sentiment = svmSentiment(vQueries)

    msg = {
        'nb_sentiment': nb_sentiment,
        'lstm_sentiment': lstm_sentiment,
        'svm_sentiment': svm_sentiment
    }

    return jsonify(msg)


if __name__ == "__main__":
    # ***** Load the saved model ******
    filename = 'nb_model.sav'
    nb_model = pickle.load(
        open(os.path.join(sys.path[0], 'files', filename), 'rb'))

    word_features = {}
    filename = 'dict.csv'
    inpTweets = csv.reader(
        open(os.path.join(sys.path[0], 'files', filename), 'r'))
    for rowTweet in inpTweets:
        if rowTweet:
            word_features[rowTweet[0]] = ''
    """
    filename = 'lstm_tokenizer.sav'
    tokenizer = pickle.load(
        open(os.path.join(sys.path[0], 'files', filename), 'rb'))

    filename = 'lstm_model.sav'
    lstm_model = pickle.load(
        open(os.path.join(sys.path[0], 'files', filename), 'rb'))
    """
    filename = 'svm_model.sav'
    svm_model = pickle.load(
        open(os.path.join(sys.path[0], 'files', filename), 'rb'))

    # run app in debug mode on port 5000
    app.run(host=SERVER_IP, port=SERVER_PORT)
