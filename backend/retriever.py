import os
from dotenv import load_dotenv
load_dotenv()
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONTRACTS_DIR = os.path.join(BASE_DIR, "contracts")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

# Initialize embedding model
embeddings = OpenAIEmbeddings()

def build_vectorstore():
    """Build FAISS index from all contracts in /contracts"""
    docs = []
    for fname in os.listdir(CONTRACTS_DIR):
        if fname.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(CONTRACTS_DIR, fname))
            file_docs = loader.load()
            # Add metadata
            for d in file_docs:
                d.metadata["source"] = fname
            docs.extend(file_docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTORSTORE_DIR)
    return db

# Load existing FAISS index or build a new one
# Ensure vectorstore path exists
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

index_file = os.path.join(VECTORSTORE_DIR, "index.faiss")

if not os.path.exists(index_file):
    print("⚡ Building new FAISS index from contracts...")
    db = build_vectorstore()
else:
    print("✅ Loading existing FAISS index...")
    db = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)

def retrieve_contract_sections(query: str, k: int = 3):
    """Return top-k contract sections relevant to query"""
    results = db.similarity_search_with_score(query, k=k)
    docs = []
    for doc, score in results:
        doc.metadata["score"] = float(score)
        docs.append(doc)
    return docs
