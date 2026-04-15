import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px
import time

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS
DB_FILE = "wallet_database.csv"

# 3. ESTILOS CSS (Menú Inferior y Botones de Acción)
st.markdown("""
<style>
    .stApp { background-color: #0E1117 !important; }

    /* Barra de Navegación Inferior Fija */
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
        flex-grow: 1;
        text-align: center;
    }

    .stTabs [aria-selected="true"] {
        color: #C69F40 !important;
        font-weight: bold !important;
    }

    /* Espaciado para el menú inferior */
    .main .block-container { padding-bottom: 120px; }

    /* Estilo de Tarjetas con soporte para botones internos */
    .history-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 5px solid #C69F40;
    }

    /* Saldo Principal */
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.15), rgba(0,0,0,0.8));
        border: 1px solid #C69F40;
        padding: 35px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Estilo para el botón de eliminar (Streamlit override) */
    div[data-testid="column"] button {
        background-
