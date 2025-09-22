from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="LLMTrust Gateway MVP")

class ChatRequest(BaseModel):
    user_id: str
    role: str
    prompt: str

class ChatResponse(BaseModel):
    response_id: str
    answer: str
    signature: str
    verified: bool

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Placeholder logic
    return {
        "response_id": "demo-123",
        "answer": "This is a placeholder AI response.",
        "signature": "fake-signature",
        "verified": True
    }

@app.post("/verify")
def verify(response: ChatResponse):
    # Always return valid for now
    return {"signature_valid": True}
