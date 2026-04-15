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
    
    /* Tarjetas sin bordes y con Glassmorphism */
    .card-resumen, .history-card {{
        background: {card_bg} !important; 
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 32px; 
        padding: 25px;
        border: none !important;
        margin-bottom: 22px;
        box-shadow: {shadow_style};
    }}
    
    /* Barra de Navegación Ajustada (Iconos más grandes) */
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
    
    /* Aumentar tamaño de iconos y texto en pestañas */
    .stTabs [data-baseweb="tab"] {{ 
        color: rgba(255,255,255,0.4) !important; 
        font-size: 1.6rem !important; /* Iconos más grandes */
        padding: 10px 0px !important;
    }}
    
    .stTabs [aria-selected="true"] {{ 
        color: {accent} !important; 
        transform: scale(1.2);
        transition: all 0.3s ease;
    }}

    /* Estilo para los botones con degradado */
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

# --- LÓGICA DE DATOS Y SEGURIDAD ---
if "authenticated" not in st.session_state:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1>👑</h1><h2 style='letter-spacing:5px;'>R.C FINANZAS</h2></div>", unsafe_allow_html=True)
    with st.form("Login"):
        u, p = st.text_input("Admin"), st.text_input("PIN", type="password")
        if st.form_submit_button("ACCEDER"):
            if u == "admin" and p == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Credenciales incorrectas")
    st.stop()

if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
goal_reached = balance >= META_AHORRO

# --- TABS CON ICONOS ESCALADOS ---
t_h, t_c, t_s, t_g, t_i = st.tabs(["🏠", "⚙️", "🐷", "🛍️", "💼"])

with t_h:
    st.markdown("### Estado Actual")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.5; font-weight:bold;'>DISPONIBLE</small><h2 style='margin:0; font-size:2.2em;'>${balance:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.5; font-weight:bold;'>PROGRESO</small><h2 style='background:{accent_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-size:2.2em;'>{perc}%</h2></div>", unsafe_allow_html=True)
    
    st.markdown("#### Historial Reciente")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(4).iterrows():
            st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><span style='color:{accent if r['Tipo']=='Ingreso' else '#FF4B4B'}; font-weight:bold;'>${r['Monto']:,.2f}</span> <small style='opacity:0.4; margin-left:10px;'>{r['Fecha']}</small></div>", unsafe_allow_html=True)

with t_s:
    st.header("Metas de Ahorro 🐷")
    m_input = st.number_input("Establecer Objetivo ($)", value=float(META_AHORRO))
    if m_input != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m_input}, f)
        st.rerun()

    prog = min(max(balance / m_input, 0.0), 1.0) if m_input > 0 else 0
    # Barra de progreso con resplandor neón
    st.markdown(f"""
        <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 20px; height: 14px; margin: 30px 0;">
            <div style="width: {prog*100}%; background: {accent_gradient}; height: 100%; border-radius: 20px; box-shadow: 0 0 20px {accent}88;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    faltante = max(m_input - balance, 0)
    st.info(f"Faltan ${faltante:,.2f} para tu objetivo.")

with t_c:
    st.subheader("Panel de Control")
    if st.button("Alternar Modo"):
        st.session_state.theme = "Claro" if st.session_state.theme == "Oscuro" else "Oscuro"
        st.rerun()
    st.divider()
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Base de Datos"):
        ed_df.to_csv(DB_FILE, index=False)
        st.success("Cambios aplicados")

with t_g:
    st.header("Añadir Gasto")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(ICONOS.keys()))
        det = st.text_input("¿En qué se gastó?")
        mon = st.number_input("Importe", min_value=0.0)
        if st.form_submit_button("REGISTRAR GASTO"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_i:
    st.header("Cargar Ingreso")
    with st.form("fi", clear_on_submit=True):
        det = st.text_input("Concepto o Fuente")
        mon = st.number_input("Monto Recibido", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()
