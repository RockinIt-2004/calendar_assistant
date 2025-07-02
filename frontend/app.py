import streamlit as st
import requests

# -----------------------
# CONFIGURATION
# -----------------------
# Replace with your Railway/Render/other deployed backend URL
BACKEND_URL = "https://calendarassistant-production.up.railway.app/chat/"

# Optional: For local testing, comment above and uncomment below
# BACKEND_URL = "http://127.0.0.1:8000/chat/"

# -----------------------
# STREAMLIT PAGE SETUP
# -----------------------
st.set_page_config(page_title="🗓️ AI Appointment Scheduler", page_icon="🗓️")

st.title("🗓️ AI Appointment Scheduler")
st.caption("Chat with the assistant to book meetings on Google Calendar")

# -----------------------
# SESSION STATE
# -----------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# -----------------------
# CHAT INPUT
# -----------------------
user_input = st.chat_input("Ask to schedule a meeting...")

if user_input:
    st.session_state.chat.append(("You", user_input))

    try:
        # Call FastAPI backend
        response = requests.post(BACKEND_URL, json={"message": user_input}, timeout=10)
        data = response.json()
        bot_response = data.get("response")
        if isinstance(bot_response, dict):
            bot_response = bot_response.get("output") or str(bot_response)
    except Exception as e:
        bot_response = f"❌ Error contacting backend: {e}"

    st.session_state.chat.append(("Bot", bot_response))

# -----------------------
# DISPLAY CHAT
# -----------------------
for speaker, message in st.session_state.chat:
    with st.chat_message(speaker):
        st.markdown(message)
