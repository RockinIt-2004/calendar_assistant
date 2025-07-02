from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.tools import StructuredTool
from calendar_utils import get_free_slots, create_event
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --------------------------------------
# Initialize Gemini LLM
# --------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    system_message=(
        "You are a helpful Google Calendar scheduling assistant. "
        "You have two tools: ListFreeSlots and BookSlot. "
        "You must help the user book meetings on Google Calendar. "
        "When the user wants to book an event, you MUST confirm you have ALL these fields: "
        "- title: a short descriptive title "
        "- start: ISO 8601 format like 2025-07-01T15:00:00 "
        "- end: ISO 8601 format "
        "If anything is missing or vague, you must ASK the user to clarify or provide it. "
        "NEVER call BookSlot unless you have all 3 fields clearly and correctly. "
        "Use friendly, natural conversation to get the info. "
        "When listing events, format times clearly."
    )
)

print("[Agent init] Google API Key loaded")
print("[Agent init] Model:", llm.model)

# --------------------------------------
# Pydantic Schemas
# --------------------------------------

class BookingInput(BaseModel):
    title: str = Field(..., description="Title of the event")
    start: str = Field(..., description="Start time in ISO 8601 format (e.g. '2025-07-01T15:00:00')")
    end: str = Field(..., description="End time in ISO 8601 format (e.g. '2025-07-01T16:00:00')")

class DummyInput(BaseModel):
    nothing: str = Field(default="none", description="Unused")

# --------------------------------------
# Tool Implementations
# --------------------------------------

def list_slots_tool(nothing: str = "none") -> str:
    print("[Tool] list_slots_tool called with:", nothing)
    try:
        events = get_free_slots()
        if not events:
            return "✅ No upcoming events found."
        formatted = "\n".join(
            f"• {e['start']['dateTime']} – {e.get('summary', 'No title')}" for e in events
        )
        return f"✅ Upcoming events:\n{formatted}"
    except Exception as e:
        print("[Error] list_slots_tool:", e)
        return "❌ Error retrieving calendar events."

    
def book_slot_tool(title: str, start: str, end: str):
    print("[Tool] book_slot_tool called with:", title, start, end)
    if not title or not start or not end:
        return "❌ Error: Missing title, start, or end. Please provide all in ISO format."

    try:
        event = create_event(title, start, end)
        print("[Tool] Event created:", event)
        return f"✅ Booked: '{event['summary']}' from {start} to {end}"
    except Exception as e:
        print("[Error] book_slot_tool:", e)
        return f"❌ Error booking event: {str(e)}"

# --------------------------------------
# Define Tools
# --------------------------------------

tools = [
    StructuredTool(
        name="ListFreeSlots",
        description="Lists the next 10 events on the Google Calendar.",
        func=list_slots_tool,
        args_schema=DummyInput
    ),
    StructuredTool(
        name="BookSlot",
        description=(
            "Books a meeting on the Google Calendar. "
            "You must provide:\n"
            "- title: a short descriptive title for the meeting (string)\n"
            "- start: the start time in ISO 8601 format (e.g. '2025-07-01T15:00:00')\n"
            "- end: the end time in ISO 8601 format (e.g. '2025-07-01T16:00:00')."
        ),
        func=book_slot_tool,
        args_schema=BookingInput
    )
]

# --------------------------------------
# Initialize Agent
# --------------------------------------

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
