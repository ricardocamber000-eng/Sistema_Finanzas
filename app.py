import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import json
import requests
from streamlit_lottie import st_lottie

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- ARCHIVOS Y PERSISTENCIA ---
DB_FILE = "wallet_database.csv"
CONFIG_FILE = "settings.json"

if "theme" not in st.session_state:
    st.session_state.theme = "Oscuro"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- DICCIONARIO DE CATEGORÍAS ---
ICONOS = {
    "Servicios": "💡", 
    "Mercado": "🛒", 
    "Deudas": "💳", 
    "Ocio": "🎬", 
    "Transporte": "🚗", 
    "Depósito": "💰", 
    "Varios": "📦"
}

# --- LÓGICA DE COLORES Y DEGRADADOS ---
if st.session_state.theme == "Claro":
    bg_gradient = "linear-gradient(135deg, #F8F9FB 0%, #E2E8F0 100%)"
    card_bg = "rgba(255, 255, 255, 0.8)"
    text_main, accent = "#1A1C1E", "#2D0066"
    accent_gradient = "linear-gradient(90deg, #2D0066 0%, #5E00D3 100%)"
    nav_bg = "rgba(255, 255, 255, 0.9)"
    shadow_style = "0 10px 40px rgba(0,0,0,0.05)"
else:
    bg_gradient = "radial-gradient(circle at top right, #2D0066 0%, #1A0040 40%, #08001A 100%)"
    card_bg = "rgba(255, 255, 255, 0.05)"
    text_main, accent = "#FFFFFF", "#D4FF00"
    accent_gradient = "linear-gradient(90deg, #D4FF00 0%, #A6FF00 100%)"
    nav_bg = "rgba(20, 10, 40, 0.7)"
    shadow_style = "0 20px 60px rgba(0,0,0,0.4)"

# --- ESTILOS CSS REFINADOS ---
st.markdown(f"""
<style>
    .stApp {{
        background: {bg_gradient} !important;
        color: {text_main};
    }}
    
    .card-resumen, .history-card {{
        background: {card_bg} !important; 
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 32px; 
        padding: 25px;
        border: none !important;
        margin-bottom: 22px;
        box-shadow: {shadow_style};
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 92%; max-width: 480px; z-index: 1000;
        background: {nav_bg} !important; 
        backdrop-filter: blur(20px);
        border-radius: 50px; 
        padding: 12px 15px;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.5);
    }}
    
    .stTabs [data-baseweb="tab"] {{ 
        color: rgba(255,255,255,0.4) !important; 
        font-size: 1.8rem !important; 
        padding: 10px 5px !important;
    }}
    
    .stTabs [aria-selected="true"] {{ 
        color: {accent} !important; 
        transform: scale(1.25);
        transition: all 0.3s ease;
    }}

    .stButton > button {{
        border-radius: 50px !important; 
        background: {accent_gradient} !important; 
        color: #000 !important; 
        font-weight: 800 !important; 
        border: none !important;
        padding: 15px 0;
        box-shadow: 0 10px 25px rgba(212, 255, 0, 0.2);
    }}

    .main .block-container {{ padding-bottom: 160px; }}
</style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if "authenticated" not in st.session_state:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1>👑</h1><h2 style='letter-spacing:5px;'>R.C FINANZAS</h2></div>", unsafe_allow_html=True)
    with st.form("Login"):
        u = st.text_input("Admin")
        p = st.text_input("PIN", type="password")
        if st.form_submit_button("ACCEDER"):
            if u == "admin" and p == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Acceso denegado")
    st.stop()

# --- CARGA DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
goal_reached = balance >= META_AHORRO

# --- TABS ---
t_h, t_c, t_s, t_g, t_i = st.tabs(["🏠", "⚙️", "🐷", "🛍️", "💼"])

with t_h:
    st.markdown("### Estado Actual")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.5;'>DISPONIBLE</small><h2 style='margin:0;'>${balance:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.5;'>PROGRESO</small><h2 style='background:{accent_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0;'>{perc}%</h2></div>", unsafe_allow_html=True)
    
    st.markdown("#### Historial")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(4).iterrows():
            icono = ICONOS.get(r['Categoría'], "📝")
            st.markdown(f"<div class='history-card'>{icono} <b>{r['Detalle']}</b><br><span style='color:{accent if r['Tipo']=='Ingreso' else '#FF4B4B'}'>${r['Monto']:,.2f}</span></div>", unsafe_allow_html=True)

with t_s:
    st.header("Metas 🐷")
    m_input = st.number_input("Objetivo ($)", value=float(META_AHORRO))
    if m_input != META_AHORRO:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"meta_ahorro": m_input}, f)
        st.rerun()

    prog = min(max(balance / m_input, 0.0), 1.0) if m_input > 0 else 0
    st.markdown(f"""
        <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 20px; height: 14px; margin: 30px 0;">
            <div style="width: {prog*100}%; background: {accent_gradient}; height: 100%; border-radius: 20px; box-shadow: 0 0 15px {accent};"></div>
        </div>
    """, unsafe_allow_html=True)

with t_c:
    st.subheader("Configuración")
    if st.button("Cambiar Tema"):
        st.session_state.theme = "Claro" if st.session_state.theme == "Oscuro" else "Oscuro"
        st.rerun()
    st.divider()
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios"):
        ed_df.to_csv(DB_FILE, index=False)
        st.success("Sincronizado")
        st.rerun()

with t_g:
    st.header("Nuevo Gasto 🛍️")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(ICONOS.keys()))
        det = st.text_input("Descripción")
        mon = st.number_input("M
