import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plost
import missingno as msn
from PIL import Image

ruta_logo = "logo3_uta.png"
logo = Image.open(ruta_logo)
tamaño_logo = (290,290)

st.set_page_config(layout="wide", page_title="Dashboard DSL", page_icon=":chart_with_upwards_trend:", initial_sidebar_state="collapsed")
st.sidebar.image(logo,width=tamaño_logo[0])

@st.cache_data

def cargar_datos(archivo_excel):
    return pd.read_excel(archivo_excel)

def df_nulos (df):   
    fig, ax = plt.subplots()
    msn.matrix(df,ax=ax, fontsize=5.5,sparkline=False)
    return st.pyplot(fig)

def porc_pend_dashboard_anual(df):
    ejec = df.Ejecutada[(df.Año==2023)&(df.Ejecutada=="Si")].value_counts()
    pend = df.Ejecutada[(df.Año==2023)&(df.Ejecutada=="No")].value_counts()
    total = np.sum(ejec)+np.sum(pend)
    porc = round(np.sum(pend)/total*100)

    if porc >= 40:
        color = 'color: red; font-size: 50px; text-align: center'
    elif porc >= 30:
        color = 'color: orange; font-size: 50px; text-align: center'
    else:
        color = 'color: #5DD39E; font-size: 50px; text-align: center'

    div_style = "background: linear-gradient(to right, #0A0908, #22333B);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Porcentaje total de pendientes"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{porc}%</span></div>"
    if total == 0:
        return st.write("Periodo no registrado")
    else:
        return st.write(metric_html,unsafe_allow_html=True)

def porc_ejec_dashboard_anual(df):
    ejec = df.Ejecutada[(df.Año==2023)&(df.Ejecutada=="Si")].value_counts()
    pend = df.Ejecutada[(df.Año==2023)&(df.Ejecutada=="No")].value_counts()
    total = np.sum(ejec)+np.sum(pend)
    porc = round(np.sum(ejec)/total*100)

    if porc >= 70:
        color = 'color: #009B72; font-size: 50px;'
    elif porc >= 60:
        color = 'color: orange; font-size: 50px;'
    else:
        color = 'color: red; font-size: 50px;'

    div_style = "background: linear-gradient(to right, #22333B, #0A0908);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Porcentaje total de ejecutadas"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{porc}%</span></div>"
    if total == 0:
        return st.write("Periodo no registrado")
    else:
        return st.write(metric_html,unsafe_allow_html=True)
    
def cant_pend_dashboard_anual(df):
    pend = df.Ejecutada[(df.Ejecutada=="No")&(df.Año==2023)].count()

    color = 'color: #F5A65B; font-size: 50px; text-align: center'
    div_style = "background: linear-gradient(to right, #0A0908, #22333B);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Cantidad total de pendientes"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{pend}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def cant_ejec_dashboard_anual(df):    
    ejec = df.Ejecutada[(df.Ejecutada=="Si")&(df.Año==2023)].count()

    color = 'color: #32E875; font-size: 50px; text-align: center'
    div_style = "background: linear-gradient(to right, #22333B, #0A0908);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Cantidad total de ejecutadas"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{ejec}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def porc_ejec_dashboard_servicio(df_filt):
    ejec = df_filt[df_filt.Ejecutada=="Si"].value_counts().values
    no_ejec = df_filt[df_filt.Ejecutada=="No"].value_counts().values
    total = np.sum(ejec) + np.sum(no_ejec)
    porc = round(np.sum(ejec)/total*100)

    if porc >= 80:
        color = 'color: green; font-size: 70px;'
    elif porc >= 50:
        color = 'color: orange; font-size: 70px;'
    else:
        color = 'color: red; font-size: 70px;'

    div_style = "background: linear-gradient(to right, white, black);padding:1px;border-radius:5px;text-align:center;"

    metric_html = f"<div style= '{div_style}'><span style= '{color}'>{porc}%</span></div>"
    if total == 0:
        return st.write("Periodo no registrado")
    else:
        return st.write(metric_html,unsafe_allow_html=True)
    

def porc_no_ejec_dashboard_servicio(df_filt):
    ejec = df_filt[df_filt.Ejecutada=="Si"].value_counts().values
    no_ejec = df_filt[df_filt.Ejecutada=="No"].value_counts().values
    total = np.sum(ejec) + np.sum(no_ejec)
    porc = round(np.sum(no_ejec)/total*100)

    if porc >= 70:
        color = 'color: red; font-size: 70px; text-align: center'
    elif porc >= 40:
        color = 'color: orange; font-size: 70px; text-align: center'
    else:
        color = 'color: green; font-size: 70px; text-align: center'

    if total == 0:
        return st.write("Periodo no registrado")
    else:
        return st.markdown(f'<p style="{color}">{porc}%</p>',unsafe_allow_html=True)
    
