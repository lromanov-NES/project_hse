import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from base_parser import BaseParser


class PolzaDietParser(BaseParser):
    def __init__(self):
        super().__init__(base_url="https://polza.diet/")

    def parse(self, html_content=None):
        print(f"Парсим {self.base_url}")

        html = html_content or self.fetch_page(self.base_url)

        if not html:
            print("Не удалось получить HTML")
            return

        soup = BeautifulSoup(html, 'html.parser')

        script_tag = soup.find('script', class_='js-react-on-rails-component')

        if not script_tag:
            print("Не найден тег с данными (js-react-on-rails-component)")
            return

        try:
            data = json.loads(script_tag.string)

            prices_data = data.get('prices', {})

            for diet_name, cities_data in prices_data.items():
                for city, days_data in cities_data.items():
                    if city != 'Moscow':
                        continue

                    for days, total_price in days_data.items():
                        days_int = int(days)

                        self.data.append({
                            'Конкурент': 'Польза Диет',
                            'Линейка': diet_name,
                            'Город': city,
                            'Дней': days_int,
                            'Цена за день (руб)': total_price // days_int,
                            'Общая цена (руб)': total_price
                        })


        except json.JSONDecodeError:
            print("Ошибка JSON")
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    parser = PolzaDietParser()

    parser.parse()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    save_path = os.path.join(project_root, 'data', 'raw', 'polza_diet.csv')

    parser.save_to_csv(save_path)