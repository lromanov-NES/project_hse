import pandas as pd

# Датасет взят из кагла и состоит из опроса американцев 9 лет назад, почему выводы актуальны для нашего проекта будет отдельный слайд
df = pd.read_csv("food_coded.csv")

# словари для перевода этих дурацких цифр в нормальные названия
gen = {1: "Female", 2: "Male"}
cook_d = {1: "Every day", 2: "2-3 times/week", 3: "Not often", 4: "Only holidays", 5: "Never"}
eat_d = {1: "Never", 2: "1-2 times/week", 3: "2-3 times/week", 4: "3-5 times/week", 5: "Every day"}
ex_d = {1: "Every day", 2: "2-3 times/week", 3: "Once a week", 4: "Sometimes", 5: "Never"}
pay_d = {1: "up to $5", 2: "$5-$10", 3: "$10-$20", 4: "$20-$30", 5: "$30-$40", 6: "more than $40"}
veg_d = {1: "Very unlikely", 2: "Unlikely", 3: "Neutral", 4: "Likely", 5: "Very likely"}
fruit_d = {1: "Very unlikely", 2: "Unlikely", 3: "Neutral", 4: "Likely", 5: "Very likely"}
inc_d = {1: "Less than $15k", 2: "$15k-$30k", 3: "$30k-$50k", 4: "$50k-$70k", 5: "$70k-$100k", 6: "More than $100k"}
grade_d = {1: "Freshman", 2: "Sophomore", 3: "Junior", 4: "Senior"}
w_d = {1: "Slim", 2: "Very fit", 3: "Just right", 4: "Slightly overweight", 5: "Overweight", 6: "Don't think in these terms"}

# применяем перевод (копипаста, но работает)
df["gender_lab"] = df["Gender"].map(gen)
df["cook_lab"] = df["cook"].map(cook_d)
df["eat_lab"] = df["eating_out"].map(eat_d)
df["ex_lab"] = df["exercise"].map(ex_d)
df["pay_lab"] = df["pay_meal_out"].map(pay_d)
df["veg_lab"] = df["veggies_day"].map(veg_d)
df["fruit_lab"] = df["fruit_day"].map(fruit_d)
df["inc_lab"] = df["income"].map(inc_d)
df["grade_lab"] = df["grade_level"].map(grade_d)
df["w_lab"] = df["self_perception_weight"].map(w_d)

print("демография\n")

print("пол:")
print(df["gender_lab"].value_counts())

print("\nкурс:")
print(df["grade_lab"].value_counts())

print("\nдоход:")
print(df["inc_lab"].value_counts().sort_index())

print("\nпривычки\n")

print("как часто готовят:")
print(df["cook_lab"].value_counts())

print("\nкак часто едят вне дома:")
print(df["eat_lab"].value_counts())

print("\nовощи:")
print(df["veg_lab"].value_counts())

print("\nфрукты:")
print(df["fruit_lab"].value_counts())

print("\nсколько готовы платить:")
print(df["pay_lab"].value_counts().sort_index())

print("\nздоровье\n")

print("спорт:")
print(df["ex_lab"].value_counts())

print("\nкак оценивают вес:")
print(df["w_lab"].value_counts())

print("\nвитамины:")
print(df["vitamins"].value_counts().map({1: "Yes", 2: "No"}))

# хз почему, но healthy_feeling почему-то 1-10 где 1 это здоров, перепутано наверное
print(f"\nсредняя оценка здоровья: {df['healthy_feeling'].mean():.2f} (1=очень здоров, 10=нет)")