import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import json
import plotly.graph_objects as go
import io

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- VARIABLES GLOBALES DE RESPALDO ---
LIMITES_DEFAULT = {"Servicios": 200.0, "Mercado": 500.0, "Deudas": 300.0, "Ocio": 150.0, "Varios": 100.0}

# --- LÓGICA DE DATOS (Definida antes de ser usada) ---
@st.cache_data
def load_all_data(db_path, config_path):
    # Cargar Base de Datos
    if os.path.exists(db_path):
        df = pd.read_csv(db_path)
        if not df.empty:
            df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
    else:
        df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
    
    # Cargar Configuración
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            cfg = json.load(f)
    else:
        cfg = {"meta_ahorro": 3000.0, "limites": LIMITES_DEFAULT}
    
    return df, cfg

def save_db(df, db_path):
    df.to_csv(db_path, index=False)
    st.cache_data.clear()
    st.rerun()

def save_config(cfg, config_path):
    with open(config_path, "w") as f:
        json.dump(cfg, f, indent=4)
    st.cache_data.clear()
    st.rerun()

# --- FUNCIONES DE ALERTA ---
def disparar_alertas_inicio(df, limites):
    """Analiza excesos y calcula el monto exacto para volver al 80%."""
    if df.empty:
        return
        
    hoy = date.today()
    df_mes = df[(df["Tipo"] == "Gasto") & 
                (pd.to_datetime(df["Fecha"]).dt.month == hoy.month) & 
                (pd.to_datetime(df["Fecha"]).dt.year == hoy.year)]
    
    if df_mes.empty:
        st.toast("👑 Iniciando mes con cuentas limpias.", icon="✅")
        return

    gastos_cat = df_mes.groupby("Categoría")["Monto"].sum().to_dict()
    encontradas = False
    for cat, lim in limites.items():
        actual = gastos_cat.get(cat, 0)
        margen_seguro = lim * 0.80
        if actual > margen_seguro:
            encontradas = True
            sobrante = actual - margen_seguro
            st.toast(f"💸 {cat}: Reduce ${sobrante:,.2f} para zona segura.", icon="⚠️")
    
    if not encontradas: 
        st.toast("👑 Finanzas bajo control.", icon="✅")

# --- CONTROL DE ACCESO ---
USUARIOS = {"admin": "1234", "roberto": "5555", "invitado": "0000"}

if "authenticated" not in st.session_state:
    st.markdown("<div style='text-align:center; padding:50px 0;'><h1>👑</h1><h2>R.C FINANZAS</h2><p style='opacity:0.5;'>V1.4 Premium</p></div>", unsafe_allow_html=True)
    with st.form("Login"):
        u = st.text_input("Usuario").lower().strip()
        p = st.text_input("PIN", type="password")
        if st.form_submit_button("ENTRAR"):
            if u in USUARIOS and USUARIOS[u] == p:
                st.session_state.authenticated = True
                st.session_state.user = u
                # Ejecutar alertas inmediatamente tras login exitoso
                df_init, cfg_init = load_all_data(f"db_{u}.csv", f"settings_{u}.json")
                disparar_alertas_inicio(df_init, cfg_init.get("limites", LIMITES_DEFAULT))
                st.rerun()
            else:
                st.error("Acceso incorrecto")
    st.stop()

# --- INICIALIZACIÓN DE SESIÓN ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

df, config_data = load_all_data(DB_FILE, CONFIG_FILE)
META_AHORRO = config_data.get("meta_ahorro", 3000.0)
LIMITES
