import numpy as np
import pandas as pd
import sys
import os
import pickle
from datetime import datetime

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# filenames
TweetFile = "processed_tweets.csv"

filePath = os.path.join(sys.path[0], '..\\files')
modelsPath = os.path.join(sys.path[0], '..\\savedModels')

starttime = datetime.now()

########## Read and create test, train data - start ##########
print('reading processed tweets...')
data = pd.read_csv(os.path.join(filePath, TweetFile), sep='\t')
# print(data)
#data = data.sample(frac=0.1)
# print(data.shape)

########## Read and create test, train data - end ##########

vectorizer = CountVectorizer(
    analyzer='word',
    ngram_range=(1, 1)
)

CountVectorizer = vectorizer.fit(data['1'].astype(str).values)
print('Vectores built')
filename = 'CountVectorizer_svm.sav'
pickle.dump(CountVectorizer, open(os.path.join(modelsPath, filename), 'wb'))
print('Vectores saved!')

# Model training
train, test = train_test_split(data, test_size=0.2)
X_train = CountVectorizer.transform(train['1'].astype(str))
X_test = CountVectorizer.transform(test['1'].astype(str))
y_train = train['0'].values
y_test = test['0'].values

model = LinearSVC(C=0.01, max_iter=X_test.size)

print('Training model...')
model.fit(X_train, y_train)

#print(model.score(X_test, y_test))

print(classification_report(y_test, model.predict(X_test), digits=4))
"""
print("Best cross-validation score: {:.2f}".format(model.best_score_))
print("Best parameters: ", model.best_params_)
print("Best estimator: ", model.best_estimator_)
"""
# **** save model on disk *****
print('\nsaving model...')
filename = 'svm_model.sav'
pickle.dump(model, open(os.path.join(modelsPath, filename), 'wb'))

print('\nModel saved!')

endtime = datetime.now()

diff = endtime - starttime

print('\nTotal time : ' + str(divmod(diff.days * 86400 + diff.seconds, 60)))

print('Done!')
