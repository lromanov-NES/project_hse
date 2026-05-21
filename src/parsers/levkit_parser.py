import json
import os
from bs4 import BeautifulSoup
from base_parser import BaseParser


class LevelKitchenParser(BaseParser):
    def __init__(self):
        super().__init__(base_url="https://levelkitchen.com/")

    def parse(self):
        print(f"Парсим {self.base_url}")
        html = self.fetch_page(self.base_url)

        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        nuxt_script = soup.find('script', id='__NUXT_DATA__')

        if not nuxt_script:
            print("Не найден тег __NUXT_DATA__.")
            return

        try:
            data = json.loads(nuxt_script.string)

            def get_val(idx):
                return data[idx] if isinstance(idx, int) and idx < len(data) else idx

            target_programs = ['ФИТ', 'ХИТ', 'ПРО']

            for item in data:
                if isinstance(item, dict) and (
                        'ruName' in item or 'label' in item) and 'calories' in item and 'variants' in item:
                    try:
                        name_idx = item.get('ruName') or item.get('label')
                        program_name = str(get_val(name_idx)).upper()

                        if program_name not in target_programs:
                            continue

                        calories = get_val(item['calories'])
                        variants_list = get_val(item['variants'])

                        if isinstance(variants_list, list):
                            for var_idx in variants_list:
                                variant = get_val(var_idx)
                                if isinstance(variant, dict) and 'price' in variant and 'length' in variant:
                                    total_price = get_val(variant['price'])
                                    days = get_val(variant['length'])

                                    if isinstance(total_price, (int, float)) and isinstance(days,
                                                                                            (int, float)) and days > 0:
                                        daily_price = int(total_price / days)

                                        self.data.append({
                                            'Конкурент': 'Level Kitchen',
                                            'Линейка': program_name,
                                            'Калорийность': f"{calories} ккал",
                                            'Дней': days,
                                            'Цена за день (руб)': daily_price,
                                            'Общая цена (руб)': total_price
                                        })
                    except Exception:
                        continue

            unique_data = [dict(t) for t in {tuple(d.items()) for d in self.data}]

            def extract_cal(val):
                try:
                    return int(str(val).split()[0])
                except:
                    return 0

            self.data = sorted(unique_data,
                               key=lambda x: (x['Линейка'], extract_cal(x['Калорийность']), int(x['Дней'])))

        except json.JSONDecodeError:
            print("Ошибка JSON")


if __name__ == "__main__":
    parser = LevelKitchenParser()
    parser.parse()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    save_path = os.path.join(project_root, 'data', 'raw', 'level_kitchen.csv')

    parser.save_to_csv(save_path)