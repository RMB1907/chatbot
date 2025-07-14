# main.py

import questionary

def run_minilm():
    from app.vectorstore import load_faiss_index, search_faiss
    index, docs = load_faiss_index()
    print("\n Using MiniLM model (Sentence-Transformers)\n")
    interactive_loop(index, docs, search_faiss)

def run_custombert():
    from app.vectorstore_custombert import load_faiss_index, search_faiss
    index, docs = load_faiss_index()
    print("\n Using Custom Bible ALBERT model\n")
    interactive_loop(index, docs, search_faiss)

def interactive_loop(index, docs, search_fn):
    print("Ask for wisdom from Proverbs (type 'exit' to quit)\n")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        results = search_fn(query, index, docs)
        for i, res in enumerate(results, 1):
            print(f"{i}. {res['text']}")

if __name__ == "__main__":
    choice = questionary.select(
        "Choose the embedding model:",
        choices=[
            "MiniLM (default)",
            "Custom Bible ALBERT"
        ]
    ).ask()

    if choice == "Custom Bible ALBERT":
        run_custombert()
    else:
        run_minilm()
