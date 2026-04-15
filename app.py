import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. ARCHIVOS
BG_IMAGE = "9313.jpg"
LOGO_FILE = "Logo_RC.png"

# 3. CSS MAESTRO (Sin sangrías peligrosas)
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

/* ICONO DORADO */
button[kind="headerNoSpacing"] svg, 
button[data-testid="sidebar-toggle"] svg {{
    fill: #C69F40 !important;
    width: 42px !important;
    height: 42px !important;
}}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background-color: rgba(15, 18, 24, 0.98);
    border-right: 2px solid #C69F40;
}}

/* TARJETA SALDO */
.main-balance {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(198, 159, 64, 0.4);
    padding: 50px 20px;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 30px;
}}

/* HISTORIAL */
.history-card {{
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 10px;
    border-left: 5px solid #C69F40;
}}

/* BOTONES */
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

saldo = df[df["Tipo"] == "Ingreso"]["Monto"].sum() - df[df["Tipo"] == "Gasto"]["Monto"].sum()

# 5. SIDEBAR
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
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

# 6. FRONT
st.markdown("<h3 style='text-align:center; opacity:0.5; letter-spacing:4px;'>R.C FINANZAS</h3>", unsafe_allow_html=True)

st.markdown(f"""
<div class="main-balance">
<p style="margin:0; color:#C69F40 !important; font-weight:bold; letter-spacing:2px;">SALDO DISPONIBLE</p>
<h1 style="margin:0; font-size:4.5em;">${saldo:,.2f}</h1>
</div>
""", unsafe_allow_html=True)

st.subheader("Movimientos Recientes")
if not df.empty:
    df_s = df.sort_values(by="Fecha", ascending=False).head(10)
    for _, r in df_s.iterrows():
        is_in = r['Tipo'] == "Ingreso"
        c = "#00ff88" if is_in else "#ff4b4b"
        s = "+" if is_in else "-"
        st.markdown(f"""
<div class="history-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<div style="font-weight:bold;">{r['Detalle']}</div>
<div style="font-size:0.8em; opacity:0.5;">{r['Categoría']} • {r['Fecha']}</div>
</div>
<div style="color:{c}; font-weight:bold; font-size:1.3em;">{s}${r['Monto']:,.2f}</div>
</div>
</div>
""", unsafe_allow_html=True)
else:
    st.info("Abre el menú dorado para registrar datos.")
