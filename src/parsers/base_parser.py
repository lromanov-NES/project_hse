import requests
import pandas as pd
import os


class BaseParser:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.data = []

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Ошибка {url}: {e}")
            return None

    def parse(self):
        raise NotImplementedError("parse() должен быть")

    def save_to_csv(self, filepath):
        if not self.data:
            print("Нет данных для сохранения")
            return

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        df = pd.DataFrame(self.data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"Сохранены в {filepath}")