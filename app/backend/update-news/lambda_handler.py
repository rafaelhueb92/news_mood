import os
import requests
import boto3
from functools import reduce
from datetime import datetime, timedelta

NEWS_API_TOKEN = os.getenv("NEWS_API_TOKEN")
NEWS_API_URL = os.getenv("NEWS_API_URL")

subjects = ['bitcoin','technology','sports','politics','world','economy','health']

def get_news(subject,today):

    yesterday = (today - timedelta(days=1))
    filters = f'q={subject}&pageSize=5&sortBy=relevancy&page=1&from={yesterday.strftime("%Y-%m-%d")}&to={today.strftime("%Y-%m-%d")}&apiKey={NEWS_API_TOKEN}&language=en'

    response = requests.get(f'{NEWS_API_URL}/everything?{filters}')
    
    # Check for HTTP request errors
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()

    if data['totalResults'] > 0:
        articles = list(map(lambda x : f"{x['title']} \ {x['description']}",data['articles']))
        return articles
    else:
        return []
    
def get_sentiment(articles):
    client = boto3.client('comprehend')
    response = client.batch_detect_sentiment(TextList=articles,LanguageCode='en')
    sentiments_score = list(map(lambda x: x['SentimentScore'] ,response['ResultList']))
    sentiments = ['Positive','Negative']#,'Neutral','Mixed']
    avg = lambda sentiment: sum(map(lambda x: x[sentiment],sentiments_score))/len(sentiments_score)
    sentiment = reduce(lambda x,y: x if avg(x) > avg(y) else y,sentiments)

    return 'Good' if sentiment == 'Positive' else 'Bad'

def lambda_handler(event, context):

    subject = event['subject']

    if subject not in subjects:
        raise ValueError(f'Subject {subject} not valid, please select a valid subject')

    today = datetime.now()

    articles = get_news(subject[2],today)

    return get_sentiment(articles)

event = {
    'subject': 'bitcoin'
}

sentiment = lambda_handler(event,None)

print(sentiment)