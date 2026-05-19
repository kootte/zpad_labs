# %% [markdown]
# # Лабораторна робота №2. Частина 2
# **Студент:** Moriarty (ФБ-44)
# **Дисципліна:** Наука про дані: підготовчий етап

# %% [markdown]
# ## 1. Завантаження та очищення датасету
# Датасет: Individual Household Electric Power Consumption

# %%
import urllib.request
import zipfile
import os
import pandas as pd
import numpy as np
import timeit
import datetime  # Додано імпорт модуля datetime для коректної роботи Завдання 2.4

def download_and_extract_power_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
    zip_path = "household_power_consumption.zip"
    txt_path = "household_power_consumption.txt"
    
    if not os.path.exists(txt_path):
        print("Завантаження датасету (близько 20МБ)...")
        urllib.request.urlretrieve(url, zip_path)
        print("Розпакування...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
    return txt_path

# Завантажуємо і читаємо дані
file_path = download_and_extract_power_data()
print("Читання датасету...")
df_power = pd.read_csv(file_path, sep=';', na_values=['?'], low_memory=False)

# Очищення (видаляємо пропущені значення)
df_power = df_power.dropna()
# Перетворюємо типи
df_power['Date'] = pd.to_datetime(df_power['Date'], format='%d/%m/%Y')
df_power['Time'] = pd.to_datetime(df_power['Time'], format='%H:%M:%S').dt.time

print("Датасет успішно завантажено та очищено. Перші 5 рядків:")
print(df_power.head())

# %% [markdown]
# ## 2. Вибірки та аналіз часу виконання (timeit)

# %% [markdown]
# ### Завдання 2.1. Обрати всі записи, у яких загальна активна споживана потужність перевищує 5 кВт.
# %%
def query_1():
    return df_power[df_power['Global_active_power'] > 5.0]

start_time = timeit.default_timer()
res_1 = query_1()
time_1 = timeit.default_timer() - start_time

print(f"Час виконання Завдання 1: {time_1:.5f} секунд. Знайдено записів: {len(res_1)}")

# %% [markdown]
# ### Завдання 2.2. Записи, у яких сила струму 19-20 А, і пральна машина з холодильником (Sub_2) споживають більше, ніж бойлер та кондиціонер (Sub_3).
# %%
def query_2():
    return df_power[
        (df_power['Global_intensity'] >= 19.0) & 
        (df_power['Global_intensity'] <= 20.0) & 
        (df_power['Sub_metering_2'] > df_power['Sub_metering_3'])
    ]

start_time = timeit.default_timer()
res_2 = query_2()
time_2 = timeit.default_timer() - start_time

print(f"Час виконання Завдання 2: {time_2:.5f} секунд. Знайдено записів: {len(res_2)}")

# %% [markdown]
# ### Завдання 2.3. Випадковим чином обрати 500 000 записів і обчислити середні величини 3-х груп споживання.
# %%
def query_3():
    sample_df = df_power.sample(n=500000, replace=False, random_state=42)
    means = sample_df[['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']].mean()
    return means

start_time = timeit.default_timer()
res_3 = query_3()
time_3 = timeit.default_timer() - start_time

print(f"Час виконання Завдання 3: {time_3:.5f} секунд.")
print("Середні значення 3-х груп:")
print(res_3)

# %% [markdown]
# ### Завдання 2.4. Складний запит (Час > 18:00, Потужність > 6, Sub_2 > Sub_1 та Sub_2 > Sub_3, кожен 3й з першої половини і кожен 4й з другої).
# %%
def query_4():
    # Фільтрація з використанням datetime.time
    q_df = df_power[
        (df_power['Time'] > datetime.time(18, 0, 0)) & 
        (df_power['Global_active_power'] > 6.0) & 
        (df_power['Sub_metering_2'] > df_power['Sub_metering_1']) & 
        (df_power['Sub_metering_2'] > df_power['Sub_metering_3'])
    ]
    
    # Поділ навпіл
    half = len(q_df) // 2
    first_half = q_df.iloc[:half]
    second_half = q_df.iloc[half:]
    
    # Вибір кожного 3го та 4го
    final_res = pd.concat([first_half.iloc[::3], second_half.iloc[::4]])
    return final_res

start_time = timeit.default_timer()
res_4 = query_4()
time_4 = timeit.default_timer() - start_time

print(f"Час виконання Завдання 4: {time_4:.5f} секунд. Знайдено записів: {len(res_4)}")

# %% [markdown]
# ## 3. Статистичний аналіз та трансформація

# %% [markdown]
# ### 3.1. Нормування та стандартизація
# %%
numeric_cols = ['Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity']

# Нормування (Min-Max Scaling)
df_normalized = (df_power[numeric_cols] - df_power[numeric_cols].min()) / (df_power[numeric_cols].max() - df_power[numeric_cols].min())

# Стандартизація (Z-score)
df_standardized = (df_power[numeric_cols] - df_power[numeric_cols].mean()) / df_power[numeric_cols].std()

print("Нормовані дані:")
print(df_normalized.head(3))
print("Стандартизовані дані:")
print(df_standardized.head(3))

# %% [markdown]
# ### 3.2. Коефіцієнти Пірсона та Спірмена
# %%
from scipy.stats import pearsonr, spearmanr

col1 = df_power['Global_active_power']
col2 = df_power['Global_intensity']

pearson_corr = col1.corr(col2, method='pearson')
spearman_corr = col1.corr(col2, method='spearman')

print(f"Кореляція між Active Power та Intensity:")
print(f"Пірсон: {pearson_corr:.4f}")
print(f"Спірмен: {spearman_corr:.4f}")

# %% [markdown]
# ### 3.3. One Hot Encoding категоріального атрибута
# Для цього створимо категоріальний атрибут "Місяць" з дати.
# %%
# Створюємо атрибут "Місяць"
df_power['Month'] = df_power['Date'].dt.month_name()

# One Hot Encoding
df_encoded = pd.get_dummies(df_power, columns=['Month'], prefix='Month')

print("Дані після One Hot Encoding (Останні 12 колонок):")
print(df_encoded.iloc[:, -12:].head())