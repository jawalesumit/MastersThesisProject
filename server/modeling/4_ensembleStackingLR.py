import numpy as np
import pandas as pd
import sys
import os
import pickle
from datetime import datetime

#from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report

# filenames
TweetFile = "processed_tweets.csv"

filePath = os.path.join(sys.path[0], '..\\files')
modelsPath = os.path.join(sys.path[0], '..\\savedModels')


starttime = datetime.now()


filename = 'CountVectorizer_svm.sav'
CountVectorizer_svm = pickle.load(
    open(os.path.join(modelsPath, filename), 'rb'))

filename = 'CountVectorizer_mNB.sav'
CountVectorizer_mnb = pickle.load(
    open(os.path.join(modelsPath, filename), 'rb'))

filename = 'TfidfTransformer_mNB.sav'
TfidfTransformer = pickle.load(open(os.path.join(modelsPath, filename), 'rb'))


########## Read and create test, train data - start ##########
print('reading processed tweets...')
data = pd.read_csv(os.path.join(filePath, TweetFile), sep='\t')
#data = data.sample(frac=0.006, random_state=1)

# Model spliting
train, test = train_test_split(data, test_size=0.2)
X_train = train['1'].astype(str)
X_test = test['1'].astype(str)
y_train = train['0']
y_test = test['0']

y_val_pred = []

########## Read and create test, train data - end ##########

########## Stacking function - start ##########


def Stacking(model_name, model, X_train1, y_train1, n_fold, y_val_flag, y_val_pred1):
    print('in stacking...')
    #n_fold = 2
    folds = StratifiedKFold(n_splits=n_fold)
    val_pred = np.zeros((0,))
    i = 0

    for train_indices, val_indices in folds.split(X_train1, y_train1):
        x_trn, x_val = X_train1.iloc[train_indices], X_train1.iloc[val_indices]
        y_trn, y_val = y_train1.iloc[train_indices], y_train1.iloc[val_indices]

        if model_name == 'svm':
            x_trn = CountVectorizer_svm.transform(x_trn)
            x_val = CountVectorizer_svm.transform(x_val)
        elif model_name == 'mnb':
            x_trn = TfidfTransformer.transform(
                CountVectorizer_mnb.transform(x_trn))
            x_val = TfidfTransformer.transform(
                CountVectorizer_mnb.transform(x_val))

        model.fit(X=x_trn, y=y_trn.values)
        val_pred = np.append(val_pred, model.predict(x_val))
        if model_name == 'svm':
            if y_val_flag == True:
                y_val_pred1 = y_val_pred1.append(y_val)
            else:
                y_val_pred1 = y_val
                y_val_flag = True

        i = i + 1
        print('stacked ' + model_name + ' ' + str(i))

    return val_pred.reshape(-1, 1), y_val_pred1
########## Stacking function - end ##########


############################ SVM Base Model - START ##############################
print('\nbase model - SVM')

model_svm = LinearSVC(C=0.01, max_iter=X_test.size)

print('stacking svm...')
train_pred_svm, y_val_svm = Stacking(
    model_name='svm', model=model_svm, n_fold=10, X_train1=X_train, y_train1=y_train, y_val_flag=False, y_val_pred1=y_val_pred)

print('training whole svm...')
model_svm.fit(CountVectorizer_svm.transform(X_train), y_train.values)
test_pred_svm = model_svm.predict(CountVectorizer_svm.transform(X_test))

train_pred_svm = pd.DataFrame(train_pred_svm)
test_pred_svm = pd.DataFrame(test_pred_svm)

############################ SVM Base Model - END ##############################

############################ Multinomial NB Base Model - START ##############################
print('\nbase model - mnb')

model_mnb = MultinomialNB(alpha=1, class_prior=None, fit_prior=True)

print('stacking mnb...')
train_pred_mnb, y_val_pred = Stacking(
    model_name='mnb', model=model_mnb, n_fold=10, X_train1=X_train, y_train1=y_train, y_val_flag=True, y_val_pred1=y_val_svm)

print('training whole nb...')
model_mnb.fit(TfidfTransformer.transform(
    CountVectorizer_mnb.transform(X_train)), y_train.values)
test_pred_mnb = model_mnb.predict(
    TfidfTransformer.transform(CountVectorizer_mnb.transform(X_test)))

train_pred_mnb = pd.DataFrame(train_pred_mnb)
test_pred_mnb = pd.DataFrame(test_pred_mnb)

############################ Multinomial NB Base Model - END ##############################

df_x_train = pd.concat([train_pred_svm, train_pred_mnb], axis=1)

df_x_test = pd.concat([test_pred_svm, test_pred_mnb], axis=1)

############################ Logistic Regression meta-Model - START ##############################
print('\nmeta-model : LR')
model = LogisticRegression(C=0.01, max_iter=X_test.size, solver='sag',
                           class_weight='balanced', n_jobs=-1, warm_start=True)

print('training lr model...')
model.fit(df_x_train, y_val_pred)

print(classification_report(y_test, model.predict(df_x_test), digits=4))

# **** save model on disk *****
print('\nsaving model...')
filename = 'lr_meta_stacked_model.sav'
pickle.dump(model, open(os.path.join(modelsPath, filename), 'wb'))

print('\nModel saved!')

############################ Logistic Regression meta-Model - END ##############################

endtime = datetime.now()

diff = endtime - starttime

print('\nTotal time : ' + str(divmod(diff.days * 86400 + diff.seconds, 60)))

print('Done!')
