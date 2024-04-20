import streamlit as st
import google.generativeai as genai
import time

# Set page title and favicon
st.set_page_config(page_title="Data Science Tutor", page_icon="📊")

# Title and description
st.title("🤖 Data Science Tutor")
st.markdown("*Powered by Gemini 1.5 Pro🚀*")
st.markdown("Hello!, I'm Gemini the Data Science Tutor! I'm here to help with your data science questions.")

# Read the api key
with open("API Key.txt", "r") as f:
    key = f.read().strip()

# Configure the API Key
genai.configure(api_key=key)

# Initiate a Gen AI Model with system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="You are a helpful AI Assistant,Provide accurate and relevant information."
)

# Chat History
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat Object
chat = model.start_chat(history=st.session_state["chat_history"])

for msg in chat.history:
    st.chat_message(msg.role).write(msg.parts[0].text)

# Function to stream response data
def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.06)

user_prompt = st.chat_input()

if user_prompt:
    st.chat_message("user").write(user_prompt)
    try:
        response = chat.send_message(user_prompt).parts[0].text
        st.chat_message("AI").write(stream_data(response))
    except genai.generation_types.StopCandidateException as e:
        st.warning(f"StopCandidateException: {e}")
    st.session_state["chat_history"] = chat.history

# Run the App
# streamlit run app.py    
