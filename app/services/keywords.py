from typing import List, Dict


def get_keywords_stats(keywords: List[Dict]) -> Dict:
    count = len(keywords)
    total_traffic = sum(k["traffic"] for k in keywords)
    return {
        "count": count,
        "traffic": total_traffic,
    } 