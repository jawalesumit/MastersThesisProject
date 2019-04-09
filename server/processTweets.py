import sys
import re
import json
import os
import pandas as pd

QUOTECHAR = '~'
DELIMITER = '|'

# filenames
stopwordsFile = "StopWords.txt"

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filePath = os.path.join(THIS_FOLDER, 'files')

tmpFilePath = os.path.join(THIS_FOLDER, 'tempFiles')

print('create stopwords list')
stopwords_list = []
fp = open(os.path.join(filePath, stopwordsFile), 'r')
line = fp.readline()
while line:
    word = line.strip()
    stopwords_list.append(word)
    line = fp.readline()
fp.close()

def processTweets(tweetFile):
    df = pd.read_csv(os.path.join(
        tmpFilePath, tweetFile), encoding="Windows-1252", header=None, delimiter=DELIMITER, quotechar=QUOTECHAR)

    print(len(df.index))

    # Drop duplicate tweets
    df = df.drop_duplicates(subset=[2])

    # Convert into lowercase
    df[2] = df[2].str.lower()

    # Convert www.* or https?://* to ''
    df[2] = df[2].replace(regex=r'((www\.[\s]+)|(https?://[^\s]+))', value='')

    # Convert @username to ''
    df[2] = df[2].replace(regex=r'@[^\s]+', value='')

    # Replace #word with word Handling hashtags
    df[2] = df[2].replace(regex=r'#([^\s]+)', value=r'\1')

    # Deleting the reTweets
    df[2] = df[2].replace('rt', '')

    # keep only alphabets
    df[2] = df[2].replace(regex=r'[^abcdefghijklmnopqrstuvwxyz ]', value='')

    # Remove additional white spaces
    df[2] = df[2].replace(regex=r'[\s]+', value=' ')

    # replace all stopwords
    for to_replace in stopwords_list:
        df[2] = df[2].replace(regex=r'\b{}\b'.format(to_replace), value=' ')

    # Remove additional white spaces
    df[2] = df[2].replace(regex=r'[\s]+', value=' ')

    # strip white-space
    df[2] = df[2].str.strip()

    # remove blank rows
    df = df[df[2] != '']

    print(df)

    df.to_csv(os.path.join(tmpFilePath, tweetFile), sep=DELIMITER, quotechar=QUOTECHAR, index=False, header=False)