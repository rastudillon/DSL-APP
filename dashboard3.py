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
    ejec = df.Ejecutada[(df.Año=="2023")&(df.Ejecutada=="Si")].value_counts()
    pend = df.Ejecutada[(df.Año=="2023")&(df.Ejecutada=="No")].value_counts()
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
    pend = df.Ejecutada[(df.Ejecutada=="No")&(df.Año=="2023")].count()

    color = 'color: #F5A65B; font-size: 50px; text-align: center'
    div_style = "background: linear-gradient(to right, #0A0908, #22333B);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Cantidad total de pendientes"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{pend}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def cant_ejec_dashboard_anual(df):    
    ejec = df.Ejecutada[(df.Ejecutada=="Si")&(df.Año=="2023")].count()

    color = 'color: #32E875; font-size: 50px; text-align: center'
    div_style = "background: linear-gradient(to right, #22333B, #0A0908);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Cantidad total de ejecutadas"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{ejec}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def graf_ccosto_acumulado_mensual_dashboard_anual(df):
    df = df[df.Año == "2023"]
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

def graf_acumulado_servicios_mensual_dashboard_anual(df):
    df = df[df.Año == "2023"]
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

def graf_campus_acum_dashboard_anual(df):
    df = df[df.Año == "2023"]
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

def graf_ccosto_dashboard_anual(df):
    df = df[df.Año == "2023"]
    conteo_tipo_servicio = df.groupby(["Tipo de Servicio"]).size().reset_index(name="Cantidad")

    fig = px.pie(conteo_tipo_servicio,values="Cantidad",names="Tipo de Servicio",hole=.6)

    fig.update_layout(
        title={
            "text":"Porcentaje de solicitudes por servicio",
            "x":0.432,
            "xanchor": "right"},
        title_font_color= "#D8E2DC",
        font={
            "size":13}, height=350)

    st.plotly_chart(fig,use_container_width=True)
    
def dashboard_anual(df):

    size_title = 'font-size: 22px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Indicadores Dirección de Servicios y Logística - Año 2023"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    
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
        graf_acumulado_servicios_mensual_dashboard_anual(df)

    c1,c2 = st.columns(2)  
    with c1:
        graf_campus_acum_dashboard_anual(df)
    with c2:
        graf_ccosto_dashboard_anual(df)

def filtros_dashboard(df):
    st.sidebar.title("Filtros")

    historico = st.sidebar.checkbox("Resumen histórico")
    servicio = st.sidebar.selectbox("Servicio",df["Tipo de Servicio"].unique().tolist())
    año = st.sidebar.selectbox("Año", df["Año"].unique().tolist())
    if año == 2023:
        if historico:
            return df[(df["Tipo de Servicio"]==servicio)&(df.Año=="2023")], 1
        mes = st.sidebar.selectbox("Mes", df.Mes[df.Año == "2023"].unique().tolist())
        return df[(df["Tipo de Servicio"]==servicio)&(df.Año=="2023")&(df.Mes==mes)], 0
    else:
        if historico:
            return df[(df["Tipo de Servicio"]==servicio)&(df.Año==año)], 1
        mes = st.sidebar.selectbox("Mes", df["Mes"].unique().tolist())
        return df[(df["Tipo de Servicio"]==servicio)&(df.Año==año)&(df.Mes==mes)], 0
    
def porc_no_ejec_dashboard_servicio(df):
    ejec = df.Ejecutada[df.Ejecutada=="Si"].value_counts()
    pend = df.Ejecutada[df.Ejecutada=="No"].value_counts()
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
    
def porc_ejec_dashboard_servicio(df):
    ejec = df.Ejecutada[df.Ejecutada=="Si"].value_counts()
    pend = df.Ejecutada[df.Ejecutada=="No"].value_counts()
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
    
def cant_pend_dashboard(df):
    pend = df.Ejecutada[df.Ejecutada=="No"].count()

    color = 'color: #F5A65B; font-size: 50px; text-align: center'
    div_style = "background: linear-gradient(to right, #0A0908, #22333B);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Cantidad total de pendientes"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{pend}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def cant_ejec_dashboard(df):    
    ejec = df.Ejecutada[df.Ejecutada=="Si"].count()

    color = 'color: #32E875; font-size: 50px; text-align: center'
    div_style = "background: linear-gradient(to right, #22333B, #0A0908);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:#F2F4F3;margin-bottom:10px;"
    titulo = "Cantidad total de ejecutadas"

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>{ejec}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def graf_ccosto_dashboard(df):
    conteo_ccosto = df.groupby(["Fecha","Nombre CCosto"]).size().reset_index(name="Cantidad")

    fig = px.bar(conteo_ccosto, x="Fecha",y="Cantidad",color="Nombre CCosto")

    fig.update_layout(xaxis_title='Fecha',
                      yaxis_title='Cantidad de solicitudes',
                      title={
                          "text":"Cantidad diaria de solicitudes por centro de costos",
                          "x":0.5,
                          "xanchor": "center"},
                      title_font_color= "#D8E2DC",height=330)

    st.plotly_chart(fig,use_container_width=True) 

