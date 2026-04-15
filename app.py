import streamlit as st
import pandas as pd
from datetime import date
import os
import json
import requests
from streamlit_lottie import st_lottie

# 1. CONFIGURACIÓN E INICIALIZACIÓN
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

DB_FILE = "wallet_database.csv"
CONFIG_FILE = "settings.json"

if "theme" not in st.session_state:
    st.session_state.theme = "Oscuro"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f: return json.load(f)
    return {"meta_ahorro": 3000.0}

def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Recursos Visuales
lottie_win = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_TOE99i.json")
config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- LÓGICA DE COLORES DINÁMICOS ---
if st.session_state.theme == "Claro":
    bg_app, bg_glass, text_main, text_sec, accent = "#F0F2F6", "rgba(255, 255, 255, 0.6)", "#1A1C1E", "#5E6368", "#2D0066"
    border_glass, bar_bg = "rgba(0,0,0,0.05)", "#FFFFFF"
else:
    bg_app, bg_glass, text_main, text_sec, accent = "#1A0040", "rgba(255, 255, 255, 0.07)", "#FFFFFF", "#AAAAAA", "#D4FF00"
    border_glass, bar_bg = "rgba(255,255,255,0.1)", "#FFFFFF"

# --- INYECCIÓN DE ESTILOS MAESTROS ---
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_app} !important; color: {text_main}; }}
    h1, h2, h3, h4, p, span, label {{ color: {text_main} !important; }}
    
    /* Animación Neón para Meta Alcanzada */
    @keyframes neon-glow {{
        0% {{ box-shadow: 0 0 5px {accent}; border-color: {accent}; }}
        50% {{ box-shadow: 0 0 25px {accent}; border-color: #fff; }}
        100% {{ box-shadow: 0 0 5px {accent}; border-color: {accent}; }}
    }}

    .card-resumen, .history-card {{
        background: {bg_glass} !important; 
        backdrop-filter: blur(15px) saturate(160%);
        border-radius: 25px; padding: 25px;
        border: 1px solid {border_glass}; margin-bottom: 20px;
    }}
    
    .goal-active {{ animation: neon-glow 2s infinite ease-in-out; border: 2px solid {accent} !important; }}

    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 550px; z-index: 1000;
        background-color: {bar_bg} !important; border-radius: 35px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); padding: 8px 20px;
    }}

    .stButton > button {{
        border-radius: 40px !important; background-color: {accent} !important; 
        color: #000000 !important; font-weight: 800; border: none !important;
        width: 100%; transition: 0.3s;
    }}
</style>
""", unsafe_allow_html=True)

# --- SISTEMA DE SEGURIDAD PREMIUM ---
if "authenticated" not in st.session_state:
    st.markdown(f"""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 4em;">👑</h1>
            <h2 style="letter-spacing: 3px;">R.C FINANZAS <span style="color:{accent};">PRO</span></h2>
            <p style="color:{text_sec};">Acceso Restringido - Terminal de Gestión</p>
        </div>
        <style> [data-testid="stForm"] {{ background: {bg_glass} !important; border-radius: 30px !important; padding: 40px !important; }} </style>
    """, unsafe_allow_html=True)
    
    with st.form("Login"):
        u = st.text_input("Usuario", placeholder="admin")
        p = st.text_input("Contraseña", type="password", placeholder="••••")
        if st.form_submit_button("DESBLOQUEAR SISTEMA"):
            if u == "admin" and p == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Credenciales Incorrectas")
    st.stop()

# --- CARGA Y CÁLCULOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
goal_reached = balance >= META_AHORRO

# --- DASHBOARD ---
tab_h, tab_c, tab_a, tab_g, tab_i = st.tabs(["🏠\nInicio", "⚙️\nConfig", "🐷\nAhorro", "🛍️\nGasto", "💼\nIngreso"])

with tab_h:
    st.markdown("### Estado Actual")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='card-resumen'><small>DISPONIBLE</small><h1 style='color:#C69F40;'>${balance:,.2f}</h1></div>", unsafe_allow_html=True)
    with c2:
        pulse = "goal-active" if goal_reached else ""
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen {pulse}'><small>META</small><h1 style='color:{accent};'>{perc}%</h1></div>", unsafe_allow_html=True)

with tab_a:
    st.header("Meta de Ahorro")
    if goal_reached:
        st_lottie(lottie_win, height=200)
        st.balloons()
    
    m_val = st.number_input("Objetivo ($)", value=META_AHORRO)
    if m_val != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m_val}, f)
        st.rerun()
    st.progress(min(max(balance/m_val, 0.0), 1.0) if m_val > 0 else 0)

with tab_c:
    st.subheader("Personalización")
    t_ch = st.radio("Tema:", ["Oscuro", "Claro"], horizontal=True, index=0 if st.session_state.theme=="Oscuro" else 1)
    if t_ch != st.session_state.theme:
        st.session_state.theme = t_ch
        st.rerun()
    
    st.divider()
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("💾 GUARDAR CAMBIOS"):
        ed_df.to_csv(DB_FILE, index=False)
        st.rerun()

# [Lógica simplificada para Gasto e Ingreso similar a la anterior]
with tab_g:
    with st.form("g"):
        det, mon = st.text_input("Detalle"), st.number_input("Monto")
        if st.form_submit_button("REGISTRAR"):
            new_data = pd.DataFrame([[date.today(), "Gasto", "Varios", det, mon]], columns=df.columns)
            pd.concat([df, new_data]).to_csv(DB_FILE, index=False)
            st.rerun()

with tab_i:
    with st.form("i"):
        det, mon = st.text_input("Origen"), st.number_input("Monto")
        if st.form_submit_button("CARGAR"):
            new_data = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            pd.concat([df, new_data]).to_csv(DB_FILE, index=False)
            st.rerun()
