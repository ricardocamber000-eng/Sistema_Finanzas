import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS
DB_FILE = "wallet_database.csv"

# 3. ESTILOS CSS (TEMA CLARO SOBRE TU ESTRUCTURA ORIGINAL)
st.markdown("""
<style>
    /* Fondo General Claro */
    .stApp { background-color: #FFFFFF !important; color: #1F2937 !important; }

    /* Estilizar las TABS para que parezcan una barra de menú inferior */
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #F8F9FA;
        border-top: 2px solid #C69F40;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 1000;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* Estilo de cada pestaña */
    .stTabs [data-baseweb="tab"] {
        color: #6B7280 !important;
        background: transparent !important;
        border: none !important;
        flex-grow: 1;
        text-align: center;
    }

    /* Pestaña activa (Dorado) */
    .stTabs [aria-selected="true"] {
        color: #C69F40 !important;
        font-weight: bold !important;
    }

    /* Margen inferior para no tapar contenido */
    .main .block-container { padding-bottom: 120px; }

    /* Tarjetas de Historial */
    .history-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #C69F40;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Balance Central */
    .main-balance {
        background: linear-gradient(135deg, #FDFCFB 0%, #F3F4F6 100%);
        border: 1px solid #C69F40;
        padding: 40px;
        border-radius: 30px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 25px rgba(198, 159, 64, 0.15);
    }

    /* Reajuste de colores de texto para legibilidad */
    h1, h2, h3, span, label, p { color: #1F2937 !important; }
</style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS (LÓGICA RESTAURADA)
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. ESTRUCTURA DE NAVEGACIÓN
tab_home, tab_stats, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "📊 Análisis", "🛍️ Gastos", "💼 Ingresos"])

# --- TAB 1: INICIO ---
with tab_home:
    st.markdown("<h2 style='text-align:center;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
    total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
    balance = total_in - total_out

    # Métricas superiores
    col1, col2 = st.columns(2)
    col1.metric("Total Ingresos", f"${total_in:,.2f}")
    col2.metric("Total Gastos", f"${total_out:,.2f}", delta=f"-{total_out:,.2f}", delta_color="inverse")

    st.markdown(f"""
    <div class="main-balance">
        <p style="color:#C69F40; font-weight:bold; letter-spacing:2px; margin-bottom:5px;">SALDO DISPONIBLE</p>
        <h1 style="font-size:4em; margin:0; color:#1F2937;">${balance:,.2f}</h1>
    </div>
