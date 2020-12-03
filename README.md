# news-recommender

Category: Text Analysis/ Natural Language Processing

**Goal**: Create a news recommendation system that selects articles from different parts of the political spectrum.

1. Scrape posts from liberal-leaning subreddits (`r/liberal`, etc) and from conservative-leaning subreddits (`r/conservative`, etc).
2. Select posts that share a news article. Store a link to the article and a label based on the subreddit that it was posted in.
3. Vectorize each article with `word2vec` using a pre-trained model.
4. Build a vector space describing the conservative and liberal articles.
5. Make a binary classifier that takes in an article as input and categorizes it as either liberal or conservative for novel articles. 
6. Build a website where you can search a topic and then get news recommendations of different biases.



**Rubric**: 

- Use the Reddit API to access data (2 pts)
- Clean and select the data in Python (5 pts)
- Embed word vectors using `word2vec` to categorize each post/article (5 pts)
- Train a machine learning model to categorize between conservative-leaning and liberal-leaning news articles (10 pts)
- Communicated 250-500 words explaining the project goals and outcomes. (10 pts)
- Build a web API (Extra credit: 3 pts)

Basic Text Analysis Rubric:

Choose a relevant text. Be able to explain why you chose that text.
Use the various functions, like the one in the Gandhi speech analysis, and see what you learn about the text.
Write a short paper describing what you found. You may write this a scientific paper (thesis, testing, conclusions) or as a more narrative/historical paper (intro, discussion, conclusions). The paper should be around 750 words and should contain graphs taken from your R work as well as snippets of the code you used.
Turn in the paper.

Contacts for help:

Steve Bascoff

Cliff Anderson

