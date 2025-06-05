import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_app_details_rapidapi(appid, country="us"):
    url = "https://apple-app-store-scraper.p.rapidapi.com/v1/appstore?appid=544007664&country=us"
    params = {"appid": appid, "country": country}
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text, "status": response.status_code}

# Пошук app_id по назві додатку (через iTunes Search API)
def find_app_id_by_name(query: str, country: str = "us") -> str:
    url = "https://itunes.apple.com/search"
    params = {"term": query, "country": country, "entity": "software", "limit": 1}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("resultCount", 0) > 0:
            return str(data["results"][0]["trackId"])
    return None

def search_app(query: str, platform: str = "ios") -> List[Dict]:
    results = []
    if platform == "ios":
        app_id = find_app_id_by_name(query)
        if not app_id:
            return results
        app_data = get_app_details_rapidapi(app_id)
        if "error" not in app_data:
            results.append({
                "app_id": app_id,
                "app_name": app_data.get("title"),
                "description": app_data.get("description"),
                "icon": app_data.get("icon"),
                "rating": app_data.get("score"),
                "screenshots": app_data.get("screenshots", []),
                "url": app_data.get("url"),
            })
    else:
        url = (
            "https://play.google.com/store/search?q="
            f"{requests.utils.quote(query)}&c=apps&hl=en&gl=us"
        )
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")
        for app in soup.select("a[href^='/store/apps/details']"):
            link = "https://play.google.com" + app['href']
            name = (
                app.select_one(".Epkrse").get_text(strip=True)
                if app.select_one(".Epkrse")
                else app.get('aria-label', '')
            )
            m = re.search(r'id=([\w\.]+)', link)
            app_id = m.group(1) if m else None
            if app_id:
                results.append({
                    "app_id": app_id,
                    "app_name": name,
                    "url": link
                })
    return results

# Далі залишаємо фейкові ключові слова та конкурентів для тесту

def get_app_keywords(app_id: str, region: str = "US", platform: str = "ios") -> List[Dict]:
    return [
        {"keyword": "chatbot", "position": 1, "traffic": 1200},
        {"keyword": "ai friend", "position": 3, "traffic": 900},
        {"keyword": "virtual friend", "position": 5, "traffic": 700},
    ]

def get_similar_apps(app_id: str, platform: str = "ios") -> List[Dict]:
    return [
        {"app_id": f"competitor_{i}", "app_name": f"Competitor App {i}"}
        for i in range(1, 6)
    ] 