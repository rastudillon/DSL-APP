import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

ruta_logo = "logo3_uta.png"
logo = Image.open(ruta_logo)
tamaño_logo = (290,290)

st.set_page_config(layout="wide", page_title="Dashboard DSL", page_icon=":chart_with_upwards_trend:", initial_sidebar_state="collapsed")
st.sidebar.image(logo,width=tamaño_logo[0])

@st.cache_data

def cargar_datos(archivo_excel):
    return pd.read_excel(archivo_excel)

def principal():
    size_title = 'font-size: 24px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Aplicación para análisis exploratorio y visual de la DSL"
    st.sidebar.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    st.sidebar.write("Seleccione una base de datos")
    archivo_excel = st.sidebar.file_uploader("Elija archivo Excel",type=["xlsx"])
    bd_default = "solicitudes.xlsx"
    df = cargar_datos(bd_default)
    if archivo_excel is None:
        st.write(df.head())

principal()
