import streamlit as st
import pandas as pd
from datetime import date
import os
import json
import requests
from streamlit_lottie import st_lottie # Requiere: pip install streamlit-lottie

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- FUNCIONES DE SOPORTE ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# Animación de trofeo para la meta
lottie_celebration = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_TOE99i.json")

# --- PERSISTENCIA Y CONFIGURACIÓN ---
DB_FILE = "wallet_database.csv"
CONFIG_FILE = "settings.json"

if "theme" not in st.session_state:
    st.session_state.theme = "Oscuro"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f: return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- CARGA DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
goal_reached = balance >= META_AHORRO

# --- ESTILOS CSS (CON ANIMACIONES NEÓN) ---
if st.session_state.theme == "Claro":
    bg_app, bg_glass, text_main, accent = "#F0F2F6", "rgba(255, 255, 255, 0.6)", "#1A1C1E", "#2D0066"
else:
    bg_app, bg_glass, text_main, accent = "#1A0040", "rgba(255, 255, 255, 0.07)", "#FFFFFF", "#D4FF00"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_app} !important; color: {text_main}; }}
    
    /* Animación de Pulso Neón */
    @keyframes neon-glow {{
        0% {{ box-shadow: 0 0 5px {accent}, 0 0 10px {accent}; border-color: {accent}; }}
        50% {{ box-shadow: 0 0 20px {accent}, 0 0 35px {accent}; border-color: #FFFFFF; }}
        100% {{ box-shadow: 0 0 5px {accent}, 0 0 10px {accent}; border-color: {accent}; }}
    }}

    .card-resumen, .history-card {{
        background: {bg_glass} !important; 
        backdrop-filter: blur(15px) saturate(150%);
        border-radius: 25px; padding: 25px;
        border: 1px solid rgba(255,255,255,0.1); 
        margin-bottom: 20px; transition: 0.3s;
    }}

    /* Clase especial para cuando se llega a la meta */
    .goal-active {{
        animation: neon-glow 2s infinite ease-in-out;
        border: 2px solid {accent} !important;
    }}

    .stButton > button {{
        border-radius: 40px !important; background-color: {accent} !important; 
        color: #000000 !important; font-weight: 800; border: none !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 550px; z-index: 1000;
        background-color: white !important; border-radius: 35px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); padding: 8px 20px;
    }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tab_home, tab_edit, tab_savings, tab_expenses, tab_income = st.tabs(["🏠\nInicio", "⚙️\nConfig", "🐷\nAhorro", "🛍️\nGasto", "💼\nIngreso"])

with tab_home:
    st.markdown("### Resumen Financiero")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='card-resumen'><small>DISPONIBLE</small><h1 style='color:#C69F40;'>${balance:,.2f}</h1></div>", unsafe_allow_html=True)
    with col2:
        # Aplicamos la clase de animación si la meta se cumplió
        pulse_class = "goal-active" if goal_reached else ""
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen {pulse_class}'><small>META</small><h1 style='color:{accent};'>{perc}%</h1></div>", unsafe_allow_html=True)

with tab_savings:
    st.header("Tu Meta de Ahorro 🐷")
    
    if goal_reached:
        st.markdown(f"<h2 style='text-align:center; color:{accent};'>¡LO LOGRASTE! 🏆</h2>", unsafe_allow_html=True)
        st_lottie(lottie_celebration, height=250, key="celebration")
        st.balloons()
    
    nueva_meta = st.number_input("Ajustar meta ($)", value=META_AHORRO, step=100.0)
    if nueva_meta != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": nueva_meta}, f)
        st.rerun()

    progreso = min(max(balance / nueva_meta, 0.0), 1.0)
    st.progress(progreso)
    st.write(f"Has ahorrado ${balance:,.2f} de tu objetivo de ${nueva_meta:,.2f}.")

# [Resto de las pestañas: tab_edit, tab_expenses, tab_income permanecen con la lógica previa]
