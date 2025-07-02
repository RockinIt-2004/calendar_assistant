import streamlit as st
import requests

st.title("🗓️ AI Appointment Scheduler")
st.text("Chat with the assistant to book meetings on Google Calendar")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Ask to schedule a meeting...")

if user_input:
    st.session_state.chat.append(("You", user_input))
    res = requests.post("http://127.0.0.1:8000/chat/", json={"message": user_input})
    bot_response = res.json().get("response", "Sorry, something went wrong.")
    st.session_state.chat.append(("Bot", bot_response))

for speaker, message in st.session_state.chat:
    st.chat_message(speaker).write(message)

    
API_URL = "http://127.0.0.1:8000/chat/"
