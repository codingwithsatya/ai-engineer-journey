from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are Aria, a sharp and friendly AI assistant.
You remember everything said in this conversation.
You are concise — never use more than 3 sentences unless asked.
You are helpful, direct, and occasionally witty."""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/")
def root():
    return {"status": "Aria API is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    def stream_response():
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            temperature=0.7,
            system=SYSTEM_PROMPT,
            messages=[m.dict() for m in request.messages]
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(stream_response(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    import os
    import sys
    print("Starting Aria API...", flush=True)
    print(f"Python version: {sys.version}", flush=True)
    print(f"PORT env var: {os.environ.get('PORT', 'NOT SET')}", flush=True)
    print(f"API KEY set: {bool(os.environ.get('ANTHROPIC_API_KEY'))}", flush=True)
    port = int(os.environ.get("PORT", 8000))
    print(f"Binding to port: {port}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)