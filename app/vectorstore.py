# app/vectorstore.py

import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # local, fast

def build_faiss_index(docs, save_path="data/faiss_index"):
    embeddings = model.encode([doc["text"] for doc in docs])
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))

    with open(save_path + ".pkl", "wb") as f:
        pickle.dump({"index": index, "docs": docs}, f)

def load_faiss_index(load_path="data/faiss_index"):
    with open(load_path + ".pkl", "rb") as f:
        data = pickle.load(f)
    return data["index"], data["docs"]

def search_faiss(query, index, docs, k=3):
    embedding = model.encode([query])
    D, I = index.search(np.array(embedding, dtype=np.float32), k)
    return [docs[i] for i in I[0]]
