import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. RECURSOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"
DB_FILE = "wallet_database.csv"

# 3. CSS MAESTRO (Sin columnas, centrado por Flexbox)
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("app/static/{BG_IMAGE}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #0F1218;
    }}
    
    /* Centrado del Logo y Título en Sidebar */
    .sidebar-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 20px;
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(15, 18, 24, 0.98);
        border-right: 2px solid #C69F40;
    }}

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
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

saldo = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum() if not df.empty else 0.0

# 5. SIDEBAR (Rediseñado sin st.columns)
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    st.markdown("<h2 style='color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    pestana = st.radio("Acción", ["📉 Registrar Gasto", "📈 Añadir Ingreso"])
    
    if "Gasto" in pestana:
        cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
        with st.form("f_g"):
            det = st.text_input("Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0)
            if st.form_submit_button("REGISTRAR GASTO"):
                new = pd.DataFrame([[date.today(), "Gasto", cat, det, mon]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
    else:
        with st.form("f_i"):
            ori = st.text_input("Origen")
            mon_i = st.number_input("Monto ($) ", min_value=0.0)
            if st.form_submit_button("SUMAR CAPITAL"):
                new = pd.DataFrame([[date.today(), "Ingreso", "Fondo", ori, mon_i]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# 6. CUERPO
st.markdown("<h3 style='text-align:center; opacity:0.4; letter-spacing:6px;'>R.C FINANZAS</h3>", unsafe_allow_html=True)

st.markdown(f"""
<div class="main-balance">
    <p style="margin:0; color:#C69F40 !important; font-weight:bold; letter-spacing:3px;">SALDO DISPONIBLE</p>
    <h1 style="margin:0; font-size:4.8em; font-weight:800;">${saldo:,.2f}</h1>
</div>
""", unsafe_allow_html=True)

st.subheader("Movimientos Recientes")

if not df.empty:
    for i, r in df.sort_values(by="Fecha", ascending=False).head(10).iterrows():
        col = "#00ff88" if r['Tipo'] == "Ingreso" else "#ff4b4b"
        pre = "+" if r['Tipo'] == "Ingreso" else "-"
        st.markdown(f"""
        <div class="history-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="text-align:left;">
                    <div style="font-weight:bold; color:white;">{r['Detalle']}</div>
                    <div style="font-size:0.8em; opacity:0.6;">{r['Categoría']} • {r['Fecha']}</div>
                </div>
                <div style="color:{col}; font-weight:900; font-size:1.3em;">{pre}${r['Monto']:,.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Sin registros.")
