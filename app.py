import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="R.C Finanzas", 
    page_icon="👑", 
    layout="centered"
)

# 2. DEFINICIÓN DE RECURSOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"
DB_FILE = "wallet_database.csv"

# 3. BLOQUE CSS (DISEÑO PREMIUM Y DORADOS)
# Usamos una variable separada para evitar errores de f-string en el markdown
ESTILO_CSS = f"""
<style>
    /* Fondo con imagen y textura */
    .stApp {{
        background-image: url("app/static/{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
    
    /* Transparencias para ver el fondo */
    .main .block-container {{ background-color: rgba(0,0,0,0); }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}

    /* Sidebar y Botón Dorado */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.98);
        border-right: 2px solid #C69F40;
    }}
    
    button[kind="headerNoSpacing"] svg, 
    button[data-testid="sidebar-toggle"] svg {{
        fill: #C69F40 !important;
        width: 42px !important;
        height: 42px !important;
    }}

    /* Tarjetas y Contenedores */
    .main-balance {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(198, 159, 64, 0.4);
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 30px;
    }}

    .history-card {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 10px;
        border-left: 5px solid #C69F40;
    }}

    /* Botones Estilo Lingote */
    .stButton>button {{
        background: linear-gradient(135deg, #C69F40, #8A6D2D);
        color: black !important;
        border: none;
        font-weight: 900;
        width: 100%;
        border-radius: 10px;
    }}

    /* Textos Globales */
    h1, h2, h3, p, label, span {{ color: white !important; }}
</style>
"""
st.markdown(ESTILO_CSS, unsafe_allow_html=True)

# 4. GESTIÓN DE DATOS (LECTURA)
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cálculo de Saldo
total_in = df[df["Tipo"] == "Ingreso"]["Monto"].sum() if not df.empty else 0
total_out = df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0
saldo_actual = total_in - total_out

# 5. SIDEBAR: LOGO CENTRADO Y CONTROLES
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        col_l, col_m, col_r = st.columns()
        with col_m:
            st.image(LOGO_FILE, width=150)
            
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important; margin-top:-15px;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.write("---")
    
    pestana_g, pestana_i = st.tabs(["📉 Gasto", "📈 Ingreso"])
    
    with pestana_g:
        categoria = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
        with st.form("form_gasto"):
            concepto = st.text_input("Concepto")
            monto = st.number_input("Monto ($)", min_value=0.0, step=1.0)
            if st.form_submit_button("REGISTRAR GASTO"):
                nueva_fila = pd.DataFrame([[date.today(), "Gasto", categoria, concepto, monto]], columns=df.columns)
                df = pd.concat([df, nueva_fila], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
                
    with pestana_i:
        with st.form("form_ingreso"):
            origen = st.text_input("Origen del dinero")
            monto_i = st.number_input("Monto ($) ", min_value=0.0, step=1.0)
            if st.form_submit_button("AÑADIR A SALDO"):
                nueva_fila = pd.DataFrame([[date.today(), "Ingreso", "Depósito", origen, monto_i]], columns=df.columns)
                df = pd.concat([df, nueva_fila], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# 6. CUERPO PRINCIPAL
st.markdown("<h3 style='text-align:center; opacity:0.4; letter-spacing:6px; margin-bottom:20px;'>R.C FINANZAS</h3>", unsafe_allow_html=True)

# Widget de Saldo Disponible
st.markdown(f"""
<div class="main-balance">
    <p style="margin:0; color:#C69F40 !important; font-weight:bold; letter-spacing:3px; font-size:0.9em;">SALDO DISPONIBLE</p>
    <h1 style="margin:0; font-size:4.8em; font-weight:800;">${saldo_actual:,.2f}</h1>
</div>
""", unsafe_allow_html=True)

# Sección de Historial
st.subheader("Movimientos Recientes")

if not df.empty:
    # Ordenar por fecha y mostrar los últimos 10
    df_visual = df.sort_values(by="Fecha", ascending=False).head(10)
    for index, fila in df_visual.iterrows():
        es_ingreso = fila['Tipo'] == "Ingreso"
        color_valor = "#00ff88" if es_ingreso else "#ff4b4b"
        prefijo = "+" if es_ingreso else "-"
        
        # Generar tarjeta de historial
        st.markdown(f"""
        <div class="history-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:left;">
                    <div style="font-weight:bold; font-size:1.1em; color:white;">{fila['Detalle']}</div>
                    <div style="font-size:0.85em; opacity:0.6; color:white;">{fila['Categoría']} • {fila['Fecha']}</div>
                </div>
                <div style="color:{color_valor}; font-weight:900; font-size:1.4em;
