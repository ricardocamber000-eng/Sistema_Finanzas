import streamlit as st
import pandas as pd
from datetime import date
import os
import json

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE ACCESO ---
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

# --- CARGA Y LIMPIEZA PREVENTIVA (EVITA EL CIERRE) ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"

@st.cache_data
def get_clean_data(file):
    if os.path.exists(file):
        try:
            temp_df = pd.read_csv(file)
            # Forzamos que la columna Monto sea numérica y eliminamos nulos
            temp_df['Monto'] = pd.to_numeric(temp_df['Monto'], errors='coerce').fillna(0.0)
            temp_df = temp_df.dropna(subset=['Fecha', 'Tipo'])
            return temp_df
        except:
            return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
    return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

df = get_clean_data(DB_FILE)

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #08001A !important; color: white; }
    .card-resumen, .history-card, [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab-list"] {
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 450px; z-index: 1000;
        background: #110033 !important; border-radius: 40px; height: 70px;
    }
    .stTabs [data-baseweb="tab"] { font-size: 1.8rem !important; }
    .stTabs [data-baseweb="tab"]:last-child { color: #FF4B4B !important; }
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
t_h, t_c, t_s, t_g, t_i, t_quit = st.tabs(["🏠", "⚙️", "🐷", "📊", "💼", "🔘"])

with t_h:
    balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum()
    st.markdown(f"### Hola, {USER_ID.upper()}")
    st.markdown(f"<div class='card-resumen'>Saldo Actual: <b>${balance:,.2f}</b></div>", unsafe_allow_html=True)
    
    st.write("#### Actividad")
    if not df.empty:
        # Aquí usamos .get() o validamos para que no explote si la fila está mal
        for _, r in df.sort_values(by="Fecha", ascending=False).head(5).iterrows():
            monto_val = r['Monto'] if pd.notnull(r['Monto']) else 0.0
            st.markdown(f"<div class='history-card'>{r['Detalle']} <br> <b>${monto_val:,.2f}</b></div>", unsafe_allow_html=True)

with t_quit:
    # Borrado total para forzar salida limpia
    st.session_state.clear()
    st.rerun()

# (Resto de pestañas t_c, t_s, t_g, t_i siguen la misma lógica de registro)
