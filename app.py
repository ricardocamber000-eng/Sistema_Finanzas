import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS Y CARGA DE DATOS
DB_FILE = "wallet_database.csv"

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
        df['Monto'] = pd.to_numeric(df['Monto'])
        return df
    return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

df = load_data()

# 3. ESTILOS CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117 !important; }
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #07090D;
        border-top: 2px solid #C69F40;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 1000;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888 !important;
        background: transparent !important;
        border: none !important;
        flex-grow: 1;
        text-align: center;
    }
    .stTabs [aria-selected="true"] {
        color: #C69F40 !important;
        font-weight: bold !important;
    }
    .main .block-container { padding-bottom: 150px; }
    .history-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #C69F40;
    }
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.1), rgba(0,0,0,0.6));
        border: 1px solid #C69F40;
        padding: 40px;
        border-radius: 30px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 5. ESTRUCTURA DE NAVEGACIÓN
tab_home, tab_stats, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "📊 Análisis", "🛍️ Gastos", "💼 Ingresos"])

# --- TAB 1: INICIO ---
with tab_home:
    st.markdown("<h2 style='text-align:center;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    balance = total_in - total_out

    col1, col2 = st.columns(2)
    col1.metric("Total Ingresos", f"${total_in:,.2f}")
    col2.metric("Total Gastos", f"${total_out:,.2f}", delta=f"-{total_out:,.2f}", delta_color="inverse")

    st.markdown(f"""
    <div class="main-balance">
        <p style="color:#C69F40; font-weight:bold; letter-spacing:2px;">SALDO DISPONIBLE</p>
        <h1 style="font-size:4em; margin:0; color:white;">${balance:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Historial Reciente")
    if not df.empty:
        for i, r in df.sort_values(by="Fecha", ascending=False).head(8).iterrows():
            color = "#00FF9D" if r['Tipo'] == "Ingreso" else "#FF4B4B"
            st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between;">
                    <div><b>{r['Detalle']}</b><br><small>{r['Categoría']} | {r['Fecha']}</small></div>
                    <div style="color:{color}; font-size:1.2em; font-weight:bold;">${r['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aún no hay movimientos registrados.")

# --- TAB 2: ANÁLISIS ---
with tab_stats:
    st.header("Análisis de Finanzas")
    
    if not df.empty:
        # 1. Gráfico de Tendencia (Evolución)
        st.subheader("Evolución Temporal")
        df_trend = df.groupby(['Fecha', 'Tipo'])['Monto'].sum().reset_index
