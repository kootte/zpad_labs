# %% [markdown]
# # Лабораторна робота №2. Частина 1
# **Студент:** Moriarty (ФБ-44)
# **Дисципліна:** Наука про дані: підготовчий етап

# %% [markdown]
# ## 1. Завантаження даних

# %%
import urllib.request
import os
import datetime
import pandas as pd

def download_noaa_data(province_id, target_dir="vhi_data"):
    """
    Завантажує файл VHI для заданої області, якщо він ще не завантажений.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    
    existing_files = [f for f in os.listdir(target_dir) if f.startswith(f"vhi_id_{province_id}_")]
    if existing_files:
        print(f"Дані для області {province_id} вже завантажено: {existing_files[0]}")
        return
        
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2024&type=Mean"
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = os.path.join(target_dir, f"vhi_id_{province_id}_{timestamp}.csv")
    
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
            
            text = text.replace("<tt><pre>", "").replace("</pre></tt>", "")
            with open(filename, 'w') as out:
                out.write(text)
        print(f"Завантажено: {filename}")
    except Exception as e:
        print(f"Помилка завантаження області {province_id}: {e}")


print("--- ПОЧАТОК ЗАВАНТАЖЕННЯ ---")
for i in range(1, 28):
    download_noaa_data(i)
print("--- ЗАВАНТАЖЕННЯ ЗАВЕРШЕНО ---")

# %% [markdown]
# ## 2. Data Cleaning та підготовка DataFrame

# %%
def create_dataframe(data_dir="vhi_data"):
    """
    Зчитує всі CSV файли з директорії, ігноруючи помилки форматування NOAA 
    (зайві коми в кінці рядка).
    """
    files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]
    dfs = []
    
    for file in files:
        
        original_id = int(file.split('vhi_id_')[1].split('_')[0])
        
        
        with open(file, 'r') as f:
            lines = f.readlines()
            
        clean_data = []
        for line in lines:
            
            line = line.replace('<tt><pre>', '').replace('</pre></tt>', '').strip()
            
            
            if not line or 'year' in line.lower():
                continue
                
            parts = [p.strip() for p in line.split(',')]
            
           
            if len(parts) >= 7:
                try:
                    year = int(parts[0])
                    week = int(parts[1])
                    vci = float(parts[4])
                    tci = float(parts[5])
                    vhi = float(parts[6])
                    
                    
                    if vhi != -1:
                        clean_data.append([year, week, vci, tci, vhi])
                except ValueError:
                    
                    continue
        
        
        df = pd.DataFrame(clean_data, columns=['year', 'week', 'VCI', 'TCI', 'VHI'])
        df['Original_ID'] = original_id
        dfs.append(df)
        
    if not dfs:
        return pd.DataFrame()
        
    full_df = pd.concat(dfs, ignore_index=True)
    
    
    noaa_to_ukr = {
        24: 1, 25: 2, 5: 3, 6: 4, 27: 5, 23: 6, 26: 7, 7: 8, 11: 9, 13: 10,
        14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 21: 17, 22: 18, 8: 19,
        9: 20, 10: 21, 1: 22, 3: 23, 2: 24, 4: 25, 12: 26, 20: 27
    }
    
    ukr_names = {
        1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
        6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
        11: 'Луганська', 12: 'Львівська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська',
        16: 'Рівненська', 17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
        21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська', 25: 'Республіка Крим',
        26: 'Київ', 27: 'Севастополь'
    }
    
    full_df['Province_ID'] = full_df['Original_ID'].map(noaa_to_ukr)
    full_df['Province_Name'] = full_df['Province_ID'].map(ukr_names)
    
    
    return full_df[['year', 'week', 'Province_ID', 'Province_Name', 'VHI', 'VCI', 'TCI']]

df = create_dataframe()
print(df.head())

# %% [markdown]
# ## 3. Процедури для формування вибірок

# %% [markdown]
# ### 3.1. Ряд VHI для області за вказаний рік
# %%
def get_vhi_by_year_and_province(dataframe, province_id, year):
    """Повертає ряд VHI для вказаної області та року."""
    res = dataframe[(dataframe['Province_ID'] == province_id) & (dataframe['year'] == year)]
    return res[['week', 'VHI']]

print("Вибірка: VHI для Київської області (ID: 9) за 2020 рік:")
print(get_vhi_by_year_and_province(df, 9, 2020).head())

# %% [markdown]
# ### 3.2. Ряд VHI за вказаний діапазон років для вказаних областей
# %%
def get_vhi_by_years_and_provinces(dataframe, province_ids, year_min, year_max):
    """Повертає ряд VHI для діапазону років та списку областей."""
    res = dataframe[
        (dataframe['Province_ID'].isin(province_ids)) & 
        (dataframe['year'] >= year_min) & 
        (dataframe['year'] <= year_max)
    ]
    return res[['year', 'week', 'Province_Name', 'VHI']]

print("Вибірка: VHI для Київської (9) та Одеської (14) областей за 2021-2022 роки:")
print(get_vhi_by_years_and_provinces(df, [9, 14], 2021, 2022).head())

# %% [markdown]
# ### 3.3. Пошук екстремумів, середнього та медіани
# %%
def get_vhi_stats(dataframe, province_id, year):
    """Пошук екстремумів (min/max), середнього та медіани."""
    subset = dataframe[(dataframe['Province_ID'] == province_id) & (dataframe['year'] == year)]['VHI']
    
    if subset.empty:
        return {"min": None, "max": None, "mean": None, "median": None}
        
    return {
        "min": subset.min(),
        "max": subset.max(),
        "mean": subset.mean(),
        "median": subset.median()
    }

stats = get_vhi_stats(df, 9, 2020)
print(f"Статистика VHI для Київської області за 2020 рік:\nМінімум: {stats['min']}\nМаксимум: {stats['max']}\nСереднє: {stats['mean']:.2f}\nМедіана: {stats['median']}")