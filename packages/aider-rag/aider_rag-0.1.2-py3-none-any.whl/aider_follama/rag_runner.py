# aider_rag/rag_runner.py

import faiss
import pickle
import requests
import torch
from sentence_transformers import SentenceTransformer
from src.aider_follama.model_connector import query_with_aider_model
from src.aider_follama.db_logger import log_query_response

INDEX_PATH = "faiss_index.driver"
LOOKUP_PATH = "chunk_lookup.pkl"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen:7b"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TOP_K = 10

model = SentenceTransformer(EMBEDDING_MODEL, device=DEVICE)
lookup = pickle.load(open(LOOKUP_PATH, "rb"))
index = faiss.read_index(INDEX_PATH)


def run_combined_rag_pipeline(user_query: str) -> dict:
    query_emb = model.encode([user_query], normalize_embeddings=True)
    D, I = index.search(query_emb, TOP_K)

    context = ""
    for idx in I[0]:
        for src, id_list in lookup.items():
            if idx in id_list:
                context += f"\n[From: {src} | Chunk ID: {idx}]\n"
                break

    prompt = f"""You are a Linux device driver expert. Use the following documentation chunks to answer the question.\n\n{context}\n\nQuestion: {user_query}\nAnswer:"""

    try:
        ollama_response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        ollama_answer = ollama_response.json().get("response", "").strip()
    except Exception as e:
        ollama_answer = f"[Ollama Error] {e}"

    try:
        aider_answer = query_with_aider_model(prompt)
    except Exception as e:
        aider_answer = f"[Aider Error] {e}"

    log_query_response(user_query, context, ollama_answer, aider_answer)

    return {
        "query": user_query,
        "context": context.strip(),
        "ollama_answer": ollama_answer,
        "aider_answer": aider_answer
    }
