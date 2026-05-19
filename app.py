import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Data Science Lab 5 - Moriarty", layout="wide")


@st.cache_data
def get_data():
    np.random.seed(42)
    years = np.arange(1981, 2025)
    weeks = np.arange(1, 53)
    data = []
    for y in years:
        for w in weeks:
            for p in range(1, 28):
                data.append([y, w, p, np.random.uniform(10, 90), np.random.uniform(10, 90), np.random.uniform(10, 90)])
    return pd.DataFrame(data, columns=['Year', 'Week', 'Province', 'VCI', 'TCI', 'VHI'])

df = get_data()


provinces = {1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
             6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
             11: 'Луганська', 12: 'Львівська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська',
             16: 'Рівненська', 17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
             21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська', 25: 'Республіка Крим',
             26: 'Київ', 27: 'Севастополь'}


st.sidebar.header("Налаштування фільтрів")


def reset():
    st.session_state.p = 1
    st.session_state.i = 'VHI'
    st.session_state.y = (1981, 2024)
    st.session_state.w = (1, 52)

st.sidebar.button("Очистити все", on_click=reset)

selected_ind = st.sidebar.selectbox("Оберіть індекс:", ['VCI', 'TCI', 'VHI'], key='i')
selected_prov = st.sidebar.selectbox("Оберіть область:", options=list(provinces.keys()), format_func=lambda x: provinces[x], key='p')
year_range = st.sidebar.slider("Роки:", 1981, 2024, (1981, 2024), key='y')
week_range = st.sidebar.slider("Тижні:", 1, 52, (1, 52), key='w')

st.sidebar.markdown("---")
asc = st.sidebar.checkbox("Сортувати за зростанням")
desc = st.sidebar.checkbox("Сортувати за спаданням")


st.title("Аналіз стану рослинності в Україні")
st.write(f"**Область:** {provinces[selected_prov]} | **Індекс:** {selected_ind}")


filt = df[(df['Province'] == selected_prov) & 
          (df['Year'].between(year_range[0], year_range[1])) &
          (df['Week'].between(week_range[0], week_range[1]))].copy()


if asc and desc:
    st.warning("⚠️ Виберіть лише один тип сортування!")
elif asc:
    filt = filt.sort_values(by=selected_ind)
elif desc:
    filt = filt.sort_values(by=selected_ind, ascending=False)


tab1, tab2 = st.tabs(["📊 Графіки", "📄 Дані"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Динаміка індексу")
        fig, ax = plt.subplots()
        sns.lineplot(data=filt, x='Year', y=selected_ind, ax=ax, color='green')
        st.pyplot(fig)
    with col2:
        st.subheader("Розподіл значень")
        fig2, ax2 = plt.subplots()
        sns.histplot(filt[selected_ind], kde=True, ax=ax2, color='orange')
        st.pyplot(fig2)

with tab2:
    st.dataframe(filt[['Year', 'Week', selected_ind]], use_container_width=True)