import requests
import json
import os
import time

def get_proverbs_chapter(chapter_num):
    url = f"https://bible-api.com/proverbs%20{chapter_num}?translation=kjv"
    print(f"Fetching: {url}")
    resp = requests.get(url)
    if resp.status_code == 429:
        print("Rate limited. Sleeping for 10 seconds...")
        time.sleep(10)
        resp = requests.get(url)  # Retry once
    resp.raise_for_status()
    data = resp.json()
    verses = data.get("verses", [])
    return [
        {"chapter": v["chapter"], "verse": v["verse"], "text": v["text"].strip()}
        for v in verses
    ]

def main():
    all_verses = []
    for ch in range(1, 32):
        try:
            all_verses.extend(get_proverbs_chapter(ch))
            time.sleep(2)  # polite delay between calls
        except Exception as e:
            print(f"Failed to fetch chapter {ch}: {e}")
            continue

    os.makedirs("data", exist_ok=True)
    with open("data/proverbs.json", "w", encoding="utf-8") as f:
        json.dump(all_verses, f, indent=2, ensure_ascii=False)

    print(f"\nFetched and saved {len(all_verses)} verses to 'data/proverbs.json'")

if __name__ == "__main__":
    main()
