import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(
    page_title="WalletPro: Dark Edition", 
    page_icon="💰", 
    layout="centered"
)

# 2. RUTA DE LA IMAGEN DE FONDO
BG_IMAGE = "9313.jpg" 

# 3. ESTILO CSS (Actualizado para Sidebar Dark)
st.markdown(f"""
    <style>
    /* Fondo General */
    .stApp {{
        background-image: url("{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
    
    /* Sidebar Estilo Dark */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Tarjeta de Saldo Principal */
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

    /* Tarjetas de Historial */
    .history-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 12px;
    }}

    /* Botones */
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white !important;
        border-radius: 14px;
        border: none;
        font-weight: bold;
        width: 100%;
        height: 3.2em;
    }}

    h1, h2, h3, p, label, span, .stMarkdown {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. GESTIÓN DE DATOS
DB_FILE = "wallet_database.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cálculos
saldo_vivo = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum()

# --- 5. PANEL LATERAL (SIDEBAR) ---
# Aquí movemos todo lo que quieres "fuera" del front principal
with st.sidebar:
    st.header("🛒 Registro de Gastos")
    st.write("Registra tus salidas de dinero aquí para mantener el balance actualizado.")
    
    cat_gasto = st.selectbox("Selecciona Categoría", ["Deudas", "Servicios", "Mercado", "Placeres"])
    
    with st.form("form_gastos_sidebar"):
        detalle_g = st.text_input("Detalle", placeholder=f"Ej: Pago de {cat_gasto}")
        monto_g = st.number_input("Monto ($)", min_value=0.01, step=1.0)
        
        if st.form_submit_button("REGISTRAR GASTO"):
            nuevo_g = pd.DataFrame([[date.today(), "Gasto", cat_gasto, detalle_g, monto_g]], columns=df.columns)
            df = pd.concat([df, nuevo_g], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

# --- 6. FRONT PRINCIPAL (DASHBOARD) ---
st.markdown(f"""
    <div class="main-balance">
        <p style="margin:0; opacity:0.6; letter-spacing: 3px; font-size:0.8em;">MI FONDO MOMENTÁNEO</p>
        <h1 style="margin:0; font-size:4em; font-weight:800;">${saldo_vivo:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# Botón de Ingreso Rápido en el Front
with st.expander("➕ SUMAR INGRESO EXTRA", expanded=False):
    with st.form("form_ingresos"):
        m_in = st.number_input("Monto a ingresar ($)", min_value=0.01, step=1.0)
        d_in = st.text_input("Concepto", placeholder="Ej: Pago extra...")
        if st.form_submit_button("AÑADIR AL FONDO"):
            nuevo = pd.DataFrame([[date.today(), "Ingreso", "Fondo", d_in, m_in]], columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.rerun()

st.divider()

# Historial Bancario
st.subheader("Movimientos Recientes")
if not df.empty:
    df_sorted = df.sort_values(by="Fecha", ascending=False).head(15)
    for _, row in df_sorted.iterrows():
        is_ingreso = row['Tipo'] == "Ingreso"
        color_monto = "#00ff88" if is_ingreso else "#ff4b4b"
        simb = "+" if is_ingreso else "-"
        
        st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; color:white;">{row['Detalle']}</div>
                        <div style="font-size:0.85em; opacity:0.6; color:white;">{row['Categoría']} • {row['Fecha']}</div>
                    </div>
                    <div style="color:{color_monto}; font-weight:800; font-size:1.25em;">
                        {simb}${row['Monto']:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No hay movimientos registrados.")
