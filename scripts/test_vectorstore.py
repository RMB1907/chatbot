# test_vectorstore.py (optional test)

from app.vectorstore import build_faiss_index, load_faiss_index, search_faiss

sample_docs = [
    {"text": "A soft answer turneth away wrath."},
    {"text": "Pride goeth before destruction."},
    {"text": "Trust in the Lord with all thine heart."}
]

build_faiss_index(sample_docs)

index, docs = load_faiss_index()
results = search_faiss("anger management advice", index, docs)

for res in results:
    print(res["text"])
