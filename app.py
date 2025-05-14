import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Cargar datos
df = pd.read_csv("aplicaciones.csv")

# Renombrar columnas
df = df.rename(columns={
    'Producto Aplicado': 'Producto',
    'Fecha Inicio': 'Inicio',
    'Fecha Fin': 'Fin',
    'Source.Name': 'Cuartel'
})

# Convertir fechas
df['Inicio'] = pd.to_datetime(df['Inicio'])
df['Fin'] = pd.to_datetime(df['Fin'])


# App
app = Dash(__name__)
app.title = "Gantt de Aplicaciones"

# Gráfico Gantt
fig = px.timeline(
    df,
    x_start="Inicio",
    x_end="Fin",
    y="Producto",
    color="Cuartel",
    title="Carta Gantt de Aplicaciones",
    hover_data=[
        "Cuartel", "Inicio", "Fin",
        "Estado Fenológico", "Suma de Total concentración", "Suma de Total superficie"
    ]
)
fig.update_yaxes(autorange="reversed")

# Layout
app.layout = html.Div([
    html.H2("Gantt Interactivo de Aplicaciones", style={"textAlign": "center"}),
    dcc.Graph(id="gantt-graph", figure=fig, clear_on_unhover=True),
    html.Div(id="hover-date", style={"textAlign": "center", "marginTop": "20px", "fontSize": "18px", "color": "gray"})
])

# Callback para mostrar la fecha del cursor
@app.callback(
    Output("hover-date", "children"),
    Input("gantt-graph", "hoverData")
)
def mostrar_fecha_hover(hoverData):
    if hoverData and "points" in hoverData:
        point = hoverData["points"][0]
        x_val = point.get("x")
        if x_val:
            fecha = pd.to_datetime(x_val).strftime("%d-%m-%Y")
            return f"Fecha fin labor: {fecha}"
    return "Pasa el cursor sobre el gráfico para ver la fecha"

# Render
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
