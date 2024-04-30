'''from results import YouTubeCommentsAnalyzer
from extractingcomments import YouTubeCommentsExtractor
import pandas as pd
api_key="AIzaSyCcp49l_YL1lisFQqp10ay7xnT1oCSx0qo"
analyzer = YouTubeCommentsAnalyzer(api_key)
result = analyzer.get_sentiment_for_each_comment(videoID="bI6q16ffdgQ")
df=pd.read_csv('youtube_comments.csv')
#print(result)
df['Sentiment Type']=result
df.to_csv('Sentiment_final_results.csv',index=False)
print(len(result))

df = pd.read_csv('Sentiment_final_results.csv')

# Calculate value counts for each comment year-wise
#value_counts_yearwise = df.groupby('Published Year')['Sentiment Type'].value_counts()
value_counts_yearwise = df.groupby(['Published Year', 'Sentiment Type']).size().unstack(fill_value=0)
value_counts_dict = value_counts_yearwise.to_dict()

# Print the dictionary
print(value_counts_dict)'''
import json
import pandas as pd
from results import YouTubeCommentsAnalyzer
from extractingcomments import YouTubeCommentsExtractor
  
class  SentimentResults():
    def __init__(self, api_key):
        self.api_key = api_key
        self.analyzer = YouTubeCommentsAnalyzer(api_key)
        self.extractor = YouTubeCommentsExtractor(api_key)
    def analyze_and_save(self, video_id):
        result = self.analyzer.get_sentiment_for_each_comment(videoID=video_id)
        self.extractor.extract_comments(video_id)
        df = pd.read_csv('youtube_comments.csv')
        df['Sentiment Type'] = result
        df.to_csv('Sentiment_final_results.csv', index=False)
        df = pd.read_csv('Sentiment_final_results.csv')
        value_counts_yearwise = df.groupby(['Published Year', 'Sentiment Type']).size().unstack(fill_value=0)
        value_counts_dict = value_counts_yearwise.to_dict()
        return value_counts_dict
'''
api_key = "AIzaSyCcp49l_YL1lisFQqp10ay7xnT1oCSx0qo"
video_id = "bI6q16ffdgQ"
youtube_analysis = SentimentResults(api_key)
yearwise_sentiment_counts=youtube_analysis.analyze_and_save(video_id)
print(yearwise_sentiment_counts)
years = set()
for sentiment in yearwise_sentiment_counts.values():
    years.update(sentiment.keys())
years_data=sorted(years)
print(years_data)

comments_count_yearwise = [
        [yearwise_sentiment_counts['Positive'].get(year, 0) for year in years_data],
        [yearwise_sentiment_counts['Neutral'].get(year, 0) for year in years_data],
        [yearwise_sentiment_counts['Negative'].get(year, 0) for year in years_data]
    ]

    # Serialize data to JSON format
years_data_json = json.dumps(years_data)
comments_count_yearwise_json = json.dumps(comments_count_yearwise)
print(comments_count_yearwise_json)'''
