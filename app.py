import streamlit as st
import pandas as pd
from datetime import date
import os
import json

# 1. CONFIGURACIÓN E IDENTIDAD
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

# --- CARGA DE DATOS BLINDADA ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

@st.cache_data(show_spinner=False)
def load_and_clean_data(file_path):
    if os.path.exists(file_path):
        try:
            temp_df = pd.read_csv(file_path)
            # LIMPIEZA CRÍTICA: Convertir a número y llenar vacíos con 0.0
            temp_df['Monto'] = pd.to_numeric(temp_df['Monto'], errors='coerce').fillna(0.0)
            # Asegurar que Fecha sea datetime
            temp_df['Fecha'] = pd.to_datetime(temp_df['Fecha'], errors='coerce').dt.date
            # Eliminar filas donde Tipo o Fecha sean nulos
            temp_df = temp_df.dropna(subset=['Tipo', 'Fecha'])
            return temp_df
        except Exception:
            return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
    return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cargamos los datos ya limpios
df = load_and_clean_data(DB_FILE)

# --- ESTILOS CSS ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #08001A !important; }}
    .card-resumen, .history-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 20px; padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
    }}
    /* BARRA INFERIOR */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 450px; z-index: 1000;
        background: #110033 !important; border-radius: 40px; height: 70px;
        display: flex; align-items: center; justify-content: space-around;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    .stTabs [data-baseweb="tab"] {{ font-size: 1.8rem !important; background: transparent !important; }}
    .stTabs [aria-selected="true"] {{ color: #D4FF00 !important; }}
    .stTabs [data-baseweb="tab"]:last-child {{ color: #FF4B4B !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
t_h, t_c, t_s, t_g, t_i, t_quit = st.tabs(["🏠", "⚙️", "🐷", "📊", "💼", "🔘"])

with t_h:
    balance = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum()
    st.markdown(f"### Hola, {USER_ID.upper()}")
    st.markdown(f"<div class='card-resumen'>Saldo: <span style='color:#D4FF00;'>${balance:,.2f}</span></div>", unsafe_allow_html=True)
    
    st.write("#### Actividad Reciente")
    if not df.empty:
        # Ordenar y mostrar solo los 5 últimos con montos válidos
        recents = df.sort_values(by="Fecha", ascending=False).head(5)
        for _, r in recents.iterrows():
            # Validación extra antes del renderizado
            val = float(r['Monto']) if pd.notnull(r['Monto']) else 0.0
            st.markdown(f"<div class='history-card'><b>{r['Detalle']}</b><br><small>{r['Fecha']}</small> • ${val:,.2f}</div>", unsafe_allow_html=True)

with t_c:
    st.subheader("⚙️ Editor de Datos")
    new_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios"):
        new_df.to_csv(DB_FILE, index=False)
        st.cache_data.clear() # Limpiar cache para recargar datos frescos
        st.rerun()

with t_quit:
    # Botón de apagado: Limpia sesión y regresa al login
    st.session_state.clear()
    st.rerun()
