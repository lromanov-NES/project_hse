import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#добавить обработку если нет отзывов
# эта х иногда падает хз почему

class YandexParser:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        # self.counter = 0  # закомментил, не понадобилось

    def setup_driver(self):
        opts = Options()

        if self.headless:
            opts.add_argument('--headless=new')  # скрытый режим

        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--window-size=1920,1080')
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
        opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        # через менеджер сам скачает драйвер
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=opts)

    def parse_org(self, org_id, org_name, min_rat=1, max_rat=3):
        url = f"https://yandex.ru/maps/org/{org_name}/{org_id}/reviews/"

        if not self.driver:
            self.setup_driver()

        self.driver.get(url)
        time.sleep(5)  # ждем загрузки, без этого не работает

        self._scroll_and_load()
        revs = self._get_reviews(min_rat, max_rat)

        if revs:
            self._save_csv(revs, org_name)
            print(f"✅ {org_name}: {len(revs)} отзывов")
        else:
            print(f"❌ {org_name}: нифига не нашлось")

        return revs

    # скроллю страницу пока не кончатся отзывы
    def _scroll_and_load(self):
        last_count = 0
        empty_count = 0

        for _ in range(50):  # лимит чтоб не зависнуть
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.5)

            # пытаюсь раскрыть длинные отзывы (кнопка "ещё")
            try:
                btns = self.driver.find_elements(By.CSS_SELECTOR, "span.business-review-view__expand")
                for b in btns:
                    if b.is_displayed():
                        b.click()
                        time.sleep(0.2)
            except:
                pass  # если нет кнопок - похуй

            # кнопка "загрузить ещё"
            try:
                more = self.driver.find_element(By.CSS_SELECTOR, "button[class*='load-more']")
                if more.is_displayed():
                    more.click()
                    time.sleep(1)
            except:
                pass

            cnt = len(self.driver.find_elements(By.CSS_SELECTOR, "div.business-review-view"))

            if cnt > last_count:
                last_count = cnt
                empty_count = 0
            else:
                empty_count += 1

            if empty_count >= 10:  # 10 раз подряд без новых - выходим
                break

    def _get_reviews(self, min_rat, max_rat):
        rez = []
        blocks = self.driver.find_elements(By.CSS_SELECTOR, "div.business-review-view")

        for blk in blocks:
            try:
                rat = self._parse_rating(blk)
                txt = self._parse_text(blk)
                d = self._parse_date(blk)
                a = self._parse_author(blk)

                if rat and min_rat <= rat <= max_rat and txt:
                    rez.append({
                        'author': a,
                        'date': d,
                        'rating': rat,
                        'text': txt
                    })
            except Exception as e:
                # иногда падает, хз почему
                continue

        # сортируем по убыванию чтобы сначала плохие
        rez.sort(key=lambda x: x['rating'])
        return rez

    def _parse_rating(self, el):
        try:
            cont = el.find_element(By.CSS_SELECTOR, "[aria-label*='Оценка']")
            lbl = cont.get_attribute("aria-label")
            m = re.search(r'Оценка\s+(\d)', lbl)
            if m:
                return int(m.group(1))
        except:
            pass
        return None

    def _parse_text(self, el):
        try:
            t = el.find_element(By.CSS_SELECTOR, "span.spoiler-view__text-container")
            return t.text.strip()
        except:
            pass

        # запасной вариант
        try:
            t = el.find_element(By.CSS_SELECTOR, "div.business-review-view__body span")
            return t.text.strip()
        except:
            pass

        return ""

    def _parse_date(self, el):
        try:
            d = el.find_element(By.CSS_SELECTOR, "span.business-review-view__date")
            return d.text.strip()
        except:
            pass
        return ""

    def _parse_author(self, el):
        try:
            a = el.find_element(By.CSS_SELECTOR, "div.business-review-view__author-name span")
            return a.text.strip()
        except:
            pass
        return "Аноним"

    def _save_csv(self, revs, name):
        tm = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_bad_reviews_{tm}.csv"

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["author", "date", "rating", "text"], delimiter=';')
            writer.writeheader()
            writer.writerows(revs)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None


if __name__ == "__main__":
    # словарь с компаниями (организация -> id)
    orgs = {
        "grow_food": "232887303625",
        "befit": "107091068962",
        "level_kitchen": "176629784362"
    }

    p = YandexParser(headless=True)

    for name, id in orgs.items():
        print(f"\nпарсю {name}")
        p.parse_org(org_id=id, org_name=name, min_rat=1, max_rat=3)
        time.sleep(2)

    p.close()
    print("\nготово")