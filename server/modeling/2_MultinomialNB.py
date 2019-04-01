import numpy as np
import pandas as pd
import sys
import os
import pickle
from datetime import datetime

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
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
#data = data.sample(frac=0.006, random_state=1)
# print(data.shape)
# print(data)

vectorizer = CountVectorizer(
    analyzer='word',
    ngram_range=(1, 2)
)

CountVectorizer = vectorizer.fit(data['1'].astype(str).values)
print('Vectores built')
filename = 'CountVectorizer_mNB.sav'
pickle.dump(CountVectorizer, open(os.path.join(modelsPath, filename), 'wb'))
print('Vectores saved!')

transformer = TfidfTransformer(
    use_idf=False,
    norm='l1'
)

TfidfTransformer = transformer.fit(
    CountVectorizer.transform(data['1'].astype(str)))
print('transformer built')
filename = 'TfidfTransformer_mNB.sav'
pickle.dump(TfidfTransformer, open(os.path.join(modelsPath, filename), 'wb'))
print('transformer saved!')

train, test = train_test_split(data, test_size=0.2)
X_train = TfidfTransformer.transform(
    CountVectorizer.transform(train['1'].astype(str)))
X_test = TfidfTransformer.transform(
    CountVectorizer.transform(test['1'].astype(str)))
y_train = train['0'].values
y_test = test['0'].values

model = MultinomialNB(alpha=1, class_prior=None, fit_prior=True)

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
filename = 'mnb_model.sav'
pickle.dump(model, open(os.path.join(modelsPath, filename), 'wb'))

print('\nModel saved!')

endtime = datetime.now()

diff = endtime - starttime

print('\nTotal time : ' + str(divmod(diff.days * 86400 + diff.seconds, 60)))

print('Done!')
