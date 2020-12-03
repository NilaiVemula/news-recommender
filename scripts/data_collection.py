#!/usr/bin/env python
""" Collect data from Reddit and parse news articles."""

import datetime
import secrets  # secrets.py file with username, password, etc
import string

import pandas as pd  # dataframes
import praw  # reddit API wrapper
# newspaper parser
from newspaper import Article
from newspaper import Config

# set up newspaper parser
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

# number of top posts to access from each subreddit
n_submissions = 1000


def clean_text(input_string):
    """ clean the text parsed from the news articles

    :param input_string: raw plain text from article
    :return: clean_string: cleaned article text
    """
    clean_string = (input_string.translate(str.maketrans('', '', string.punctuation))).lower()
    clean_string = ' '.join(clean_string.split())
    return clean_string


# set up instance of reddit API
r = praw.Reddit(username=secrets.REDDIT_USERNAME,
                password=secrets.REDDIT_PASSWORD,
                client_id=secrets.ID,
                client_secret=secrets.SECRET,
                user_agent='python:news-recommender:v0.0.1 (by /u/vudhnews)')
print('Logged in to Reddit.')

# urls to exclude from our analysis (mostly images, videos, etc) and other reddit comments
ignore_urls = ['redd.it', 'youtube.com', 'imgur', 'reddit.com/gallery', '.jpg', 'twitter.com', '/comments/',
               'reddit.com', 'youtu.be', '.jpeg', '.png', 'gfycat.com' ]

# subreddits to scrape
subreddits = [
    # left-leaning subreddits
    'Liberal',
    'Democrats',
    'LateStageCapitalism',
    'JoeBiden',
    # right-leaning subreddits
    'Republican',
    'Conservative',
    'donaldtrump',
    'Anarcho_Capitalism'
]

# run scraping code for each subreddit
for subreddit in subreddits:
    # hold data in a list where each datapoint is a tuple
    data = []

    # access top posts
    all_submissions = r.subreddit(subreddit).top(limit=n_submissions)
    print(f'Accessed {n_submissions} submissions from r/{subreddit}.')

    # for each post
    for submission in all_submissions:
        # choose only news articles
        if not any(url in submission.url for url in ignore_urls):
            # parse article and clean text
            try:
                html = Article(submission.url, config=config)
                html.download()
                html.parse()
                website_text = clean_text(html.text)
            except:
                print("parse failure: ", submission.url)
                website_text = float('NaN')

            # save post data in a tuple and append it to the data list
            data_point = (
                submission.id,
                datetime.datetime.fromtimestamp(submission.created),
                subreddit,
                submission.title,
                submission.url,
                submission.author,
                submission.score,
                round((1 / submission.upvote_ratio) * submission.score * (1 - submission.upvote_ratio)),
                website_text,
            )
            data.append(data_point)

    # convert data list to a dataframe and save it as a csv file
    file_name = f"../data/{subreddit}_top_articles.csv"
    df = pd.DataFrame(
        data,
        columns=[
            'submission_id',
            'posted_time_stamp',
            'subreddit',
            'title',
            'url',
            'author',
            'upvotes',
            'downvotes',
            'article_text'
        ]
    )
    df.to_csv(file_name, index=False)
    print(f"Finished collecting data for r/{subreddit}. Saved data at {file_name}.")

print("Finished")
