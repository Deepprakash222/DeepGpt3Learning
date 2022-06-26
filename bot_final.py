from os import environ
import streamlit as st
from streamlit_chat import message as st_message
from openai_api import *
from stqdm import stqdm


if os.getenv("OPENAI_API_KEY")!="":
    pass
else:
    api=st.text_input("Enter your OpenAI API",type="password")
    if api!="":
        st.write("API Successfully acepted")
    os.environ['OPENAI_API_KEY'] = api


openai.api_key = os.getenv("OPENAI_API_KEY")
approved=[]
paragraph=[]
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 800px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []
    intro="Hello there, you are with King! I am an Artificial Intelligent Assistant for helping you create beautiful, inspired, horror, supernatural fiction, suspense, crime, science-fiction, fantasy articles, and novels. Please tell me if you have an idea for a title for what you want to write about.\n"
    st.session_state.history.append({"message": intro, "is_user": False})
if 'liked' not in st.session_state:
    st.session_state['liked'] = []
if 'para' not in st.session_state:
    st.session_state['para'] = []

st.title("King:- Your Friend in need")



def store_content(user_insertion: Text):
  if re.search(r'(title approved)', user_insertion, re.IGNORECASE):
    st.session_state.liked.append(st.session_state.history[-1])
    return chatbot(user_insertion)
  elif re.search(r'(sub-headers approved)', user_insertion, re.IGNORECASE):
    st.session_state.liked.append(st.session_state.history[-1])
    return chatbot(user_insertion)
  elif re.search(r'(expand sub-headers)', user_insertion, re.IGNORECASE):
    for i in stqdm(range(len(st.session_state.liked))):
        paragraph.append(st.session_state.liked[i]["message"])
        st.session_state.para.append(paragraph[-1])
        st.session_state.para.append(paragraph_generator(paragraph[-1]))
        st.session_state.para.append("\n")
        
    return "Sorry if it took much time. I hope you would like the content of each sub-header."
  elif re.search(r'(content approved)', user_insertion, re.IGNORECASE):
    return "I'm happy that I was able to help you. Please give us feedback about your satisfaction this would mean a lot to me as an author."
  else:
    return chatbot(user_insertion)

def generate_answer():

    user_message = st.session_state.input_text
    result = store_content(user_message)
    for i in stqdm(range(len(st.session_state.liked))):
        approved.append(st.session_state.liked[i]["message"])
   
    st.sidebar.text_area(label="Approved Suggestion List:", value="\n".join(approved), height=20)
    if len(st.session_state.para)!=0:
        st.sidebar.text_area(label=st.session_state.liked[0]["message"], value="\n".join(st.session_state.para), height=350)

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": result, "is_user": False})


st.text_input("Talk to the bot", key="input_text", on_change=generate_answer,max_chars=100000)



k=1
for chat in (reversed(st.session_state.history)):
    st_message(**chat,key=str(k)) 
    k=k+1


