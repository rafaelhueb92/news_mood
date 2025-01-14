from functools import reduce

sentiments_score= [
    {'Positive': 0.7, 'Negative': 1, 'Neutral': 0.15, 'Mixed': 0.05},
    {'Positive': 0.6, 'Negative': 1, 'Neutral': 0.1, 'Mixed': 0.1},
    {'Positive': 0.8, 'Negative': 1, 'Neutral': 0.1, 'Mixed': 0.05},
]
sentiments = ['Positive','Negative','Neutral','Mixed']
avg = lambda sentiment: sum(map(lambda x: x[sentiment],sentiments_score))/len(sentiments_score)
sentiment = reduce(lambda x,y: x if avg(x) > avg(y) else y,sentiments)
print(sentiment)