import sys
import os
import pickle
import re
import pandas as pd
import collections

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
modelsPath = os.path.join(THIS_FOLDER, 'savedModels')

# ***** Load the saved model ******
print('Loading all models...')
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

print('All models loaded!')

# ************************

# ---------------analyze sentiment---------------


def analyzeSentiment(vQueries):
    vQueries = vQueries[0].astype(str)

    vector = CountVectorizer_svm.transform(vQueries)
    svm_pred = svm_model.predict(vector)

    vector = TfidfTransformer_mnb.transform(
        CountVectorizer_mnb.transform(vQueries))
    mnb_pred = mnb_model.predict(vector)

    df = pd.concat([pd.DataFrame(svm_pred), pd.DataFrame(mnb_pred)], axis=1)

    lr_pred = lr_meta_model.predict(df)

    """
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
    """

    counter1 = collections.Counter(mnb_pred)
    mnb_positive = counter1[4]
    mnb_negative = counter1[0]

    counter1 = collections.Counter(svm_pred)
    svm_positive = counter1[4]
    svm_negative = counter1[0]

    counter1 = collections.Counter(lr_pred)
    lr_positive = counter1[4]
    lr_negative = counter1[0]

    return mnb_positive, mnb_negative, svm_positive, svm_negative, lr_positive, lr_negative
