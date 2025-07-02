from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent import agent
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.post("/chat/")
async def chat(req: Request):
    data = await req.json()
    user_input = data.get("message")
    # NEW invoke-style call
    response = await agent.ainvoke(user_input)
    return {"response": response}

@app.get("/")
def home():
    return {"message": "API is up!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)