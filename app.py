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
    bg_gradient = "linear-gradient(135deg, #F0F2F6 0%, #DDE1E7 100%)"
    card_bg = "rgba(255, 255, 255, 0.7)"
    text_main, accent = "#1A1C1E", "#2D0066"
    accent_gradient = "linear-gradient(90deg, #2D0066 0%, #5E00D3 100%)"
else:
    # Degradado Púrpura Profundo para el fondo
    bg_gradient = "radial-gradient(circle at top right, #2D0066 0%, #1A0040 40%, #0D0026 100%)"
    # Fondo de tarjeta con ligero tinte
    card_bg = "linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.03) 100%)"
    text_main, accent = "#FFFFFF", "#D4FF00"
    # Degradado Neón para botones y barras
    accent_gradient = "linear-gradient(90deg, #D4FF00 0%, #8FFF00 100%)"

# --- ESTILOS CSS CON DEGRADADOS ---
st.markdown(f"""
<style>
    /* Fondo Global con Degradado */
    .stApp {{
        background: {bg_gradient} !important;
        color: {text_main};
    }}
    
    h1, h2, h3, h4, p, span, label {{ color: {text_main} !important; }}
    
    /* Tarjetas con Glassmorphism y Degradado Interno */
    .card-resumen, .history-card {{
        background: {card_bg} !important; 
        backdrop-filter: blur(20px) saturate(160%);
        border-radius: 28px; padding: 25px;
        border: 1px solid rgba(255,255,255,0.1); 
        margin-bottom: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }}
    
    /* Historial con borde neón degradado */
    .history-card {{ 
        border-left: 6px solid;
        border-image: {accent_gradient} 1;
        text-align: left; 
    }}
    
    /* Pestañas Flotantes Estilo Apple */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 550px; z-index: 1000;
        background: rgba(255, 255, 255, 0.9) !important; 
        border-radius: 40px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.4); 
        padding: 10px 25px;
        display: flex; justify-content: space-around; border: none !important;
    }}
    
    /* Botones con Degradado */
    .stButton > button {{
        border-radius: 50px !important; 
        background: {accent_gradient} !important; 
        color: #000000 !important; 
        font-weight: 800 !important; 
        border: none !important; 
        width: 100%;
        box-shadow: 0 4px 15px rgba(212, 255, 0, 0.3);
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 255, 0, 0.5);
    }}

    .main .block-container {{ padding-bottom: 160px; }}
</style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if "authenticated" not in st.session_state:
    st.markdown(f"<div style='text-align:center; padding-top:50px;'><h1>👑</h1><h2 style='letter-spacing:5px;'>R.C FINANZAS PRO</h2><p style='opacity:0.6;'>Inicia sesión para continuar</p></div>", unsafe_allow_html=True)
    with st.form("Login"):
        u, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
        if st.form_submit_button("DESBLOQUEAR SISTEMA"):
            if u == "admin" and p == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Acceso Denegado")
    st.stop()

# --- CARGA DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
goal_reached = balance >= META_AHORRO

# --- NAVEGACIÓN ---
t_h, t_c, t_s, t_g, t_i = st.tabs(["🏠\nInicio", "⚙️\nConfig", "🐷\nAhorro", "🛍️\nGasto", "💼\nIngreso"])

with t_h:
    st.markdown("### Resumen Patrimonial")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.7;'>DISPONIBLE</small><h1 style='color:#C69F40; margin:0;'>${balance:,.2f}</h1></div>", unsafe_allow_html=True)
    with c2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.7;'>META</small><h1 style='background:{accent_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0;'>{perc}%</h1></div>", unsafe_allow_html=True)
    
    st.subheader("Movimientos Recientes")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(4).iterrows():
            m_color = "#D4FF00" if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><span style='color:{m_color}; font-size:1.2em;'>${r['Monto']:,.2f}</span></div>", unsafe_allow_html=True)

with t_s:
    st.header("Centro de Ahorro 🐷")
    
    if goal_reached:
        st.balloons()
        if lottie_win: st_lottie(lottie_win, height=150)
        st.markdown(f"<h2 style='text-align:center; color:{accent}'>¡META LOGRADA! 🏆</h2>", unsafe_allow_html=True)

    col_m, col_f = st.columns(2)
    with col_m: m_input = st.number_input("Objetivo Final ($)", value=float(META_AHORRO))
    with col_f: f_input = st.date_input("Fecha límite", value=date.today() + timedelta(days=90))

    if m_input != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m_input}, f)
        st.rerun()

    faltante = max(m_input - balance, 0)
    dias = (f_input - date.today()).days
    esfuerzo = faltante / dias if dias > 0 else 0

    st.markdown(f"""
    <div style="display: flex; gap: 15px; margin: 20px 0;">
        <div class="card-resumen" style="flex:1; padding:20px; text-align:center;">
            <small style="opacity:0.6;">ME FALTAN</small><br><b style="font-size:1.5em;">${faltante:,.2f}</b>
        </div>
        <div class="card-resumen" style="flex:1; padding:20px; text-align:center;">
            <small style="opacity:0.6;">META DIARIA</small><br><b style="font-size:1.5em; color:{accent}">${esfuerzo:,.2f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    prog = min(max(balance / m_input, 0.0), 1.0) if m_input > 0 else 0
    st.markdown(f"""
        <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 20px; height: 18px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="width: {prog*100}%; background: {accent_gradient}; height: 100%; border-radius: 20px; box-shadow: 0 0 20px {accent}77;"></div>
        </div>
        <p style='text-align:right; font-size:0.8em; margin-top:5px; opacity:0.7;'>Progreso: {int(prog*100)}%</p>
    """, unsafe_allow_html=True)

with t_c:
    st.subheader("Configuración")
    theme = st.radio("Tema Visual:", ["Oscuro", "Claro"], horizontal=True, index=0 if st.session_state.theme=="Oscuro" else 1)
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    st.divider()
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("💾 SINCRONIZAR DATOS"):
        ed_df.to_csv(DB_FILE, index=False)
        st.success("Sincronización exitosa")
        st.rerun()

with t_g:
    st.header("Registrar Gasto 🛍️")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(ICONOS.keys()))
        det = st.text_input("Descripción")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("REGISTRAR"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_i:
    st.header("Nuevo Ingreso 💼")
    with st.form("fi", clear_on_submit=True):
        det = st.text_input("Origen")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("CARGAR"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()
