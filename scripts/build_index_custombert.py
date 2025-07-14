# scripts/build_index_custombert.py

import json
from app.vectorstore_custombert import build_faiss_index

# Load Proverbs data
with open("data/proverbs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalize structure to: list of {"text": ...}
if isinstance(data, list):
    if isinstance(data[0], str):
        docs = [{"text": verse} for verse in data]
    elif isinstance(data[0], dict) and "text" in data[0]:
        docs = data
    else:
        raise ValueError("Unexpected format in proverbs.json")
else:
    docs = [{"text": verse} for verse in data.values()]

# Build FAISS index using CustomBERT
build_faiss_index(docs)
print("CustomBERT FAISS index built and saved.")
