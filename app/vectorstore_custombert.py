import torch
import numpy as np
import faiss
import pickle
from transformers import AutoTokenizer, AutoModel

# ✅ Change model name here
model_name = "Pragash-Mohanarajah/albert-base-v2-finetuned-bible-accelerate"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

def get_embedding(text):
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
        outputs = model(**inputs)
        attention_mask = inputs["attention_mask"]

        # Mean Pooling excluding padding
        embeddings = outputs.last_hidden_state
        masked_embeddings = embeddings * attention_mask.unsqueeze(-1)
        summed = masked_embeddings.sum(1)
        counts = attention_mask.sum(1).unsqueeze(-1)
        mean_pooled = summed / counts

        return mean_pooled.squeeze().numpy()

def build_faiss_index(docs, save_path="data/faiss_index_custombert"):
    embeddings = [get_embedding(doc["text"]) for doc in docs]
    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))

    with open(save_path + ".pkl", "wb") as f:
        pickle.dump({"index": index, "docs": docs}, f)

def load_faiss_index(load_path="data/faiss_index_custombert"):
    with open(load_path + ".pkl", "rb") as f:
        data = pickle.load(f)
    return data["index"], data["docs"]

def search_faiss(query, index, docs, k=3):
    embedding = get_embedding(query)
    D, I = index.search(np.array([embedding], dtype=np.float32), k)
    return [docs[i] for i in I[0]]
