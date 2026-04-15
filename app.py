import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import json
import plotly.graph_objects as go
import io

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- FUNCIONES DE ALERTA Y CÁLCULO ---
def disparar_alertas_inicio(df, limites):
    """Analiza excesos y calcula el monto exacto para volver al 80%."""
    hoy = date.today()
    df_mes = df[(df["Tipo"] == "Gasto") & 
                (pd.to_datetime(df["Fecha"]).dt.month == hoy.month) & 
                (pd.to_datetime(df["Fecha"]).dt.year == hoy.year)]
    
    gastos_cat = df_mes.groupby("Categoría")["Monto"].sum().to_dict()
    encontradas = False
    for cat, lim in limites.items():
        actual = gastos_cat.get(cat, 0)
        margen_seguro = lim * 0.80
        if actual > margen_seguro:
            encontradas = True
            sobrante = actual - margen_seguro
            st.toast(f"💸 {cat}: Reduce ${sobrante:,.2f} para volver a zona segura.", icon="⚠️")
    if not encontradas: st.toast("👑 Finanzas bajo control.", icon="✅")

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
                # Ejecutar alertas al entrar
                df_init, cfg_init = load_all_data(f"db_{u}.csv", f"settings_{u}.json")
                disparar_alertas_inicio(df_init, cfg_init.get("limites", {}))
                st.rerun()
            else: st.error("Acceso incorrecto")
    st.stop()

# --- LÓGICA DE DATOS ---
USER_ID = st.session_state.user
DB_FILE = f"db_{USER_ID}.csv"
CONFIG_FILE = f"settings_{USER_ID}.json"

LIMITES_DEFAULT = {"Servicios": 200.0, "Mercado": 500.0, "Deudas": 300.0, "Ocio": 150.0, "Varios": 100.0}

@st.cache_data
def load_all_data(db_path, config_path):
    df = pd.read_csv(db_path) if os.path.exists(db_path) else pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])
    if not df.empty: df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
    if os.path.exists(config_path):
        with open(config_path, "r") as f: cfg = json.load(f)
    else: cfg = {"meta_ahorro": 3000.0, "limites": LIMITES_DEFAULT}
    return df, cfg

def save_db(df):
    df.to_csv(DB_FILE, index=False)
    st.cache_data.clear()
    st.rerun()

df, config_data = load_all_data(DB_FILE, CONFIG_FILE)
META_AHORRO = config_data["meta_ahorro"]
LIMITES = config_data.get("limites", LIMITES_DEFAULT)

total_ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
balance = total_ingresos - total_gastos
ratio_consumo = (total_gastos / total_ingresos) if total_ingresos > 0 else 0
color_main = "#FF3131" if ratio_consumo > 0.80 else "#D4FF00"

# --- ESTILOS CSS ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #08001A !important; background-image: radial-gradient(at 0% 0%, rgba(45,0,102,0.4) 0px, transparent 55%), radial-gradient(at 100% 0%, rgba(212,255,0,0.08) 0px, transparent 50%); background-attachment: fixed; }}
    .card-resumen, .history-card, [data-testid="stForm"] {{ background: rgba(255, 255, 255, 0.03) !important; backdrop-filter: blur(35px); border-radius: 28px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.08) !important; margin-bottom: 20px; }}
    .stButton > button {{ background: {color_main} !important; color: #000 !important; font-weight: 800 !important; border-radius: 18px !important; }}
    .stTabs [data-baseweb="tab-list"] {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 92%; max-width: 600px; z-index: 1000; background: rgba(10,0,30,0.9) !important; border-radius: 40px; padding: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
t_h, t_stats, t_s, t_g, t_i, t_c = st.tabs(["🏠", "📊", "🐷", "🛍️", "💼", "⚙️"])

with t_h:
    st.markdown(f"### Hola, {USER_ID.upper()}")
    
    # Gráfico Gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = ratio_consumo * 100,
        number = {'suffix': "%", 'font': {'color': "#FFFFFF"}},
        title = {'text': "Consumo de Ingresos", 'font': {'color': color_main}},
        gauge = {
            'axis': {'range':, 'tickcolor': "white"},
            'bar': {'color': color_main},
            'steps': [{'range':, 'color': "rgba(212, 255, 0, 0.1)"}, {'range':, 'color': "rgba(255, 49, 49, 0.1)"}],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 80}
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=300, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='card-resumen'><small>DISPONIBLE</small><h2 style='color:{color_main}'>${balance:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        p_ahorro = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"<div class='card-resumen'><small>META AHORRO</small><h2>{p_ahorro}%</h2></div>", unsafe_allow_html=True)

with t_stats:
    st.subheader("Análisis de Límites y Seguridad (80%)")
    df_mes = df[(df["Tipo"] == "Gasto") & (pd.to_datetime(df["Fecha"]).dt.month == date.today().month)]
    gastos_cat = df_mes.groupby("Categoría")["Monto"].sum().to_dict()

    for cat, lim in LIMITES.items():
        actual = gastos_cat.get(cat, 0)
        seguro = lim * 0.8
        diff = seguro - actual
        c_bar = "#D4FF00" if diff > 0 else "#FF3131"
        
        st.markdown(f"**{cat}** | {'Zona Segura: +$' if diff > 0 else 'Exceso: -$'}{abs(diff):,.2f}")
        st.progress(min(actual/lim, 1.0))

with t_c:
    st.subheader("Gestión de Datos y Reportes")
    if st.button("Cerrar Sesión"):
        del st.session_state.authenticated
        st.rerun()
    
    st.divider()
    if not df.empty:
        # Generar Excel con Proyecciones
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
            df.to_excel(wr, sheet_name='Movimientos', index=False)
            # Proyección 12 meses basada en últimos 90 días
            df_90 = df[pd.to_datetime(df['Fecha']).dt.date >= (date.today() - timedelta(days=90))]
            ahorro_anual = (df_90[df_90["Tipo"]=="Ingreso"]["Monto"].sum() - df_90[df_90["Tipo"]=="Gasto"]["Monto"].sum()) * 4
            pd.DataFrame({"Métrica": ["Proyección Ahorro Anual"], "Valor": [ahorro_anual]}).to_excel(wr, sheet_name='Proyecciones', index=False)
        
        st.download_button("Descargar Reporte Excel (.xlsx)", buf.getvalue(), f"finanzas_{USER_ID}.xlsx")

# --- REGISTROS (Resumidos para brevedad) ---
with t_g:
    st.header("Gasto")
    with st.form("fg", True):
        cat = st.selectbox("Categoría", list(LIMITES.keys()))
        det = st.text_input("Detalle")
        mon = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("REGISTRAR"): save_db(pd.concat([df, pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)]))

with t_i:
    st.header("Ingreso")
    with st.form("fi", True):
        det = st.text_input("Origen")
        mon = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("CARGAR"): save_db(pd.concat([df, pd.DataFrame([[date.today(), "Ingreso", "Depósito", det, mon]], columns=df.columns)]))

df, config_data = load_all_data(DB_FILE, CONFIG_FILE)
META_AHORRO = config_data.get("meta_ahorro", 3000.0)
LIMITES
