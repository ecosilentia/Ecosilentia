import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Título
st.title("Simulación de dispersión de ruido submarino")

# Parámetros de entrada para las frecuencias, distancias y fuentes
frecuencia = st.slider("Frecuencia (Hz)", min_value=20, max_value=20000, step=10, value=5000)
distancia_max_km = st.slider("Distancia máxima (km)", min_value=1, max_value=100, step=10, value=10)
factor_k = st.slider("Factor geométrico (k)", min_value=10, max_value=20, step=1, value=15)

# Selección de umbral de afectación por categoría (seres humanos, lobos marinos, cetáceos, peces)
umbral_categoria = st.selectbox("Selecciona la categoría de umbral de afectación", 
                                ["Seres Humanos", "Lobos Marinos", "Cetáceos", "Peces"])
umbral_dict = {
    "Seres Humanos": 120,
    "Lobos Marinos": 130,
    "Cetáceos": 140,
    "Peces": 150
}
umbral_usuario = umbral_dict[umbral_categoria]

# Selección de la fuente de emisión de ruido
fuente_emision = st.selectbox("Selecciona la fuente de emisión de ruido", 
                              ["Motor de Embarcaciones", "Hincado de Pilotes", "Explosivos", "Ruido de Fondo"])

# Asignación de nivel de presión sonora en función de la fuente seleccionada
fuente_db_dict = {
    "Motor de Embarcaciones": 160,
    "Hincado de Pilotes": 210,
    "Explosivos": 250,
    "Ruido de Fondo": 85  # Para ruido de fondo se asigna 85 dB
}
fuente_db = fuente_db_dict[fuente_emision]

# Cálculo de atenuación
distancias_km = np.linspace(0.1, distancia_max_km, 500)
atenuacion = factor_k * np.log10(distancias_km)  # atenuación geométrica
absorcion = 0.001 * frecuencia * distancias_km   # atenuación por absorción simplificada
nivel_presion = fuente_db - atenuacion - absorcion  # Ajustar el nivel de presión sonora

# Crear la figura de Plotly
fig = go.Figure()

# Añadir la línea del nivel de presión sonora
fig.add_trace(go.Scatter(x=distancias_km, y=nivel_presion, mode='lines', name="sonido", line=dict(color='lightblue')))

# Añadir la línea del umbral de afectación
fig.add_trace(go.Scatter(x=[distancias_km[0], distancias_km[-1]], y=[umbral_usuario, umbral_usuario],
                         mode='lines', name="umbral", line=dict(color='red', dash='dash')))

# Configurar el layout del gráfico
fig.update_layout(
    title=f"Simulación a {frecuencia} Hz con fuente de {fuente_emision}",
    xaxis_title="Distancia (km)",
    yaxis_title="Nivel de presión sonora (dB)",
    showlegend=True,
    template="plotly_dark",  # Estilo visual oscuro
    yaxis=dict(range=[50, fuente_db + 10]),  # Establecer el rango del eje Y desde 50 dB
    margin=dict(l=40, r=40, t=40, b=40),  # Márgenes ajustados para mejor presentación
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
