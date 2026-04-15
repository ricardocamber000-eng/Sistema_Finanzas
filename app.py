import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px
import json

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="R.C Finanzas Pro", page_icon="👑", layout="centered")

# --- ARCHIVOS DE PERSISTENCIA ---
DB_FILE = "wallet_database.csv"
CONFIG_FILE = "settings.json"

# --- CARGA DE CONFIGURACIÓN (Meta de Ahorro Persistente) ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"meta_ahorro": 3000.0}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config_data = load_config()
META_AHORRO = config_data["meta_ahorro"]

# --- DICCIONARIOS ---
ICONOS = {
    "Servicios": "💡", "Mercado": "🛒", "Deudas": "💳", 
    "Ocio": "🎬", "Transporte": "🚗", "Depósito": "💰", "Varios": "📦"
}

# --- SISTEMA DE SEGURIDAD ---
if "authenticated" not in st.session_state:
    st.markdown("<h2 style='text-align:center;'>👑 R.C Finanzas</h2>", unsafe_allow_html=True)
    with st.form("Login"):
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Ingresar"):
            if user == "admin" and password == "1234":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Error de acceso")
    st.stop()

# --- CARGA DE DATOS ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# --- CÁLCULOS GLOBALES ---
total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
balance = total_in - total_out

# --- ESTILOS CSS (BARRA BLANCA FLOTANTE + UI KEVIN MERICO STYLE) ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #0E1117 !important; }}
    
    /* Barra Flotante Blanca */
    .stTabs [data-baseweb="tab-list"] {{
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 500px; z-index: 1000;
        background-color: #FFFFFF !important; border-radius: 30px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.5); padding: 5px 15px;
        display: flex; justify-content: space-around; border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important; border: none !important;
        color: #666666 !important; transition: all 0.3s ease; font-size: 0.8em;
    }}
    .stTabs [aria-selected="true"] {{ color: #C69F40 !important; font-weight: bold; transform: scale(1.1); }}
    .stTabs [data-baseweb="tab-highlight"] {{ background-color: transparent !important; }}
    
    .main .block-container {{ padding-bottom: 150px; }}

    /* Cards Estilo Moderno */
    .card-resumen {{
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 25px;
        border: 1px solid rgba(255,255,255,0.05); text-align: center; margin-bottom: 20px;
    }}
    .history-card {{
        background: rgba(255, 255, 255, 0.04); border-radius: 15px;
        padding: 15px; margin-bottom: 10px; border-left: 4px solid #C69F40;
    }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tab_home, tab_edit, tab_savings, tab_expenses, tab_income = st.tabs([
    "🏠\nInicio", "📝\nEditar", "🐷\nAhorro", "🛍️\nGasto", "💼\nIngreso"
])

with tab_home:
    st.markdown("### Hola, Administrador! 👋")
    st.markdown("<p style='color:#888;'>Gestiona tus finanzas con precisión.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class='card-resumen'>
            <small style='color:#888;'>DISPONIBLE</small><br>
            <h2 style='color:#C69F40;'>${balance:,.2f}</h2>
        </div>""", unsafe_allow_html=True)
    with col2:
        # Mini métrica de porcentaje de meta
        perc = min(int((balance/META_AHORRO)*100), 100) if META_AHORRO > 0 else 0
        st.markdown(f"""<div class='card-resumen'>
            <small style='color:#888;'>META AHORRO</small><br>
            <h2 style='color:#00FF9D;'>{perc}%</h2>
        </div>""", unsafe_allow_html=True)

    st.subheader("Transacciones")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(5).iterrows():
            icono = ICONOS.get(r['Categoría'], "📝") if r['Tipo'] == "Gasto" else "💰"
            color_monto = "#00FF9D" if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><b>{icono} {r['Detalle']}</b><br><small style="color:#666;">{r['Categoría']}</small></div>
                    <div style="color:{color_monto}; font-weight:bold;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_edit:
    st.header("Gestión de Datos ⚙️")
    
    # Editor de datos avanzado
    st.subheader("Editar Histórico")
    edited_df = st.data_editor(
        df, num_rows="dynamic", use_container_width=True, hide_index=True,
        column_config={
            "Monto": st.column_config.NumberColumn(format="$%.2f"),
            "Tipo": st.column_config.SelectboxColumn(options=["Ingreso", "Gasto"]),
            "Categoría": st.column_config.SelectboxColumn(options=list(ICONOS.keys())),
            "Fecha": st.column_config.DateColumn()
        }
    )
    
    if st.button("💾 GUARDAR CAMBIOS"):
        edited_df.to_csv(DB_FILE, index=False)
        st.success("¡Base de datos actualizada!")
        st.rerun()

    st.divider()
    with st.expander("🚨 Zona de Peligro"):
        st.write("Estas acciones no se pueden deshacer.")
        if st.button("REINICIAR TODO EL SISTEMA", type="primary"):
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            st.rerun()

with tab_savings:
    st.header("Meta de Ahorro 🐷")
    
    # Ajuste de Meta Dinámica
    nueva_meta = st.number_input("Ajustar mi meta ($)", value=META_AHORRO, step=100.0)
    if nueva_meta != META_AHORRO:
        save_config({"meta_ahorro": nueva_meta})
        st.rerun()

    progreso = min(max(balance / nueva_meta, 0.0), 1.0)
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.03); border-radius: 20px; padding: 30px; border: 1px solid #C69F40; text-align: center;">
        <h1 style="color: #C69F40;">{int(progreso*100)}%</h1>
        <p>Progreso hacia ${nueva_meta:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progreso)

with tab_expenses:
    st.header("Nuevo Gasto 🛍️")
    with st.form("f_gasto", clear_on_submit=True):
        c = st.selectbox("Categoría", list(ICONOS.keys()))
        d = st.text_input("Detalle")
        m = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("REGISTRAR"):
            new = pd.DataFrame([[date.today(), "Gasto", c, d, m]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()

with tab_income:
    st.header("Nuevo Ingreso 💼")
    with st.form("f_ingreso", clear_on_submit=True):
        d = st.text_input("Origen")
        m = st.number_input("Monto", min_value=0.0)
        if st.form_submit_button("CARGAR"):
            new = pd.DataFrame([[date.today(), "Ingreso", "Depósito", d, m]], columns=df.columns)
            pd.concat([df, new]).to_csv(DB_FILE, index=False)
            st.rerun()
            
