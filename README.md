# ASO Конкурентний Аналізатор

## Опис
Сервіс для аналізу індексації додатків у App Store (iOS) та Google Play (Android) за ключовими словами та конкурентного аналізу.

## Технології
- FastAPI (бекенд + фронтенд)
- Jinja2 (шаблони)
- requests, BeautifulSoup (парсинг Google Play)

## Запуск

1. Встановіть залежності:
```
pip install -r requirements.txt
```
2. Запустіть FastAPI:
```
uvicorn app.main:app --reload
```

## Налаштування
- API ключі RapidAPI зберігаються у .env (для iOS)

## Функціонал
- Пошук додатку за назвою/лінком
- Збір ключових слів та трафіку (фейкові дані для MVP)
- Пошук 5 конкурентів (фейкові дані для MVP)
- Порівняльна аналітика
- Простий веб-інтерфейс у темному стилі

## Як працює
- **Android (Google Play):** парсинг через requests + BeautifulSoup (без API, стабільно працює)
- **iOS (App Store):** використовується RapidAPI (apple-app-store-scraper) для отримання даних про додаток

## Відомі проблеми та обмеження
- **iOS (App Store) не працює стабільно:**
    - RapidAPI часто повертає помилки 403 ("You are not subscribed to this API") або 429 ("Too many requests"), навіть при наявності підписки та валідного ключа.
    - Можливі причини: ліміти RapidAPI, політика Apple щодо скрапінгу, блокування з боку API-провайдера, нестабільність сервісу.
    - Офіційного безкоштовного API для повного аналізу App Store не існує, а сторонні API часто платні або нестабільні.
    - Парсинг напряму через Selenium блокується App Store (динамічне завантаження, захист від ботів, капчі).
- **Android (Google Play) працює стабільно** через парсер, але структура сторінки може змінюватися Google.

## Рекомендації
- Для стабільного аналізу iOS-додатків використовуйте платні сервіси (ASOMobile, AppTweak, SensorTower) або власний парсер з ротацією проксі та антибот-захистом.
- Для MVP/демо-версії сервіс працює для Android, для iOS — лише якщо RapidAPI не блокує запити. 