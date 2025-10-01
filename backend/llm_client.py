# backend/llm_client.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(query: str, docs: list) -> str:
    """
    Query the LLM with the user's question and the retrieved contract sections.
    """
    # Join top docs into context
    context = "\n\n".join([f"Source ({d.metadata.get('source', 'unknown')}):\n{d.page_content}" for d in docs])

    prompt = f"""
    You are a legal assistant AI. Answer the following question based ONLY on the provided documents.

    Question: {query}

    Documents:
    {context}

    If the answer cannot be found, say "The documents do not contain enough information."
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a careful legal assistant that only uses provided documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
