from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
import base64
import re
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

# Local imports (placeholders – we’ll implement next)
from backend.retriever import retrieve_contract_sections
from backend.llm_client import ask_llm
from backend.trust_layer import trust_wrap
from backend.audit import get_audit_by_id, log_audit


# -------------------------
# Setup FastAPI
# -------------------------
app = FastAPI(title="LLMTrust Gateway – Legal Edition")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Keypair for signing
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
    query: str   # renamed from "prompt"

class ChatResponse(BaseModel):
    response_id: str
    answer: str
    citations: list[str]
    confidence: float
    audit_id: str
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
    # 1. Clean the query
    clean_query = sanitize_input(request.query)

    # 2. Retrieve supporting contract sections
    docs = retrieve_contract_sections(clean_query)

    # 3. Ask LLM to summarize/answer using retrieved docs
    answer = ask_llm(clean_query, docs)

    # 4. Wrap with trust metadata (citations, confidence, audit_id)
    response_id = str(uuid.uuid4())
    response = trust_wrap(response_id, clean_query, answer, docs)

    # 5. Log audit trail
    log_audit(response)

    # 6. Sign payload
    payload = {
        "response_id": response["response_id"],
        "answer": response["answer"],
        "citations": response["citations"],
        "confidence": response["confidence"],
        "audit_id": response["audit_id"]
    }
    signature = sign_response(payload)

    return {
        **payload,
        "signature": signature,
        "public_key": public_pem
    }

@app.get("/audit/{audit_id}")
def get_audit(audit_id: str):
    """Fetch full audit log"""
    return get_audit_by_id(audit_id)

@app.post("/verify")
def verify(response: ChatResponse):
    """Check if signature is valid"""
    payload = {
        "response_id": response.response_id,
        "answer": response.answer,
        "citations": response.citations,
        "confidence": response.confidence,
        "audit_id": response.audit_id
    }
    is_valid = verify_signature(payload, response.signature)
    return {"signature_valid": is_valid}
