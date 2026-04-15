import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN INICIAL (Obligatorio como primera instrucción)
st.set_page_config(
    page_title="WalletPro: Dark Edition", 
    page_icon="💰", 
    layout="centered"
)

# 2. RUTA DE LA IMAGEN DE FONDO
# Si está en tu repo de GitHub, basta con el nombre del archivo
BG_IMAGE = "9313.jpg" 

# 3. ESTILO CSS INTEGRADO
# Hemos ajustado el contraste para que el texto blanco resalte sobre tu fondo negro
st.markdown(f"""
    <style>
    /* Fondo con la imagen texturizada */
    .stApp {{
        background-image: url("{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218; /* Respaldo en caso de error de carga */
    }}

    /* Tarjeta de Saldo Principal (Efecto Cristal) */
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 28px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    /* Estilo de Tarjetas de Historial */
    .history-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 12px;
        transition: 0.3s;
    }}

    /* Botones con Degradado Azul */
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white !important;
        border-radius: 14px;
        border: none;
        font-weight: bold;
        width: 100%;
        height: 3.2em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Forzar color blanco en textos de control */
    h1, h2, h3, p, label, span, .stMarkdown {{
        color: white !important;
    }}
    
    /* Estilo para los inputs */
    .stNumberInput input, .stTextInput input {{
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. GESTIÓN DE BASE DE DATOS LOCAL (CSV)
DB_FILE = "wallet_database.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cálculo de Saldo Vivo (Fondo Momentáneo)
total_ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
total_gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()
saldo_vivo = total_ingresos - total_gastos

# 5. HEADER: FONDO DISPONIBLE
st.markdown(f"""
    <div class="main-balance">
        <p style="margin:0; opacity:0.6; letter-spacing: 3px; font-size:0.8em;">MI FONDO MOMENTÁNEO</p>
        <h1 style="margin:0; font-size:4em; font-weight:800;">${saldo_vivo:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# --- SECCIÓN A: SUMAR FONDOS (INGRESOS) ---
with st.expander("➕ AGREGAR INGRESO EXTRA", expanded=False):
    with st.form("form_ingresos"):
        m_in = st.number_input("Monto a ingresar ($)", min_value=0.01, step=1.0)
        d_in = st.text_input("Concepto / Origen", placeholder="Ej: Pago de cliente, Bono...")
        if st.form_submit_button("CONFIRMAR INGRESO"):
            nuevo = pd.DataFrame([[date.today(), "Ingreso", "Fondo", d_in, m_in]], columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

st.divider()

# --- SECCIÓN B: GASTOS CATEGORIZADOS ---
st.subheader("Registrar Movimiento")
categoria_gasto = st.selectbox(
    "Selecciona Categoría", 
    ["Deudas", "Servicios", "Mercado", "Placeres"]
)

with st.form("form_gastos"):
    if categoria_gasto == "Deudas":
        label_det = "Descripción de deuda (Cashea, personal...)"
    elif categoria_gasto == "Servicios":
        label_det = "Servicio (Netflix, Luz, Internet...)"
    else:
        label_det = "Detalle del gasto"
        
    detalle_g = st.text_input(label_det, placeholder="Escribe aquí...")
    monto_g = st.number_input("Monto a descontar ($)", min_value=0.01, step=1.0)
    
    if st.form_submit_button(f"REGISTRAR EN {categoria_gasto.upper()}"):
        nuevo_g = pd.DataFrame([[date.today(), "Gasto", categoria_gasto, detalle_g, monto_g]], columns=df.columns)
        df = pd.concat([df, nuevo_g], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.toast(f"Gasto en {categoria_gasto} registrado", icon="📉")
        st.rerun()

# --- SECCIÓN C: HISTORIAL TIPO BANCARIO ---
st.subheader("Movimientos Recientes")
if not df.empty:
    # Mostramos los últimos 10 movimientos
    df_sorted = df.sort_values(by="Fecha", ascending=False).head(10
