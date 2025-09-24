# LLMTrust Frontend (Planned)

This will be a simple web UI:

- Input box for a question
- Display verified answer + signature
- Verify page to paste a response and check signature

Phase 1: MVP Pipeline (✅ Done)

- Input sanitization (emails, SSNs, phones)
- Hardcoded claims (✔ Verified / ❓ Unknown)
- Cryptographic signing
- Verification API
- Minimal web UI

Phase 2: Wikipedia Integration (🟢 Current)

- Extract claims from AI answers
- Verify against Wikipedia summaries
- Label claims dynamically
- Demo "✔ Verified / ⚠ Contested / ❓ Unknown" with evidence

Phase 3: Multi-Source Verification (🔜 Next)

- Check claims against multiple sources:
  - Wikipedia
  - Government APIs (FDA, SEC, WHO)
  - Academic datasets
- Cross-verify for consistency
- Confidence scores from multiple evidence providers

Phase 4: Enterprise-Grade Trust (🌐 Future Vision)

- Enterprises plug in their own ground truth (databases, policies, docs)
- Policy engine (block financial/medical leaks, enforce domain rules)
- Evidence hashing → cryptographic audit logs / ledger
- Becomes the "JWT/OAuth2 for AI outputs"
