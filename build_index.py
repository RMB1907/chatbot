import json
from app.vectorstore import build_faiss_index

with open("data/proverbs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# If it's a list of strings, wrap them in dicts
if isinstance(data, list):
    if isinstance(data[0], str):
        docs = [{"text": verse} for verse in data]
    elif isinstance(data[0], dict) and "text" in data[0]:
        docs = data
    else:
        raise ValueError("Unexpected format in proverbs.json")
else:
    docs = [{"text": verse} for verse in data.values()]

build_faiss_index(docs)
