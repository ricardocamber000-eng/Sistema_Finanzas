import streamlit as st
import pandas as pd
from datetime import date
import os
import json
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- CONTROL DE ACCESO (V1.3) ---
USUARIOS = {"admin": "1234", "roberto": "5555", "invitado": "0000"}

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

# --- LÓGICA DE DATOS Y CONFIGURACIÓN ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

LIMITES_DEFAULT = {"Servicios": 200.0, "Mercado": 500.0, "Deudas": 300.0, "Ocio": 150.0, "Varios": 100.0}
CATEGORIA_TIPO = {"Servicios": "Fijo", "Mercado": "Fijo", "Deudas": "Fijo", "Ocio": "Variable", "Varios": "Variable"}

@st.cache_data
def load_all_data(db_path, config_path):
    # Cargar DB
    if os.path.exists(db_path):
        df = pd.read_csv(db_path)
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
    else:
        df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
    
    # Cargar Config
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            cfg = json.load(f)
    else:
        cfg = {"meta_ahorro": 3000.0, "limites": LIMITES_DEFAULT}
    
    return df, cfg

def save_db(df):
    df.to_csv(DB_FILE, index=False)
    st.cache_data.clear()
    st.rerun()

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)
    st.cache_data.clear()
    st.rerun()

df, config_data = load_all_data(DB_FILE, CONFIG_FILE)
META_AHORRO = config_data["meta_ahorro"]
LIMITES = config_data.get("limites", LIMITES_DEFAULT)

# --- CÁLCULOS FINANCIEROS ---
total_ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
balance = total_ingresos - total_gastos
ratio_consumo = (total_gastos / total_ingresos) if total_ingresos > 0 else 0

# Alerta de color (80%)
alerta_critica = ratio_consumo > 0.80
color_main = "#FF3131" if alerta_critica else "#D4FF00"

# --- ESTILOS CSS ---
st.markdown(f"""
<style>
    .stApp {{
        background-color: #08001A !important;
        background-image: radial-gradient(at 0% 0%, rgba(45,0,102,0.4) 0px, transparent 55%), radial-gradient(at 100% 0%, rgba(212,255,0,0.08) 0px, transparent 50%);
        background-attachment: fixed;
    }}
    .card-resumen, .history-card, [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(35px); border-radius: 28px; padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.08) !important; margin-bottom: 20px;
    }}
    .stButton > button {{
        background: {color_main} !important; color: #000 !important; font-weight: 800 !important; border-radius: 18px !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 92%; max-width: 600px; z-index: 1000; background: rgba(10,0,30,0.9) !important;
        backdrop-filter: blur(20px); border-radius: 40px; padding: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
t_h, t_stats, t_s, t_g, t_i, t_c = st.tabs(["🏠", "📊", "🐷", "🛍️", "💼", "⚙️"])

with t_h:
    st.markdown(f"### Hola, {USER_ID.upper()}")
    if alerta_critica:
        st.error(f"⚠️ ¡ATENCIÓN! Has gastado el {ratio_consumo:.1%} de tus ingresos.")
    
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='card-resumen'><small>DISPONIBLE</small><h2 style='color:{color_main}'>${balance:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small>META</small><h2>{perc}%</h2></div>", unsafe_allow_html=True)

with t_stats:
    st.subheader("Análisis de Límites Mensuales")
    hoy = date.today()
    df_mes = df[(df["Tipo"] == "Gasto") & (pd.to_datetime(df["Fecha"]).dt.month == hoy.month)]
    gastos_cat = df_mes.groupby("Categoría")["Monto"].sum().to_dict()

    for cat, lim in LIMITES.items():
        actual = gastos_cat.get(cat, 0)
        p = min(actual/lim, 1.0)
        c_bar = "#FF3131" if p > 0.8 else "#D4FF00"
        st.markdown(f"**{cat}** (${actual:,.0f} / ${lim:,.0f})")
        st.progress(p)

with t_s:
    st.header("Meta de Ahorro")
    new_meta = st.number_input("Objetivo Global ($)", value=float(META_AHORRO))
    if st.button("Actualizar Meta"):
        config_data["meta_ahorro"] = new_meta
        save_config(config_data)

with t_g:
    st.header("Registrar Gasto")
    with st.form("fg", clear_on_submit=True):
        cat = st.selectbox("Categoría", list(LIMITES.keys()))
        det = st.text_input("Descripción")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("REGISTRAR"):
            new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
            save_db(pd.concat([df, new]))

with t_i:
    st.header("Registrar Ingreso")
    with st.form("fi", clear_on_submit=True):
        det = st.text_input("Origen")
        mon = st.number_input("Monto ($)", min_value=0.0)
        if st.form_submit_button("CARGAR INGRESO"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)
            save_db(pd.concat([df, new]))

with t_c:
    st.subheader("Configuración Avanzada")
    if st.button("Cerrar Sesión"):
        del st.session_state.authenticated
        st.rerun()
    
    st.markdown("### Editar Límites por Categoría")
    nuevos_limites = {}
    for cat, lim in LIMITES.items():
        nuevos_limites[cat] = st.number_input(f"Límite {cat}", value=float(lim))
    
    if st.button("Guardar Nuevos Límites"):
        config_data["limites"] = nuevos_limites
        save_config(config_data)
