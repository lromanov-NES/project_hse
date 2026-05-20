from ymrp.parser import Parser
import pandas as pd
import time


class SafeParser(Parser):
    def get_yandex_reviews(self, url, max_reviews=100):
        from playwright.sync_api import sync_playwright

        reviews = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()

            print(f"🔄 Загружаю {url}...")
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)

            # Прокручиваем
            for _ in range(5):
                page.evaluate("window.scrollBy(0, 800)")
                page.wait_for_timeout(2000)

            # Поиск отзывов
            review_blocks = page.query_selector_all('[data-testid="review-item"]')
            if not review_blocks:
                review_blocks = page.query_selector_all('.business-review-view')

            print(f"📝 Найдено блоков: {len(review_blocks)}")

            for block in review_blocks[:max_reviews]:
                try:
                    text_elem = block.query_selector('[itemprop="reviewBody"], .business-review-view__body')
                    text = text_elem.inner_text() if text_elem else ""

                    rating_elem = block.query_selector('[itemprop="ratingValue"], .business-rating-stars-view')
                    rating = rating_elem.get_attribute("aria-label") if rating_elem else ""

                    date_elem = block.query_selector('time')
                    date = date_elem.get_attribute("datetime") if date_elem else ""

                    author_elem = block.query_selector('[itemprop="author"], .business-review-view__author')
                    author = author_elem.inner_text() if author_elem else "Аноним"

                    reviews.append({
                        "text": text[:2000],
                        "rating": rating,
                        "date": date,
                        "author": author
                    })
                    print(f"✅ Собрано {len(reviews)} отзывов")
                except:
                    continue

            browser.close()

        return reviews


# ПРАВИЛЬНЫЕ ссылки
companies = [
    {"name": "Grow Food", "url": "https://yandex.ru/maps/org/grow_food/232887303625/reviews/"},
    {"name": "Level Kitchen", "url": "https://yandex.ru/maps/org/level_kitchen/176629784362/reviews/?ll=37.422584%2C55.694510&z=16"},
    {"name": "BeFit", "url": "https://yandex.ru/maps/org/befit/107091068962/reviews/?ll=37.599004%2C55.600389&z=16"},
]

all_reviews = []

for company in companies:
    print(f"\n{'=' * 50}")
    print(f"🏢 Парсинг {company['name']}...")
    print('=' * 50)

    parser = SafeParser()
    try:
        reviews = parser.get_yandex_reviews(company["url"], max_reviews=100)
        print(f"✅ Итого: {len(reviews)} отзывов для {company['name']}")

        for review in reviews:
            all_reviews.append({
                "company": company["name"],
                **review
            })
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    time.sleep(3)

if all_reviews:
    df = pd.DataFrame(all_reviews)
    df.to_csv("competitors_reviews.csv", index=False, encoding="utf-8-sig")
    print(f"\n✅ ВСЕГО СОБРАНО: {len(all_reviews)} отзывов")

    # Анализ минусов
    print("\n" + "=" * 50)
    print("📊 АНАЛИЗ МИНУСОВ КОНКУРЕНТОВ")
    print("=" * 50)

    negative_keywords = {
        "доставка": ["задержк", "опозд", "вовремя", "час", "ждал", "долго"],
        "температура": ["холодн", "остывш", "негоряч", "тепл"],
        "качество": ["невкусн", "резин", "сух", "просроч"],
        "порции": ["маленьк", "мало", "не наелся", "голодн"],
        "цена": ["дорог", "цена", "деньг", "стоим", "дешев"],
        "сервис": ["поддержк", "связь", "дозвонить", "ответ", "извин"]
    }

    for company in companies:
        company_reviews = [r for r in all_reviews if r["company"] == company["name"]]
        if not company_reviews:
            print(f"\n🏢 {company['name']}: ❌ нет данных")
            continue

        print(f"\n🏢 {company['name']} (отзывов: {len(company_reviews)})")

        issues = {}
        for category, keywords in negative_keywords.items():
            count = 0
            for kw in keywords:
                count += sum(1 for r in company_reviews if kw.lower() in r["text"].lower())
            if count > 0:
                issues[category] = count

        if issues:
            sorted_issues = sorted(issues.items(), key=lambda x: x[1], reverse=True)
            print(f"   ⚠️ ТОП проблем:")
            for cat, cnt in sorted_issues[:3]:
                print(f"      - {cat}: {cnt} упоминаний")
        else:
            print("   👍 Явных проблем не обнаружено")
else:
    print("❌ Не удалось собрать отзывы")