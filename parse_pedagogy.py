import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://pedsovet.org/"

def parse_pedagogy_articles():
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # --- Проверено через Inspect — малые карточки находятся в блоках .card-mini ---
    # Если сайт обновится, селектор можно поменять
    cards = soup.select(".card-mini")

    results = []

    for card in cards:
        # Заголовок может быть в <a> или <div class="title">
        title_tag = card.select_one(".title, a")
        link_tag = card.find("a")

        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = urljoin(BASE_URL, link_tag.get("href"))

        results.append({
            "title": title,
            "link": link
        })

    return results


if __name__ == "__main__":
    data = parse_pedagogy_articles()

    print(json.dumps(data, ensure_ascii=False, indent=4))

    # сохраняем в файл
    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("\nГотово! Данные сохранены в articles.json")
