from pydantic import BaseModel
from typing import List


class AppInfo(BaseModel):
    app_id: str
    app_name: str
    platform: str
    region: str


class KeywordInfo(BaseModel):
    keyword: str
    position: int
    traffic: float


class CompetitorInfo(BaseModel):
    app_id: str
    app_name: str
    keywords_count: int
    traffic: float
    top_keywords: List[KeywordInfo]


class AnalysisResult(BaseModel):
    app: AppInfo
    keywords_count: int
    traffic: float
    competitors: List[CompetitorInfo]
    avg_keywords: float
    max_keywords: int
    avg_traffic: float
    max_traffic: float
    traffic_loss: float 