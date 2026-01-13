import streamlit as st
import pandas as pd

# path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'


st.title("Загрузка данных")

if "df" in st.session_state:
    tips_df = st.session_state.df
else:
    tips_df = None

@st.cache_data(ttl=3600)
def load_file(file_tips):
    if file_tips is not None:
        try:
            df = pd.read_csv(file_tips)
            st.success("Файл успешно загружен!")
            st.session_state["df"] = df
            return df
        except Exception as e:
            st.error(f"Ошибка при чтении файла: {e}")
            return None
    else:
        st.warning("Пожалуйста, загрузите CSV-файл.")
        return None

with st.sidebar:
    file_tips = st.file_uploader("Upload file CSV", type=["csv"])

    if file_tips is not None:
        tips_df = load_file(file_tips)
    elif "df" in st.session_state:
        tips_df = st.session_state.df


if tips_df is not None:
    st.subheader("Загруженный датафрейм `tips`")    
    st.dataframe(tips_df)

    st.subheader("Размер датафрейма `tips`")    
    row_df = tips_df.shape[0]
    col_df = tips_df.shape[1]
    st.write(f"Размер датафрейма: {row_df} строк на {col_df} колонок")

    st.subheader("Статистика `tips`")    
    st.dataframe(tips_df.describe(include='all'))


