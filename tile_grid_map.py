import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import streamlit as st


st.set_page_config(page_title="Tile grid Map: Accidentes de Bicicletas", layout="wide")
st.title("Tile grid Map: Accidentes de Bicicletas por Distrito y Tipo de Accidente")

df = pd.read_csv('csv/AccidentesBicicletas_2024.csv', sep=';', encoding='utf-8-sig')

# Agrupar datos por distrito y tipo de accidente
accidents = df.groupby(['distrito', 'tipo_accidente']).size().unstack(fill_value=0)

# Crear coordenadas de la grilla para cada distrito con una separación entre distritos
district_coords = pd.DataFrame({
    'distrito': accidents.index,
    'x': [0, 1.2, 2.4, 0, 1.2, 2.4, 3.6, 4.8, 0, 1.2, 2.4, 3.6, 4.8, 0, 1.2, 2.4, 3.6, 4.8, 0, 1.2, 2.4],
    'y': [0, 0, 0, 1.2, 1.2, 1.2, 1.2, 1.2, 2.4, 2.4, 2.4, 2.4, 2.4, 3.6, 3.6, 3.6, 3.6, 3.6, 4.8, 4.8, 4.8]
})

# Merge coordenadas con los datos de accidentes
accidents = accidents.merge(district_coords, left_index=True, right_on='distrito')

# Obtener los tipos de accidentes
accident_types = list(accidents.columns[:-3])  # Excluir las columnas x, y, distrito

#Colores según el número de tipos de accidentes
colors = cm.get_cmap('tab20', len(accident_types)).colors 

# Sidebar para seleccionar tipos de accidentes a mostrar
st.sidebar.header("Filtros")
selected_types = st.sidebar.multiselect(
    "Selecciona los tipos de accidentes a mostrar:",
    options=accident_types,
    default=accident_types  
)

# Filtrar los tipos de accidentes seleccionados
filtered_accident_types = selected_types
filtered_colors = [colors[accident_types.index(tipo)] for tipo in filtered_accident_types]

fig, ax = plt.subplots(figsize=(14, 12))

# Dibujar gráficos apilados para cada distrito
for _, row in accidents.iterrows():
    x, y = row['x'], row['y']
    bottom = y - 0.5
    total = row[filtered_accident_types].sum()
    if total == 0:
        continue
    for i, tipo in enumerate(filtered_accident_types):
        count = row[tipo]
        height = count / total
        ax.bar(
            x, height=height, width=1, bottom=bottom, align='center',
            color=filtered_colors[i], edgecolor="black", label=tipo if _ == accidents.index[0] else ""
        )
        bottom += height

# Etiquetas de los distritos
for _, row in district_coords.iterrows():
    ax.text(row['x'], row['y'], row['distrito'], fontsize=8, ha='center', va='center', color='black')

# Leyenda
legend_patches = [mpatches.Patch(color=filtered_colors[i], label=tipo) for i, tipo in enumerate(filtered_accident_types)]
ax.legend(handles=legend_patches, title="Tipos de Accidentes", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

ax.invert_yaxis()
ax.set_title('Tile grid Map: Accidentes de Bicicletas por Distrito y Tipo de Accidente', fontsize=16)
ax.axis('off')
plt.tight_layout()
st.pyplot(fig)
