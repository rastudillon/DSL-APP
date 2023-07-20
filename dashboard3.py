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

def df_mod(df):
    df.drop(columns=["Adj.","Resumen","Fecha de Recepción","Funcionario Encargado_cod","Funcionario Encargado_dsc",
                     "Solicitud de Compra","Nº de Horas Hombre","Cantidad de Personas Involucradas","Material Utilizado",
                     "Rut Responsable_dsc"], inplace=True)
    df.fillna(0, inplace=True)
    df["Ejecutada"] = df["Fecha de Término"].apply(lambda x: "No" if x == 0 else "Si")
    cambiar_nombres = {"Centro de Costo_cod":"Código CCosto","Centro de Costo_dsc":"Nombre CCosto"}

    df.rename(columns=cambiar_nombres, inplace=True)

    df.Fecha = pd.to_datetime(df.Fecha, format= "%d-%m-%Y")
    df["Mes"] = df.Fecha.dt.strftime("%B")
    df["Año"] = df.Fecha.dt.strftime("%Y")

    return df

def cargar_datos(archivo_excel):
    return pd.read_excel(archivo_excel)

def div_st_metric():
    div_style = "background: linear-gradient(to right, #0A0908, #22333B);padding:1px;border-radius:5px;text-align:center;"
    return div_style

def tit_st_metric():
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    return title_style

def porc_pend_dashboard_anual(df):
    ejec = df.Ejecutada[(df.Año=="2023")&(df.Ejecutada=="Si")].value_counts()
    pend = df.Ejecutada[(df.Año=="2023")&(df.Ejecutada=="No")].value_counts()
    total = np.sum(ejec)+np.sum(pend)
    porc = round(np.sum(pend)/total*100)

    if porc >= 40:
        color = 'color: red; font-size: 50px; text-align: center'
    elif porc >= 30:
        color = 'color: orange; font-size: 50px; text-align: center'
    else:
        color = 'color: #5DD39E; font-size: 50px; text-align: center'

    titulo = "Porcentaje total de pendientes"

    metric_html = f"<div style= '{div_st_metric()}'>"\
        f"<span style= '{tit_st_metric()}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{porc}%</span></div>"
    if total == 0:
        return st.write("Periodo no registrado")
    else:
        return st.write(metric_html,unsafe_allow_html=True)
    
def dashboard_anual(df):

    size_title = 'font-size: 22px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Indicadores Dirección de Servicios y Logística - Año 2023"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        porc_pend_dashboard_anual(df)

    with c2:
        pass
        # porc_ejec_dashboard_anual(df)

    with c3:
        pass
        # cant_pend_dashboard_anual(df)

    with c4:
        pass
        # cant_ejec_dashboard_anual(df)  

def principal():
    size_title = 'font-size: 24px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Aplicación para análisis exploratorio y visual de la DSL"
    st.sidebar.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    st.sidebar.write("Seleccione una base de datos")
    archivo_excel = st.sidebar.file_uploader("Elija Base de Datos",type=["xlsx"])
    bd_default = "solicitudes.xlsx"
    df_default = cargar_datos(bd_default)
    if archivo_excel is None:
        df = df_mod(df_default)
        dashboard_anual(df)

principal()
