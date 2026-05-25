import streamlit as st
import pandas as pd
import os

def load_data():
    if os.path.exists("vhi_data.csv"):
        return pd.read_csv("vhi_data.csv")
    else:
        return pd.DataFrame({
            "Year": [2020, 2020, 2021, 2021],
            "Week": [1, 2, 1, 2],
            "Province": [1, 1, 2, 2],
            "VCI": [40, 45, 50, 55],
            "TCI": [30, 35, 40, 45],
            "VHI": [35, 40, 45, 50]
        })

st.set_page_config(layout="wide")

df = load_data()

col1, col2 = st.columns([1, 3])

with col1:
    indicator = st.selectbox("Оберіть індекс", ["VCI", "TCI", "VHI"])
    province = st.selectbox("Оберіть область", df['Province'].unique())
    
    min_week, max_week = int(df['Week'].min()), int(df['Week'].max())
    week_range = st.slider("Інтервал тижнів", min_week, max_week, (min_week, max_week))
    
    min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
    year_range = st.slider("Інтервал років", min_year, max_year, (min_year, max_year))
    
    sort_asc = st.checkbox("За зростанням")
    sort_desc = st.checkbox("За спаданням")
    
    if st.button("Скинути фільтри"):
        st.rerun()

filtered_df = df[
    (df['Province'] == province) &
    (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) &
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
]

if sort_asc and sort_desc:
    st.warning("Оберіть лише один тип сортування.")
elif sort_asc:
    filtered_df = filtered_df.sort_values(by=indicator, ascending=True)
elif sort_desc:
    filtered_df = filtered_df.sort_values(by=indicator, ascending=False)

with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця даних", "Графік відфільтрованих даних", "Порівняння по областях"])
    
    with tab1:
        st.dataframe(filtered_df)
        
    with tab2:
        chart_data = filtered_df.copy()
        chart_data['Time'] = chart_data['Year'].astype(str) + " - W" + chart_data['Week'].astype(str)
        st.line_chart(chart_data.set_index('Time')[indicator])
        
    with tab3:
        comp_df = df[
            (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) &
            (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
        ]
        comp_df['Time'] = comp_df['Year'].astype(str) + " - W" + comp_df['Week'].astype(str)
        comp_pivot = comp_df.pivot_table(index='Time', columns='Province', values=indicator)
        st.line_chart(comp_pivot)