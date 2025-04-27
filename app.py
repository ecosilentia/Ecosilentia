import matplotlib.pyplot as plt
import random

# --- Configuración de simulación ---
dias = list(range(0, 61))         # 60 días
NH4_inicial = 12.0                # Concentración inicial (mg/L)
ingreso_diario = 1.8              # Ingreso normal diario (mg/L)
ingreso_extremo = 6.0             # Ingreso por evento extremo (mg/L)
evento_extremo_dia = 20           # Día de evento (lluvia con escorrentía)

# --- Eficiencias promedio ---
tasa_nitrificacion_media = 0.7
tasa_fitorremediacion_media = 0.6
tasa_reduccion_natural = 0.15

# --- Inicialización de listas ---
NH4_con_sistema = [NH4_inicial]
NH4_sin_sistema = [NH4_inicial]

# --- Estados ---
NH4_sys = NH4_inicial
NO3_sys = 0.0
NH4_nosys = NH4_inicial

# --- Simulación día por día ---
for dia in dias[1:]:
    # Determinar ingreso diario según evento
    if dia == evento_extremo_dia:
        ingreso = ingreso_extremo
    else:
        ingreso = ingreso_diario

    # Variabilidad de eficiencia (±5%)
    tasa_nitri = tasa_nitrificacion_media * random.uniform(0.95, 1.05)
    tasa_fito = tasa_fitorremediacion_media * random.uniform(0.95, 1.05)

    # --- CON SISTEMA ---
    NH4_sys += ingreso
    convertido_NO3 = NH4_sys * tasa_nitri
    NH4_sys -= convertido_NO3
    NO3_sys += convertido_NO3

    absorbido = NO3_sys * tasa_fito
    NO3_sys -= absorbido

    NH4_con_sistema.append(NH4_sys)

    # --- SIN SISTEMA ---
    NH4_nosys += ingreso
    NH4_nosys -= NH4_nosys * tasa_reduccion_natural
    NH4_sin_sistema.append(NH4_nosys)

# --- Visualización ---
plt.figure(figsize=(12, 6))
plt.plot(dias, NH4_con_sistema, label='Con sistema de biorremediación', color='blue', linewidth=2)
plt.plot(dias, NH4_sin_sistema, label='Sin sistema (acumulación)', color='red', linestyle='--', linewidth=2)
plt.axvline(evento_extremo_dia, color='gray', linestyle=':', linewidth=2, label='Evento extremo (lluvia)')

plt.title("Evolución de la Concentración de Amonio (NH₄⁺) con y sin Sistema", fontsize=14)
plt.xlabel("Días", fontsize=12)
plt.ylabel("Concentración de NH₄⁺ (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
