import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage
import plotly.figure_factory as ff

data = pd.read_csv("csv/Crime_Incidents_in_2024")
# Agrupar los datos  
crime_grouped = data.groupby(['METHOD', 'OFFENSE']).size().reset_index(name='COUNT')

# Convertir categorías a valores numéricos 
crime_encoded = pd.get_dummies(crime_grouped[['METHOD', 'OFFENSE']])

# Realizar el enlace jerárquico
Z = linkage(crime_encoded.values, method='ward')

labels = crime_grouped['METHOD'] + " | " + crime_grouped['OFFENSE']

# Generar el dendrograma 
fig = ff.create_dendrogram(
    crime_encoded.values,
    orientation='left',
    labels=labels.tolist(),
    linkagefun=lambda x: linkage(x, 'ward')
)

for i in range(len(fig['data'])):
    fig['data'][i]['hovertemplate'] = labels[i % len(labels)]
    fig['data'][i]['name'] = labels[i % len(labels)]

st.plotly_chart(fig, use_container_width=True)
