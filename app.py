import streamlit as st
import pandas as pd
from datetime import date
import os
import json
import requests
from streamlit_lottie import st_lottie

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE USUARIOS ---
USUARIOS = {
    "admin": "1234",
    "roberto": "5555",
    "invitado": "0000"
}

# --- LÓGICA DE LOGIN ---
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

# --- ARCHIVOS Y PERSISTENCIA POR USUARIO ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"
OLD_DB = "wallet_database.csv" # Archivo original a migrar

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
    btn_bg = "#E0E0E0" # Fondo gris claro para botones en tema claro
    btn_text = "#000000"
else:
    bg_gradient = "radial-gradient(circle at top right, #2D0066 0%, #1A0040 40%, #08001A 100%)"
    card_bg = "rgba(255, 255, 255, 0.05)"
    text_main, accent = "#FFFFFF", "#D4FF00"
    accent_gradient = "linear-gradient(90deg, #D4FF00 0%, #A6FF00 100%)"
    shadow_style = "0 20px 50px rgba(0,0,0,0.3)"
    btn_bg = "#333333" # Fondo gris oscuro para botones en tema oscuro (MEJORA CONTRAS)
    btn_text = "#FFFFFF"

# --- ESTILOS CSS REFINADOS (V1.2 CORRECCIONES) ---
st.markdown(f"""
<style>
    .stApp {{ background: {bg_gradient} !important; color: {text_main}; }}
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
    .history-card {{ border-left: 4px solid {accent} !important; background: rgba(255,255,255,0.03) !important; }}
    
    /* MEJORA: Menú Inferior (Iconos más grandes y espaciados) */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 95%; max-width: 550px; z-index: 1000;
        background: rgba(255, 255, 255, 0.1) !important; 
        backdrop-filter: blur(15px);
        border-radius: 50px; 
        padding: 15px 25px; /* Más padding vertical */
        border: 1px solid rgba(255,255,255,0.1) !important;
        display: flex; justify-content: space-around; /* Espaciado uniforme */
    }}
    
    .stTabs [data-baseweb="tab"] {{ 
        color: rgba(255,255,255,0.5) !important; 
        font-size: 1.2rem; /* Iconos más grandes */
        padding: 0 10px;
    }}
    .stTabs [aria-selected="true"] {{ color: {accent} !important; transform: scale(1.1); }}

    /* MEJORA: Botones (Padding y Contraste de Color) */
    .stButton > button {{
        border-radius: 50px !important; 
        background: {btn_bg} !important; /* Nuevo fondo gris oscuro */
        color: {btn_text} !important; /* Texto blanco legible */
        font-weight: 700 !important; 
        border: none !important;
        padding: 12px 24px !important; /* Padding ajustado */
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }}

    /* MEJORA: Editor de Datos (Eliminar fondo blanco) */
    .stDataEditor {{ background-color: transparent !important; }}
    .stDataEditor div[data-testid="stDataEditorDataFrame"] {{ 
        background-color: {card_bg} !important; 
        backdrop-filter: blur(25px);
        border-radius: 20px;
    }}

    .main .block-container {{ padding-bottom: 150px; }}
</style>
""", unsafe_allow_html=True)

# --- SISTEMA DE IMPORTACIÓN INTELIGENTE ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
elif os.path.exists(OLD_DB):
    df = pd.read_csv(OLD_DB)
    df.to_csv(DB_FILE, index=False)
    st.toast(f"✅ Datos migrados a {USER_ID.upper()}")
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

if not df.empty:
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
goal_reached = balance >= META_AHORRO

# --- CABECERA ---
st.markdown(f"<div style='text-align:right;'><small style='opacity:0.5;'>Sesión: </small><b>{USER_ID.upper()}</b></div>", unsafe_allow_html=True)

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
        # MEJORA: Filtrar filas con datos válidos para evitar nan/NaT
        recent_df = df[df['Detalle'].notna() & df['Fecha'].notna()].sort_values(by="Fecha", ascending=False).head(4)
        if not recent_df.empty:
            for i, r in recent_df.iterrows():
                st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><small>{r['Fecha']}</small> • <span style='color:{accent if r['Tipo']=='Ingreso' else '#FF4B4B'}'>${r['Monto']:,.2f}</span></div>", unsafe_allow_html=True)
        else:
            st.info("No hay actividad reciente válida.")
    else:
        st.info("Haga su primera transacción para ver la actividad.")

with t_s:
    st.header("Metas 🐷")
    if goal_reached:
        if lottie_win: st_lottie(lottie_win, height=150)
        st.balloons()
    
    m_input = st.number_input("Objetivo ($)", value=float(META_AHORRO))
    if m_input != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m_input}, f)
        st.rerun()

    # MEJORA: VOLVEMOS A LA BARRA DE PROGRESO DINÁMICA DE LA V1
    prog = min(max(balance / m_input, 0.0), 1.0) if m_input > 0 else 0
    st.markdown(f"""
        <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 20px; height: 15px; margin: 30px 0; box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);">
            <div style="width: {prog*100}%; background: {accent_gradient}; height: 100%; border-radius: 20px; box-shadow: 0 0 20px {accent}; transition: width 0.5s ease-out;"></div>
        </div>
        <p style='text-align:center; opacity:0.7;'>Llevas ${balance:,.2f} de ${m_input:,.2f}</p>
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
    # MEJORA: Editor ahora usa el estilo oscuro/borroso
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
    
    # MEJORA: Lógica de Autocompletado para el Origen
    origenes_sugeridos = []
    if not df.empty:
        origenes_sugeridos = df[df["Tipo"] == "Ingreso"]["Detalle"].dropna().unique().tolist()
        origenes_sugeridos = sorted([str(o) for o in origenes_sugeridos])

    with st.form("fi", clear_on_submit=True):
        # MEJORA: Usamos selectbox para autocompletar (puedes escribir y buscar)
        det = st.selectbox("Origen", options=origenes_sugeridos, index=None, placeholder="Escriba o seleccione origen...", help="Empiece a escribir para ver sugerencias pasadas")
        
        mon = st.number_input("Monto", min_value=0.0)
        
        if st.form_submit_button("CARGAR INGRESO"):
            if det and mon > 0:
                new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
                pd.concat([df, new]).to_csv(DB_FILE, index=False)
                st.rerun()
            else:
                st.warning("Por favor complete el origen y el monto.")
