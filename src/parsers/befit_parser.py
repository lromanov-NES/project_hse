import json
import os
from bs4 import BeautifulSoup
from base_parser import BaseParser


class BeFitParser(BaseParser):
    def __init__(self):
        super().__init__(base_url="https://letbefit.ru/")

    def parse(self):
        print(f"Парсим {self.base_url}")
        html = self.fetch_page(self.base_url)

        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        nuxt_script = soup.find('script', id='__NUXT_DATA__')

        if not nuxt_script:
            print("Не найден тег __NUXT_DATA__")
            return

        try:
            data = json.loads(nuxt_script.string)

            def get_val(idx):
                return data[idx] if isinstance(idx, int) and idx < len(data) else idx

            for item in data:
                if isinstance(item, dict) and 'courseId' in item and 'name' in item and 'kkal' in item:
                    try:
                        name = get_val(item['name'])
                        kkal = get_val(item['kkal'])

                        price5 = get_val(item.get('price'))
                        price7 = get_val(item.get('price7'))

                        if isinstance(name, str) and len(name) > 2:
                            if str(price5).isdigit() and int(price5) > 0:
                                self.data.append({
                                    'Конкурент': 'BeFit',
                                    'Линейка': name.upper(),
                                    'Калорийность': f"{kkal} ккал",
                                    'Дней': 5,
                                    'Цена за день (руб)': int(price5) // 5,
                                    'Общая цена (руб)': int(price5)
                                })
                            if str(price7).isdigit() and int(price7) > 0:
                                self.data.append({
                                    'Конкурент': 'BeFit',
                                    'Линейка': name.upper(),
                                    'Калорийность': f"{kkal} ккал",
                                    'Дней': 7,
                                    'Цена за день (руб)': int(price7) // 7,
                                    'Общая цена (руб)': int(price7)
                                })
                    except Exception:
                        continue

            unique_data = [dict(t) for t in {tuple(d.items()) for d in self.data}]

            def extract_cal(val):
                try:
                    return int(str(val).split()[0])
                except:
                    return 0

            self.data = sorted(unique_data, key=lambda x: (extract_cal(x['Калорийность']), x['Дней']))


        except json.JSONDecodeError:
            print("Ошибка JSON")


if __name__ == "__main__":
    parser = BeFitParser()
    parser.parse()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    save_path = os.path.join(project_root, 'data', 'raw', 'befit.csv')

    parser.save_to_csv(save_path)