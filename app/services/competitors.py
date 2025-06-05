from .asomobile import get_similar_apps, get_app_keywords
from typing import List, Dict


def get_top_keywords(keywords, n=3):
    return sorted(keywords, key=lambda k: k["traffic"], reverse=True)[:n]


def get_competitors_stats(app_id: str, region: str = "US", platform: str = "ios") -> List[Dict]:
    competitors = get_similar_apps(app_id, platform)
    results = []
    for comp in competitors:
        keywords = get_app_keywords(comp["app_id"], region, platform)
        results.append({
            "app_id": comp["app_id"],
            "app_name": comp["app_name"],
            "keywords_count": len(keywords),
            "traffic": sum(k["traffic"] for k in keywords),
            "top_keywords": get_top_keywords(keywords),
        })
    return results 