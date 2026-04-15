import streamlit as st
import pandas as pd
from datetime import date
import os
import json

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE ACCESO (V1.3) ---
USUARIOS = {"admin": "1234", "roberto": "5555", "invitado": "0000"}

# Inyectamos CSS para centrar el Login y mejorar la UI
st.markdown("""
<style>
    [data-testid="stForm"] {
        max-width: 450px;
        margin: 0 auto;
    }
    .stTabs [data-baseweb="tab-list"] {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 92%; max-width: 500px; z-index: 1000;
        background: rgba(10, 0, 30, 0.85) !important;
        backdrop-filter: blur(25px);
        border-radius: 40px; padding: 10px 20px;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .main .block-container { padding-bottom: 150px; }
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.markdown("<div style='text-align:center; padding:50px 0;'><h1>👑</h1><h2>R.C FINANZAS</h2><p style='opacity:0.5;'>V1.3 Premium</p></div>", unsafe_allow_html=True)
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

# --- LÓGICA DE DATOS CON CACHE (Eficiencia V1.3) ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

@st.cache_data
def load_data(file):
    if os.path.exists(file):
        df = pd.read_csv(file)
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
        return df
    return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

def save_and_refresh(df_to_save):
    df_to_save.to_csv(DB_FILE, index=False)
    st.cache_data.clear()
    st.rerun()

df = load_data(DB_FILE)

# C
