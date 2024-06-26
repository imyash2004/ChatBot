import json
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
work_direc = os.path.dirname(os.path.abspath(__file__))

file_path=f"{work_direc}/config.json"
data=json.load(open(file_path))


GOOGLE_API_KEY=data["GOOGLE_API_KEY"]



genai.configure(api_key=GOOGLE_API_KEY)

def load_gemini_pro_model():
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    return gemini_pro_model


def gemini_pro_vision_response(prompt,image):
    gemini_pro_vision_model=genai.GenerativeModel("gemini-pro-vision")
    response=gemini_pro_vision_model.generate_content([prompt,image])
    result=response.text
    return result


def embedding_model_response(input_text):
    embedding_model="models/embedding-001"

    embedding=genai.embed_content(model=embedding_model,content=input_text,task_type="retrieval_document")
    embedding_list=embedding["embedding"]

    return embedding_list

def transcript_video_text(video_url):
    try:
        video_id=video_url.split("=")[1]
        print(video_id)

        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text:
            transcript+= " "+ i["text"]
        return transcript
    except Exception as e:
        print(e)
        problem="Error occured please provide the valid url and check if the the video contains captions"
        return problem



def get_transcript(video_id, lang='en'):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Fetch the transcript in the specified language
        if lang in transcript_list.languages:
            transcript = transcript_list.find_transcript([lang])
        else:
            print(f"Transcript not available in {lang}, fetching in 'hi' (Hindi).")
            transcript = transcript_list.find_generated_transcript(['hi'])

        return transcript.fetch()
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for the video https://www.youtube.com/watch?v={video_id}")
    except NoTranscriptFound:
        print(f"No transcript found for the video https://www.youtube.com/watch?v={video_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None








