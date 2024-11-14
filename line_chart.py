import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Line chart: Agrupados por rango de edad")
data = pd.read_csv("csv/AccidentesBicicletas_2024.csv", sep=";")
data['fecha'] = pd.to_datetime(data['fecha'], format='%d/%m/%Y')

# Agrupar datos por rango de edad y fecha
grouped_data = data.groupby(['rango_edad', data['fecha']]).size().reset_index(name='accidents')

# Crear el gráfico con plotly
fig = px.line(
    grouped_data,
    x='fecha',
    y='accidents',
    color='rango_edad',
    title="Accidentes por rango de edad en el tiempo",
    labels={'fecha': 'Fecha', 'accidents': 'Número de Accidentes', 'rango_edad': 'Rango de Edad'},
    template='plotly_white'
)

# Personalizar interactividad
fig.update_layout(
    legend_title_text='Rangos de Edad',
    hovermode='x unified'
)

st.plotly_chart(fig)
