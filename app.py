import streamlit as st
import pandas as pd
from datetime import date
import os
import json

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE ACCESO (V1.2) ---

USUARIOS = {"admin": "1234", "roberto": "5555", "invitado": "0000"}



if "authenticated" not in st.session_state:

    st.markdown("<div style='text-align:center; padding:50px 0;'><h1>👑</h1><h2>R.C FINANZAS</h2><p style='opacity:0.5;'>V1.2 Premium</p></div>", unsafe_allow_html=True)

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

# --- LÓGICA DE DATOS PERSISTENTES POR USUARIO (V1.2) ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f: return json.load(f)
    return {"meta_ahorro": 3000.0}

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- ESTILOS CSS (AURA + GLASSMORPHISM V1.2) ---
st.markdown(f"""
<style>
    /* FONDO DE AURA DINÁMICA */
    .stApp {{
        background-color: #08001A !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(45, 0, 102, 0.4) 0px, transparent 55%), 
            radial-gradient(at 100% 0%, rgba(212, 255, 0, 0.08) 0px, transparent 50%), 
            radial-gradient(at 100% 100%, rgba(94, 0, 211, 0.3) 0px, transparent 55%),
            radial-gradient(at 0% 100%, rgba(0, 212, 255, 0.12) 0px, transparent 50%);
        background-attachment: fixed;
        animation: aura-flow 25s ease infinite alternate;
    }}

    @keyframes aura-flow {{
        0% {{ background-size: 100% 100%; background-position: 0% 0%; }}
        50% {{ background-size: 115% 115%; background-position: 50% 50%; }}
        100% {{ background-size: 100% 100%; background-position: 100% 100%; }}
    }}

    /* TARJETAS GLASSMORPHISM */
    .card-resumen, .history-card, [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(35px) saturate(170%);
        border-radius: 28px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }}

    .history-card {{ border-left: 5px solid #D4FF00 !important; }}

    /* BOTONES NEÓN LIMA */
    .stButton > button {{
        width: 100%;
        border-radius: 18px !important;
        background: #D4FF00 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: none !important;
        padding: 14px 25px !important;
        box-shadow: 0 0 15px rgba(212, 255, 0, 0.2);
    }}

    /* MENÚ INFERIOR FLOTANTE */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 92%; max-width: 500px; z-index: 1000;
        background: rgba(10, 0, 30, 0.85) !important;
        backdrop-filter: blur(25px);
        border-radius: 40px; padding: 10px 20px;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    .stTabs [data-baseweb="tab"] {{ font-size: 1.5rem; color: rgba(255,255,255,0.4) !important; }}
    .stTabs [aria-selected="true"] {{ color: #D4FF00 !important; transform: scale(1.15); }}

    .main .block-container {{ padding-bottom: 150px; }}
</style>
""", unsafe_allow_html=True)

# --- PROCESAMIENTO DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

if not df.empty:
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date

balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0

# --- NAVEGACIÓN POR TABS ---
t_h, t_c, t_s, t_g, t_i = st.tabs(["🏠", "⚙️", "🐷", "🛍️", "💼"])

with t_h:
    st.markdown(f"### Hola, {USER_ID.upper()}")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.6;'>DISPONIBLE</small><h2 style='margin:0; color:#D4FF00;'>${balance:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small style='opacity:0.6;'>META</small><h2 style='margin:0;'>{perc}%</h2></div>", unsafe_allow_html=True)
    
    st.markdown("#### Actividad Reciente")
    if not df.empty:
        recents = df[df['Detalle'].notna()].sort_values(by="Fecha", ascending=False).head(5)
        for _, r in recents.iterrows():
            st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><small>{r['Fecha']}</small> • <span style='color:#D4FF00;'>${r['Monto']:,.2f}</span></div>", unsafe_allow_html=True)

with t_s:
    st.header("Metas de Ahorro")
    m_input = st.number_input("Objetivo ($)", value=float(META_AHORRO))
    if m_input != META_AHORRO:
        with open(CONFIG_FILE, "w") as f: json.dump({"meta_ahorro": m_input}, f)
        st.rerun()

    prog = min(max(balance / m_input, 0.0), 1.0) if m_input > 0 else 0
    st.markdown(f"""
        <div style="width: 100%; background: rgba(255,255,255,0.05); border-radius: 20px; height: 18px; margin: 30px 0;">
            <div style="width: {prog*100}%; background: linear-gradient(90deg, #D4FF00, #A6FF00); height: 100%; border-radius: 20px; box-shadow: 0 0 25px #D4FF00;"></div>
        </div>
    """, unsafe_allow_html=True)

with t_c:
    st.subheader("Configuración")
    if st.button("Cerrar Sesión"):
        del st.session_state.authenticated
        st.rerun()
    st.divider()
    st.markdown("#### Gestión de Datos")
    ed_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios"):
        ed_df.to_csv(DB_FILE, index=False)
        st.success("Base de datos actualizada")

with t_g:
    st.header("Registrar Gasto")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", ["Servicios", "Mercado", "Deudas", "Ocio", "Varios"])
        det = st.text_input("Descripción")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("REGISTRAR"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with t_i:
    st.header("Registrar Ingreso")
    # LÓGICA DE AUTOCOMPLETADO DINÁMICO (V1.2)
    options = df[df["Tipo"] == "Ingreso"]["Detalle"].unique().tolist() if not df.empty else []
    with st.form("fi", clear_on_submit=True):
        det_select = st.selectbox("Origen del Dinero", options=options, index=None, placeholder="Selecciona un origen frecuente...")
        det_new = st.text_input("O escribe uno nuevo")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            final_det = det_select if det_select else det_new
            if final_det and mon > 0:
                new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", final_det, mon]], columns=df.columns)
                pd.concat([df, new]).to_csv(DB_FILE, index=False)
                st.rerun()