def cant_pend_dashboard(df):
    pend = df.Ejecutada[df.Ejecutada=="No"].count()
    color = 'color: #FD5200; font-size: 70px; text-align: center'
    return st.markdown(f'<p style="{color}">{pend}</p>',unsafe_allow_html=True)

def cant_ejec_dashboard(df):    
    ejec = df.Ejecutada[df.Ejecutada=="Si"].count()
    color = 'color: #2D936C; font-size: 70px; text-align: center'
    return st.markdown(f'<p style="{color}">{ejec}</p>',unsafe_allow_html=True)

def graf_ccosto_dashboard_anual(df):
    df = df[df.Año == 2023]
    conteo_tipo_servicio = df.groupby(["Tipo de Servicio"]).size().reset_index(name="Cantidad")

    fig = px.pie(conteo_tipo_servicio,values="Cantidad",names="Tipo de Servicio",hole=.6)

    fig.update_layout(
        title={
            "text":"Porcentaje de solicitudes por servicio",
            "x":0.4,
            "xanchor": "right"
        },
        title_font_color= "#D8E2DC",
        font={
            "size":13}, height=350)

    st.plotly_chart(fig,use_container_width=True)

def graf_ccosto_acumulado_mensual_dashboard_anual(df):
    df = df[df.Año == 2023]
    conteo_ccosto = df.groupby(["Fecha","Nombre CCosto"]).size().reset_index(name="Cantidad")
    cant_ccosto_filtrados = conteo_ccosto.groupby('Nombre CCosto').filter(lambda x: x['Cantidad'].sum() > 40)

    fig = px.bar(cant_ccosto_filtrados, x="Fecha",y="Cantidad",color="Nombre CCosto")

    fig.update_layout(xaxis_title='Fecha',
                      yaxis_title='Cantidad de solicitudes',
                      title={
                          "text":"Cantidad diaria/mensual de solicitudes por centro de costos",
                          "x":0.5,
                          "xanchor": "center"},
                      title_font_color= "#D8E2DC",height=330)

    st.plotly_chart(fig,use_container_width=True) 

def graf_acumulado_servicios_mensual_dashboard(df):
    df = df[df.Año == 2023]
    df.Fecha = pd.to_datetime(df.Fecha)
    conteo_servicios = df.groupby([pd.Grouper(key="Fecha",freq="M"),"Tipo de Servicio"]).size().reset_index(name="Cantidad")
    fig = px.line(conteo_servicios, x="Fecha",y="Cantidad",color="Tipo de Servicio",markers=True)

    fig.update_layout(xaxis_title='Fecha',
                      yaxis_title='Cantidad de solicitudes',
                      title={
                          "text":"Cantidad mensual de solicitudes por servicio",
                          "x":0.5,
                          "xanchor": "center"},
                      title_font_color= "#D8E2DC", height=330)
    
    st.plotly_chart(fig,use_container_width=True)

def graf_campus_acum_dashboard(df):
    df = df[df.Año == 2023]
    conteo_campus = df.groupby(["Ubicación del Trabajo/Servicio"]).size().reset_index(name="Cantidad")
    fig = px.bar(conteo_campus,x="Cantidad",y="Ubicación del Trabajo/Servicio",color="Ubicación del Trabajo/Servicio")

    fig.update_layout(xaxis_title='Cantidad',
                      yaxis_title='Campus',
                      title={
                          "text":"Cantidad de solicitudes por campus",
                          "x":0.5,
                          "xanchor": "center"},
                      title_font_color= "#D8E2DC",height=300)
    
    st.plotly_chart(fig,use_container_width=True)    

def graf_ccosto_dashboard(df):
    df_graf = df["Nombre CCosto"].value_counts()

    graf = pd.DataFrame({
         "Centro de Costo": df_graf.index,
         "Cantidad" : df_graf.values})
    
    return plost.bar_chart(
        data=graf,
        bar="Centro de Costo",
        value="Cantidad",
        direction="horizontal",
        color="Centro de Costo")

