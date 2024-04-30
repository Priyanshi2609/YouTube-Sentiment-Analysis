from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import numpy as np
import spacy

class GenerateSummary:
    def __init__(self):
        self.stopwords = list(STOP_WORDS)
        self.nlp = spacy.load('en_core_web_sm')

    def generate_negative_summary(self, videoID):
        try:
            # Get transcript of the YouTube video
            transcript = YouTubeTranscriptApi.get_transcript(videoID)
        except Exception as e:
            print("Error:", e)
            return None
        
        text = ' '.join([line['text'] for line in transcript])
        doc = self.nlp(text)
        
        word_frequency = {}
        for word in doc:
            if word.text.lower() not in self.stopwords and word.text.lower() not in punctuation:
                if word.text not in word_frequency.keys():
                    word_frequency[word.text] = 1
                else:
                    word_frequency[word.text] += 1
        max_frequency = max(word_frequency.values()) 
        for word in word_frequency.keys():
            word_frequency[word] = word_frequency[word] / max_frequency
        
        sentence_tokens = [sent for sent in doc.sents]          

        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequency.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequency[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequency[word.text.lower()]
        
        select_length = int(len(sentence_tokens) * 0.05)
        summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)
        return summary

summary = GenerateSummary()

