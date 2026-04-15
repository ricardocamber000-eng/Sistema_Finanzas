import streamlit as st
import pandas as pd
from datetime import date
import os
import json
import requests
from streamlit_lottie import st_lottie

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE USUARIOS (NUEVO) ---
USUARIOS = {
    "admin": "1234",
    "roberto": "5555",
    "invitado": "0000"
}

# --- LÓGICA DE LOGIN (BLOQUEANTE) ---
if "authenticated" not in st.session_state:
    st.markdown("<div style='text-align:center; padding:50px 0;'><h1>👑</h1><h2 style='letter-spacing:5px;'>R.C FINANZAS</h2><p style='opacity:0.5;'>Control de Acceso</p></div>", unsafe_allow_html=True)
    with st.form("Login"):
        u = st.text_input("Usuario").lower().strip()
        p = st.text_input("PIN", type="password")
        if st.form_submit_button("ENTRAR"):
            if u in USUARIOS and USUARIOS[u] == p:
                st.session_state.authenticated = True
                st.session_state.user = u
                st.rerun()
            else: 
                st.error("Acceso incorrecto")
    st.stop()

# --- ARCHIVOS Y PERSISTENCIA (AHORA POR USUARIO) ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

if "theme" not in st.session_state:
    st.session_state.theme = "Oscuro"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_win = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_TOE99i.json")

# --- DICCIONARIOS ---
ICONOS = {
    "Servicios": "💡", "Mercado": "🛒", "Deudas": "💳", 
    "Ocio": "🎬", "Transporte": "🚗", "Depósito": "💰", "Varios": "📦"
}

# --- LÓGICA DE COLORES Y DEGRADADOS ---
if st.session_state.theme == "Claro":
    bg_gradient = "linear-gradient(135deg, #F5F7FA 0%, #E4E8ED 100%)"
    card_bg = "rgba(255, 255, 255, 0.8)"
    text_main, accent = "#1A1C1E", "#2D0066"
    accent_gradient = "linear-gradient(90deg, #2D0066 0%, #5E00D3 100%)"
    shadow_style = "0 10px 30px rgba(0,0,0,0.05)"
else:
    bg_gradient = "radial-gradient(circle at top right, #2D0066 0%, #1A0040 40%, #08001A 100%)"
    card_bg = "rgba(255, 255, 255, 0.05)"
    text_main, accent = "#FFFFFF", "#D4FF00"
    accent_gradient = "linear-gradient(90deg, #D4FF00 0%, #A6FF00 100%)"
    shadow_style = "0 20px 50px rgba(0,0,0,0.3)"

# --- ESTILOS CSS REFINADOS (V1 ORIGINAL) ---
st.markdown(f"""
<style>
    .stApp {{
        background: {bg_gradient} !important;
        color: {text_main};
    }}
    
    h1, h2, h3, h4, p, span, label {{ color: {text_main} !important; }}
    
    .card-resumen, .history-card {{
        background: {card_bg} !important; 
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-radius: 30px; 
        padding: 25px;
        border: none !important;
        margin-bottom: 22px;
        box-shadow: {shadow_style};
    }}
    
    .history-card {{ 
        border-left: 4px solid {accent} !important;
        background: rgba(255,255,255,0.03) !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 500px; z-index: 1000;
        background: rgba(255, 255, 255, 0.1) !important; 
        backdrop-filter: blur(15px);
        border-radius: 50px; 
        padding: 10px 20px;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{ color: rgba(255,255,255,0.5) !important; font-size: 0.8em; }}
    .stTabs [aria-selected="true"] {{ color: {accent} !important; font-weight: bold; }}

    .stButton > button {{
        border-radius: 50px !important; 
        background: {accent_gradient} !important; 
        color: #000 !important; 
        font-weight: 800 !important; 
        border: none !important;
        padding: 12px 0;
        box-shadow: 0 10px 20px rgba(212, 255, 0, 0.2);
    }}

    .main .block-container {{ padding-bottom: 150px; }}
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
goal_reached = balance >= META_AHORRO

# --- CABECERA DE USUARIO ---
st.markdown(f"<div style='text-align:right;'><small style='opacity:0.5;'>Usuario: </small><b>{USER_ID.upper()}</b></div>", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
t_h, t_c, t_s, t_g, t_i = st.tabs(["🏠", "⚙️", "🐷", "🛍️", "💼"])

with t_h:
    st.markdown("### Resumen")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.5;'>SALDO</small><h2 style='margin:0;'>${balance:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.5;'>META</small><h2 style='color:{accent}; margin:0;'>{perc}%</h2></div>", unsafe_allow_html=True)
    
    st.markdown("#### Actividad Reciente")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(4).iterrows():
            st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><small>{r['Fecha']}</small> • <span style='color:{accent if r['Tipo']=='Ingreso' else '#FF4B4B'}'>${r['Monto']:,.2f}</span></div>", unsafe_allow_html=True)

with t_s:
    st.header("Metas 🐷")
    if goal_reached:
        if lottie_win: st_lottie(lottie_win, height=150)
        st.balloons()
    
    m_input = st.number_input("Objetivo ($)", value=float(META_AHORRO))
    if m_input != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m_input}, f)
        st.rerun()

    prog = min(max(balance / m_input, 0.0), 1.0) if m_input > 0 else 0
    st.markdown(f"""
        <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 20px; height: 10px; margin: 20px 0;">
            <div style="width: {prog*100}%; background: {accent_gradient}; height: 100%; border-radius: 20px; box-shadow: 0 0 15px {accent};"></div>
        </div>
    """, unsafe_allow_html=True)

with t_c:
    st.subheader("Configuración")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cambiar Tema"):
            st.session_state.theme = "Claro" if st.session_state.theme == "Oscuro" else "Oscuro"
            st.rerun()
    with col2:
        if st.button("Cerrar Sesión"):
            del st.session_state.authenticated
            st.rerun()
            
    st.divider()
    st.markdown("#### Gestión de Datos")
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios"):
        ed_df.to_csv(DB_FILE, index=False)
        st.rerun()

with t_g:
    st.header("Gasto")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(ICONOS.keys()))
        det = st.text_input("Nota")
        mon = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("REGISTRAR GASTO"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_i:
    st.header("Ingreso")
    with st.form("fi", clear_on_submit=True):
        det = st.text_input("Origen")
        mon = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

# --- LÓGICA DE COLORES Y DEGRADADOS (ESTILO V1) ---
if st.session_state.
