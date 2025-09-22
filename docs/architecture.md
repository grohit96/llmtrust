# LLMTrust Architecture (MVP)

User ---> [ LLMTrust Gateway ] ---> LLM Model
| Inbound Guards
| Policy Engine
| Claim Verification
| Signing + Audit
v
Verified + Signed Response
