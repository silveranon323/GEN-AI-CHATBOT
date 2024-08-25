import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
st.set_page_config(page_title="Conversational Q/A ChatBot", page_icon="🤖", layout="wide")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

st.markdown("""
    <style>
    body {
        background-color: #f0f0f5;
    }
    .stTextInput input {
        border: 2px solid #FF6F61;
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
        color: #333;
    }
    .stButton button {
        background-color: #FF6F61;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 18px;
    }
    .stProgress > div > div > div {
        background-color: #FF6F61;
    }
    .stTitle {
        color: #FF6F61;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    .stSubheader {
        color: #333;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Conversational Q/A ChatBot")

chat = ChatOpenAI(temperature=0.5, openai_api_key=api_key)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="You are a comedian AI Assistant")
    ]

def get_chatmodel_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    with st.spinner("Generating response..."):
        answer = chat(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

input = st.text_input("Input:", key="input")
submit = st.button("Ask any Question")

if submit and input:
    st.subheader("The response is")
    response = get_chatmodel_response(input)
    st.write(response)
