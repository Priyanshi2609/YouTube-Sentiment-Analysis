from results import YouTubeCommentsAnalyzer
from extractingcomments import YouTubeCommentsExtractor

api_key="AIzaSyCcp49l_YL1lisFQqp10ay7xnT1oCSx0qo"

class  HighlightComments():
    def __init__(self, api_key):
        self.api_key = api_key
        self.analyzer = YouTubeCommentsAnalyzer(api_key)
        self.extractor = YouTubeCommentsExtractor(api_key)
    def highlight_requests(self, video_id):
        cleaned_comments_list=self.analyzer.get_cleaned_comments(video_id)
        request_comments = []
        suggestion_comments = []

        
        request_keywords = [
    "request",
    "please make a video about",
    "can you talk about",
    "can you make a video on",
    "could you make a video about",
    "it would be great if you made a video on",
    "I'd like to see a video about",
    "could you talk about",
    "can you create a video on",
    "make a video on",
    "do a video on",
    "explore",
    "address",
    "touch upon"
]

        suggestion_keywords = [
    "suggest",
    "you should make a video about",
    "you can talk about",
    "you can make a video on",
    "you could make a video about",
    "you might consider making a video on",
    "it would be nice if you made a video on",
    "how about making a video on",
    "have you considered making a video on",
    "why not make a video on",
    "you might want to talk about",
    "have you thought about discussing",
    "you might want to explore",
    "I suggest",
    "it would be great if you talked about",
    "you might want to address",
    "you could touch upon"
]

        for comment in cleaned_comments_list:
            
            if any(keyword in comment.lower() for keyword in request_keywords):
                request_comments.append(comment)
            
            elif any(keyword in comment.lower() for keyword in suggestion_keywords):
                suggestion_comments.append(comment)

        return request_comments+ suggestion_comments
    







    

    