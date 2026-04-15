import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="WalletPro: Dark Edition", page_icon="💰", layout="centered")

# URL de la imagen que proporcionaste (asegúrate de subirla a tu GitHub junto al app.py)
# Si la subes a GitHub, la ruta sería "9313.jpg"
BG_IMAGE_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/9313.jpg"

# --- INTERFAZ DARK PREMIUM CON CSS ---
st.markdown(f"""
    <style>
    /* Fondo con la imagen texturizada */
    .stApp {{
        background-image: url("{BG_IMAGE_URL}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Contenedor del Saldo Principal (Look de Tarjeta Bancaria) */
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }}

    /* Botones y Selectores */
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }}
    
    /* Estilo para las tarjetas de historial */
    .history-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: white;
    }}

    /* Ajuste de textos para fondo oscuro */
    h1, h2, h3, p, label {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS Y LÓGICA ---
DB_FILE = "movimientos_premium.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Concepto", "Monto"])

# Cálculo de saldo
saldo_actual = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum()

# --- VISTA PRINCIPAL ---
st.markdown(f"""
    <div class="main-balance">
        <p style="margin:0; opacity:0.6; letter-spacing: 2px; font-size:0.9em;">FONDO DISPONIBLE</p>
        <h1 style="margin:0; font-size:3.5em; font-weight:800;">${saldo_actual:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# Botón rápido de ingreso
with st.expander("💳 Sumar Ingreso"):
    with st.form("ingreso_extra"):
        m_in = st.number_input("Monto ($)", min_value=0.01)
        f_in = st.text_input("Nota", placeholder="Ej: Pago de cliente")
        if st.form_submit_button("Aumentar Saldo"):
            nuevo = pd.DataFrame([[date.today(), "Ingreso", "Extra", f_in, m_in]], columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

st.divider()

# --- MENÚ DE GASTOS POR CATEGORÍA ---
st.subheader("Registrar Gasto")
cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Placeres"])

with st.form("registro_gastos"):
    nombre = st.text_input("Detalle", placeholder=f"Ej: Pago de {cat}")
    monto = st.number_input("Monto ($)", min_value=0.01)
    if st.form_submit_button(f"Descontar de {cat}"):
        nuevo_g = pd.DataFrame([[date.today(), "Gasto", cat, nombre, monto]], columns=df.columns)
        df = pd.concat([df, nuevo_g], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.rerun()

# --- HISTORIAL MINIMALISTA ---
st.divider()
st.subheader("Movimientos Recientes")
if not df.empty:
    for _, row in df.sort_values(by="Fecha", ascending=False).head(8).iterrows():
        color = "#00ff88" if row['Tipo'] == "Ingreso" else "#ff4b4b"
        simb = "+" if row['Tipo'] == "Ingreso" else "-"
        st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:bold; font-size:1.1em;">{row['Concepto']}</div>
                        <div style="font-size:0.8em; opacity:0.5;">{row['Categoría']} • {row['Fecha']}</div>
                    </div>
                    <div style="color:{color}; font-weight:800; font-size:1.2em;">{simb}${row['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
