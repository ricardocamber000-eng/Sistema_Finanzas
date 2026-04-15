import streamlit as st
import pandas as pd
from datetime import date
import os

# --- 1. CONFIGURACIÓN (Debe ser lo primero) ---
st.set_page_config(page_title="WalletPro: Dark Edition", page_icon="💰", layout="centered")

# --- 2. DIRECCIÓN DE LA IMAGEN ---
# REEMPLAZA ESTO con tu link real de GitHub (el que dice 'raw')
BG_IMAGE = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/9313.jpg"

# --- 3. ESTILO CSS ROBUSTO ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #000000; /* Fondo de respaldo si falla la imagen */
    }}

    /* Tarjeta de Saldo Principal */
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 35px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }}

    /* Botones Azules */
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white !important;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        width: 100%;
        height: 3em;
    }}

    /* Estilo para los inputs y selectores (mejorar visibilidad en fondo oscuro) */
    .stSelectbox, .stNumberInput, .stTextInput {{
        background-color: rgba(255,255,255,0.1) !important;
        border-radius: 10px;
    }}

    h1, h2, h3, p, label, span {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LÓGICA DE DATOS ---
DB_FILE = "data_wallet.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cálculo de Saldo Vivo
total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum()
saldo = total_in - total_out

# --- 5. VISTA DE SALDO ---
st.markdown(f"""
    <div class="main-balance">
        <p style="margin:0; opacity:0.7; letter-spacing: 2px;">SALDO DISPONIBLE</p>
        <h1 style="margin:0; font-size:3.5em;">${saldo:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# Botón para Sumar Fondos
with st.expander("💵 Agregar Ingreso Extra"):
    with st.form("form_ingreso"):
        m_in = st.number_input("Monto a sumar", min_value=0.01)
        d_in = st.text_input("Nota", placeholder="Ej: Pago extra")
        if st.form_submit_button("Confirmar Ingreso"):
            nuevo = pd.DataFrame([[date.today(), "Ingreso", "Fondo", d_in, m_in]], columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

st.divider()

# --- 6. CATEGORÍAS DE GASTO (Desplegable) ---
st.subheader("Registrar Gasto")
opcion = st.selectbox("¿En qué gastaste?", ["Deudas", "Servicios", "Mercado", "Placeres"])

with st.form("form_gastos"):
    if opcion == "Servicios":
        detalle = st.text_input("Nombre del Servicio", placeholder="Netflix, Agua, Luz...")
    elif opcion == "Deudas":
        detalle = st.text_input("A quién pagaste", placeholder="Cashea, Banco, Juan...")
    else:
        detalle = st.text_input("Detalle", placeholder=f"Gasto en {opcion}")
        
    monto_g = st.number_input("Monto ($)", min_value=0.01)
    
    if st.form_submit_button(f"Registrar Gasto en {opcion}"):
        nuevo_g = pd.DataFrame([[date.today(), "Gasto", opcion, detalle, monto_g]], columns=df.columns)
        df = pd.concat([df, nuevo_g], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.rerun()

# --- 7. HISTORIAL TIPO BANCARIO ---
st.subheader("Movimientos")
if not df.empty:
    for _, row in df.sort_values(by="Fecha", ascending=False).head(10).iterrows():
        simbolo = "+" if row['Tipo'] == "Ingreso" else "-"
        color_monto = "#00ff88" if row['Tipo'] == "Ingreso" else "#ff4b4b"
        
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding:15px; border-radius:12px; margin-bottom:10px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-weight:bold;">{row['Detalle']}</span>
                    <span style="color:{color_monto}; font-weight:bold;">{simbolo} ${row['Monto']:,.2f}</span>
                </div>
                <div style="font-size:0.8em; opacity:0.5;">{row['Categoría']} • {row['Fecha']}</div>
            </div>
            """, unsafe_allow_html=True)
                    <div style="color:{color}; font-weight:800; font-size:1.2em;">{simb}${row['Monto']:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
