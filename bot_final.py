from typing import Literal
import streamlit as st
from streamlit_chat import message as st_message

if "history" not in st.session_state:
    st.session_state.history = []
    intro="King is an intelligent assistant author of horror, supernatural fiction, suspense, crime, science-fiction, and fantasy novels inspired by Stephen King. It has great ideas for articles, blogs, and movie creation. It is helping to provide article titles, sub-headers for the article's title, and also great, flourishing, expensive vocabularies within paragraphs. If the user said no to something, King will offer to help the user. If the user liked an idea, King politely ask for confirmation."
    st.session_state.history.append({"message": intro, "is_user": False})
if 'liked' not in st.session_state:
    st.session_state['liked'] = []

st.sidebar.title("Kings")
def first_api(input):
    return "ABC" + input
def second_api(input):
    return "CDE" +input

def generate_answer():
    user_message = st.session_state.input_text
    if "Thanks. Can you check" in user_message:
        result= second_api(user_message)
        last_recommendation= st.session_state.history[-1]["message"]
        st.session_state.liked.append({"message": last_recommendation, "is_user": True})
        st.session_state.liked.append({"message": user_message, "is_user": True})
        st.session_state.liked.append({"message": result, "is_user": False})
    else:
        result = first_api(user_message)

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": result, "is_user": False})




for chat in (st.session_state.history):
    st_message(**chat)  # unpacking

st.text_input("Talk to the bot", key="input_text", on_change=generate_answer,max_chars=100000)
