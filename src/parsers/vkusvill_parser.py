import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from base_parser import BaseParser


class VkusVillParser(BaseParser):
    def __init__(self):
        super().__init__(base_url="https://food.vkusvill.ru/")

    def parse(self, html_content=None):
        print(f"Парсим {self.base_url}")

        html = html_content or self.fetch_page(self.base_url)


        soup = BeautifulSoup(html, 'html.parser')

        rations = soup.find_all('div', class_='js-card-ration')


        for ration in rations:
            name = ration.get('data-name', 'Неизвестная линейка')

            prices_json = ration.get('data-prices')

            if not prices_json:
                continue

            try:
                prices = json.loads(prices_json)

                for p in prices:
                    days = p.get('days')
                    total_price = p.get('price')

                    if days and total_price:
                        calories = name.split()[-1]
                        cal_str = f"{calories} ккал" if calories.isdigit() else "ХЗ"

                        # Пакуем всё в наш список
                        self.data.append({
                            'Конкурент': 'VkusVill',
                            'Линейка': name.upper(),
                            'Калорийность': cal_str,
                            'Дней': days,
                            'Цена за день (руб)': total_price
                        })
            except json.JSONDecodeError:
                print(f"Ошибка JSON")

        unique_data = [dict(t) for t in {tuple(d.items()) for d in self.data}]

        self.data = sorted(unique_data, key=lambda x: (x['Линейка'], x['Дней']))


if __name__ == "__main__":
    parser = VkusVillParser()

    parser.parse()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    save_path = os.path.join(project_root, 'data', 'raw', 'vkusvill.csv')

    parser.save_to_csv(save_path)