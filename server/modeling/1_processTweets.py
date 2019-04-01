import sys
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime

delimiter = ','
quotechar = '"'
filePath = os.path.join(sys.path[0], '..\\files')

#no_of_tweets = 5000

# filenames
tweetFile = "kaggle_tweets.csv"
stopwordsFile = "StopWords.txt"

starttime = datetime.now()

print('reading tweets...')
df = pd.read_csv(os.path.join(
    filePath, tweetFile), header=None, delimiter=delimiter, quotechar=quotechar)

# select only sentiment, tweet columns
df = df.loc[:, [0, 5]]
# print(df)

# get 'no_of_tweets' for each sentiment
#df = df.groupby(0).head(no_of_tweets)
#df = df.reset_index(drop=True)

# reset column indexing
df.columns = range(df.shape[1])
# print(df)

print('create stopwords list')
stopwords_list = []
fp = open(os.path.join(filePath, stopwordsFile), 'r')
line = fp.readline()
while line:
    word = line.strip()
    stopwords_list.append(word)
    line = fp.readline()
fp.close()

print('process tweets...')
# Convert into lowercase
df[1] = df[1].str.lower()

# Convert www.* or https?://* to ''
df[1] = df[1].replace(regex=r'((www\.[\s]+)|(https?://[^\s]+))', value='')

# Convert @username to ''
df[1] = df[1].replace(regex=r'@[^\s]+', value='')

# Replace #word with word Handling hashtags
df[1] = df[1].replace(regex=r'#([^\s]+)', value=r'\1')

# Deleting the reTweets
df[1] = df[1].replace('rt', '')

# keep only alphabets
df[1] = df[1].replace(regex=r'[^abcdefghijklmnopqrstuvwxyz ]', value='')

# Remove additional white spaces
df[1] = df[1].replace(regex=r'[\s]+', value=' ')

# replace all stopwords
for to_replace in stopwords_list:
    df[1] = df[1].replace(regex=r'\b{}\b'.format(to_replace), value=' ')

# Remove additional white spaces
df[1] = df[1].replace(regex=r'[\s]+', value=' ')

# strip white-space
df[1] = df[1].str.strip()

# remove blank rows
df = df[df[1] != '']

# re-shuffle the rows for randomness
print('shuffle rows')
df = df.sample(frac=1).reset_index(drop=True)

# save the dfframe to csv
file_name = 'processed_tweets.csv'
df.to_csv(os.path.join(filePath, file_name), sep='\t')

print('\nSaved processed tweets!')

endtime = datetime.now()

diff = endtime - starttime

print('\nTotal time : ' + str(divmod(diff.days * 86400 + diff.seconds, 60)))
