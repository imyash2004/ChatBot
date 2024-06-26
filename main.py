import string

import streamlit as st
import os
import streamlit_option_menu
from PIL import Image

from utils import load_gemini_pro_model,gemini_pro_vision_response,embedding_model_response



work_direc = os.path.dirname(os.path.abspath(__file__))

print(work_direc)

st.set_page_config(
    page_title="Gemini Ai",
    page_icon="💀",
    layout="centered"
)
with st.sidebar:
    selected = streamlit_option_menu.option_menu("Gemini AI", ["CHATBOT", "IMAGE CAPTIONING", "EMBEDED TEXT"],
                                                 menu_icon='robot',
                                                 icons=['chat-dots-fill', 'arrow-through-heart-fill', 'arrow-through-heart']
                                                 , default_index=0)


def role_for_streamlit(user_role):
    if(user_role=='model'):
        return "assistant"
    else:
        return user_role

if selected=="CHATBOT":
    model=load_gemini_pro_model()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])



    st.title("CHATBOT")
    for message in st.session_state.chat_session.history:
        with st.chat_message(role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)


    prompt=st.chat_input("Ask Gemini Pro...")

    if prompt:
        st.chat_message("user").markdown(prompt)
        response=st.session_state.chat_session.send_message(prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)




if selected=="IMAGE CAPTIONING":
    st.title("Snap Narate")

    upload_image=st.file_uploader("Upload an image...",type=["jpg","jpeg","png"])

    text=st.text_input("Enter what you want ...")

    if st.button("Generate"):

        image=Image.open(upload_image)

        col1,col2=st.columns(2)

        with col1:
            resized_image=image.resize((800,500))

            st.image(resized_image)

        default="write a short caption for this image..."
        if not text:
            response2 = gemini_pro_vision_response(default,image)
        else:
            response2 = gemini_pro_vision_response(text,image)

        with col2:
            st.info(response2)


if selected=="EMBEDED TEXT":
    st.title("Embedded Text")

    input_text=st.text_area(label="",placeholder="Enter the text to get the embedding")

    if st.button("get embeddings"):
        response=embedding_model_response(input_text)
        st.markdown(response)




