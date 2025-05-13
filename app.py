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

# Crear la app
app = Dash(__name__)
app.title = "Gantt de Aplicaciones"

# Crear gráfico Gantt interactivo
fig = px.timeline(
    df,
    x_start="Inicio",
    x_end="Fin",
    y="Producto",
    color="Cuartel",
    title="Carta Gantt de Aplicaciones",
    hover_data=[
        "Cuartel",
        "Inicio",
        "Fin",
        "Estado Fenológico",
        "Suma de Total concentración",
        "Suma de Total superficie"
    ]
)

# Invertir eje Y
fig.update_yaxes(autorange="reversed")

# Layout
app.layout = html.Div([
    html.H2("Gantt Interactivo de Aplicaciones", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

# Ejecutar en Render
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
