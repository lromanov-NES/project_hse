import pandas as pd
import re
import matplotlib.pyplot as plt

df = pd.read_csv("grow_food_bad_reviews.csv", delimiter=';')

# Словари для поиска проблем
problems = {
    "доставка": ["доставк", "привезл", "опозд", "задержк", "вовремя", "ждал", "курьер"],
    "сервис_поддержка": ["поддержк", "дозвонить", "ответ", "связь", "менеджер", "чат"],
    "качество_еды": ["невкусн", "вкус", "качеств", "свеж", "тухл", "просроч", "сух", "резин"],
    "цена": ["дорог", "цен", "деньг", "стоим", "руб"],
    "порции": ["маленьк", "мало", "порци", "голодн", "наелся"],
    "состав_обман": ["состав", "ингредиент", "мясо", "куриц", "на сайте", "картинк", "обман"]
}

# Анализируем каждый отзыв
results = []
for _, row in df.iterrows():
    text = row["text"].lower()
    found = {}
    for category, keywords in problems.items():
        matches = [kw for kw in keywords if kw in text]
        if matches:
            found[category] = matches
    results.append({
        "rating": row["rating"],
        "text": row["text"],
        "problems": found
    })

# Считаем статистику
stats = {}
for res in results:
    for cat in res["problems"].keys():
        stats[cat] = stats.get(cat, 0) + 1


print("топ проблем")

for cat, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
    print(f"{cat}: {count} упоминаний ({count/len(df)*100:.1f}%)")

print("примеры")

for cat in problems.keys():
    print(f"\n{cat.upper()} ")
    examples = [res["text"] for res in results if cat in res["problems"]]
    if examples:
        print(f"\"{examples[0][:200]}...\"")


# Теперь графики
data = {
    "Проблема": ["Доставка", "Качество еды", "Сервис/поддержка", "Цена","состав/обман"],
    "Упоминания": [8, 4, 2, 3, 1]
}

df = pd.DataFrame(data)


colors = ["#ff6b6b", "#ffa502", "#ff6348", "#7bed9f", "#70a1ff"]


fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df["Проблема"], df["Упоминания"], color=colors)


for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
            f'{int(width)}', ha='left', va='center', fontsize=12, fontweight='bold')


ax.set_xlabel("Количество упоминаний", fontsize=12)
ax.set_title("Главные проблемы конкурента (по отзывам)", fontsize=14, fontweight='bold')
ax.invert_yaxis()

plt.tight_layout()
plt.savefig("competitor_problems.png", dpi=150, bbox_inches="tight")
plt.show()