def graf_ccosto_pie_dashboard(df):
    conteo_ccosto = df.groupby("Nombre CCosto").size().reset_index(name="Cantidad")
    cant_ccosto_filtrado = conteo_ccosto.groupby('Nombre CCosto').filter(lambda x: x['Cantidad'].sum() > 2)

    fig = px.pie(cant_ccosto_filtrado,values="Cantidad",names="Nombre CCosto",hole=.6)

    fig.update_layout(
        title={
            "text":"Total mensual por Centros de costo",
            "x":0.5,
            "xanchor": "center"},
        title_font_color= "#D8E2DC",
        font={
            "size":13}, height=350)

    st.plotly_chart(fig,use_container_width=True)

def graf_dias_dashboard(df):
    conteo_servicio = df.groupby(["Tipo de Servicio","Fecha"]).size().reset_index(name="Cantidad")
    fig = px.line(conteo_servicio, x="Fecha",y="Cantidad",markers=True)

    fig.update_layout(xaxis_title='Fecha',
                      yaxis_title='Cantidad de solicitudes',
                      title={
                          "text":"Cantidad diaria de solicitudes",
                          "x":0.5,
                          "xanchor": "center"},
                      title_font_color= "#D8E2DC", height=255)
    
    st.plotly_chart(fig,use_container_width=True)

def graf_pie_campus_dashboard(df):
    conteo_campus = df.groupby(["Ubicación del Trabajo/Servicio"]).size().reset_index(name="Cantidad")

    fig = px.pie(conteo_campus,values="Cantidad",names="Ubicación del Trabajo/Servicio",hole=.5)

    fig.update_layout(
        title={
            "text":"Porcentaje de solicitudes por campus",
            "x":0.5,
            "xanchor": "center"},
        title_font_color= "#D8E2DC",
        font={
            "size":13}, height=320)

    st.plotly_chart(fig,use_container_width=True)    

def dashboard_personalizado(df):
    filtro, titulo = filtros_dashboard(df)

    size_title = 'font-size: 22px; text-align: center; color: #D8E2DC; font-weight: lighter'
    if titulo == 1:
            title = f"El servicio de {filtro['Tipo de Servicio'].unique().tolist()[0]} históricamente en el año {filtro.Año.unique().tolist()[0]} presenta los siguientes indicadores"
            st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    else:
        title = f"El servicio de {filtro['Tipo de Servicio'].unique().tolist()[0]} en el mes de {filtro.Mes.unique().tolist()[0]} del año {filtro.Año.unique().tolist()[0]} presenta los siguientes indicadores"
        st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        porc_no_ejec_dashboard_servicio(filtro)

    with c2:
        porc_ejec_dashboard_servicio(filtro)

    with c3:
        cant_pend_dashboard(filtro)

    with c4:
        cant_ejec_dashboard(filtro)

    c1,c2 = st.columns(2)
    with c1:
        graf_ccosto_dashboard(filtro)

    with c2:
        graf_ccosto_pie_dashboard(filtro)

    c1,c2 = st.columns(2)  
    with c1:
        graf_dias_dashboard(filtro)
    with c2:
        pass
        graf_pie_campus_dashboard(filtro)

def pie_valores_nulos(df):
    fig = px.pie(df.isnull().sum(),values=df.isnull().sum().values,names=df.isnull().sum().index.tolist(),hole=0.3)     
    st.plotly_chart(fig,use_container_width=True)

def bar_cantidad_nulos(df):
    fig = px.bar(df.isnull().sum(),x=df.isnull().sum().values,y=df.isnull().sum().index.tolist())      
    st.plotly_chart(fig,use_container_width=True)

