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

# --- LÓGICA DE COLORES ---
if st.session_state.theme == "Claro":
    bg_app, bg_glass, text_main, text_sec, accent = "#F0F2F6", "rgba(255, 255, 255, 0.6)", "#1A1C1E", "#5E6368", "#2D0066"
    border_glass, bar_bg, bar_shadow = "rgba(0,0,0,0.05)", "#FFFFFF", "rgba(0,0,0,0.1)"
else:
    bg_app, bg_glass, text_main, text_sec, accent = "#1A0040", "rgba(255, 255, 255, 0.07)", "#FFFFFF", "#AAAAAA", "#D4FF00"
    border_glass, bar_bg, bar_shadow = "rgba(255,255,255,0.1)", "#FFFFFF", "rgba(0,0,0,0.5)"

# --- ESTILOS CSS ---
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_app} !important; color: {text_main}; }}
    h1, h2, h3, h4, p, span, label {{ color: {text_main} !important; }}
    
    .card-resumen, .history-card {{
        background: {bg_glass} !important; 
        backdrop-filter: blur(15px) saturate(160%);
        border-radius: 25px; padding: 25px;
        border: 1px solid {border_glass}; margin-bottom: 20px;
    }}
    
    .history-card {{ border-left: 6px solid {accent} !important; text-align: left; padding: 15px; }}
    
    /* Barra de Navegación */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 550px; z-index: 1000;
        background-color: {bar_bg} !important; border-radius: 35px; 
        box-shadow: 0 10px 30px {bar_shadow}; padding: 8px 20px;
        display: flex; justify-content: space-around; border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{ color: #666666 !important; font-size: 0.85em; flex-direction: column; }}
    .stTabs [aria-selected="true"] {{ color: #C69F40 !important; font-weight: bold; transform: scale(1.1); }}

    .stButton > button {{
        border-radius: 40px !important; background-color: {accent} !important; 
        color: #000000 !important; font-weight: 800; border: none !important; width: 100%;
    }}
    
    .main .block-container {{ padding-bottom: 160px; }}
</style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if "authenticated" not in st.session_state:
    st.markdown("<div style='text-align:center;'><h1>👑</h1><h2>R.C FINANZAS PRO</h2></div>", unsafe_allow_html=True)
    with st.form("Login"):
        u, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
        if st.form_submit_button("DESBLOQUEAR"):
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
    with c1: st.markdown(f"<div class='card-resumen'><small>DISPONIBLE</small><h1 style='color:#C69F40;'>${balance:,.2f}</h1></div>", unsafe_allow_html=True)
    with c2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small>META</small><h1 style='color:{accent};'>{perc}%</h1></div>", unsafe_allow_html=True)
    
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(3).iterrows():
            color = accent if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><span style='color:{color}'>${r['Monto']:,.2f}</span></div>", unsafe_allow_html=True)

with t_s:
    st.header("Centro de Ahorro 🐷")
    
    if goal_reached:
        st.balloons()
        if lottie_win: st_lottie(lottie_win, height=150)
        st.success("¡Meta alcanzada!")

    col_m, col_f = st.columns(2)
    with col_m: 
        m_input = st.number_input("Objetivo Final ($)", value=float(META_AHORRO))
    with col_f:
        f_input = st.date_input("Fecha límite", value=date.today() + timedelta(days=90))

    if m_input != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m_input}, f)
        st.rerun()

    # Cálculos Inteligentes
    faltante = max(m_input - balance, 0)
    dias = (f_input - date.today()).days
    esfuerzo = faltante / dias if dias > 0 else 0

    st.markdown(f"""
    <div style="display: flex; gap: 10px; margin: 15px 0;">
        <div class="card-resumen" style="flex:1; padding:15px;">
            <small>ME FALTA</small><br><b>${faltante:,.2f}</b>
        </div>
        <div class="card-resumen" style="flex:1; padding:15px;">
            <small>AHORRO DIARIO</small><br><b style="color:{accent}">${esfuerzo:,.2f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    prog = min(max(balance / m_input, 0.0), 1.0) if m_input > 0 else 0
    st.markdown(f"""
        <div style="width: 100%; background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px;">
            <div style="width: {prog*100}%; background: {accent}; height: 100%; border-radius: 10px; box-shadow: 0 0 10px {accent};"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Hitos de Progreso")
    h_cols = st.columns(4)
    for idx, h in enumerate([0.25, 0.5, 0.75, 1.0]):
        status = "✅" if prog >= h else "🔒"
        h_cols[idx].markdown(f"<div style='text-align:center; opacity:{1 if prog>=h else 0.3}'>{status}<br><small>{int(h*100)}%</small></div>", unsafe_allow_html=True)

with t_c:
    st.subheader("Configuración")
    theme = st.radio("Tema:", ["Oscuro", "Claro"], horizontal=True, index=0 if st.session_state.theme=="Oscuro" else 1)
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    st.divider()
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("💾 GUARDAR TODO"):
        ed_df.to_csv(DB_FILE, index=False)
        st.rerun()

with t_g:
    st.header("Registrar Gasto 🛍️")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(ICONOS.keys()))
        det = st.text_input("¿En qué gastaste?")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("AÑADIR GASTO"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_i:
    st.header("Nuevo Ingreso 💼")
    with st.form("fi", clear_on_submit=True):
        det = st.text_input("Origen del dinero")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("CARGAR DINERO"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()
