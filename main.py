# main.py

import questionary

def run_ask_mode():
    from app.vectorstore import load_faiss_index, search_faiss
    index, docs = load_faiss_index()
    print("\nAsk Mode — Using MiniLM model\n")
    interactive_loop(index, docs, search_faiss)

def run_play_mode():
    from app.proverbs_mlm import play_round
    print("\nPlay Mode — Fill in the blank from Proverbs\n")
    while True:
        play_round()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break

def interactive_loop(index, docs, search_fn):
    print("Ask for wisdom from Proverbs (type 'exit' to quit)\n")
    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            break
        results = search_fn(query, index, docs)
        for i, res in enumerate(results, 1):
            print(f"{i}. {res['text']}")

if __name__ == "__main__":
    choice = questionary.select(
        "Choose the mode:",
        choices=[
            "Ask Mode (default)",
            "Play Mode (MLM quiz)"
        ]
    ).ask()

    if choice == "Play Mode (MLM quiz)":
        run_play_mode()
    else:
        run_ask_mode()

#  .\venv\Scripts\Activate.ps1
#  python main.py