import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. ARCHIVOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"

# 3. CSS (Separado para evitar errores de sintaxis)
st.markdown(f"""
<style>
.stApp {{
    background-image: url("app/static/{BG_IMAGE}");
    background-size: cover;
    background-attachment: fixed;
    background-color: #0F1218;
}}
.main .block-container {{ background-color: rgba(0,0,0,0); }}
[data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}

button[kind="headerNoSpacing"] svg, 
button[data-testid="sidebar-toggle"] svg {{
    fill: #C69F40 !important;
    width: 42px !important;
}}

[data-testid="stSidebar"] {{
    background-color: rgba(15, 18, 24, 0.98);
    border-right: 2px solid #C69F40;
}}

.main-balance {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(198, 159, 64, 0.4);
    padding: 50px 20px;
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

.stButton>button {{
    background: linear-gradient(135deg, #C69F40, #8A6D2D);
    color: black !important;
    border: none;
    font-weight: 900;
    width: 100%;
}}

h1, h2, h3, p, label, span {{ color: white !important; }}
</style>
""", unsafe_allow_html=True)

# 4. DATOS
DB_FILE = "wallet_database.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# Cálculo de Saldo (Protección contra archivos vacíos)
if not df.empty:
    saldo = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum()
else:
    saldo = 0.0

# 5. SIDEBAR
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        c1, c2, c3 = st.columns()
        with c2:
            st.image(LOGO_FILE, width=150)
            
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important; margin-top:-10px;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.write("---")
    
    t1, t2 = st.tabs(["📉 Gasto", "📈 Ingreso"])
    with t1:
        cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
        with st.form("f_gasto"):
            det = st.text_input("Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0)
            if st.form_submit_button("REGISTRAR GASTO"):
                new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
    with t2:
        with st.form("f_ingreso"):
            det_i = st.text_input("Origen")
            mon_i = st.number_input("Monto ($) ", min_value=0.0)
            if st.form_submit_button("SUMAR CAPITAL"):
                new = pd.DataFrame([[date.today(), "Ingreso", "Fondo", det_i, mon_i]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# 6. FRONT PRINCIPAL
st.markdown("
