import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("food_coded.csv")

comfort_map = {
    1: "Стресс",
    2: "Скука",
    3: "Грусть",
    4: "Голод",
    5: "Другое",
    6: "Другое"
}

cook_map = {
    1: "Каждый день",
    2: "2-3 раза\nв неделю",
    3: "Не часто",
    4: "Только по\nпраздникам",
    5: "Никогда"
}

eating_out_map = {
    1: "Никогда",
    2: "1-2 раза\nв неделю",
    3: "2-3 раза\nв неделю",
    4: "3-5 раз\nв неделю",
    5: "Каждый день"
}

income_map = {
    1: "Менее\n$15k",
    2: "$15k-\n$30k",
    3: "$30k-\n$50k",
    4: "$50k-\n$70k",
    5: "$70k-\n$100k",
    6: "Более\n$100k"
}

gender_map = {1: "Женщины", 2: "Мужчины"}

fig, axes = plt.subplots(2, 3, figsize=(16, 12))

# круговая почему едят вредную (комфортную) еду
comfort_counts = df["comfort_food_reasons_coded"].map(comfort_map).value_counts()
axes[0, 0].pie(comfort_counts.values, labels=comfort_counts.index, autopct="%1.1f%%", startangle=90, colors=["#ff6b6b", "#ffa502", "#ff6348", "#7bed9f", "#70a1ff"])
axes[0, 0].set_title("Почему люди едят комфортную еду?")

# столбики как часто готовят
cook_counts = df["cook"].map(cook_map).value_counts()
cook_order = ["Каждый день", "2-3 раза\nв неделю", "Не часто", "Только по\nпраздникам", "Никогда"]
cook_counts = cook_counts.reindex(cook_order)
axes[0, 1].bar(cook_counts.index, cook_counts.values, color="#4ecdc4")
axes[0, 1].set_title("Как часто люди готовят сами?")
axes[0, 1].tick_params(axis='x', rotation=0)

# опять столбики как часть едят все дома
eating_counts = df["eating_out"].map(eating_out_map).value_counts()
eating_order = ["Никогда", "1-2 раза\nв неделю", "2-3 раза\nв неделю", "3-5 раз\nв неделю", "Каждый день"]
eating_counts = eating_counts.reindex(eating_order)
axes[0, 2].bar(eating_counts.index, eating_counts.values, color="#45b7d1")
axes[0, 2].set_title("Как часто едят вне дома?")
axes[0, 2].tick_params(axis='x', rotation=0)

# гистограмма доходов
income_counts = df["income"].map(income_map).value_counts()
income_order = ["Менее\n$15k", "$15k-\n$30k", "$30k-\n$50k", "$50k-\n$70k", "$70k-\n$100k", "Более\n$100k"]
income_counts = income_counts.reindex(income_order)
axes[1, 0].bar(income_counts.index, income_counts.values, color="#f39c12")
axes[1, 0].set_title("Распределение доходов ЦА")
axes[1, 0].tick_params(axis='x', rotation=0)

#Круговая пол
gender_counts = df["Gender"].map(gender_map).value_counts()
axes[1, 1].pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%", startangle=90, colors=["#ff69b4", "#4169e1"])
axes[1, 1].set_title("Пол ЦА")

# Пустой график а то выглядит не оч
axes[1, 2].axis("off")

plt.tight_layout()
plt.savefig("audience_analysis.png", dpi=200, bbox_inches="tight")
plt.show()