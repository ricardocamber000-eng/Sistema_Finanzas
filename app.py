import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN INICIAL (Debe ser la primera instrucción)
st.set_page_config(
    page_title="R.C Finanzas: Gold Edition", 
    page_icon="💰", 
    layout="centered"
)

# 2. RUTA DE LA IMAGEN DE FONDO
BG_IMAGE = "9313.jpg" 

# 3. ESTILO CSS: ICONO DORADO Y DISEÑO PREMIUM
st.markdown(f"""
    <style>
    /* Fondo General */
    .stApp {{
        background-image: url("{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}

    /* ICONO DEL SIDEBAR EN DORADO */
    button[data-testid="sidebar-toggle"] svg {{
        fill: #FFD700 !important;
        width: 40px;
        height: 40px;
    }}
    
    /* Estilo de la Barra Lateral */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.98);
        border-right: 2px solid #FFD700;
    }}

    /* Tarjeta de Saldo Principal */
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px 20px;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }}

    /* Tarjetas de Historial */
    .history-card {{
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 5px;
    }}

    /* Botones con degradado azul */
    .stButton>button {{
        background: linear-gradient(135deg, #007bff, #001f3f);
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        font-weight: bold;
        text-transform: uppercase;
        width: 100%;
    }}

    /* Textos en blanco */
    h1, h2, h3, p, label, span, .stMarkdown {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. GESTIÓN DE DATOS (CSV Local)
DB_FILE = "wallet_database.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cálculo de Saldo Vivo
total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum()
saldo = total_in - total_out

# --- 5. SIDEBAR: REGISTRO DE MOVIMIENTOS ---
with st.sidebar:
    st.title("💸 Operaciones")
    st.write("---")
    
    tab_gasto, tab_ingreso = st.tabs(["📉 Gasto", "📈 Ingreso"])
    
    with tab_gasto:
        cat_g = st.selectbox("Categoría de Gasto", ["Deudas", "Servicios", "Mercado", "Placeres"])
        with st.form("form_gasto_sidebar"):
            det_g = st.text_input("Detalle", placeholder="Ej: Pago de Netflix")
            mon_g = st.number_input("Monto ($)", min_value=0.01, step=1.0)
            if st.form_submit_button("REGISTRAR PAGO"):
                nuevo = pd.DataFrame([[date.today(), "Gasto", cat_g, det_g, mon_g]], columns=df.columns)
                df = pd.concat([df, nuevo], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
                
    with tab_ingreso:
        with st.form("form_ingreso_sidebar"):
            det_i = st.text_input("Origen del dinero", placeholder="Ej: Depósito bancario")
            mon_i = st.number_input("Monto a sumar ($)", min_value=0.01, step=1.0)
            if st.form_submit_button("SUMAR FONDOS"):
                nuevo = pd.DataFrame([[date.today(), "Ingreso", "Fondo", det_i, mon_i]], columns=df.columns)
                df = pd.concat([df, nuevo], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# --- 6. FRONT PRINCIPAL: DASHBOARD ---
st.markdown("<h3 style='text-align: center; opacity: 0.5; letter-spacing: 5px;'>WALLETPRO</h3>", unsafe_allow_html=True)

# Widget de Saldo
st.markdown(f"""
    <div class="main-balance">
        <p style="margin:0; opacity:0.6; letter-spacing: 4px; font-size:0.9em;">SALDO DISPONIBLE</p>
        <h1 style="margin:0; font-size:4.5em; font-weight:900;">${saldo:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# Historial de Movimientos
st.subheader("Historial de Movimientos")

if not df.empty:
    # Lógica de ordenado corregida sin errores de paréntesis
    df_sorted = df.sort_values(by="Fecha", ascending=False).head(20)
    
    for _, row in df_sorted.iterrows():
        is_in = row['Tipo'] == "Ingreso"
        c_monto = "#00ff88" if is_in else "#ff4b4b"
        simb = "+" if is_in else "-"
        
        st.markdown(f"""
            <div class="history-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; font-size:1.1em; color:white;">{row['Detalle']}</div>
                        <div style="font-size:0.8em; opacity:0.5; color:white;">{row['Categoría']} • {row['Fecha']}</div>
                    </div>
                    <div style="color:{c_monto}; font-weight:800; font-size:1.3em;">
                        {simb}${row['Monto']:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("El historial está vacío. Despliega el menú lateral (icono dorado) para comenzar.")
