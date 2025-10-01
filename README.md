LLMTrust

AI outputs can hallucinate, leak secrets, and can’t be verified. LLMTrust is a security + trust layer that solves this — starting with legal documents.

🚩 The Initial Problem

Large Language Models (LLMs) are powerful but risky to use directly:

They may hallucinate facts and present them as truth.

They may leak sensitive data from user prompts.

Their outputs cannot be independently verified or audited.

This makes adoption difficult in regulated industries (finance, healthcare, law, government) where trust and compliance are critical.

🔑 The Solution

LLMTrust is a security and trust gateway that sits between users and AI models.

It provides:

Input Guards – prevent prompt injection, strip PII/secrets.

Evidence-Based Outputs – every answer comes with citations + confidence scores.

Cryptographic Signing – responses are signed and auditable (tamper-proof).

Audit Trail – every interaction is logged for compliance review.

Think of it as the JWT/OAuth2 of AI responses — a standard way to ensure provenance, auditability, and trust.

🔄 Pivot: Legal First

While the long-term vision is AI trust for all industries, we’ve pivoted the MVP to focus on legal and compliance documents because:

📄 Contracts, NDAs, and policies are easier to ingest/test (structured PDF docs).

⚖️ Legal is a high-trust, compliance-heavy domain → perfect fit for LLMTrust.

🚀 Quickest way to demonstrate “LLM with receipts”: citations, audit trail, signed answers.

📊 Current High-Level Flow
User ---> [ LLMTrust Gateway ] ---> LLM Model
| Input Guard
| Retrieval from legal PDFs/contracts
| Claim Verification + Citations
| Signing + Audit Trail
v
Verified + Signed Answer

📌 Current Status

We now have a working backend prototype with:

✅ PDF ingestion + FAISS vector search

✅ /chat API endpoint (FastAPI)

✅ Verified answers with citations + confidence score

✅ Cryptographic signing (tamper-proof)

✅ Audit logging (every request/response tracked)

Example output:

Answer with citations from PDF

Confidence = 0.46

Audit ID for traceability

Digital signature + public key

🛠️ Next Phases (Roadmap)

Phase 1 (Done) → Backend skeleton + retrieval + signing

Phase 2 (Now) → Input sanitization + richer audit logging

Phase 3 → Reasoning trace (“show the work”)

Phase 4 → Minimal frontend (upload PDF + chat UI)

Phase 5 → Packaging (Docker, demo repo, live demo)

Phase 6 → Expand to other domains (finance, healthcare, compliance APIs)

🚀 Quickstart
Backend (FastAPI)

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn backend.main:app --reload

Test with:

curl -X POST "http://127.0.0.1:8000/chat" \
 -H "Content-Type: application/json" \
 -d '{"user_id":"123","role":"analyst","query":"Summarize contract terms"}'

Frontend (coming soon 🚧)

Minimal React/Vue app where users can upload PDFs and query.

Shows:

Answer

Citations (with scores)

Confidence level

Digital signature + Verify button

🎯 Vision

LLMTrust is building the trust + compliance layer for AI. Starting with legal contracts, expanding into finance, healthcare, and government.

Every AI answer will be: auditable, verifiable, signed.
