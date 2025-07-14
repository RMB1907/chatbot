from app.vectorstore import load_faiss_index, search_faiss

index, docs = load_faiss_index()

print("Ask for wisdom from Proverbs (type 'exit' to quit)\n")

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break

    results = search_faiss(query, index, docs)
    for i, res in enumerate(results, 1):
        print(f"{i}. {res['text']}")
