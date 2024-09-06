import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()

st.set_page_config(
    page_title="GenAI-ChatBot",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

def save_chat_history(filename):
    with open(filename, "w") as file:
        for message in st.session_state.chat_session.history:
            role = translate_role_for_streamlit(message.role)
            file.write(f"{role}: {message.parts[0].text}\n")

def load_chat_history(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            lines = file.readlines()
        return lines
    return None

def reset_session():
    st.session_state.chat_session = model.start_chat(history=[])

if "chat_session" not in st.session_state:
    reset_session()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

st.title("🤖 Gen AI - ChatBot")

st.markdown(f"""
    <style>
    body {{
        background-color: {'#333' if st.session_state.theme == 'dark' else '#FFF'};
        color: {'#FFF' if st.session_state.theme == 'dark' else '#000'};
    }}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Chat Settings")
new_chat = st.sidebar.button("New Chat")
if new_chat:
    reset_session()
    st.experimental_rerun()

save_chat = st.sidebar.button("Save Chat History")
if save_chat:
    save_chat_history("chat_history.txt")
    st.sidebar.success("Chat history saved!")

load_chat = st.sidebar.button("Load Chat History")
if load_chat:
    loaded_history = load_chat_history("chat_history.txt")
    if loaded_history:
        reset_session()
        for line in loaded_history:
            role, text = line.strip().split(": ", 1)
            st.session_state.chat_session.history.append(
                {"role": "model" if role == "assistant" else "user", "parts": [{"text": text}]}
            )
        st.sidebar.success("Chat history loaded!")
    else:
        st.sidebar.error("No chat history found!")

delete_chat = st.sidebar.button("Delete Chat History")
if delete_chat:
    reset_session()
    st.experimental_rerun()

toggle_theme = st.sidebar.button("Toggle Dark Mode")
if toggle_theme:
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.experimental_rerun()

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Message Bot...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.sidebar.header("Model Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 1, 2048, 512)
st.sidebar.text(f"Temperature: {temperature}")
st.sidebar.text(f"Max Tokens: {max_tokens}")

st.session_state.chat_session.temperature = temperature
st.session_state.chat_session.max_tokens = max_tokens
