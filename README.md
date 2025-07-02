# 📅 AI-Powered Google Calendar Scheduling Assistant

A conversational AI assistant that helps users list their upcoming Google Calendar events and book new meetings using natural language.

✅ Fully conversational interface (Streamlit)  
✅ Integrates with Google Calendar API  
✅ Deployed backend (FastAPI) on Railway  
✅ Deployed frontend (Streamlit) on Streamlit Cloud

---

## 🚀 Live Demo

- **Backend (FastAPI) on Railway**: ([railway-backend-url](https://calendarassistant-production.up.railway.app/))
- **Frontend (Streamlit) on Streamlit Cloud**: ([streamlit-app-url](https://calendarassistant-mwlg8xyxx6mhuu8o8btrst.streamlit.app/))

---

## 🗂️ Project Structure
├── backend/
│ ├── main.py
│ ├── agent.py
│ ├── calendar_utils.py
│ ├── requirements.txt
│ └── ...
└── frontend/
├── app.py
├── requirements.txt
└── ...


---

## ⚙️ Features

✅ List upcoming Google Calendar events  
✅ Book new events by providing title, start, and end time  
✅ Multi-turn conversational flow with memory  
✅ Google Calendar API integration via service account  

---

## 💻 Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM**: Gemini 1.5 Flash (via LangChain)
- **Hosting**:
  - Railway (Backend)
  - Streamlit Cloud (Frontend)
- **Auth**: Google Service Account

---

## 🎯 How It Works

1️⃣ User types a natural language request (e.g. *"Schedule a meeting at 3 PM today"*)  
2️⃣ Streamlit app sends the message to the FastAPI backend  
3️⃣ LLM parses the intent and required fields  
4️⃣ Backend calls Google Calendar API to list or book events  
5️⃣ Response is returned and displayed in the chat  

---

## 🛠️ Local Development

### Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
