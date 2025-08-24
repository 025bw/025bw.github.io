import requests
from bs4 import BeautifulSoup
import json
import os
import re

POKEDEX_URL = "https://pokemongohub.net/pokedex"
BASE_URL = "https://pokemongohub.net"

os.makedirs("data", exist_ok=True)

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)

def get_legendaries():
    print("Fetching Pokédex index...")
    r = requests.get(POKEDEX_URL, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    mons = []
    for card in soup.select(".pokedex-entry"):
        tags = card.select(".pokemon-tag")
        if not tags:
            continue
        tag_texts = [t.get_text(strip=True).lower() for t in tags]
        if any(t in ["legendary", "mythical", "ultra beast"] for t in tag_texts):
            link = card.find("a", href=True)
            if link:
                mons.append(BASE_URL + link["href"])
    print(f"Found {len(mons)} legendary/mythical/UB Pokémon.")
    return mons

def scrape_iv_chart(url):
    slug = url.strip("/").split("/")[-1]
    print("Fetching", slug)
    r = requests.get(url + "/iv-chart", timeout=20)
    if r.status_code != 200:
        print("No IV chart for", slug)
        return

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    if not table:
        print("No table found for", slug)
        return

    headers = [th.text.strip() for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cols = [td.text.strip() for td in tr.find_all("td")]
        if cols:
            rows.append(dict(zip(headers, cols)))

    filename = f"data/{slugify(slug)}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print("Saved", filename)

def main():
    mons = get_legendaries()
    index = []
    for url in mons:
        try:
            slug = url.strip("/").split("/")[-1]
            scrape_iv_chart(url)
            index.append(slug)
        except Exception as e:
            print("Error scraping", url, e)

    # Save index.json
    with open("data/index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

if __name__ == "__main__":
    main()