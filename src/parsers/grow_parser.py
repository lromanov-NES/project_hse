import json
import os
from bs4 import BeautifulSoup
from base_parser import BaseParser


class GrowFoodParser(BaseParser):
    def __init__(self):
        super().__init__(base_url="https://growfood.pro/")

    def parse(self):
        print(f"Парсинг {self.base_url}")
        html = self.fetch_page(self.base_url)

        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')

        scripts = soup.find_all('script', type='application/ld+json')

        found_data = False
        for script in scripts:
            try:
                data = json.loads(script.string)

                if data.get('@type') == 'ItemList' and 'itemListElement' in data:
                    for element in data['itemListElement']:
                        item = element.get('item', {})
                        offer = item.get('offers', {})

                        name = item.get('name')
                        price = offer.get('price')
                        description = item.get('description', '')

                        if name and price:
                            self.data.append({
                                'Конкурент': 'Grow Food',
                                'Калорийность': name,
                                'Цена за день (руб)': price,
                                'Описание': description
                            })
                            found_data = True
            except (json.JSONDecodeError, TypeError, KeyError):
                continue

        if not found_data:
            print("Данных нет")


if __name__ == "__main__":
    parser = GrowFoodParser()
    parser.parse()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    save_path = os.path.join(project_root, 'data', 'raw', 'grow_food.csv')

    parser.save_to_csv(save_path)