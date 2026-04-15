import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS
DB_FILE = "wallet_database.csv"

# 3. ESTILOS CSS (Tu diseño original intacto)
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
    }
</style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS (Mejorada para evitar errores de tipo)
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
    df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0)
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. ESTRUCTURA DE NAVEGACIÓN (TABS ORIGINALES)
tab_home, tab_stats, tab_expenses, tab_income = st.tabs(["🏠 Inicio", "
