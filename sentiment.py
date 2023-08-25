import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
#nltk.download('vader_lexicon')


df = pd.read_csv("Master.csv")
df["Tweet"] = df["Tweet"].astype(str).str.lower()

df["tweet_token"] = df["Tweet"].apply(RegexpTokenizer("\w+").tokenize)

stopwords = nltk.corpus.stopwords.words("english")

df["tweet_token"] = df["tweet_token"].apply(lambda x: [item for item in x if item not in stopwords])

df["tweet_string"] = df["tweet_token"].apply(lambda x: " ".join([item for item in x]))

all_words = " ".join([word for word in df["tweet_string"]])
tokenized_words = nltk.tokenize.word_tokenize(all_words)

fdist = FreqDist(tokenized_words)

#print(len(fdist))
#newDict = {}

#for key in fdist:
#    if fdist[key] >= 3:
#        newDict[key] = fdist[key]
#print(len(newDict))

df["tweet_string_fdist"] = df["tweet_token"].apply(lambda x: " ".join([item for item in x if fdist[item] >= 3 ]))

df['tweet_string_lem'] = df['tweet_string_fdist'].apply(WordNetLemmatizer().lemmatize)




analyzer = SentimentIntensityAnalyzer()
df['polarity'] = df['tweet_string_lem'].apply(lambda x: analyzer.polarity_scores(x))

df = pd.concat(
    [df.drop(['polarity'], axis=1),
     df['polarity'].apply(pd.Series)], axis=1)

df.to_excel('Master_sentiment.xlsx')