def distribucion_col_num(df):
    df = df.drop("Adj.", axis=1)
    df = df.drop("Rut Responsable_dsc",axis=1)
    size_title = 'font-size: 30px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Distribución de columnas numéricas"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    for col in df.select_dtypes(include=np.number):
        fig = px.histogram(df, x=col)
        fig.update_layout(title={
                                "text":f"Distribución de {col}",
                                "x":0.5,
                                "xanchor": "center"},
                      title_font_color= "#D8E2DC")       
        st.plotly_chart(fig,use_container_width=True)

def distribucion_col_categoricas(df):
    df = df.drop(["Resumen","Detalle","Ubicación","Anexo","Funcionario de Contacto_cod","Funcionario de Contacto_cod",
                  "Funcionario de Contacto_dsc","Fecha de Recepción","Funcionario Encargado_cod","Funcionario Encargado_dsc",
                  "Funcionario Ejecutor_cod","Fecha de Término","Observación","Material Utilizado","Rut Responsable_cod","Rut Responsable_dsc"],axis=1)
   
    size_title = 'font-size: 30px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Frecuencia de columnas categóricas"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    for col in df.select_dtypes(include=object):
        fig = px.histogram(df, x=col)
        fig.update_layout(title={
                                "text":f"Frecuencia de {col}",
                                "x":0.5,
                                "xanchor": "center"},
                      title_font_color= "#D8E2DC") 
        st.plotly_chart(fig,use_container_width=True) 

def analisis_exp(df):
    size_title = 'font-size: 40px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Análisis explotario de la base de datos ingresada"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True) 
    size_title = 'font-size: 30px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Cabecera de la base de datos"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True) 
    st.write(df.head(5))
    size_title = 'font-size: 30px; text-align: center; color: #D8E2DC; font-weight: lighter'
    title = "Descripción estadística de la base de datos"
    st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True) 
    st.write(df.describe())

    c1,c2 = st.columns(2)
    with c1:
        size_title = 'font-size: 30px; text-align: center; color: #D8E2DC; font-weight: lighter'
        title = "Porcentaje de valores nulos por columna"
        st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True) 
        pie_valores_nulos(df)
    with c2:
        size_title = 'font-size: 30px; text-align: center; color: #D8E2DC; font-weight: lighter'
        title = "Cantidad de valores nulos por columna"
        st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)        
        bar_cantidad_nulos(df)
    c1,c2 = st.columns(2)
    with c1:
        distribucion_col_num(df)
        size_title = 'font-size: 30px; text-align: center; color: #D8E2DC; font-weight: lighter'
        title = "Tipos de datos por columna"
        st.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)       
        st.dataframe(df.dtypes)
    with c2:
        distribucion_col_categoricas(df)

def grafico_barras(df):

    df.drop(columns=["Adj.","Fecha de Recepción","Funcionario Encargado_cod","Funcionario Encargado_dsc","Fecha de Asignación","Funcionario Ejecutor_cod","Funcionario Ejecutor_dsc","Solicitud de Compra","Observación","Cantidad de Personas Involucradas","Nº de Horas Hombre","Material Utilizado","Rut Responsable_dsc"],inplace=True)
    

    st.title('Generador de Gráficos de Barras')
    valores_columnas = ['Centro de Costo_dsc', 'Nº de Solicitud']
   

    x_col = st.selectbox('Selecciona la columna para el eje X', options=df.columns)
    val_col = st.selectbox('Selecciona la columna para el eje X', options=valores_columnas)

 
    if st.button('Generar Gráfico de Barras'):
       
        # Contar los valores de la columna seleccionada y obtener los 10 más importantes
        counts = df[x_col].value_counts().nlargest(10).reset_index()
        counts.columns = [x_col, val_col]

        # Generar el gráfico de líneas
        st.markdown(f"## Gráfico de barras de {x_col}")
        fig = px.bar(counts, x=x_col, y=val_col,  labels={'index': x_col}, title=f'Gráfico de barras de {x_col}')
        
        st.plotly_chart(fig)

def grafico_lineas(df):

    df.drop(columns=["Adj.","Fecha de Recepción","Funcionario Encargado_cod","Funcionario Encargado_dsc","Fecha de Asignación","Funcionario Ejecutor_cod","Funcionario Ejecutor_dsc","Solicitud de Compra","Observación","Cantidad de Personas Involucradas","Nº de Horas Hombre","Material Utilizado","Rut Responsable_dsc"],inplace=True)
    

    st.title('Generador de Gráficos de Líneas')

    valores_columnas = ['Centro de Costo_dsc', 'Nº de Solicitud']
   

    x_col = st.selectbox('Selecciona la columna para el eje X', options=df.columns)
    val_col = st.selectbox('Selecciona la columna para el eje X', options=valores_columnas)

    # Contar los valores de la columna seleccionada y obtener los 10 más importantes
    counts = df[x_col].value_counts().nlargest(10).reset_index()
    counts.columns = [x_col, val_col]

    # Generar el gráfico de líneas
    fig = px.line(counts, x=x_col, y=val_col, title='Gráfico de Líneas')
    st.plotly_chart(fig)

