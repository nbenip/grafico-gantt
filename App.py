import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Cargar los datos exportados desde Power BI
df = pd.read_csv("aplicaciones.csv")

# Renombrar columnas si es necesario
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
    hover_data=["Cuartel", "Inicio", "Fin"]
)

# Invertir eje Y para que se vea como un Gantt clásico
fig.update_yaxes(autorange="reversed")

# Layout de la app
app.layout = html.Div([
    html.H2("Gantt Interactivo de Aplicaciones", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

# Ejecutar servidor local
if __name__ == "__main__":
    app.run(debug=True)