def graf_ubic_dashboard(df):
    df_graf = df["Ubicación del Trabajo/Servicio"].value_counts()

    graf = pd.DataFrame({
        "Ubicacion":df_graf.index,
        "Cantidad":df_graf.values
    })

    return plost.donut_chart(
        data=graf,
        theta="Cantidad",
        color="Ubicacion")

def graf_tipo_dashboard(df):
    df_graf = df["Tipo de Trabajo"].value_counts()

    graf = pd.DataFrame({
        "Tipo":df_graf.index,
        "Cantidad":df_graf.values
    })

    return plost.pie_chart(
        data=graf,
        theta="Cantidad",
        color="Tipo")

def graf_dias_dashboard(df):
    df_graf = df.Día.value_counts()

    graf = pd.DataFrame({
        "Día":df_graf.index,
        "Cantidad":df_graf.values
    })

    return plost.line_chart(
        data=graf.sort_values(by="Día"),
        x="Día",
        y="Cantidad")

def filtros_dashboard(df):
    st.sidebar.title("Filtros")

    servicio = st.sidebar.selectbox("Servicio",df["Tipo de Servicio"].unique().tolist())
    año = st.sidebar.selectbox("Año", df["Año"].unique().tolist())
    mes = st.sidebar.selectbox("Mes", df["Mes"].unique().tolist())
    # lista_dias = df.Día.unique().tolist()
    # lista_dias.sort()
    # dia = st.sidebar.selectbox("Día",lista_dias)
    # ccosto = st.sidebar.selectbox("Centro de costo",df["Nombre CCosto"].unique().tolist())
    df_filt = df[(df["Tipo de Servicio"]==servicio)&(df.Año==año)&(df.Mes==mes)]
    return df_filt

def dashboard_anual(df):
    df_filtrado(df)

    # df_filt1 = filtros_dashboard(df)

    size_title = 'font-size: 22px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Indicadores Dirección de Servicios y Logística - Año 2023"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)

    # st.subheader(f"El servicio de {df_filt1['Tipo de Servicio'].unique().tolist()[0]} en el mes de {df_filt1.Mes.unique().tolist()[0]} del año {df_filt1.Año.unique().tolist()[0]} presenta los siguientes indicadores")
    
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        porc_pend_dashboard_anual(df)

    with c2:
        porc_ejec_dashboard_anual(df)

    with c3:
        cant_pend_dashboard_anual(df)

    with c4:
        cant_ejec_dashboard_anual(df)

    c1,c2 = st.columns(2)
    with c1:
        graf_ccosto_acumulado_mensual_dashboard_anual(df)

    with c2:
        graf_acumulado_servicios_mensual_dashboard(df)

    c1,c2 = st.columns(2)  
    with c1:
        graf_campus_acum_dashboard(df)
    with c2:
        graf_ccosto_dashboard_anual(df)

# def detener_dashboard():
#     global mostrar_dashboard
#     mostrar_dashboard = False

def df_filtrado (df):
    df.drop(columns=["Adj.","Resumen","Detalle","Anexo","Funcionario de Contacto_cod",
                 "Funcionario de Contacto_dsc","Fecha de Recepción","Funcionario Encargado_cod",
                "Funcionario Encargado_dsc","Fecha de Asignación","Funcionario de Contacto_cod",
                "Solicitud de Compra","Observación","Nº de Horas Hombre","Cantidad de Personas Involucradas",
                "Material Utilizado","Rut Responsable_cod","Rut Responsable_dsc","Funcionario Ejecutor_cod","Funcionario Ejecutor_dsc",
                "Ubicación Específica","Ubicación","Fecha y Hora Sistema"], inplace=True)
    df.fillna(0,inplace=True)
    df["Ejecutada"] = df["Fecha de Término"].apply(lambda x: "No" if x == 0 else "Si")
    dicc_meses = {
        1:"Enero",
        2:"Febrero",
        3:"Marzo",
        4:"Abril",
        5:"Mayo",
        6:"Junio",
        7:"Julio",
        8:"Agosto",
        9:"Septiembre",
        10:"Octubre",
        11:"Noviembre",
        12:"Diciembre"}

    df["Año"] = df["Fecha"].dt.year
    df["Mes"] = df["Fecha"].dt.month
    # df["Día"] = df["Fecha"].dt.day
    df.Mes = df.Mes.map(dicc_meses,na_action="ignore")
    
    cambiar_nombres = {"Centro de Costo_cod":"Código CCosto","Centro de Costo_dsc":"Nombre CCosto"}
    
    df.rename(columns=cambiar_nombres, inplace=True)
    
    return df

