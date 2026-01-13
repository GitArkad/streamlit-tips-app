import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import io
import datetime

st.title("Графики")

if "df" in st.session_state:
    tips_df = st.session_state.df
else:
    tips_df = None

if tips_df is None:
    st.warning("Загрузите CSV-файл на странице 'load data'.")
else:
    with st.sidebar:
        st.header("тип графика")
        chart_type = st.radio(
            "Выберите тип графика",
            ["Линейный", "Гистограмма", "Виолин", "Ящик с усами", "Скаттер"]
        )
        
        if chart_type == "Скаттер":
            x_df = st.selectbox("Ось X", list(tips_df.select_dtypes(include=['int64', 'float64']).columns))
            y_df = st.selectbox("Оси Y", tips_df.select_dtypes(include=['int64', 'float64']).columns)
            hue_df = st.selectbox("Группировка hue", [None] + list(tips_df.columns))
        elif chart_type == "Линейный":
            x_df = st.selectbox("Ось X", list(tips_df.select_dtypes(include=['int64', 'float64']).columns))
            y_df = st.selectbox("Оси Y", tips_df.select_dtypes(include=['int64', 'float64']).columns)
            hue_df = st.selectbox("Группировка", [None] + list(tips_df.select_dtypes(include=['category', 'bool', 'object']).columns))
        elif chart_type == "Гистограмма":
            x_df = st.selectbox("Ось X", list(tips_df.select_dtypes(include=['int64', 'float64']).columns))
            hue_df = st.selectbox("Группировка", [None] + list(tips_df.select_dtypes(include=['category', 'bool', 'object']).columns))
        elif chart_type == "Виолин":
            y_df = st.selectbox("Числовая переменная (Y)", list(tips_df.select_dtypes(include=['int64', 'float64']).columns))
            x_df = st.selectbox("Категория (X)", list(tips_df.select_dtypes(include=['category', 'bool', 'object']).columns))
            hue_df = st.selectbox("Группировка", [None] + list(tips_df.select_dtypes(include=['category', 'bool', 'object']).columns)) 
        else:  # Ящик с усами
            y_df = st.selectbox("Числовая переменная (Y)", list(tips_df.select_dtypes(include=['int64', 'float64']).columns))
            x_df = st.selectbox("Категория (X)", list(tips_df.select_dtypes(include=['category', 'bool', 'object']).columns))
            hue_df = st.selectbox("Группировка", [None] + list(tips_df.select_dtypes(include=['category', 'bool', 'object']).columns))       

    st.title(f"{chart_type}")

    fig = None
    if x_df:
        if chart_type == "Скаттер":
            fig = px.scatter(tips_df, x=x_df, y=y_df, color=hue_df if hue_df else None, template="plotly_white")
        elif chart_type == "Линейный":
            fig = px.line(tips_df, x=x_df, y=y_df, color=hue_df if hue_df else None, template="plotly_white")
        elif chart_type == "Гистограмма":
            fig = px.histogram(tips_df, x=x_df, color=hue_df if hue_df else None, template="plotly_white")
        elif chart_type == "Виолин":
            fig = px.violin(tips_df, x=x_df, y=y_df, color=hue_df if hue_df else None, points="all", template="plotly_white")
        else:  # боксплот
            fig = px.box(tips_df, x=x_df, y=y_df, points="all", color=hue_df if hue_df else None, template="plotly_white")

        if fig:
            st.plotly_chart(fig, use_container_width=True)

            buffer = io.BytesIO()
            img_bytes = pio.to_image(fig, format='png', width=1200, height=800, scale=2)
            st.sidebar.download_button(
                label="Скачать график (PNG)",
                data=img_bytes,
                file_name=f"{chart_type.lower().replace(' ', '_')}_plot_{datetime.datetime.now().strftime("%d%m%Y%H%M%S")}.png",
                mime="image/png"
            )
    else:
        st.warning("Выберите хотя бы одну колонку для оси X.")
