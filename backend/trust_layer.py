# backend/trust_layer.py
import uuid

def trust_wrap(response_id: str, query: str, answer: str, docs: list):
    """
    Wraps the LLM answer with trust metadata:
    - Citations from docs
    - Confidence score (simple heuristic for now)
    - Audit ID for logging
    """
    # Collect citations (sources of retrieved docs)
    citations = [f"{d.metadata.get('source', 'unknown')} (score={d.metadata.get('score', 0):.2f})"
                 for d in docs]

    # Naive confidence: based on retrieval scores (average of top-3)
    if docs:
        avg_score = sum(d.metadata.get("score", 0) for d in docs) / len(docs)
        confidence = max(0.1, 1.0 - avg_score)  # lower score = higher confidence
    else:
        confidence = 0.2  # fallback low confidence if no docs

    # Unique audit trail ID
    audit_id = str(uuid.uuid4())

    return {
        "response_id": response_id,
        "answer": answer,
        "citations": citations,
        "confidence": confidence,
        "audit_id": audit_id,
    }