def grafico_boxplot(df):
    df.drop(columns=["Adj.","Fecha de Recepción","Funcionario Encargado_cod","Funcionario Encargado_dsc","Fecha de Asignación","Funcionario Ejecutor_cod","Funcionario Ejecutor_dsc","Solicitud de Compra","Observación","Material Utilizado","Rut Responsable_dsc"],inplace=True)
    

    st.title('Generador de Gráficos de Líneas')
    valores_columnas = ['Centro de Costo_dsc', 'Nº de Solicitud']
    groupby_columna=['Ubicación del Trabajo/Servicio','Tipo de Trabajo','Nº de Horas Hombre','Cantidad de Personas Involucradas']
    
    # Solicitar al usuario el valor de la columna y la columna para agrupar
    valor_columna = st.selectbox("Selecciona la columna de valor", valores_columnas)
    groupby_x = st.selectbox("Selecciona la columna para agrupar", groupby_columna)
    # Generar el gráfico de cajas utilizando plotly.express
    fig = px.box(df, y=valor_columna, x=groupby_x)

    # Mostrar el gráfico utilizando Streamlit
    st.plotly_chart(fig)

def grafico_histograma(df):
    st.title('Generador de Gráficos de Histograma')

    columnas = ['Nº de Solicitud', 'Fecha', 'Tipo de Servicio', 'Nº de Horas Hombre', 
                'Cantidad de Personas Involucradas', 'Material Utilizado', 'Ubicación del Trabajo/Servicio']

    # Seleccionar una columna para el gráfico de histograma
    columna_graficar = st.selectbox('Elige una columna para generar el histograma', options=columnas)

    # Filtrar valores nulos en la columna seleccionada
    df_filtrado = df[df[columna_graficar].notnull()]

    # Generar el gráfico de histograma
    fig = px.histogram(df_filtrado, x=columna_graficar, title=f'Histograma de {columna_graficar}')

    # Mostrar el gráfico
    st.plotly_chart(fig)

def grafico_pastel(df):
    st.title('Generador de Gráfico de Pastel')

    # Definir las columnas adecuadas para el gráfico de pastel
    columnas = ['Tipo de Servicio', 'Centro de Costo_dsc', 'Funcionario Encargado_dsc', 'Ubicación del Trabajo/Servicio']

    # Seleccionar una columna para el gráfico de pastel
    columna_graficar = st.selectbox('Elige una columna para el gráfico de pastel', options=columnas)

    if columna_graficar:
        valores = df[columna_graficar].value_counts().head(10)
        fig = px.pie(valores, values=valores, names=valores.index, title=f'Distribución de los 10 más importantes en {columna_graficar}')
        st.plotly_chart(fig)
    else:
        st.warning('No hay columnas disponibles para generar el gráfico de pastel.')

def crear_grafico (tipo,df):

    if (len(tipo)>=0):
        
        if tipo == "Barras":
            grafico_barras(df)

        elif tipo == "Lineas":
           grafico_lineas(df)

        elif tipo == "BoxPlot":
           grafico_boxplot(df)

        elif tipo == "Histograma":
           grafico_histograma(df)
        
        elif tipo =="Pastel":
            grafico_pastel(df)

    else:
        st.write("Algo Salio mal vuelve a intentarlo")

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
    else:
        opciones = st.sidebar.radio("Tipo de análisis", options=["Dashboard Anual","Dashboard Personalizado","Análisis Exploratorio","Generador de Gráficos"])    
        bd = cargar_datos(archivo_excel)
        df = df_mod(bd)

        if opciones == "Dashboard Personalizado":
            dashboard_personalizado(df)
        elif opciones == "Dashboard Anual":
            dashboard_anual(df)
        elif opciones == "Análisis Exploratorio":
            analisis_exp(bd)
        elif opciones == "Generador de Gráficos":
            tipo_grafico = st.sidebar.selectbox("Seleccione el tipo de grafico", ["Barras","Lineas","BoxPlot","Histograma","Pastel"])
            crear_grafico(tipo_grafico,bd)

principal()
