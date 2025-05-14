import requests
from bs4 import BeautifulSoup
import json
import time
import re

# --------------------------------------------------------------------------------------------------
# Script to crawl DLsite genre pages and build a JSON mapping of genre codes to names.
# Uses <title> parsing with explicit locale query (?locale=ja_JP / ?locale=ko_KR).
# Ignores non-HTML responses and excludes meta genres like 日本語作品 言語不問作品.
# --------------------------------------------------------------------------------------------------

def fetch_genre_name(code: str, locale: str):
    url = f"https://www.dlsite.com/maniax/fsr/=/genre/{code}/from/work.genre/?locale={locale}"
    try:
        res = requests.get(url)
        content_type = res.headers.get("Content-Type", "")
        if res.status_code != 200 or "text/html" not in content_type:
            print(f"[WARN] Non-HTML response for {code} ({locale}): {content_type}")
            return None
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.find("title")
        if title:
            text = title.text.strip()
            if "「" in text and "」" in text and ("の作品一覧" in text or "의 작품 일람" in text):
                name = text.split("「")[1].split("」")[0].strip()
                if name in ["日本語作品 言語不問作品"]:
                    return None
                return name
            else:
                return None
    except Exception as e:
        print(f"Error fetching code {code} in {locale}: {e}")
    return None


def is_roman(text):
    return bool(re.fullmatch(r'[A-Za-z0-9 /:#+.-]+', text))


def main():
    genres = {}
    missing_streak = 0
    MAX_MISSING = 100

    for i in range(1, 350):  # 전체 범위 설정
        code = f"{i:03d}"
        jp = fetch_genre_name(code, "ja_JP")
        kr = fetch_genre_name(code, "ko_KR")

        if jp:
            if kr == jp and not is_roman(jp):
                kr = ""
            genres[code] = {"jp": jp, "kr": kr or ""}
            print(f"Found {code}: jp={jp} | kr={genres[code]['kr']}")
            missing_streak = 0
        else:
            print(f"Skipping {code} (no genre)")
            missing_streak += 1
            if missing_streak >= MAX_MISSING:
                print("Reached maximum consecutive misses, stopping crawl.")
                break

        time.sleep(0.3)

    with open('genre_fin.json', 'w', encoding='utf-8') as f:
        json.dump(genres, f, ensure_ascii=False, indent=2)
    print(f"[DONE] Saved all {len(genres)} genres to genre_fin.json")


if __name__ == '__main__':
    main()
