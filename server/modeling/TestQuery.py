import sys
import os
import pickle
import re
import pandas as pd

# filenames
stopwordsFile = "StopWords.txt"

filePath = os.path.join(sys.path[0], '..\\files')
modelsPath = os.path.join(sys.path[0], '..\\savedModels')

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
CountVectorizer_mnb = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))

filename = 'TfidfTransformer_mNB.sav'
TfidfTransformer_mnb = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))

filename = 'svm_model.sav'
svm_model = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))

filename = 'CountVectorizer_svm.sav'
CountVectorizer_svm = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))

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

var = ''
while(var != 'exit'):
    input1 = input(
        '\nPlease write a sentence to be tested sentiment. If you type - exit- the program will exit \n')
    #input = 'The film is very good'
    # print('\n')
    if input1 == 'exit':
        print('Exiting the program')
        var = 'exit'
        # break
    else:
        input1 = processText(input1)
        print(input1)

        vector = CountVectorizer_svm.transform([input1])
        svm_pred = svm_model.predict(vector)

        vector = TfidfTransformer_mnb.transform(CountVectorizer_mnb.transform([input1]))
        mnb_pred = mnb_model.predict(vector)

        df = pd.concat([pd.DataFrame(svm_pred), pd.DataFrame(mnb_pred)], axis=1)

        sentiment = lr_meta_model.predict(df)
        #print(sentiment)
        if(sentiment == [4]):
            print('positive')
        else:
            print('negative')
