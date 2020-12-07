#### import packages

# webapp
import streamlit as st

# data analysis
import pandas as pd
import numpy as np

# get news articles
from GoogleNews import GoogleNews

# parse news articles
from newspaper import Article
from newspaper import Config
import requests
import string

# process text
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

# word2vec
import gensim
import pickle

# classification
import gensim

print("SUCCESSFULLY IMPORTED ALL LIBRARIES")

st.write("This is an application for finding news articles that are predicted to be popular in left-leaning or right-reading subreddits. Give me a few moments while I get set-up...")

#### set up models

# set up google news
googlenews = GoogleNews()
googlenews = GoogleNews(lang='en')
googlenews = GoogleNews(encode='utf-8')

# set up newspaper parser
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

# set up word2vec model
filename = 'models/GoogleNews-vectors-negative300.bin.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(filename, binary=True)

# set up classification model
classifier=pickle.load(open('models/xgboost_trained.pickle','rb'))



### DATA INPUT

st.write("Please enter a news topic below. The default is 'president'.")

user_input = st.text_input("news topic", 'president')

st.write(f"Thanks! Give me a few minutes to run your analysis on the search term: {user_input}. You might want to grab a coffee...")

### Run analysis

# get news articles
googlenews.get_news(user_input)
articles = googlenews.get_links()
if len(articles)>25:
    articles = articles[:25]

def clean_text(input_string):
    """ clean the text parsed from the news articles

    :param input_string: raw plain text from article
    :return: clean_string: cleaned article text
    """
    clean_string = (input_string.translate(str.maketrans('', '', string.punctuation))).lower()
    clean_string = ' '.join(clean_string.split())
    return clean_string

st.write("Good news! I found some news articles using Google News!")

# parse articles
data = {}

for google_news_article in articles:
    google_news_article = 'http://' + google_news_article
    r = requests.get(google_news_article)
    article_url = r.url

    try:
        html = Article(article_url, config=config)
        html.download()
        html.parse()
        website_text = clean_text(html.text)
        data[article_url] = website_text
    except Exception as e:
        pass
    
df = pd.DataFrame(data.items(), columns=['url','website_text'])
df.dropna(inplace=True)
df = df[df['website_text'].str.len() > 50]

st.write("I just finished reading through those articles. They seem interesting!")

# nlp pre-processing

stop_words=stopwords.words('english')+list(string.punctuation) + ['“','”','–','—','’']

word_frequencies = []

for index, row in df.iterrows():
    #print(index, row['subreddit'])
    cleaneddoc=[word.lower() for word in word_tokenize(row['website_text']) if word not in stop_words]
    word_frequencies.append(FreqDist(cleaneddoc))
    #print([FreqDist(cleaneddoc)])

df['word_frequencies'] = word_frequencies


# word2vec
all_vectors=np.zeros((len(df),300))
total_zeros=0
# iterate through each row (document) in the dataframe
for index, row in df.iterrows(): 
    total_words_from_doc=0
    document_vector=np.zeros((300,))
    for word in row['word_frequencies'].keys():
        frequency = row['word_frequencies'][word]
        try:
            document_vector+=model[word]*(frequency)
            total_words_from_doc+=frequency
        except:
            pass
    if total_words_from_doc>0:
        all_vectors[index]=document_vector/total_words_from_doc
    else:
        total_zeros+=1
        all_vectors[index]=document_vector


st.write("Woohoo! I created a 300-dimensional vector space to describe these articles using ~linear algebra~. Let me classify them now! Stay tuned!")

# classification
predictions = classifier.predict_proba(all_vectors)
df['prediction'] = predictions[:,0]

df.sort_values(by=['prediction'], inplace=True)

googlenews.clear()

#### DISPLAY OUTPUT

st.header("Left-leaning")

if(len(df[df['prediction'] > 0.5])):
    st.write(df['url'].iloc[0])
    
else:
    st.write('Sorry, I could not find any articles for you.')


st.header("Right-leaning")

if(len(df[df['prediction'] < 0.5])):
    st.write(df['url'].iloc[-1])
else:
    st.write('Sorry, I could not find any articles for you.')
