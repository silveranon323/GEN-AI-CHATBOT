import os
import time
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="Advanced Gemini ChatBot", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #f4f4f9;
        color: #333;
    }
    .stTextInput input {
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 12px;
        font-size: 18px;
        color: #333;
        background-color: #fff;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 18px;
    }
    .stTitle {
        color: #4CAF50;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    .stSubheader {
        color: #333;
        font-size: 24px;
        font-weight: bold;
    }
    .chat-bubble {
        padding: 15px;
        margin: 8px;
        border-radius: 12px;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #4CAF50;
        color: white;
        align-self: flex-end;
    }
    .ai-bubble {
        background-color: #e1e1e8;
        color: black;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 15px;
    }
    .timestamp {
        font-size: 12px;
        color: #888;
        text-align: right;
    }
    .header-container {
        text-align: center;
        padding: 20px;
        background-color: #4CAF50;
        color: white;
        border-radius: 15px;
    }
    .header-container h1 {
        margin: 0;
        font-size: 36px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-container'><h1>Advanced Gemini ChatBot</h1></div>", unsafe_allow_html=True)

st.sidebar.title("Settings")
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"], index=0)
font_size = st.sidebar.slider("Font Size:", 14, 24, 18)
st.sidebar.title("Options")
clear_chat = st.sidebar.button("Clear Chat")
new_conversation = st.sidebar.button("Start New Conversation")
custom_greeting = st.sidebar.text_input("Custom Greeting Message:", "Hello! How can I assist you today?")
save_history = st.sidebar.button("Save Chat History")
load_history = st.sidebar.button("Load Chat History")
download_history = st.sidebar.button("Download Chat History")
chatbot_name = st.sidebar.text_input("Chatbot Name:", "Gemini")

if theme == "Dark":
    st.markdown(f"""
        <style>
        body {{
            background-color: #333;
            color: #f4f4f9;
        }}
        .stTextInput input {{
            border: 2px solid #4CAF50;
            border-radius: 15px;
            padding: 12px;
            font-size: {font_size}px;
            color: #f4f4f9;
            background-color: #555;
        }}
        .stButton button {{
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: {font_size}px;
        }}
        .stTitle, .stSubheader {{
            color: #4CAF50;
        }}
        .chat-bubble {{
            background-color: #444;
            color: #f4f4f9;
        }}
        .user-bubble {{
            background-color: #4CAF50;
            color: white;
        }}
        .ai-bubble {{
            background-color: #666;
            color: #f4f4f9;
        }}
        .timestamp {{
            color: #aaa;
        }}
        .header-container {{
            background-color: #4CAF50;
            color: white;
        }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <style>
        body {{
            background-color: #f4f4f9;
            color: #333;
        }}
        .stTextInput input {{
            border: 2px solid #4CAF50;
            border-radius: 15px;
            padding: 12px;
            font-size: {font_size}px;
            color: #333;
            background-color: #fff;
        }}
        .stButton button {{
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: {font_size}px;
        }}
        .stTitle, .stSubheader {{
            color: #4CAF50;
        }}
        .chat-bubble {{
            background-color: #fff;
            color: #333;
        }}
        .user-bubble {{
            background-color: #4CAF50;
            color: white;
        }}
        .ai-bubble {{
            background-color: #e1e1e8;
            color: black;
        }}
        .timestamp {{
            color: #888;
        }}
        .header-container {{
            background-color: #4CAF50;
            color: white;
        }}
        </style>
    """, unsafe_allow_html=True)

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

if new_conversation:
    st.session_state['conversation'] = []

if clear_chat:
    st.session_state['conversation'] = []

if not st.session_state['conversation'] and custom_greeting:
    st.session_state['conversation'].append({
        "role": "assistant",
        "content": custom_greeting,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    })

def display_chat():
    for entry in st.session_state['conversation']:
        role = entry['role']
        content = entry['content']
        timestamp = entry['timestamp']
        bubble_class = 'user-bubble' if role == 'user' else 'ai-bubble'
        name_display = f"{chatbot_name}:" if role == 'assistant' else "You:"
        st.markdown(
            f"<div class='chat-container'><div class='chat-bubble {bubble_class}'>{name_display} {content}</div>"
            f"<div class='timestamp'>{timestamp}</div></div>",
            unsafe_allow_html=True
        )

input_placeholder = "Type your question here..."
user_input = st.text_input(input_placeholder, key="input")

submit = st.button("Send")

def add_message(role, content):
    st.session_state['conversation'].append({
        "role": role,
        "content": content,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    })

if submit and user_input:
    add_message("user", user_input)
    with st.spinner("Gemini is thinking..."):
        response = get_gemini_response(user_input)
        for chunk in response:
            add_message("assistant", chunk.text)
            st.experimental_rerun()

def save_chat_history():
    with open("chat_history.json", "w") as f:
        json.dump(st.session_state['conversation'], f)
    st.success("Chat history saved successfully!")

def load_chat_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as f:
            st.session_state['conversation'] = json.load(f)
        st.success("Chat history loaded successfully!")
    else:
        st.error("No chat history file found.")

def download_chat_history():
    chat_history = json.dumps(st.session_state['conversation'])
    st.download_button(
        label="Download Chat History",
        data=chat_history,
        file_name="chat_history.json",
        mime="application/json"
    )

if save_history:
    save_chat_history()

if load_history:
    load_chat_history()

if download_history:
    download_chat_history()

def add_voice_input():
    st.markdown("""
        <script>
        const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        
        function startListening() {
            recognition.start();
        }
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            window.parent.postMessage({type: 'VOICE_INPUT', data: transcript}, '*');
        };
        
        document.addEventListener('DOMContentLoaded', () => {
            const button = document.getElementById('voice-input-button');
            button.addEventListener('click', startListening);
        });
        </script>
        <button id="voice-input-button">🎤 Speak</button>
    """, unsafe_allow_html=True)
    
    st.write("Speak your question and it will be transcribed.")

    st.markdown("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'VOICE_INPUT') {
                const inputElement = document.getElementById('input');
                inputElement.value = event.data.data;
                inputElement.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });
        </script>
    """, unsafe_allow_html=True)

add_voice_input()

st.subheader("Conversation History")
display_chat()

st.sidebar.markdown("---")
st.sidebar.text("Developed by Hem Kishore Pradhan")
