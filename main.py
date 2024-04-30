from results import YouTubeCommentsAnalyzer
from extractingcomments import YouTubeCommentsExtractor
from flask import Flask, request, render_template
from onlycomments import OnlyComments
import yt_video
from graph import SentimentResults
import json
from highting_requests import HighlightComments
from summary import GenerateSummary
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("YOUTUBE_API_KEY")

#api_key="AIzaSyCcp49l_YL1lisFQqp10ay7xnT1oCSx0qo"
youtube_analysis = SentimentResults(api_key)
app = Flask(__name__)
highlighter = HighlightComments(api_key=api_key)
analyzer = YouTubeCommentsAnalyzer(api_key)
summary=GenerateSummary()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process_input", methods=["POST"])

def take_input():
    video_id = request.form["query"]
    result = analyzer.get_result(videoID=video_id)
    my_youtube_video = yt_video.YoutubeInput(video_id=video_id)
    
    image_thumbnail_url = my_youtube_video.get_thumbnail()
    video_name = my_youtube_video.yt.title
    positive = result["positive_count"]
    neutral = result["neutral_count"]
    negative = result["negative_count"]
    
    result_list: list = [positive, neutral, negative]
    no_of_comments = sum(result_list)
    p_result_list = [round(count*100/no_of_comments, 2) for count in result_list]
    yearwise_sentiment_counts=youtube_analysis.analyze_and_save(video_id)
    years = set()
    for sentiment in yearwise_sentiment_counts.values():
        years.update(sentiment.keys())
    years_data=sorted(years)
    comments_count_yearwise = [
        [yearwise_sentiment_counts['Positive'].get(year, 0) for year in years_data],
        [yearwise_sentiment_counts['Neutral'].get(year, 0) for year in years_data],
        [yearwise_sentiment_counts['Negative'].get(year, 0) for year in years_data]
    ]

    # Serialize data to JSON format
    years_data_json = json.dumps(years_data)
    comments_count_yearwise_json = json.dumps(comments_count_yearwise)
    highlighted_comments = highlighter.highlight_requests(video_id)
    summary_result=summary.generate_negative_summary(videoID=video_id)
    
    # Print highlighted comments in terminal
    print("Highlighted Comments:")
    for comment in  highlighted_comments:
        print(comment)
   
    return render_template("data_results.html",
                           result=p_result_list,
                           result_dict=result,
                           image_thumbnail_url=image_thumbnail_url,
                           video_name=video_name,
                           comments=result_list,
                           years_data=years_data,
                           comments_count_yearwise=comments_count_yearwise_json,
                            highlighted_comments=highlighted_comments,
                           summary_final_result=summary_result
                           )

    

if __name__ == "__main__":
    app.run(debug=True)
