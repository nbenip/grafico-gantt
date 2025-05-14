import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Cargar los datos exportados desde Power BI
df = pd.read_csv("aplicaciones.csv")

# Renombrar columnas si lo deseas
df = df.rename(columns={
    'Producto Aplicado': 'Producto',
    'Fecha Inicio': 'Inicio',
    'Fecha Fin': 'Fin',
    'Source.Name': 'Cuartel'
})

# Convertir fechas
df['Inicio'] = pd.to_datetime(df['Inicio'])
df['Fin'] = pd.to_datetime(df['Fin'])

# Asegurarse de que los valores sean numéricos
df["Suma de Total concentración"] = pd.to_numeric(df["Suma de Total concentración"], errors="coerce")
df["Suma de Total superficie"] = pd.to_numeric(df["Suma de Total superficie"], errors="coerce")

# Crear la app
app = Dash(__name__)
app.title = "Gantt de Aplicaciones"

# Agregar columna con etiqueta única por fila para separar visualmente
df['ProductoVisual'] = df['Producto'] + " (" + df['Cuartel'].astype(str) + ")"

# Crear gráfico Gantt con separación visual
fig = px.timeline(
    df,
    x_start="Inicio",
    x_end="Fin",
    y="ProductoVisual",  # Esta columna asegura separación entre filas
    color="Cuartel",
    title="Carta Gantt de Aplicaciones"
)

# Formato del hover (tooltip) con decimales
fig.update_traces(
    hovertemplate=
        "Cuartel: %{customdata[0]}<br>" +
        "Inicio: %{customdata[1]|%Y-%m-%d}<br>" +
        "Fin: %{customdata[2]|%Y-%m-%d}<br>" +
        "Estado Fenológico: %{customdata[3]}<br>" +
        "Concentración: %{customdata[4]:.3f}<br>" +
        "Superficie: %{customdata[5]:.3f}<extra></extra>",
    customdata=df[[  # Asegura que estos campos estén en el orden correcto
        "Cuartel",
        "Inicio",
        "Fin",
        "Estado Fenológico",
        "Suma de Total concentración",
        "Suma de Total superficie"
    ]]
)

# Invertir eje Y para que se vea como Gantt clásico
fig.update_yaxes(autorange="reversed")

# Layout
app.layout = html.Div([
    html.H2("Gantt Interactivo de Aplicaciones", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

# Ejecutar en Render
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
