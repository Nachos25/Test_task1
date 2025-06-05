from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from .services.asomobile import search_app, get_app_keywords
from .services.competitors import get_competitors_stats
from .services.keywords import get_keywords_stats
from .schemas import AnalysisResult, AppInfo, CompetitorInfo, KeywordInfo
import traceback

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(traceback.format_exc())  # Вивід у консоль
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/analyze")
def analyze(query: str, platform: str = "ios"):
    # 1. Пошук додатку
    apps = search_app(query, platform)
    if not apps:
        return JSONResponse({"error": "Додаток не знайдено"}, status_code=404)
    app_data = apps[0]
    app_id = app_data.get("app_id")
    app_name = app_data.get("app_name")
    region = "US"
    # 2. Ключові слова
    keywords = get_app_keywords(app_id, region, platform)
    kw_stats = get_keywords_stats(keywords)
    # 3. Конкуренти
    competitors = get_competitors_stats(app_id, region, platform)
    if not competitors:
        return JSONResponse({"error": "Конкуренти не знайдені"}, status_code=404)
    avg_keywords = sum(c["keywords_count"] for c in competitors) / len(competitors)
    max_keywords = max(c["keywords_count"] for c in competitors)
    avg_traffic = sum(c["traffic"] for c in competitors) / len(competitors)
    max_traffic = max(c["traffic"] for c in competitors)
    traffic_loss = avg_traffic - kw_stats["traffic"]
    # 4. Формування відповіді
    result = AnalysisResult(
        app=AppInfo(
            app_id=app_id,
            app_name=app_name,
            platform=platform,
            region=region
        ),
        keywords_count=kw_stats["count"],
        traffic=kw_stats["traffic"],
        competitors=[
            CompetitorInfo(
                app_id=c["app_id"],
                app_name=c["app_name"],
                keywords_count=c["keywords_count"],
                traffic=c["traffic"],
                top_keywords=[
                    KeywordInfo(
                        keyword=kw["keyword"],
                        position=kw["position"],
                        traffic=kw["traffic"]
                    ) for kw in c["top_keywords"]
                ]
            ) for c in competitors
        ],
        avg_keywords=round(avg_keywords, 2),
        max_keywords=max_keywords,
        avg_traffic=round(avg_traffic, 2),
        max_traffic=max_traffic,
        traffic_loss=round(traffic_loss, 2)
    )
    return result.dict() 