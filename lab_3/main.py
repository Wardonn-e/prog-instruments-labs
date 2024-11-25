import pandas as pd
import re

# Регулярное выражение email
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Чтение CSV
df = pd.read_csv("data.csv", sep=";", encoding="UTF-16")

email_column = df.iloc[:, 0]

invalid_data = []

for index, value in email_column.items():
    if not re.match(email_regex, str(value)):
        invalid_data.append(index)

print("Невалидные email:")
print(email_column[invalid_data])

print("\nНомера строк с невалидными email:")
print(invalid_data)


