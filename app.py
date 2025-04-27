import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Título
st.title("Simulación de dispersión de ruido submarino")

# Parámetros de entrada para las frecuencias, distancias y fuentes
frecuencia = st.slider("Frecuencia (Hz)", min_value=30, max_value=20000, step=10, value=500)
distancia_max_km = st.slider("Distancia máxima (km)", min_value=1, max_value=40, step=1, value=10)
fuente_db = st.slider("Nivel de fuente sonora (dB)", min_value=100, max_value=240, step=1, value=180)
factor_k = st.slider("Factor geométrico (k)", min_value=10, max_value=20, step=1, value=20)

# Selección de umbral de afectación por categoría (seres humanos, lobos marinos, cetáceos, peces)
umbral_categoria = st.selectbox("Selecciona la categoría de umbral de afectación", 
                                ["Seres Humanos", "Lobos Marinos", "Cetáceos", "Peces"])
umbral_dict = {
    "Seres Humanos": 120,
    "Lobos Marinos": 130,
    "Cetáceos": 140,
    "Peces": 100
}
umbral_usuario = umbral_dict[umbral_categoria]

# Parámetros adicionales
fuente_emision = st.selectbox("Selecciona la fuente de emisión de ruido", 
                              ["Chancado de Pilotes", "Motor de Embarcación", "Aparatos Acústicos Submarinos"])
fuente_db_dict = {
    "Chancado de Pilotes": 210,
    "Motor de Embarcación": 180,
    "Aparatos Acústicos Submarinos": 200
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
fig.add_trace(go.Scatter(x=distancias_km, y=nivel_presion, mode='lines', name="Nivel de presión sonora", line=dict(color='blue')))

# Añadir la línea del umbral de afectación
fig.add_trace(go.Scatter(x=[distancias_km[0], distancias_km[-1]], y=[umbral_usuario, umbral_usuario],
                         mode='lines', name=f'Umbral de afectación ({umbral_usuario} dB)', line=dict(color='red', dash='dash')))

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
