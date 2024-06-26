import string

import streamlit as st
import os
import streamlit_option_menu
from PIL import Image

from utils import load_gemini_pro_model, gemini_pro_vision_response, embedding_model_response, transcript_video_text

work_direc = os.path.dirname(os.path.abspath(__file__))

print(work_direc)

st.set_page_config(
    page_title="Gemini Ai",
    page_icon="💀",
    layout="centered"
)
with st.sidebar:
    selected = streamlit_option_menu.option_menu("Gemini AI",
                                                 ["CHATBOT", "IMAGE CAPTIONING", "EMBEDED TEXT", "UTUBE TRANSCRIBER"],
                                                 menu_icon='robot',
                                                 icons=['chat-dots-fill', 'arrow-through-heart-fill',
                                                        'arrow-through-heart', 'activity']
                                                 , default_index=0)


def role_for_streamlit(user_role):
    if (user_role == 'model'):
        return "assistant"
    else:
        return user_role


if selected == "CHATBOT":
    model = load_gemini_pro_model()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("📀CHATBOT")
    for message in st.session_state.chat_session.history:
        with st.chat_message(role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    prompt = st.chat_input("Ask Gemini Pro...")

    if prompt:
        st.chat_message("user").markdown(prompt)
        response = st.session_state.chat_session.send_message(prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)

if selected == "IMAGE CAPTIONING":
    st.title("👾Snap Narate")

    upload_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    text = st.text_input("Enter what you want ...")

    if st.button("Generate"):

        image = Image.open(upload_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))

            st.image(resized_image)

        default = "write a short caption for this image..."
        if not text:
            response2 = gemini_pro_vision_response(default, image)
        else:
            response2 = gemini_pro_vision_response(text, image)

        with col2:
            st.info(response2)

if selected == "EMBEDED TEXT":
    st.title("👾Embedded Text")

    input_text = st.text_area(label="", placeholder="Enter the text to get the embedding")

    if st.button("get embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)

if selected == "UTUBE TRANSCRIBER":
    st.title("⏩UTUBE TRANSCRIBER")

    utube_link = st.text_input("Enter You tube video link")
    if utube_link:
        video_id = utube_link.split("v=")[1].split("&")[0]

        thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"

        st.image(thumbnail_url, use_column_width=True)



    model = load_gemini_pro_model()
    prompt = """"You are a youtube video summarizer.You will be taking the transcript text
        and summarize the entire video and provide the important summary in points
        within 300 words.The transcript text will be appended here :"""

    if st.button("Get Detailed Notes"):
        transcript_text = transcript_video_text(utube_link)

        if transcript_text:
            response = model.generate_content(prompt + transcript_text)
            st.write("#####Detailed Notes")
            st.markdown(response.text)
