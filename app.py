# %% Importar librerías
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# %% Título
st.title("Simulación de dispersión de ruido submarino")

# %% Parámetros de entrada
frecuencia = st.slider("Frecuencia (Hz)", min_value=30, max_value=20000, step=10, value=500)
distancia_max_km = st.slider("Distancia máxima (km)", min_value=1, max_value=20, step=1, value=10)
fuente_db = st.slider("Nivel de fuente sonora (dB)", min_value=100, max_value=240, step=1, value=180)
factor_k = st.slider("Factor geométrico (k)", min_value=10, max_value=20, step=1, value=20)
umbral_usuario = st.number_input("Umbral de afectación (dB)", min_value=0.0, max_value=200.0, value=120.0, step=1.0)

# %% Cálculo
distancias_km = np.linspace(0.1, distancia_max_km, 500)
atenuacion = factor_k * np.log10(distancias_km)  # atenuación geométrica
absorcion = 0.001 * frecuencia * distancias_km   # atenuación por absorción simplificada
nivel_presion = fuente_db - atenuacion - absorcion

# %% Crear la figura de Plotly
fig = go.Figure()

# Añadir la línea del nivel de presión sonora
fig.add_trace(go.Scatter(x=distancias_km, y=nivel_presion, mode='lines', name="Nivel de presión sonora", line=dict(color='blue')))

# Añadir la línea del umbral de afectación
fig.add_trace(go.Scatter(x=[distancias_km[0], distancias_km[-1]], y=[umbral_usuario, umbral_usuario],
                         mode='lines', name=f'Umbral de afectación ({umbral_usuario} dB)', line=dict(color='red', dash='dash')))

# Configurar el layout del gráfico
fig.update_layout(
    title=f"Simulación a {frecuencia} Hz",
    xaxis_title="Distancia (km)",
    yaxis_title="Nivel de presión sonora (dB)",
    showlegend=True,
    template="plotly_dark"  # Estilo visual oscuro para mejor contraste
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
