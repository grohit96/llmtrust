from fastapi import FastAPI
from pydantic import BaseModel
import re
import uuid
import json
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from fastapi.middleware.cors import CORSMiddleware

# -------------------------
# Setup FastAPI
# -------------------------
app = FastAPI(title="LLMTrust Gateway MVP")

# -------------------------
# Keypair for signing
# (in real version: store in Vault or env var)
# -------------------------
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode("utf-8")

# -------------------------
# Data Models
# -------------------------
class ChatRequest(BaseModel):
    user_id: str
    role: str
    prompt: str

class Claim(BaseModel):
    text: str
    label: str
    confidence: float

class ChatResponse(BaseModel):
    response_id: str
    answer: str
    claims: list[Claim]
    signature: str
    public_key: str

# -------------------------
# Utility Functions
# -------------------------
def sanitize_input(text: str) -> str:
    """Basic PII redaction: emails, phone numbers, SSNs"""
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)
    text = re.sub(r"\b\d{10}\b", "[REDACTED_PHONE]", text)
    return text

def sign_response(payload: dict) -> str:
    """Create Ed25519 signature over the response payload"""
    message = json.dumps(payload, sort_keys=True).encode("utf-8")
    signature = private_key.sign(message)
    return base64.b64encode(signature).decode("utf-8")

def verify_signature(payload: dict, signature_b64: str) -> bool:
    """Verify signature with stored public key"""
    try:
        signature = base64.b64decode(signature_b64.encode("utf-8"))
        message = json.dumps(payload, sort_keys=True).encode("utf-8")
        public_key.verify(signature, message)
        return True
    except Exception:
        return False

# -------------------------
# Routes
# -------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # 1. Sanitize input
    clean_prompt = sanitize_input(request.prompt)

    # 2. Dummy AI response (replace later with real LLM call)
    answer = f"Processed your prompt safely: '{clean_prompt}'"

    # 3. Fake claim verification (static for demo)
    claims = [
        {"text": "AI answers can hallucinate", "label": "verified", "confidence": 0.95},
        {"text": "This gateway is already production-ready", "label": "unknown", "confidence": 0.40}
    ]

    # 4. Build payload
    response_id = str(uuid.uuid4())
    payload = {
        "response_id": response_id,
        "answer": answer,
        "claims": claims
    }

    # 5. Sign payload
    signature = sign_response(payload)

    return {
        **payload,
        "signature": signature,
        "public_key": public_pem
    }

@app.post("/verify")
def verify(response: ChatResponse):
    payload = {
        "response_id": response.response_id,
        "answer": response.answer,
        "claims": [c.dict() for c in response.claims],
    }
    is_valid = verify_signature(payload, response.signature)
    return {"signature_valid": is_valid}


# Allow frontend (local HTML file) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in dev: allow all, in prod: restrict domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)