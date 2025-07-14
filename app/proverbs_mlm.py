import random
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
import json

# Load model and tokenizer
model_name = "Pragash-Mohanarajah/albert-base-v2-finetuned-bible-accelerate"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)
mlm = pipeline("fill-mask", model=model, tokenizer=tokenizer)

# Load proverbs
with open("data/proverbs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

proverbs = [v["text"] if isinstance(v, dict) else v for v in data]

# Skip common uninformative words
SKIP_WORDS = set("""
he she it they his her their him them to of for and or but with from by as at is was are be been being shall will can may must a an the in on if not nor do does did have has had
""".split())

def choose_masked_word(text):
    words = text.split()
    candidates = [i for i, w in enumerate(words) if w.lower().strip(",.?!;:") not in SKIP_WORDS and len(w) > 2]
    if not candidates:
        return None, None
    i = random.choice(candidates)
    original = words[i]
    words[i] = tokenizer.mask_token
    return " ".join(words), original

def play_round():
    verse = random.choice(proverbs)
    masked_text, original_word = choose_masked_word(verse)
    if not masked_text:
        print("Skipping verse (no suitable word to mask)...")
        return

    print("\nFill in the blank:\n")
    print(masked_text)
    guess = input("\nYour guess: ").strip().lower()

    outputs = mlm(masked_text)
    predictions = [o["token_str"].lower() for o in outputs]

    if guess == original_word.lower():
        print("Correct!")
    else:
        print("Try again.")
        print("Top predictions:", ", ".join(predictions[:5]))
        print("Original word:", original_word)
