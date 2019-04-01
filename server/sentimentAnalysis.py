import sys
import os
import pickle
import re
import pandas as pd

# filenames
stopwordsFile = "StopWords.txt"

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filePath = os.path.join(THIS_FOLDER, 'files')
modelsPath = os.path.join(THIS_FOLDER, 'savedModels')

print('create stopwords list')
stopwords_list = []
fp = open(os.path.join(filePath, stopwordsFile), 'r')
line = fp.readline()
while line:
    word = line.strip()
    stopwords_list.append(word)
    line = fp.readline()
fp.close()

# ***** Load the saved model ******
filename = 'mnb_model.sav'
mnb_model = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))

filename = 'CountVectorizer_mNB.sav'
CountVectorizer_mnb = pickle.load(
    open(os.path.join(modelsPath, filename), 'rb'))

filename = 'TfidfTransformer_mNB.sav'
TfidfTransformer_mnb = pickle.load(
    open(os.path.join(modelsPath, filename), 'rb'))

filename = 'svm_model.sav'
svm_model = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))

filename = 'CountVectorizer_svm.sav'
CountVectorizer_svm = pickle.load(
    open(os.path.join(modelsPath, filename), 'rb'))

filename = 'lr_meta_stacked_model.sav'
lr_meta_model = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))

# ************************


def processText(txt_input):
    # Convert into lowercase
    Tweet = txt_input.lower()

    # Convert www.* or https?://* to ''
    Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))', '', Tweet)

    # Convert @username to ''
    Tweet = re.sub('@[^\s]+', '', Tweet)

    # Replace #word with word Handling hashtags
    Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)

    # Deleting the Twitter reTweets
    rt = 'rt'
    Tweet = Tweet.replace(rt, '')

    legal = set(' abcdefghijklmnopqrstuvwxyz')
    Tweet = "".join(char if char in legal else '' for char in Tweet)

    Tweet = Tweet.strip()

    Tweet = " ".join(Tweet.split())

    tweet_without_stopwords = ''
    for x in Tweet.split(' '):
        if x in stopwords_list:
            continue
        else:
            tweet_without_stopwords = tweet_without_stopwords + x + ' '

    return tweet_without_stopwords
# ---------------------------------------

# ---------------analyze sentiment---------------


def analyzeSentiment(vQueries):
    input1 = processText(vQueries)
    print(input1)

    vector = CountVectorizer_svm.transform([input1])
    svm_pred = svm_model.predict(vector)

    vector = TfidfTransformer_mnb.transform(
        CountVectorizer_mnb.transform([input1]))
    mnb_pred = mnb_model.predict(vector)

    df = pd.concat([pd.DataFrame(svm_pred), pd.DataFrame(mnb_pred)], axis=1)

    lr_pred = lr_meta_model.predict(df)
    if(lr_pred == [4]):
        lr_pred = 'positive'
    else:
        lr_pred = 'negative'

    if(svm_pred == [4]):
        svm_pred = 'positive'
    else:
        svm_pred = 'negative'

    if(mnb_pred == [4]):
        mnb_pred = 'positive'
    else:
        mnb_pred = 'negative'

    return mnb_pred, svm_pred, lr_pred
