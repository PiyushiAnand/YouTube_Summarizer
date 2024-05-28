from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from transformers import pipeline
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class GenerateAndSummarize(Resource):
    def extract_video_id(self, youtube_url):
        # Regex to extract video id from various YouTube URL formats
        video_id_match = re.match(r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)|.*[?&]v=)|youtu\.be/)([^"&?/ ]{11})', youtube_url)
        return video_id_match.group(1) if video_id_match else None
    
    def get(self):
        youtube_url = request.args.get('youtube_url')
        if not youtube_url:
            return jsonify({"error": "No YouTube URL provided"}), 400
        
        # Extract the video ID from the YouTube URL
        video_id = self.extract_video_id(youtube_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        try:
            # Fetch the transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = " ".join(entry['text'] for entry in transcript_list)
            
            # Summarize the transcript
            summarization = pipeline("summarization", model="facebook/bart-large-cnn")
            summary_texts = []
            batch_size = 1000  # Adjust the batch size as needed
            
            # Split the transcript into smaller batches and process each batch
            for i in range(0, len(full_transcript), batch_size):
                batch = full_transcript[i:i + batch_size]
                summary_text = summarization(batch, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                summary_texts.append(summary_text)
            
            # Concatenate the summaries from all batches
            full_summary = ' '.join(summary_texts)
            return jsonify({"summary": full_summary})
        
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            return jsonify({"error": str(e)}), 404

api.add_resource(GenerateAndSummarize, '/api/summarize')
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
   
    app.run(debug=True)
