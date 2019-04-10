import sys
import os
import pickle
import pandas as pd

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


def analyzeSentiment(df):

    vector = CountVectorizer_svm.transform(df[2])
    svm_pred = svm_model.predict(vector)

    vector = TfidfTransformer_mnb.transform(
        CountVectorizer_mnb.transform(df[2]))
    mnb_pred = mnb_model.predict(vector)

    svm_mnb_df = pd.concat([pd.DataFrame(svm_pred), pd.DataFrame(mnb_pred)], axis=1)

    lr_pred = lr_meta_model.predict(svm_mnb_df)

    df = pd.concat([df, svm_mnb_df, pd.DataFrame(lr_pred)], axis=1, ignore_index=True)

    return df