def filtro_df (df):
    st.sidebar.header("Filtrar por")

    lista_servicios = st.sidebar.selectbox("Servicio",df["Tipo de Servicio"].unique().tolist())
    año = st.sidebar.selectbox("Año", df["Año"].unique().tolist())
    mes = st.sidebar.selectbox("Mes", df["Mes"].unique().tolist())
    return df[(df["Tipo de Servicio"] == lista_servicios)&(df["Año"] == año)&(df["Mes"]==mes)]


def analisis_exp(df):
    st.write("Analisis Explotario General")
    st.write("Cabecera de los datos")
    st.write(df.head(10))
    st.write("Descripcion")
    st.write(df.describe())
    st.write("Datos faltantes")
    df_nulos(df)

def analisis_exp_pers (df):

    df.drop(columns=["Adj."],inplace=True)
    df.fillna(0,inplace=True)

    dicc_meses = {
        1:"Enero",
        2:"Febrero",
        3:"Marzo",
        4:"Abril",
        5:"Mayo",
        6:"Junio",
        7:"Julio",
        8:"Agosto",
        9:"Septiembre",
        10:"Octubre",
        11:"Noviembre",
        12:"Diciembre"}

    df["Año"] = df["Fecha"].dt.year
    df["Mes"] = df["Fecha"].dt.month
    df["Día"] = df["Fecha"].dt.day
    df.Mes = df.Mes.map(dicc_meses,na_action="ignore")

    st.write("Para filtrar datos utilize las opciones del panel lateral")
    st.dataframe(filtro_df(df))

def crear_grafico (tipo,df,x,y):

    st.write("# Visualizacion de datos")

    if tipo == "Barras":
        st.header("Grafico de barras")
        fig = px.bar(df, x=x, y=y, color="Tipo de Servicio")
        st.plotly_chart(fig)

    if tipo == "Lineas":
        st.header("Grafico de lineas")
        fig = px.line(df, x=x, y=y)
        st.plotly_chart(fig)

    if tipo == "Dispersion":
        st.header("Grafico de dispersion")
        fig = px.scatter(df, x=x, y=y, color="Tipo de Servicio")
        st.plotly_chart(fig)

    if tipo == "Histograma":
        st.header("Histograma")

        fig = px.histogram(df, x=x, y=y, color="Tipo de Servicio")
        st.plotly_chart(fig)

def principal():
    size_title = 'font-size: 24px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Aplicacion para analisis exploratorio y visual de la DSL"
    st.sidebar.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    # st.sidebar.write("# Aplicacion para analisis exploratorio y visual de la DSL")
    st.sidebar.write("Seleccione una base de datos")
    archivo_excel = st.sidebar.file_uploader("Elija archivo Excel",type=["xlsx"])
    bd_default = "solicitudes.xlsx"
    df = cargar_datos(bd_default)
    if archivo_excel is None:
        dashboard_anual(df)
    # opciones = st.sidebar.radio("Tipo de analisis", options=["Dashboard Anual","Dashboard Personalizado","Analisis Exploratorio"])# General","Analisis Exploratorio Personalizado","Analisis Visual"])
    if archivo_excel is not None:
        opciones = st.sidebar.radio("Tipo de analisis", options=["Dashboard Anual","Dashboard Personalizado","Analisis Exploratorio"])
        bd_default = "solicitudes.xlsx"
        df = cargar_datos(bd_default)
        df_dsl = cargar_datos(archivo_excel)
        
        if opciones == "Dashboard Personalizado":
            st.write("Dashboard Personalizado")
            # df_filt1 = filtros_dashboard(df)

        elif opciones == "Dashboard Anual":
            dashboard_anual(df)

        elif opciones == "Analisis Exploratorio":
            analisis_exp(df_dsl)
        
        # if not opciones:
        #     dashboard_inicial.empty()

        # elif opciones == "Analisis Exploratorio Personalizado":
        #     analisis_exp_pers(df_dsl)

        # elif opciones == "Analisis Visual":
        #     st.sidebar.title("Opciones de graficos")

        #     tipo_grafico = st.sidebar.selectbox("Seleccione el tipo de grafico", ["Barras","Lineas","Dispersion","Histograma","Pastel"])

        #     x = st.sidebar.selectbox("Seleccione columna (Eje X)", df_dsl.columns)
        #     y = st.sidebar.selectbox("Seleccione columna (Eje Y)", df_dsl.columns)

        #     crear_grafico(tipo_grafico,df_dsl,x,y)
            
principal()