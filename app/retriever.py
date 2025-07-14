from app.vectorstore import load_faiss_index, search_faiss

def get_relevant_proverbs(query):
    index, docs = load_faiss_index()
    return search_faiss(query, index, docs)
