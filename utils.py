import json
import os
import google.generativeai as genai
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



